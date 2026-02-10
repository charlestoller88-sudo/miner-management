"""
矿机发现服务 - 扫描IP范围发现矿机
"""
import asyncio
import ipaddress
from typing import List, Set
from miner_api import MinerAPIClient
from config import IP_RANGES

class MinerDiscovery:
    """矿机发现服务"""
    
    @staticmethod
    def ip_range_to_list(start_ip: str, end_ip: str) -> List[str]:
        """将IP范围转换为IP列表"""
        start = ipaddress.IPv4Address(start_ip)
        end = ipaddress.IPv4Address(end_ip)
        ip_list = []
        current = start
        while current <= end:
            ip_list.append(str(current))
            current += 1
        return ip_list
    
    @staticmethod
    async def check_miner(ip: str) -> bool:
        """检查IP是否为矿机"""
        try:
            client = MinerAPIClient(ip)
            summary = await client.get_summary()
            if summary and summary.get("STATUS") == "S":
                return True
        except Exception:
            # 静默处理错误
            pass
        return False
    
    @staticmethod
    async def discover_miners() -> List[str]:
        """发现所有矿机IP地址"""
        all_ips: Set[str] = set()
        
        # 收集所有IP地址
        for start_ip, end_ip in IP_RANGES:
            ip_list = MinerDiscovery.ip_range_to_list(start_ip, end_ip)
            all_ips.update(ip_list)
        
        # 并发检查所有IP
        tasks = [MinerDiscovery.check_miner(ip) for ip in all_ips]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 找出在线的矿机
        miner_ips = []
        for ip, is_miner in zip(all_ips, results):
            if isinstance(is_miner, bool) and is_miner:
                miner_ips.append(ip)
        
        return miner_ips
    
    @staticmethod
    async def discover_miners_batch(batch_size: int = 100, timeout_per_ip: float = 2.0) -> List[str]:
        """批量发现矿机（避免过多并发）"""
        all_ips: Set[str] = set()
        
        # 收集所有IP地址
        for start_ip, end_ip in IP_RANGES:
            ip_list = MinerDiscovery.ip_range_to_list(start_ip, end_ip)
            all_ips.update(ip_list)
        
        miner_ips = []
        ip_list = list(all_ips)
        
        # 分批处理，使用更大的批次和超时控制
        for i in range(0, len(ip_list), batch_size):
            batch = ip_list[i:i + batch_size]
            tasks = []
            for ip in batch:
                # 为每个任务添加超时包装
                async def check_with_timeout(ip_addr: str):
                    try:
                        return await asyncio.wait_for(
                            MinerDiscovery.check_miner(ip_addr),
                            timeout=timeout_per_ip
                        )
                    except asyncio.TimeoutError:
                        return False
                
                tasks.append(check_with_timeout(ip))
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for ip, result in zip(batch, results):
                if isinstance(result, bool) and result:
                    miner_ips.append(ip)
                # 其他情况（异常、False等）都忽略
            
            # 批次之间稍微延迟，避免过载
            if i + batch_size < len(ip_list):
                await asyncio.sleep(0.05)
        
        return miner_ips
