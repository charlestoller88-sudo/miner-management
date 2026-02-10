# GitHub仓库设置脚本
# 使用方法: .\setup-github.ps1 -GitHubUsername "your-username" -RepoName "miner-management"

param(
    [Parameter(Mandatory=$true)]
    [string]$GitHubUsername,
    
    [Parameter(Mandatory=$false)]
    [string]$RepoName = "miner-management"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GitHub 仓库设置脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否已经配置了远程仓库
$existingRemote = git remote get-url origin 2>$null
if ($existingRemote) {
    Write-Host "检测到已存在的远程仓库: $existingRemote" -ForegroundColor Yellow
    $response = Read-Host "是否要替换为新的远程仓库? (y/n)"
    if ($response -eq "y" -or $response -eq "Y") {
        git remote remove origin
    } else {
        Write-Host "操作已取消" -ForegroundColor Red
        exit
    }
}

# 设置远程仓库URL
$remoteUrl = "https://github.com/$GitHubUsername/$RepoName.git"
Write-Host "添加远程仓库: $remoteUrl" -ForegroundColor Green
git remote add origin $remoteUrl

# 检查当前分支名
$currentBranch = git branch --show-current
Write-Host "当前分支: $currentBranch" -ForegroundColor Green

# 显示下一步操作提示
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "下一步操作:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. 确保您已经在GitHub上创建了仓库: $RepoName" -ForegroundColor Yellow
Write-Host "2. 推送代码到GitHub，执行以下命令之一:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   如果使用main分支:" -ForegroundColor White
Write-Host "   git branch -M main" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "   如果使用master分支:" -ForegroundColor White
Write-Host "   git push -u origin master" -ForegroundColor Cyan
Write-Host ""
