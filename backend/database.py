"""
数据库模型和连接
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import DATABASE_URL

Base = declarative_base()

class Miner(Base):
    """矿机基本信息表"""
    __tablename__ = "miners"
    
    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, unique=True, index=True, nullable=False)
    model = Column(String)  # 矿机型号
    hostname = Column(String)  # 主机名
    mac_address = Column(String)  # MAC地址
    is_online = Column(Boolean, default=False)  # 是否在线
    last_seen = Column(DateTime, default=datetime.utcnow)  # 最后在线时间
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MinerStatus(Base):
    """矿机状态表"""
    __tablename__ = "miner_status"
    
    id = Column(Integer, primary_key=True, index=True)
    miner_id = Column(Integer, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # 温度信息
    temp_chip = Column(Float)  # 芯片温度
    temp_pcb = Column(Float)  # PCB温度
    temp_max = Column(Float)  # 最高温度
    
    # 功耗和湿度
    power_consumption = Column(Float)  # 功耗（W）
    humidity = Column(Float)  # 湿度
    
    # 算力信息
    hashrate = Column(Float)  # 总算力（TH/s）
    hashrate_5s = Column(Float)  # 5秒平均算力
    hashrate_avg = Column(Float)  # 平均算力
    
    # 风扇信息
    fan_speed_1 = Column(Integer)  # 风扇1转速
    fan_speed_2 = Column(Integer)  # 风扇2转速
    fan_speed_3 = Column(Integer)  # 风扇3转速
    fan_speed_4 = Column(Integer)  # 风扇4转速
    
    # 矿池信息
    pool_url = Column(String)  # 矿池URL
    pool_user = Column(String)  # 矿池用户名
    pool_status = Column(String)  # 矿池连接状态
    
    # 运行信息
    uptime = Column(Integer)  # 运行时间（秒）
    network_status = Column(String)  # 网络状态
    
    # 算力板信息（JSON格式存储）
    hashboard_info = Column(Text)  # 算力板详细信息

class MinerLog(Base):
    """矿机日志表"""
    __tablename__ = "miner_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    miner_id = Column(Integer, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    log_level = Column(String)  # INFO, WARNING, ERROR
    message = Column(Text)
    source = Column(String)  # 日志来源

# 创建数据库引擎和会话
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """初始化数据库"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
