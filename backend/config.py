"""
配置文件
"""
import os

# 矿机API端口
MINER_API_PORT = 4028

# IP地址范围
IP_RANGES = [
    ("10.102.0.1", "10.102.0.255"),
    ("10.102.1.1", "10.102.1.65")
]

# 数据库配置
DATABASE_URL = "sqlite:///./miners.db"

# API超时设置（秒）
API_TIMEOUT = 5

# 定时任务配置
SCAN_INTERVAL = 60  # 扫描间隔（秒）
STATUS_UPDATE_INTERVAL = 30  # 状态更新间隔（秒）

# 后端服务配置
BACKEND_HOST = "0.0.0.0"
BACKEND_PORT = 8000

# CORS配置
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
