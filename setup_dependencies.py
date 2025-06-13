#!/usr/bin/env python3
"""
Launcher для системы управления зависимостями Silk Project
Запускает главное меню из папки setup/
"""

import sys
import subprocess
import platform
from pathlib import Path

def main():
    """Запуск главного меню установки зависимостей"""
    # Определяем путь к main.py в папке setup
    script_path = Path(__file__).parent / 'setup' / 'main.py'
    
    if not script_path.exists():
        print("❌ Файл setup/main.py не найден!")
        print("Убедитесь, что папка setup содержит все необходимые файлы.")
        input("Нажмите Enter для выхода...")
        sys.exit(1)
    
    try:
        # Определяем команду Python
        python_cmd = 'py' if platform.system() == 'Windows' else 'python3'
        
        # Запускаем главное меню
        result = subprocess.run([python_cmd, str(script_path)])
        sys.exit(result.returncode)
        
    except KeyboardInterrupt:
        print("\n👋 Выход по Ctrl+C")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Ошибка при запуске: {e}")
        input("Нажмите Enter для выхода...")
        sys.exit(1)

if __name__ == "__main__":
    main() 