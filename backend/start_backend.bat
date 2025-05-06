@echo off
echo 🔥 Запуск Flask backend...

cd /d %~dp0
call venv\Scripts\activate
flask run
