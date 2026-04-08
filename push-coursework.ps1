# First-time: create GitHub repo "coursework" (public) at github.com/eunbijoel/coursework — empty, no README.
# Then run this script from PowerShell:
#   Set-Location C:\Users\keti\coursework
#   powershell -ExecutionPolicy Bypass -File .\push-coursework.ps1

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path .git)) { git init }

git config user.name "eunbijoel"
git config user.email "eunbijoel@users.noreply.github.com"

git add -A
git status

$staged = git diff --cached --name-only
if ($staged) {
  git commit -m "docs: add coursework monorepo structure and project documentation"
}

git branch -M main
$remotes = @(git remote 2>$null)
if ($remotes -contains "origin") { git remote remove origin }
git remote add origin https://github.com/eunbijoel/coursework.git
git push -u origin main

Write-Host "Done. If push failed, create the repo on GitHub or fix auth."
