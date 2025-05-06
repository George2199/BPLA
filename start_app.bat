@echo off
echo 🚀 Запускаем BPLA...

:: Запуск backend
start "" backend\start_backend.bat

:: Подождём 3 секунды, чтобы backend успел подняться
timeout /t 3 >nul

:: Запуск Electron frontend
start "" "./AeroCosmos 0.0.0.exe"
