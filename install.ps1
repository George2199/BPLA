# install.ps1
$ErrorActionPreference = "Stop"

Write-Host "→ Проверка Python..."
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Скачиваем Python..."
    $url = "https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe"
    $exe = "$env:TEMP\python.exe"
    Invoke-WebRequest $url -OutFile $exe
    Start-Process $exe -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
}

Write-Host "→ Создание виртуального окружения..."
python -m venv venv
.\venv\Scripts\pip install -r backend/requirements.txt

Write-Host "→ Проверка Node.js..."
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "Скачиваем Node.js..."
    $url = "https://nodejs.org/dist/v20.12.2/node-v20.12.2-x64.msi"
    $msi = "$env:TEMP\node.msi"
    Invoke-WebRequest $url -OutFile $msi
    Start-Process msiexec.exe -ArgumentList "/i $msi /quiet" -Wait
}

Write-Host "→ Установка npm-пакетов..."
npm install
