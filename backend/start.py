"""
启动脚本
"""
import uvicorn
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import BACKEND_HOST, BACKEND_PORT

if __name__ == "__main__":
    print(f"启动矿机管理系统后端服务...")
    print(f"访问地址: http://{BACKEND_HOST}:{BACKEND_PORT}")
    print(f"API文档: http://{BACKEND_HOST}:{BACKEND_PORT}/docs")
    uvicorn.run("main:app", host=BACKEND_HOST, port=BACKEND_PORT, reload=True)
