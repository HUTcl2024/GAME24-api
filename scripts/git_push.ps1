# scripts/git_push.ps1
Param(
  [Parameter(Mandatory=$true)] [string]$RepoUrl,
  [string]$UserName = "",
  [string]$UserEmail = ""
)

# 进入脚本所在的项目根目录（假设脚本位于项目的 scripts/ 下）
Set-Location -Path (Split-Path -Parent $PSScriptRoot)

# 可选：设置用户名邮箱
if ($UserName -ne "") { git config user.name  $UserName }
if ($UserEmail -ne "") { git config user.email $UserEmail }

# 初始化并首个提交
if (-not (Test-Path ".git")) {
  git init
}
git add .
git commit -m "Initial commit: Game24 API"

# 默认 main 分支
try { git branch -M main } catch {}

# 绑定远端
$hasOrigin = git remote | Select-String -Pattern "^origin$"
if (-not $hasOrigin) {
  git remote add origin $RepoUrl
} else {
  git remote set-url origin $RepoUrl
}

# 推送
git push -u origin main
Write-Host "Done. Pushed to $RepoUrl"
