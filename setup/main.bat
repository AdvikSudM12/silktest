@echo off
chcp 65001 > nul
title Silk Project - Управление зависимостями

echo.
echo ==========================================
echo   🎯 SILK PROJECT - УПРАВЛЕНИЕ ЗАВИСИМОСТЯМИ
echo ==========================================
echo.

REM Определяем путь к директории скрипта
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Ищем Python
set PYTHON_CMD=
for %%i in (py python python3) do (
    %%i --version >nul 2>&1
    if !errorlevel! == 0 (
        set PYTHON_CMD=%%i
        goto :found_python
    )
)

echo ❌ Python не найден!
echo Установите Python с https://python.org
echo.
pause
exit /b 1

:found_python
echo ✅ Найден Python: %PYTHON_CMD%
echo.

REM Запускаем главный скрипт
echo 🚀 Запуск главного меню...
echo.
%PYTHON_CMD% main.py

REM Ожидание перед закрытием
echo.
echo Нажмите любую клавишу для выхода...
pause > nul 