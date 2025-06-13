#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
🔍 ПРОВЕРКА ЗАВИСИМОСТЕЙ SILK PROJECT
====================================

Проверяет все установленные Python и Node.js зависимости
и генерирует подробный отчет.

Запуск: python check_dependencies.py
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import json
from datetime import datetime

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
        print(message)
    else:
        print(f"{color}{message}{Colors.END}")

def print_header():
    """Вывод заголовка проверки"""
    colored_print("=" * 60, Colors.CYAN)
    colored_print("🔍 ПРОВЕРКА ЗАВИСИМОСТЕЙ SILK PROJECT", Colors.BOLD)
    colored_print("=" * 60, Colors.CYAN)
    print()

def find_project_root():
    """Находит корень проекта"""
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    
    if (project_root / 'package.json').exists():
        return project_root
    
    for i in range(3):
        if (current_dir / 'package.json').exists():
            return current_dir
        current_dir = current_dir.parent
    
    return project_root

def check_python_environment():
    """Проверка Python окружения"""
    colored_print("🐍 ПРОВЕРКА PYTHON ОКРУЖЕНИЯ", Colors.BLUE)
    colored_print("-" * 40, Colors.BLUE)
    
    python_info = {}
    
    # Определяем команду Python
    python_commands = ['py', 'python', 'python3']
    python_cmd = None
    
    for cmd in python_commands:
        try:
            result = subprocess.run([cmd, '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                python_cmd = cmd
                python_info['command'] = cmd
                python_info['version'] = result.stdout.strip()
                colored_print(f"✅ Python: {result.stdout.strip()} (команда: {cmd})", Colors.GREEN)
                break
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue
    
    if not python_cmd:
        colored_print("❌ Python не найден!", Colors.RED)
        return None, {}
    
    # Проверяем pip
    try:
        result = subprocess.run([python_cmd, '-m', 'pip', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            python_info['pip_version'] = result.stdout.strip()
            colored_print(f"✅ pip: {result.stdout.strip()}", Colors.GREEN)
        else:
            colored_print("❌ pip не найден!", Colors.RED)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        colored_print("❌ pip не доступен!", Colors.RED)
    
    print()
    return python_cmd, python_info

def check_python_modules(python_cmd):
    """Проверка Python модулей"""
    colored_print("📦 ПРОВЕРКА PYTHON МОДУЛЕЙ", Colors.BLUE)
    colored_print("-" * 40, Colors.BLUE)
    
    # Основные модули проекта
    required_modules = {
        'PyQt6': 'GUI библиотека',
        'loguru': 'Система логирования',
        'pandas': 'Обработка данных',
        'openpyxl': 'Работа с Excel',
        'pathlib': 'Работа с путями (встроенный)',
        'json': 'JSON обработка (встроенный)',
        'os': 'Системные функции (встроенный)',
        'sys': 'Системная информация (встроенный)'
    }
    
    module_status = {}
    
    for module, description in required_modules.items():
        try:
            result = subprocess.run([python_cmd, '-c', f'import {module}; print({module}.__version__ if hasattr({module}, "__version__") else "встроенный")'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                version = result.stdout.strip()
                colored_print(f"✅ {module}: {version} - {description}", Colors.GREEN)
                module_status[module] = {'status': 'ok', 'version': version, 'description': description}
            else:
                colored_print(f"❌ {module}: не найден - {description}", Colors.RED)
                module_status[module] = {'status': 'missing', 'description': description}
        except (subprocess.TimeoutExpired, FileNotFoundError):
            colored_print(f"❌ {module}: ошибка проверки - {description}", Colors.RED)
            module_status[module] = {'status': 'error', 'description': description}
    
    print()
    return module_status

def check_nodejs_environment():
    """Проверка Node.js окружения"""
    colored_print("📦 ПРОВЕРКА NODE.JS ОКРУЖЕНИЯ", Colors.BLUE)
    colored_print("-" * 40, Colors.BLUE)
    
    nodejs_info = {}
    
    # Проверяем Node.js (используем shell=True для Windows)
    try:
        if platform.system() == 'Windows':
            result = subprocess.run('node --version', shell=True,
                                  capture_output=True, text=True, timeout=10)
        else:
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, text=True, timeout=10)
                                  
        if result.returncode == 0:
            nodejs_info['node_version'] = result.stdout.strip()
            colored_print(f"✅ Node.js: {result.stdout.strip()}", Colors.GREEN)
        else:
            colored_print("❌ Node.js не найден!", Colors.RED)
            return {}
    except (subprocess.TimeoutExpired, FileNotFoundError):
        colored_print("❌ Node.js не найден!", Colors.RED)
        return {}
    
    # Проверяем npm (используем shell=True для Windows)
    try:
        if platform.system() == 'Windows':
            result = subprocess.run('npm --version', shell=True,
                                  capture_output=True, text=True, timeout=10)
        else:
            result = subprocess.run(['npm', '--version'], 
                                  capture_output=True, text=True, timeout=10)
                                  
        if result.returncode == 0:
            nodejs_info['npm_version'] = result.stdout.strip()
            colored_print(f"✅ npm: {result.stdout.strip()}", Colors.GREEN)
        else:
            colored_print("❌ npm не найден!", Colors.RED)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        colored_print("❌ npm не найден!", Colors.RED)
    
    # Проверяем yarn (опционально, используем shell=True для Windows)
    try:
        if platform.system() == 'Windows':
            result = subprocess.run('yarn --version', shell=True,
                                  capture_output=True, text=True, timeout=10)
        else:
            result = subprocess.run(['yarn', '--version'], 
                                  capture_output=True, text=True, timeout=10)
                                  
        if result.returncode == 0:
            nodejs_info['yarn_version'] = result.stdout.strip()
            colored_print(f"✅ yarn: {result.stdout.strip()}", Colors.GREEN)
        else:
            colored_print("⚠️ yarn не найден (опционально)", Colors.YELLOW)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        colored_print("⚠️ yarn не найден (опционально)", Colors.YELLOW)
    
    print()
    return nodejs_info

def check_nodejs_packages(project_root):
    """Проверка Node.js пакетов"""
    colored_print("📦 ПРОВЕРКА NODE.JS ПАКЕТОВ", Colors.BLUE)
    colored_print("-" * 40, Colors.BLUE)
    
    # Читаем package.json
    package_json_path = project_root / 'package.json'
    if not package_json_path.exists():
        colored_print("❌ package.json не найден!", Colors.RED)
        return {}
    
    try:
        with open(package_json_path, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
    except Exception as e:
        colored_print(f"❌ Ошибка чтения package.json: {e}", Colors.RED)
        return {}
    
    # Проверяем node_modules
    node_modules_path = project_root / 'node_modules'
    if not node_modules_path.exists():
        colored_print("❌ Папка node_modules не найдена! Запустите npm install", Colors.RED)
        return {}
    
    colored_print(f"✅ Папка node_modules найдена", Colors.GREEN)
    
    # Проверяем ключевые пакеты
    key_packages = ['typescript', 'ts-node', 'axios', 'dotenv']
    package_status = {}
    
    for package in key_packages:
        package_path = node_modules_path / package
        if package_path.exists():
            try:
                package_json = package_path / 'package.json'
                if package_json.exists():
                    with open(package_json, 'r', encoding='utf-8') as f:
                        pkg_data = json.load(f)
                        version = pkg_data.get('version', 'неизвестно')
                        colored_print(f"✅ {package}: {version}", Colors.GREEN)
                        package_status[package] = {'status': 'ok', 'version': version}
                else:
                    colored_print(f"✅ {package}: установлен", Colors.GREEN)
                    package_status[package] = {'status': 'ok', 'version': 'неизвестно'}
            except Exception:
                colored_print(f"✅ {package}: установлен", Colors.GREEN)
                package_status[package] = {'status': 'ok', 'version': 'неизвестно'}
        else:
            colored_print(f"❌ {package}: не найден", Colors.RED)
            package_status[package] = {'status': 'missing'}
    
    # Проверяем ts-node (используем shell=True для Windows)
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
            colored_print(f"✅ ts-node через npx: работает", Colors.GREEN)
            package_status['ts-node-npx'] = {'status': 'ok'}
        else:
            colored_print(f"❌ ts-node через npx: не работает", Colors.RED)
            package_status['ts-node-npx'] = {'status': 'error'}
    except (subprocess.TimeoutExpired, FileNotFoundError):
        colored_print(f"❌ npx/ts-node не доступен", Colors.RED)
        package_status['ts-node-npx'] = {'status': 'error'}
    finally:
        os.chdir(original_dir)
    
    print()
    return package_status

def check_project_files(project_root):
    """Проверка файлов проекта"""
    colored_print("📁 ПРОВЕРКА ФАЙЛОВ ПРОЕКТА", Colors.BLUE)
    colored_print("-" * 40, Colors.BLUE)
    
    required_files = {
        'package.json': 'Конфигурация Node.js',
        'requirements.txt': 'Python зависимости (основные)',
        'scripts/requirements.txt': 'Python зависимости (скрипты)',
        'run_app.py': 'Запуск PyQt приложения',
        'pyqt_app/main.py': 'Основной файл приложения',
        'src/apps/release-parser-5/index.ts': 'TypeScript парсер',
        'src/apps/update-releases-shipment-statuses/index.ts': 'TypeScript обновление статусов'
    }
    
    file_status = {}
    
    for file_path, description in required_files.items():
        full_path = project_root / file_path
        if full_path.exists():
            file_size = full_path.stat().st_size
            colored_print(f"✅ {file_path}: {file_size} байт - {description}", Colors.GREEN)
            file_status[file_path] = {'status': 'ok', 'size': file_size, 'description': description}
        else:
            colored_print(f"❌ {file_path}: не найден - {description}", Colors.RED)
            file_status[file_path] = {'status': 'missing', 'description': description}
    
    print()
    return file_status

def generate_report(python_info, module_status, nodejs_info, package_status, file_status):
    """Генерация итогового отчета"""
    colored_print("📊 ИТОГОВЫЙ ОТЧЕТ", Colors.PURPLE)
    colored_print("=" * 40, Colors.PURPLE)
    
    # Подсчет статистики
    total_modules = len(module_status)
    ok_modules = sum(1 for status in module_status.values() if status['status'] == 'ok')
    
    total_packages = len(package_status)
    ok_packages = sum(1 for status in package_status.values() if status['status'] == 'ok')
    
    total_files = len(file_status)
    ok_files = sum(1 for status in file_status.values() if status['status'] == 'ok')
    
    colored_print(f"Python модули: {ok_modules}/{total_modules}", 
                 Colors.GREEN if ok_modules == total_modules else Colors.YELLOW)
    colored_print(f"Node.js пакеты: {ok_packages}/{total_packages}", 
                 Colors.GREEN if ok_packages == total_packages else Colors.YELLOW)
    colored_print(f"Файлы проекта: {ok_files}/{total_files}", 
                 Colors.GREEN if ok_files == total_files else Colors.YELLOW)
    
    # Общий статус
    all_ok = (ok_modules == total_modules and 
              ok_packages == total_packages and 
              ok_files == total_files and 
              bool(python_info) and 
              bool(nodejs_info))
    
    print()
    if all_ok:
        colored_print("🎉 ВСЕ ЗАВИСИМОСТИ УСТАНОВЛЕНЫ КОРРЕКТНО!", Colors.GREEN)
        colored_print("Проект готов к работе!", Colors.GREEN)
    else:
        colored_print("⚠️ ОБНАРУЖЕНЫ ПРОБЛЕМЫ С ЗАВИСИМОСТЯМИ", Colors.YELLOW)
        colored_print("Запустите install.py для установки недостающих компонентов", Colors.YELLOW)
    
    # Создаем JSON отчет
    report_data = {
        'timestamp': datetime.now().isoformat(),
        'system': {
            'os': platform.system(),
            'python_info': python_info,
            'nodejs_info': nodejs_info
        },
        'dependencies': {
            'python_modules': module_status,
            'nodejs_packages': package_status,
            'project_files': file_status
        },
        'summary': {
            'python_modules_ok': f"{ok_modules}/{total_modules}",
            'nodejs_packages_ok': f"{ok_packages}/{total_packages}",
            'project_files_ok': f"{ok_files}/{total_files}",
            'all_ok': all_ok
        }
    }
    
    # Сохраняем отчет
    try:
        report_path = Path(__file__).parent / 'dependency_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        colored_print(f"\n📄 Подробный отчет сохранен: {report_path}", Colors.CYAN)
    except Exception as e:
        colored_print(f"\n⚠️ Не удалось сохранить отчет: {e}", Colors.YELLOW)

def main():
    """Основная функция проверки"""
    print_header()
    
    # Находим корень проекта
    project_root = find_project_root()
    colored_print(f"🎯 Корень проекта: {project_root}", Colors.CYAN)
    print()
    
    # Проверяем Python
    python_cmd, python_info = check_python_environment()
    if not python_cmd:
        colored_print("❌ Проверка прервана", Colors.RED)
        return False
    
    # Проверяем Python модули
    module_status = check_python_modules(python_cmd)
    
    # Проверяем Node.js
    nodejs_info = check_nodejs_environment()
    
    # Проверяем Node.js пакеты
    package_status = check_nodejs_packages(project_root)
    
    # Проверяем файлы проекта
    file_status = check_project_files(project_root)
    
    # Генерируем отчет
    generate_report(python_info, module_status, nodejs_info, package_status, file_status)
    
    return True

if __name__ == "__main__":
    try:
        main()
        input("\n✅ Нажмите Enter для выхода...")
    except KeyboardInterrupt:
        print("\n\n🛑 Проверка прервана пользователем")
        sys.exit(1)
    except Exception as e:
        colored_print(f"\n💥 Критическая ошибка: {e}", Colors.RED)
        input("\n❌ Нажмите Enter для выхода...")
        sys.exit(1) 