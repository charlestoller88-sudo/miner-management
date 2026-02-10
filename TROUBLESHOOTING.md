# 故障排查指南

## 依赖安装问题

### 问题1: pydantic-core 编译错误（需要 Rust）

**错误信息**：
```
error: subprocess-exited-with-error
× Preparing metadata (pyproject.toml) did not run successfully.
```

**原因**：
- 您使用的是 Python 3.14，而 `pydantic-core` 的旧版本没有为 Python 3.14 提供预编译的 wheel
- 需要从源码编译，但系统缺少 Rust 编译器

**解决方案（按推荐顺序）**：

#### 方案1：使用更新的依赖版本（推荐）

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

如果仍有问题，尝试：

```bash
pip install fastapi uvicorn[standard] sqlalchemy apscheduler httpx pydantic python-multipart aiohttp --upgrade
```

#### 方案2：使用 Python 3.11-3.13（最稳定）

Python 3.14 是较新的版本，某些包可能还没有完全支持。建议使用 Python 3.11、3.12 或 3.13：

1. 安装 Python 3.13（推荐）或 3.12
2. 创建新的虚拟环境：
   ```bash
   python3.13 -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```
3. 重新安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

#### 方案3：安装 Rust 工具链（不推荐，除非必须）

如果您必须使用 Python 3.14 和旧版本的 pydantic：

1. 安装 Rust：
   - 访问 https://rustup.rs/
   - 下载并运行安装程序
   - 重启终端

2. 验证安装：
   ```bash
   rustc --version
   cargo --version
   ```

3. 重新安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

### 问题2: 其他常见安装错误

#### 权限错误

```bash
# Windows（以管理员身份运行 PowerShell）
pip install -r requirements.txt --user

# 或使用虚拟环境（推荐）
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### 网络超时

```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或使用阿里云镜像
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

#### 依赖冲突

```bash
# 清理并重新安装
pip uninstall -y fastapi uvicorn sqlalchemy apscheduler httpx pydantic python-multipart aiohttp
pip install -r requirements.txt
```

## 运行时问题

### 问题：无法连接到矿机

1. **检查网络连接**：
   ```bash
   ping 10.102.0.1
   ```

2. **检查防火墙**：
   - Windows: 确保允许 Python 通过防火墙
   - 确保端口 4028 未被阻止

3. **检查IP配置**：
   - 确认矿机IP在配置的范围内
   - 编辑 `backend/config.py` 检查 IP_RANGES

### 问题：数据库错误

```bash
# 删除旧数据库，重新初始化
rm backend/miners.db  # Linux/Mac
del backend\miners.db  # Windows

# 重新启动后端
python backend/start.py
```

### 问题：端口被占用

```bash
# Windows 检查端口占用
netstat -ano | findstr :8000

# 修改端口（编辑 backend/config.py）
BACKEND_PORT = 8001
```

## 前端问题

### 问题：npm install 失败

```bash
# 清理缓存
npm cache clean --force

# 删除 node_modules 重新安装
rm -rf node_modules  # Linux/Mac
rmdir /s node_modules  # Windows
npm install
```

### 问题：前端无法连接后端

1. 检查后端是否运行：访问 http://localhost:8000/docs
2. 检查 CORS 配置：编辑 `backend/config.py` 中的 `CORS_ORIGINS`
3. 检查前端 API 地址：编辑 `frontend/src/api/client.ts`

## 获取帮助

如果以上方法都无法解决问题，请提供：
1. Python 版本：`python --version`
2. 操作系统版本
3. 完整的错误信息
4. 您尝试过的解决方案
