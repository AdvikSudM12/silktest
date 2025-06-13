#!/usr/bin/env python3
"""
Главный скрипт для управления зависимостями проекта Silk
Предоставляет меню для выбора между проверкой и установкой зависимостей
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
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def colored_print(message, color=Colors.WHITE, end='\n'):
    """Печать с цветом"""
    if platform.system() == 'Windows':
        # В Windows может не поддерживаться ANSI, но попробуем
        print(f"{color}{message}{Colors.END}", end=end)
    else:
        print(f"{color}{message}{Colors.END}", end=end)

def print_header():
    """Печать заголовка"""
    colored_print("=" * 60, Colors.PURPLE)
    colored_print("🎯 SILK PROJECT - УПРАВЛЕНИЕ ЗАВИСИМОСТЯМИ", Colors.BOLD + Colors.PURPLE)
    colored_print("=" * 60, Colors.PURPLE)
    print()

def print_menu():
    """Печать меню выбора"""
    colored_print("Выберите действие:", Colors.CYAN)
    print()
    colored_print("1️⃣  Проверить зависимости", Colors.BLUE)
    colored_print("    Проверяет все установленные зависимости", Colors.WHITE)
    colored_print("    и выводит подробный отчет", Colors.WHITE)
    print()
    colored_print("2️⃣  Установить зависимости", Colors.GREEN)
    colored_print("    Устанавливает все необходимые зависимости", Colors.WHITE)
    colored_print("    для проекта (Python + Node.js)", Colors.WHITE)
    print()
    colored_print("3️⃣  Выход", Colors.RED)
    print()

def get_user_choice():
    """Получение выбора пользователя"""
    while True:
        try:
            colored_print("Введите номер (1-3): ", Colors.YELLOW, end='')
            choice = input().strip()
            
            if choice in ['1', '2', '3']:
                return int(choice)
            else:
                colored_print("❌ Неверный выбор! Введите 1, 2 или 3", Colors.RED)
                
        except KeyboardInterrupt:
            print()
            colored_print("👋 Выход по Ctrl+C", Colors.YELLOW)
            sys.exit(0)
        except Exception:
            colored_print("❌ Ошибка ввода! Попробуйте снова", Colors.RED)

def run_script(script_name, description):
    """Запуск скрипта"""
    print()
    colored_print(f"🚀 {description}", Colors.BOLD + Colors.CYAN)
    colored_print("-" * 50, Colors.CYAN)
    
    script_path = Path(__file__).parent / script_name
    
    if not script_path.exists():
        colored_print(f"❌ Скрипт {script_name} не найден!", Colors.RED)
        return False
    
    try:
        # Определяем команду Python
        python_cmd = 'py' if platform.system() == 'Windows' else 'python3'
        
        # Запускаем скрипт
        result = subprocess.run([python_cmd, str(script_path)], 
                              cwd=script_path.parent)
        
        if result.returncode == 0:
            colored_print(f"✅ {description} завершена успешно", Colors.GREEN)
            return True
        else:
            colored_print(f"❌ {description} завершена с ошибками", Colors.RED)
            return False
            
    except KeyboardInterrupt:
        print()
        colored_print("⏹️ Выполнение прервано пользователем", Colors.YELLOW)
        return False
    except Exception as e:
        colored_print(f"❌ Ошибка при запуске скрипта: {e}", Colors.RED)
        return False

def wait_for_user():
    """Ожидание нажатия клавиши"""
    print()
    colored_print("Нажмите Enter для продолжения...", Colors.CYAN)
    try:
        input()
    except KeyboardInterrupt:
        print()
        sys.exit(0)

def main():
    """Главная функция"""
    try:
        while True:
            # Очистка экрана
            if platform.system() == 'Windows':
                os.system('cls')
            else:
                os.system('clear')
            
            # Заголовок и меню
            print_header()
            print_menu()
            
            # Получение выбора
            choice = get_user_choice()
            
            if choice == 1:
                # Проверка зависимостей
                success = run_script('check_dependencies.py', 
                                   'Проверка зависимостей')
                wait_for_user()
                
            elif choice == 2:
                # Установка зависимостей
                success = run_script('install.py', 
                                   'Установка зависимостей')
                wait_for_user()
                
            elif choice == 3:
                # Выход
                print()
                colored_print("👋 До свидания!", Colors.GREEN)
                sys.exit(0)
                
    except KeyboardInterrupt:
        print()
        colored_print("👋 Выход по Ctrl+C", Colors.YELLOW)
        sys.exit(0)
    except Exception as e:
        colored_print(f"❌ Неожиданная ошибка: {e}", Colors.RED)
        sys.exit(1)

if __name__ == "__main__":
    main() 