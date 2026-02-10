"""
矿机API客户端 - 用于与Antminer设备通信
"""
import httpx
import json
from typing import Dict, Optional, List
from config import MINER_API_PORT, API_TIMEOUT, DEBUG_MODE

class MinerAPIClient:
    """Antminer API客户端"""
    
    def __init__(self, ip_address: str):
        self.ip_address = ip_address
        self.base_url = f"http://{ip_address}:{MINER_API_PORT}"
        self.timeout = API_TIMEOUT
    
    async def _request(self, command: Dict) -> Optional[Dict]:
        """发送API请求"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.base_url,
                    json=command,
                    headers={"Content-Type": "application/json"}
                )
                if response.status_code == 200:
                    return response.json()
                return None
        except (httpx.TimeoutException, httpx.ConnectError, httpx.NetworkError):
            # 静默处理超时和连接错误（这些是正常的，因为很多IP不是矿机）
            return None
        except Exception:
            # 其他错误也静默处理
            return None
    
    async def get_summary(self) -> Optional[Dict]:
        """获取矿机摘要信息"""
        command = {"command": "summary"}
        return await self._request(command)
    
    async def get_stats(self) -> Optional[Dict]:
        """获取矿机统计信息"""
        command = {"command": "stats"}
        return await self._request(command)
    
    async def get_pools(self) -> Optional[Dict]:
        """获取矿池配置"""
        command = {"command": "pools"}
        return await self._request(command)
    
    async def get_devs(self) -> Optional[Dict]:
        """获取设备（算力板）详细信息"""
        command = {"command": "devs"}
        return await self._request(command)
    
    async def get_version(self) -> Optional[Dict]:
        """获取版本信息"""
        command = {"command": "version"}
        return await self._request(command)
    
    async def get_network(self) -> Optional[Dict]:
        """获取网络配置"""
        command = {"command": "network"}
        return await self._request(command)
    
    async def get_all_info(self) -> Optional[Dict]:
        """获取所有信息"""
        try:
            summary = await self.get_summary()
            stats = await self.get_stats()
            pools = await self.get_pools()
            devs = await self.get_devs()
            version = await self.get_version()
            network = await self.get_network()
            
            return {
                "summary": summary,
                "stats": stats,
                "pools": pools,
                "devs": devs,
                "version": version,
                "network": network,
                "ip_address": self.ip_address
            }
        except Exception as e:
            print(f"获取 {self.ip_address} 信息失败: {e}")
            return None
    
    def parse_miner_data(self, data: Dict) -> Dict:
        """解析矿机数据为标准格式"""
        if not data:
            return {}
        
        result = {
            "ip_address": self.ip_address,
            "is_online": False,
            "model": None,
            "hostname": None,
            "temp_chip": None,
            "temp_pcb": None,
            "temp_max": None,
            "power_consumption": None,
            "humidity": None,
            "hashrate": None,
            "hashrate_5s": None,
            "hashrate_avg": None,
            "fan_speeds": [],
            "pool_info": [],
            "uptime": None,
            "network_status": "unknown",
            "hashboard_info": []
        }
        
        try:
            summary = data.get("summary", {})
            stats = data.get("stats", [{}])[0] if data.get("stats") else {}
            pools = data.get("pools", {}).get("POOLS", [])
            devs = data.get("devs", {}).get("DEVS", [])
            version = data.get("version", [{}])[0] if data.get("version") else {}
            network = data.get("network", [{}])[0] if data.get("network") else {}
            
            # 基本信息
            if summary.get("STATUS") == "S":
                result["is_online"] = True
            
            result["model"] = summary.get("Type", version.get("Type"))
            result["hostname"] = summary.get("Hostname", network.get("Hostname"))
            
            # 温度信息
            if "SUMMARY" in summary:
                summary_data = summary["SUMMARY"]
                if len(summary_data) > 0:
                    result["temp_chip"] = summary_data[0].get("Temperature")
                    result["temp_pcb"] = summary_data[0].get("PCB Temperature")
            
            # 算力信息
            if summary.get("SUMMARY"):
                summary_data = summary["SUMMARY"]
                if len(summary_data) > 0:
                    hashrate_str = summary_data[0].get("GHS 5s", "0")
                    result["hashrate_5s"] = float(hashrate_str.replace("T", "").replace("G", "")) / 1000 if "T" not in hashrate_str else float(hashrate_str.replace("T", ""))
                    
                    hashrate_avg_str = summary_data[0].get("GHS av", "0")
                    result["hashrate_avg"] = float(hashrate_avg_str.replace("T", "").replace("G", "")) / 1000 if "T" not in hashrate_avg_str else float(hashrate_avg_str.replace("T", ""))
            
            # 风扇转速
            if summary.get("SUMMARY"):
                summary_data = summary["SUMMARY"]
                if len(summary_data) > 0:
                    fan_speeds = []
                    for i in range(1, 5):
                        fan_key = f"Fan Speed In{i}"
                        if fan_key in summary_data[0]:
                            fan_speeds.append(summary_data[0][fan_key])
                    result["fan_speeds"] = fan_speeds
            
            # 功耗
            if stats.get("STATS"):
                stats_data = stats["STATS"]
                if len(stats_data) > 0:
                    power_str = stats_data[0].get("Power", "0")
                    if power_str:
                        result["power_consumption"] = float(power_str.replace("W", ""))
            
            # 运行时间
            if summary.get("SUMMARY"):
                summary_data = summary["SUMMARY"]
                if len(summary_data) > 0:
                    uptime_str = summary_data[0].get("Elapsed", "0")
                    if uptime_str:
                        # 解析运行时间格式 "123456" (秒)
                        try:
                            result["uptime"] = int(uptime_str)
                        except:
                            result["uptime"] = 0
            
            # 矿池信息
            pool_list = []
            for pool in pools:
                pool_info = {
                    "url": pool.get("URL", ""),
                    "user": pool.get("User", ""),
                    "status": pool.get("Status", ""),
                    "priority": pool.get("Priority", 0)
                }
                pool_list.append(pool_info)
            result["pool_info"] = pool_list
            
            # 算力板信息
            hasboard_list = []
            for dev in devs:
                hasboard_info = {
                    "id": dev.get("ID", 0),
                    "status": dev.get("Status", ""),
                    "temperature": dev.get("Temperature", 0),
                    "hashrate": dev.get("MHS 5s", "0"),
                    "chip_temp": dev.get("Chip Temp", 0),
                    "pcb_temp": dev.get("PCB Temp", 0),
                    "fan_speed": dev.get("Fan Speed", 0),
                    "chain": dev.get("Chain", "")
                }
                hasboard_list.append(hashboard_info)
            result["hashboard_info"] = hasboard_list
            
            # 网络状态
            if network.get("STATUS"):
                network_status = network["STATUS"]
                if len(network_status) > 0:
                    result["network_status"] = network_status[0].get("Status", "unknown")
            
        except Exception as e:
            if DEBUG_MODE:
                print(f"解析 {self.ip_address} 数据失败: {e}")
        
        return result
