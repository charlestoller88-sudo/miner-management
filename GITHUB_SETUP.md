# GitHub 部署指南

## 步骤1：在GitHub上创建新仓库

1. 登录您的GitHub账号
2. 点击右上角的 "+" 号，选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: `miner-management` (或您喜欢的名称)
   - **Description**: `Antminer S19 XP系列矿机管理系统`
   - **Visibility**: 选择 Public（公开）或 Private（私有）
   - **不要**勾选 "Initialize this repository with a README"（我们已经有了）
4. 点击 "Create repository"

## 步骤2：连接本地仓库到GitHub

创建仓库后，GitHub会显示设置说明。执行以下命令：

### 如果您的GitHub用户名是 `your-username`，仓库名是 `miner-management`：

```bash
# 添加远程仓库（请替换为您的实际GitHub用户名和仓库名）
git remote add origin https://github.com/your-username/miner-management.git

# 或者使用SSH（如果您配置了SSH密钥）
git remote add origin git@github.com:your-username/miner-management.git
```

### 查看远程仓库配置：

```bash
git remote -v
```

## 步骤3：推送代码到GitHub

```bash
# 推送代码到GitHub（首次推送）
git branch -M main
git push -u origin main
```

**注意**：如果您的默认分支是 `master` 而不是 `main`，使用：
```bash
git push -u origin master
```

## 步骤4：验证

推送成功后，刷新GitHub仓库页面，您应该能看到所有文件已经上传。

## 后续开发工作流

### 日常开发流程：

1. **修改代码后，查看更改**：
   ```bash
   git status
   git diff
   ```

2. **添加更改到暂存区**：
   ```bash
   git add .
   # 或添加特定文件
   git add backend/main.py
   ```

3. **提交更改**：
   ```bash
   git commit -m "描述您的更改内容"
   ```

4. **推送到GitHub**：
   ```bash
   git push
   ```

### 从GitHub拉取最新代码：

```bash
git pull origin main
# 或
git pull origin master
```

## 常见问题

### Q: 推送时提示需要认证？

**A**: 您需要配置Git认证：

1. **使用Personal Access Token（推荐）**：
   - GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - 生成新token，勾选 `repo` 权限
   - 推送时使用token作为密码

2. **或配置SSH密钥**：
   - 生成SSH密钥：`ssh-keygen -t ed25519 -C "your_email@example.com"`
   - 将公钥添加到GitHub：Settings → SSH and GPG keys

### Q: 如何查看Git配置？

```bash
# 查看用户名和邮箱
git config user.name
git config user.email

# 设置用户名和邮箱（如果还没设置）
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Q: 如何创建新分支？

```bash
# 创建并切换到新分支
git checkout -b feature/new-feature

# 推送新分支到GitHub
git push -u origin feature/new-feature
```

## 推荐的Git提交信息格式

- `feat: 添加新功能`
- `fix: 修复bug`
- `docs: 更新文档`
- `style: 代码格式调整`
- `refactor: 代码重构`
- `test: 添加测试`
- `chore: 构建/工具相关`

示例：
```bash
git commit -m "feat: 添加矿机温度告警功能"
git commit -m "fix: 修复IP扫描超时问题"
```

## 下一步

1. ✅ 初始化Git仓库（已完成）
2. ✅ 创建初始提交（已完成）
3. ⏭️ 在GitHub创建仓库
4. ⏭️ 连接远程仓库
5. ⏭️ 推送代码

完成这些步骤后，您的项目就可以在GitHub上协同开发了！
