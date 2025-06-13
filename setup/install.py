#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
🚀 УСТАНОВКА ЗАВИСИМОСТЕЙ SILK PROJECT
=====================================

Автоматическая установка всех Python и Node.js зависимостей
для проекта Silk. Работает на любом устройстве и ОС.

Запуск: python install.py
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

class Colors:
    """Цвета для консольного вывода"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def colored_print(message, color=Colors.WHITE):
    """Цветной вывод в консоль"""
    if platform.system() == 'Windows':
        # На Windows цвета могут не работать, используем обычный вывод
        print(message)
    else:
        print(f"{color}{message}{Colors.END}")

def print_header():
    """Вывод заголовка установки"""
    colored_print("=" * 60, Colors.CYAN)
    colored_print("🚀 УСТАНОВКА ЗАВИСИМОСТЕЙ SILK PROJECT", Colors.BOLD)
    colored_print("=" * 60, Colors.CYAN)
    print()

def find_project_root():
    """Находит корень проекта по наличию package.json"""
    current_dir = Path(__file__).parent
    
    # Поднимаемся на один уровень вверх (из setup/ в корень проекта)
    project_root = current_dir.parent
    
    # Проверяем наличие package.json
    if (project_root / 'package.json').exists():
        colored_print(f"✅ Найден корень проекта: {project_root}", Colors.GREEN)
        return project_root
    
    # Если не найден, ищем в текущей директории
    for i in range(3):  # Поиск максимум 3 уровня вверх
        if (current_dir / 'package.json').exists():
            colored_print(f"✅ Найден корень проекта: {current_dir}", Colors.GREEN)
            return current_dir
        current_dir = current_dir.parent
    
    colored_print(f"⚠️ Корень проекта не найден, используем: {project_root}", Colors.YELLOW)
    return project_root

def check_python():
    """Проверка Python"""
    colored_print("[1/4] Проверка Python...", Colors.BLUE)
    
    # Пробуем разные команды Python
    python_commands = ['py', 'python', 'python3']
    
    for cmd in python_commands:
        try:
            result = subprocess.run([cmd, '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                version = result.stdout.strip()
                colored_print(f"✅ Python найден: {version} (команда: {cmd})", Colors.GREEN)
                return cmd
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue
    
    colored_print("❌ Python не найден!", Colors.RED)
    colored_print("Установите Python с https://python.org", Colors.YELLOW)
    return None

def check_nodejs():
    """Проверка Node.js"""
    colored_print("[2/4] Проверка Node.js...", Colors.BLUE)
    
    node_found = False
    npm_found = False
    
    try:
        # Проверяем Node.js (используем shell=True для Windows)
        if platform.system() == 'Windows':
            result = subprocess.run('node --version', shell=True,
                                  capture_output=True, text=True, timeout=10)
        else:
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            node_version = result.stdout.strip()
            colored_print(f"✅ Node.js найден: {node_version}", Colors.GREEN)
            node_found = True
        else:
            colored_print("❌ Node.js не найден!", Colors.RED)
            
    except (subprocess.TimeoutExpired, FileNotFoundError):
        colored_print("❌ Node.js не найден!", Colors.RED)
    
    try:
        # Проверяем npm (используем shell=True для Windows)
        colored_print("🔍 Проверяем npm...", Colors.CYAN)
        if platform.system() == 'Windows':
            result = subprocess.run('npm --version', shell=True,
                                  capture_output=True, text=True, timeout=30)
        else:
            result = subprocess.run(['npm', '--version'], 
                                  capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            npm_version = result.stdout.strip()
            colored_print(f"✅ npm найден: {npm_version}", Colors.GREEN)
            npm_found = True
        else:
            colored_print(f"❌ npm не найден! Код возврата: {result.returncode}", Colors.RED)
            colored_print(f"stderr: {result.stderr}", Colors.RED)
            
    except subprocess.TimeoutExpired:
        colored_print("❌ npm таймаут!", Colors.RED)
    except FileNotFoundError:
        colored_print("❌ npm команда не найдена!", Colors.RED)
    except Exception as e:
        colored_print(f"❌ npm ошибка: {e}", Colors.RED)
    
    if not node_found or not npm_found:
        if not node_found:
            colored_print("Установите Node.js с https://nodejs.org", Colors.YELLOW)
        if not npm_found:
            colored_print("npm должен поставляться с Node.js", Colors.YELLOW)
        return False
    
    return True

def install_python_dependencies(python_cmd, project_root):
    """Установка Python зависимостей"""
    colored_print("[3/4] Установка Python зависимостей...", Colors.BLUE)
    
    # Список файлов requirements.txt
    requirements_files = [
        project_root / 'requirements.txt',
        project_root / 'scripts' / 'requirements.txt'
    ]
    
    success = True
    
    # Обновляем pip
    try:
        colored_print("🔄 Обновление pip...", Colors.CYAN)
        subprocess.run([python_cmd, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                      check=True)
        colored_print("✅ pip обновлен", Colors.GREEN)
    except subprocess.CalledProcessError:
        colored_print("⚠️ Не удалось обновить pip", Colors.YELLOW)
    
    # Устанавливаем зависимости из каждого файла
    for req_file in requirements_files:
        if req_file.exists():
            try:
                colored_print(f"📦 Установка из {req_file.name}...", Colors.CYAN)
                subprocess.run([python_cmd, '-m', 'pip', 'install', '-r', str(req_file)], 
                              check=True)
                colored_print(f"✅ Зависимости из {req_file.name} установлены", Colors.GREEN)
            except subprocess.CalledProcessError as e:
                colored_print(f"❌ Ошибка установки из {req_file.name}: {e}", Colors.RED)
                success = False
        else:
            colored_print(f"⚠️ Файл {req_file} не найден", Colors.YELLOW)
    
    return success

def install_nodejs_dependencies(project_root):
    """Установка Node.js зависимостей"""
    colored_print("[4/4] Установка Node.js зависимостей...", Colors.BLUE)
    
    # Меняем рабочую директорию на корень проекта
    original_dir = os.getcwd()
    
    try:
        os.chdir(project_root)
        colored_print(f"📁 Переход в {project_root}", Colors.CYAN)
        
        # Проверяем наличие package.json
        if not (project_root / 'package.json').exists():
            colored_print("❌ Файл package.json не найден!", Colors.RED)
            return False
        
        # Определяем пакетный менеджер
        package_manager = 'npm'
        if (project_root / 'yarn.lock').exists():
            try:
                if platform.system() == 'Windows':
                    subprocess.run('yarn --version', shell=True,
                                  capture_output=True, text=True, timeout=10)
                else:
                    subprocess.run(['yarn', '--version'], 
                                  capture_output=True, text=True, timeout=10)
                package_manager = 'yarn'
                colored_print("🔍 Используем yarn", Colors.CYAN)
            except (subprocess.TimeoutExpired, FileNotFoundError):
                colored_print("🔍 Yarn не найден, используем npm", Colors.CYAN)
        
        # Установка зависимостей
        colored_print(f"📦 Установка через {package_manager}...", Colors.CYAN)
        
        if package_manager == 'yarn':
            if platform.system() == 'Windows':
                subprocess.run('yarn install', shell=True, check=True)
            else:
                subprocess.run(['yarn', 'install'], check=True)
        else:
            if platform.system() == 'Windows':
                subprocess.run('npm install', shell=True, check=True)
            else:
                subprocess.run(['npm', 'install'], check=True)
        
        colored_print("✅ Node.js зависимости установлены", Colors.GREEN)
        
        # Проверяем ts-node (используем shell=True для Windows)
        try:
            if platform.system() == 'Windows':
                result = subprocess.run('npx ts-node --version', shell=True,
                                      capture_output=True, text=True, timeout=10)
            else:
                result = subprocess.run(['npx', 'ts-node', '--version'], 
                                      capture_output=True, text=True, timeout=10)
                                      
            if result.returncode == 0:
                colored_print("✅ ts-node работает", Colors.GREEN)
            else:
                colored_print("⚠️ ts-node может не работать", Colors.YELLOW)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            colored_print("⚠️ Не удалось проверить ts-node", Colors.YELLOW)
        
        return True
        
    except subprocess.CalledProcessError as e:
        colored_print(f"❌ Ошибка установки Node.js зависимостей: {e}", Colors.RED)
        return False
    finally:
        os.chdir(original_dir)

def final_check(python_cmd, project_root):
    """Финальная проверка установленных зависимостей"""
    colored_print("\n🔍 ФИНАЛЬНАЯ ПРОВЕРКА", Colors.PURPLE)
    colored_print("=" * 30, Colors.PURPLE)
    
    # Проверка Python модулей
    python_modules = ['PyQt6', 'loguru', 'pandas', 'openpyxl']
    
    for module in python_modules:
        try:
            subprocess.run([python_cmd, '-c', f'import {module}'], 
                          check=True, capture_output=True)
            colored_print(f"✅ {module}", Colors.GREEN)
        except subprocess.CalledProcessError:
            colored_print(f"❌ {module}", Colors.RED)
    
    # Проверка Node.js (используем shell=True для Windows)
    original_dir = os.getcwd()
    try:
        os.chdir(project_root)
        if platform.system() == 'Windows':
            result = subprocess.run('npx ts-node --version', shell=True,
                                  capture_output=True, text=True, timeout=10)
        else:
            result = subprocess.run(['npx', 'ts-node', '--version'], 
                                  capture_output=True, text=True, timeout=10)
                                  
        if result.returncode == 0:
            colored_print("✅ ts-node работает", Colors.GREEN)
        else:
            colored_print("❌ ts-node не работает", Colors.RED)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        colored_print("❌ npx/ts-node не доступен", Colors.RED)
    finally:
        os.chdir(original_dir)

def print_success_message(project_root):
    """Вывод сообщения об успешной установке"""
    print()
    colored_print("🎉 УСТАНОВКА ЗАВЕРШЕНА УСПЕШНО!", Colors.GREEN)
    colored_print("=" * 40, Colors.GREEN)
    print()
    colored_print("Для запуска приложения:", Colors.BOLD)
    colored_print(f"  py {project_root}/run_app.py", Colors.CYAN)
    print()
    colored_print("Для запуска скриптов:", Colors.BOLD)
    colored_print("  npm run start:release-parser-5", Colors.CYAN)
    colored_print("  npm run start:update-releases-shipment-statuses", Colors.CYAN)
    print()

def main():
    """Основная функция установки"""
    print_header()
    
    # Находим корень проекта
    project_root = find_project_root()
    
    # Проверяем Python
    python_cmd = check_python()
    if not python_cmd:
        colored_print("❌ Установка прервана", Colors.RED)
        return False
    
    # Проверяем Node.js
    if not check_nodejs():
        colored_print("❌ Установка прервана", Colors.RED)
        return False
    
    # Устанавливаем Python зависимости
    if not install_python_dependencies(python_cmd, project_root):
        colored_print("⚠️ Ошибки при установке Python зависимостей", Colors.YELLOW)
    
    # Устанавливаем Node.js зависимости
    if not install_nodejs_dependencies(project_root):
        colored_print("⚠️ Ошибки при установке Node.js зависимостей", Colors.YELLOW)
    
    # Финальная проверка
    final_check(python_cmd, project_root)
    
    # Сообщение об успехе
    print_success_message(project_root)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            input("\n✅ Нажмите Enter для выхода...")
        else:
            input("\n❌ Нажмите Enter для выхода...")
    except KeyboardInterrupt:
        print("\n\n🛑 Установка прервана пользователем")
        sys.exit(1)
    except Exception as e:
        colored_print(f"\n💥 Критическая ошибка: {e}", Colors.RED)
        input("\n❌ Нажмите Enter для выхода...")
        sys.exit(1) 