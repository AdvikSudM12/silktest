"""
🎯 GoSilk Staff - PyQt6 Application Package

Основные модули приложения:
- main.py - главное окно приложения  
- env_manager.py - управление окружением и конфигурацией
- script_manager.py - запуск и управление скриптами
- session_data_manager.py - управление сессионными данными
- auth_manager.py - аутентификация и авторизация
- components.py - UI компоненты
- logger_config.py - настройка логирования

Папки:
- pages/ - страницы приложения
- dialogs/ - диалоговые окна
- workers/ - фоновые процессы
- resources/ - ресурсы (иконки, стили)
- data/ - данные приложения
- logs/ - файлы логов
"""

__version__ = "1.0.0"
__author__ = "GoSilk Staff Team"

# Основные импорты для удобства (без main.py во избежание циклических импортов)
from .env_manager import EnvManager
from .script_manager import ScriptManager  
from .session_data_manager import SessionDataManager
from .auth_manager import AuthManager
from .logger_config import setup_debug_logging

__all__ = [
    'EnvManager',
    'ScriptManager', 
    'SessionDataManager',
    'AuthManager',
    'setup_debug_logging'
] 