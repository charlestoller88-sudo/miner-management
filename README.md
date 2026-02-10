# 矿机管理系统

一个用于管理Antminer S19 XP系列矿机的Web管理系统。

## 功能特性

- ✅ 实时监控矿机状态（温度、功耗、湿度、算力、风扇转速等）
- ✅ 矿池连接状态监控
- ✅ 网络连接状态检查
- ✅ 运行日志查看
- ✅ 算力板实时算力监控
- ✅ 运行时间统计
- ✅ 自动发现局域网内矿机
- ✅ 历史数据图表展示

## 技术栈

- 后端：Python FastAPI
- 前端：React + TypeScript
- 数据库：SQLite
- 定时任务：APScheduler

## 安装和运行

### 1. 后端设置

```bash
cd backend
pip install -r requirements.txt
python start.py
```

后端将在 http://localhost:8000 运行
API文档可在 http://localhost:8000/docs 查看

### 2. 前端设置

```bash
cd frontend
npm install
npm start
```

前端将在 http://localhost:3000 运行

## 配置

矿机IP地址范围（在 `backend/config.py` 中配置）：
- 10.102.0.1 - 10.102.0.255
- 10.102.1.1 - 10.102.1.65

API端口：4028

### 修改配置

编辑 `backend/config.py` 文件可以修改：
- IP地址范围
- API超时时间
- 扫描间隔
- 状态更新间隔

## 使用说明

1. **启动系统**：先启动后端服务，再启动前端服务
2. **发现矿机**：点击"发现新矿机"按钮，系统会自动扫描配置的IP范围
3. **查看状态**：在仪表板可以看到所有矿机的实时状态
4. **查看详情**：点击矿机卡片可以查看详细信息，包括：
   - 温度、功耗、湿度等实时数据
   - 算力板详细信息
   - 历史趋势图表
   - 运行日志

## API接口

- `GET /api/miners` - 获取所有矿机列表
- `GET /api/miners/{id}` - 获取矿机详细信息
- `GET /api/miners/{id}/status` - 实时获取矿机状态
- `POST /api/miners/discover` - 手动触发矿机发现
- `GET /api/stats` - 获取统计信息

## 注意事项

1. 确保您的电脑可以通过局域网访问所有矿机
2. 矿机API端口4028需要在防火墙中开放
3. 首次运行会自动创建数据库文件 `miners.db`
4. 系统会每30秒自动更新矿机状态，每60秒扫描新矿机

## 故障排查

如果无法连接到矿机：
1. 检查网络连接
2. 确认矿机IP地址在配置的范围内
3. 检查防火墙设置
4. 查看后端日志输出
