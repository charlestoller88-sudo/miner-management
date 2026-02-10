"""
主应用入口
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from config import CORS_ORIGINS, STATUS_UPDATE_INTERVAL, SCAN_INTERVAL
from database import init_db, get_db, Miner, MinerStatus, MinerLog
from miner_api import MinerAPIClient
from miner_discovery import MinerDiscovery
import json

app = FastAPI(title="矿机管理系统API")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库
init_db()

# 定时任务调度器
scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup_event():
    """启动时初始化"""
    scheduler.start()
    # 启动定时任务
    scheduler.add_job(
        update_all_miners_status,
        IntervalTrigger(seconds=STATUS_UPDATE_INTERVAL),
        id="update_status"
    )
    scheduler.add_job(
        discover_new_miners,
        IntervalTrigger(seconds=SCAN_INTERVAL),
        id="discover_miners"
    )

@app.on_event("shutdown")
async def shutdown_event():
    """关闭时清理"""
    scheduler.shutdown()

# ============ API路由 ============

@app.get("/")
async def root():
    """根路径"""
    return {"message": "矿机管理系统API", "version": "1.0.0"}

@app.get("/api/miners", response_model=List[dict])
async def get_miners(db: Session = Depends(get_db)):
    """获取所有矿机列表"""
    miners = db.query(Miner).all()
    result = []
    for miner in miners:
        # 获取最新状态
        latest_status = db.query(MinerStatus).filter(
            MinerStatus.miner_id == miner.id
        ).order_by(MinerStatus.timestamp.desc()).first()
        
        miner_dict = {
            "id": miner.id,
            "ip_address": miner.ip_address,
            "model": miner.model,
            "hostname": miner.hostname,
            "mac_address": miner.mac_address,
            "is_online": miner.is_online,
            "last_seen": miner.last_seen.isoformat() if miner.last_seen else None,
            "latest_status": None
        }
        
        if latest_status:
            miner_dict["latest_status"] = {
                "timestamp": latest_status.timestamp.isoformat(),
                "temp_chip": latest_status.temp_chip,
                "temp_pcb": latest_status.temp_pcb,
                "temp_max": latest_status.temp_max,
                "power_consumption": latest_status.power_consumption,
                "humidity": latest_status.humidity,
                "hashrate": latest_status.hashrate,
                "hashrate_5s": latest_status.hashrate_5s,
                "hashrate_avg": latest_status.hashrate_avg,
                "fan_speed_1": latest_status.fan_speed_1,
                "fan_speed_2": latest_status.fan_speed_2,
                "fan_speed_3": latest_status.fan_speed_3,
                "fan_speed_4": latest_status.fan_speed_4,
                "pool_url": latest_status.pool_url,
                "pool_user": latest_status.pool_user,
                "pool_status": latest_status.pool_status,
                "uptime": latest_status.uptime,
                "network_status": latest_status.network_status,
                "hashboard_info": json.loads(latest_status.hashboard_info) if latest_status.hashboard_info else []
            }
        
        result.append(miner_dict)
    
    return result

@app.get("/api/miners/{miner_id}")
async def get_miner_detail(miner_id: int, db: Session = Depends(get_db)):
    """获取矿机详细信息"""
    miner = db.query(Miner).filter(Miner.id == miner_id).first()
    if not miner:
        raise HTTPException(status_code=404, detail="矿机不存在")
    
    # 获取最新状态
    latest_status = db.query(MinerStatus).filter(
        MinerStatus.miner_id == miner_id
    ).order_by(MinerStatus.timestamp.desc()).first()
    
    # 获取历史状态（最近24小时）
    yesterday = datetime.utcnow() - timedelta(days=1)
    history = db.query(MinerStatus).filter(
        MinerStatus.miner_id == miner_id,
        MinerStatus.timestamp >= yesterday
    ).order_by(MinerStatus.timestamp.asc()).all()
    
    # 获取日志
    logs = db.query(MinerLog).filter(
        MinerLog.miner_id == miner_id
    ).order_by(MinerLog.timestamp.desc()).limit(100).all()
    
    result = {
        "id": miner.id,
        "ip_address": miner.ip_address,
        "model": miner.model,
        "hostname": miner.hostname,
        "mac_address": miner.mac_address,
        "is_online": miner.is_online,
        "last_seen": miner.last_seen.isoformat() if miner.last_seen else None,
        "latest_status": None,
        "history": [],
        "logs": []
    }
    
    if latest_status:
        result["latest_status"] = {
            "timestamp": latest_status.timestamp.isoformat(),
            "temp_chip": latest_status.temp_chip,
            "temp_pcb": latest_status.temp_pcb,
            "temp_max": latest_status.temp_max,
            "power_consumption": latest_status.power_consumption,
            "humidity": latest_status.humidity,
            "hashrate": latest_status.hashrate,
            "hashrate_5s": latest_status.hashrate_5s,
            "hashrate_avg": latest_status.hashrate_avg,
            "fan_speed_1": latest_status.fan_speed_1,
            "fan_speed_2": latest_status.fan_speed_2,
            "fan_speed_3": latest_status.fan_speed_3,
            "fan_speed_4": latest_status.fan_speed_4,
            "pool_url": latest_status.pool_url,
            "pool_user": latest_status.pool_user,
            "pool_status": latest_status.pool_status,
            "uptime": latest_status.uptime,
            "network_status": latest_status.network_status,
            "hashboard_info": json.loads(latest_status.hashboard_info) if latest_status.hashboard_info else []
        }
    
    result["history"] = [{
        "timestamp": s.timestamp.isoformat(),
        "temp_chip": s.temp_chip,
        "temp_pcb": s.temp_pcb,
        "hashrate": s.hashrate,
        "power_consumption": s.power_consumption
    } for s in history]
    
    result["logs"] = [{
        "id": log.id,
        "timestamp": log.timestamp.isoformat(),
        "log_level": log.log_level,
        "message": log.message,
        "source": log.source
    } for log in logs]
    
    return result

@app.get("/api/miners/{miner_id}/status")
async def get_miner_status(miner_id: int, db: Session = Depends(get_db)):
    """实时获取矿机状态（直接从矿机API获取）"""
    miner = db.query(Miner).filter(Miner.id == miner_id).first()
    if not miner:
        raise HTTPException(status_code=404, detail="矿机不存在")
    
    client = MinerAPIClient(miner.ip_address)
    data = await client.get_all_info()
    
    if not data:
        raise HTTPException(status_code=503, detail="无法连接到矿机")
    
    parsed_data = client.parse_miner_data(data)
    return parsed_data

@app.post("/api/miners/discover")
async def discover_miners_endpoint(db: Session = Depends(get_db)):
    """手动触发矿机发现"""
    miner_ips = await MinerDiscovery.discover_miners_batch()
    
    discovered_count = 0
    for ip in miner_ips:
        existing = db.query(Miner).filter(Miner.ip_address == ip).first()
        if not existing:
            # 获取矿机详细信息
            client = MinerAPIClient(ip)
            data = await client.get_all_info()
            if data:
                parsed = client.parse_miner_data(data)
                
                miner = Miner(
                    ip_address=ip,
                    model=parsed.get("model"),
                    hostname=parsed.get("hostname"),
                    is_online=True,
                    last_seen=datetime.utcnow()
                )
                db.add(miner)
                db.commit()
                db.refresh(miner)
                discovered_count += 1
    
    return {"message": f"发现 {discovered_count} 台新矿机", "total": len(miner_ips)}

@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """获取统计信息"""
    total_miners = db.query(Miner).count()
    online_miners = db.query(Miner).filter(Miner.is_online == True).count()
    
    # 总算力
    latest_statuses = db.query(MinerStatus).join(Miner).filter(
        Miner.is_online == True
    ).distinct(MinerStatus.miner_id).all()
    
    total_hashrate = sum(s.hashrate or 0 for s in latest_statuses)
    total_power = sum(s.power_consumption or 0 for s in latest_statuses)
    
    return {
        "total_miners": total_miners,
        "online_miners": online_miners,
        "offline_miners": total_miners - online_miners,
        "total_hashrate": total_hashrate,
        "total_power": total_power
    }

# ============ 定时任务 ============

async def update_all_miners_status():
    """更新所有矿机状态"""
    from database import SessionLocal
    db = SessionLocal()
    try:
        miners = db.query(Miner).all()
        for miner in miners:
            try:
                client = MinerAPIClient(miner.ip_address)
                data = await client.get_all_info()
                
                if data:
                    parsed = client.parse_miner_data(data)
                    
                    # 更新矿机基本信息
                    miner.is_online = parsed.get("is_online", False)
                    miner.last_seen = datetime.utcnow()
                    if parsed.get("model"):
                        miner.model = parsed.get("model")
                    if parsed.get("hostname"):
                        miner.hostname = parsed.get("hostname")
                    
                    # 保存状态
                    status = MinerStatus(
                        miner_id=miner.id,
                        temp_chip=parsed.get("temp_chip"),
                        temp_pcb=parsed.get("temp_pcb"),
                        temp_max=parsed.get("temp_max"),
                        power_consumption=parsed.get("power_consumption"),
                        humidity=parsed.get("humidity"),
                        hashrate=parsed.get("hashrate"),
                        hashrate_5s=parsed.get("hashrate_5s"),
                        hashrate_avg=parsed.get("hashrate_avg"),
                        fan_speed_1=parsed.get("fan_speeds", [None])[0] if len(parsed.get("fan_speeds", [])) > 0 else None,
                        fan_speed_2=parsed.get("fan_speeds", [None])[1] if len(parsed.get("fan_speeds", [])) > 1 else None,
                        fan_speed_3=parsed.get("fan_speeds", [None])[2] if len(parsed.get("fan_speeds", [])) > 2 else None,
                        fan_speed_4=parsed.get("fan_speeds", [None])[3] if len(parsed.get("fan_speeds", [])) > 3 else None,
                        pool_url=parsed.get("pool_info", [{}])[0].get("url") if parsed.get("pool_info") else None,
                        pool_user=parsed.get("pool_info", [{}])[0].get("user") if parsed.get("pool_info") else None,
                        pool_status=parsed.get("pool_info", [{}])[0].get("status") if parsed.get("pool_info") else None,
                        uptime=parsed.get("uptime"),
                        network_status=parsed.get("network_status"),
                        hasboard_info=json.dumps(parsed.get("hashboard_info", []))
                    )
                    db.add(status)
                    
                    # 记录日志
                    if not parsed.get("is_online"):
                        log = MinerLog(
                            miner_id=miner.id,
                            log_level="WARNING",
                            message=f"矿机离线: {miner.ip_address}",
                            source="system"
                        )
                        db.add(log)
                else:
                    miner.is_online = False
                    
            except Exception as e:
                print(f"更新矿机 {miner.ip_address} 状态失败: {e}")
                miner.is_online = False
        
        db.commit()
    except Exception as e:
        print(f"更新矿机状态失败: {e}")
        db.rollback()
    finally:
        db.close()

async def discover_new_miners():
    """发现新矿机"""
    from database import SessionLocal
    db = SessionLocal()
    try:
        miner_ips = await MinerDiscovery.discover_miners_batch()
        
        for ip in miner_ips:
            existing = db.query(Miner).filter(Miner.ip_address == ip).first()
            if not existing:
                client = MinerAPIClient(ip)
                data = await client.get_all_info()
                if data:
                    parsed = client.parse_miner_data(data)
                    
                    miner = Miner(
                        ip_address=ip,
                        model=parsed.get("model"),
                        hostname=parsed.get("hostname"),
                        is_online=True,
                        last_seen=datetime.utcnow()
                    )
                    db.add(miner)
        
        db.commit()
    except Exception as e:
        print(f"发现矿机失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    from config import BACKEND_HOST, BACKEND_PORT
    uvicorn.run(app, host=BACKEND_HOST, port=BACKEND_PORT)
