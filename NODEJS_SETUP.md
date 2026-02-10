# Node.js 安装指南

## 问题说明

错误信息 `无法将"npm"项识别为 cmdlet` 表示：
- Node.js 未安装，或
- Node.js 已安装但未添加到系统 PATH 环境变量

## 解决方案

### 方案1：安装 Node.js（如果未安装）

1. **下载 Node.js**：
   - 访问 https://nodejs.org/
   - 下载 **LTS 版本**（推荐，例如 v20.x 或 v18.x）
   - 选择 Windows Installer (.msi) 64位版本

2. **安装 Node.js**：
   - 运行下载的 .msi 安装程序
   - **重要**：安装时确保勾选 "Add to PATH" 选项
   - 按照向导完成安装

3. **验证安装**：
   - **关闭当前 PowerShell 窗口**（重要！）
   - 打开新的 PowerShell 窗口
   - 运行以下命令验证：
     ```powershell
     node --version
     npm --version
     ```
   - 应该显示版本号，例如：
     ```
     v20.11.0
     10.2.4
     ```

### 方案2：如果已安装但无法识别（PATH 问题）

#### 检查 Node.js 是否已安装：

```powershell
# 检查 Node.js 是否在常见位置
Test-Path "C:\Program Files\nodejs\node.exe"
Test-Path "C:\Program Files (x86)\nodejs\node.exe"
```

#### 手动添加到 PATH：

1. **查找 Node.js 安装路径**：
   - 通常在 `C:\Program Files\nodejs\` 或 `C:\Program Files (x86)\nodejs\`

2. **添加到 PATH**：
   - 按 `Win + R`，输入 `sysdm.cpl`，回车
   - 点击"高级"选项卡
   - 点击"环境变量"
   - 在"系统变量"中找到 `Path`，点击"编辑"
   - 点击"新建"，添加 Node.js 路径（例如：`C:\Program Files\nodejs`）
   - 点击"确定"保存

3. **重启 PowerShell**：
   - 关闭所有 PowerShell 窗口
   - 重新打开 PowerShell
   - 验证：`node --version` 和 `npm --version`

### 方案3：使用 nvm-windows（推荐用于多版本管理）

如果您需要管理多个 Node.js 版本：

1. **下载 nvm-windows**：
   - 访问 https://github.com/coreybutler/nvm-windows/releases
   - 下载 `nvm-setup.exe`

2. **安装 nvm-windows**：
   - 运行安装程序
   - 完成后重启 PowerShell

3. **安装 Node.js**：
   ```powershell
   # 安装最新的 LTS 版本
   nvm install lts
   
   # 使用该版本
   nvm use lts
   
   # 验证
   node --version
   npm --version
   ```

## 安装完成后的操作

1. **验证安装**：
   ```powershell
   node --version
   npm --version
   ```

2. **进入前端目录**：
   ```powershell
   cd frontend
   ```

3. **安装依赖**：
   ```powershell
   npm install
   ```

4. **如果下载慢，使用国内镜像**：
   ```powershell
   npm install --registry=https://registry.npmmirror.com
   ```

   或设置永久镜像：
   ```powershell
   npm config set registry https://registry.npmmirror.com
   ```

## 常见问题

### Q: 安装后仍然无法识别 npm？

**A**: 
1. 确保**完全关闭并重新打开** PowerShell（不是只关闭标签页）
2. 检查 PATH 是否正确添加
3. 尝试重启电脑

### Q: npm install 很慢？

**A**: 使用国内镜像源：
```powershell
npm config set registry https://registry.npmmirror.com
npm install
```

### Q: 需要什么版本的 Node.js？

**A**: 
- **最低要求**：Node.js 14.x 或更高
- **推荐**：Node.js 18.x LTS 或 20.x LTS
- 本项目使用 React 18，兼容 Node.js 14+

### Q: 如何检查 Node.js 是否在 PATH 中？

**A**: 
```powershell
$env:Path -split ';' | Select-String nodejs
```

如果显示包含 nodejs 的路径，说明已添加。

## 快速检查清单

- [ ] Node.js 已下载并安装
- [ ] 安装时勾选了 "Add to PATH"
- [ ] 已关闭并重新打开 PowerShell
- [ ] `node --version` 显示版本号
- [ ] `npm --version` 显示版本号
- [ ] 可以执行 `npm install`

## 下一步

安装完成后，继续执行：

```powershell
cd frontend
npm install
npm start
```
