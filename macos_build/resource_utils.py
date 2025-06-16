#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Утилиты для работы с ресурсами в macOS app bundle
Определяет правильные пути для хранения пользовательских данных
"""

import os
import sys
from pathlib import Path


def is_app_bundle() -> bool:
    """
    Проверяет, запущено ли приложение из macOS app bundle
    
    Returns:
        True если приложение запущено из .app bundle
    """
    if sys.platform != 'darwin':
        return False
        
    # Проверяем, находимся ли мы внутри .app bundle
    executable_path = sys.executable
    return '.app/Contents/' in executable_path


def get_app_data_dir() -> Path:
    """
    Получает директорию для пользовательских данных приложения
    
    Returns:
        Path к директории данных приложения
    """
    if is_app_bundle():
        # Для app bundle используем скрытую папку в домашней директории
        home_dir = Path.home()
        app_data_dir = home_dir / '.gosilk_staff'
    else:
        # В режиме разработки используем локальную папку data
        app_data_dir = Path(__file__).parent.parent / 'pyqt_app' / 'data'
    
    # Создаем директорию если её нет
    app_data_dir.mkdir(exist_ok=True)
    
    return app_data_dir


def get_logs_dir() -> Path:
    """
    Получает директорию для логов приложения
    
    Returns:
        Path к директории логов
    """
    if is_app_bundle():
        # Для app bundle используем стандартную папку логов macOS
        home_dir = Path.home()
        logs_dir = home_dir / 'Library' / 'Logs' / 'GoSilk Staff'
    else:
        # В режиме разработки используем локальную папку logs
        logs_dir = Path(__file__).parent.parent / 'pyqt_app' / 'logs'
    
    # Создаем директорию если её нет
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    return logs_dir


def get_env_file_path() -> Path:
    """
    Получает путь к .env файлу
    
    Returns:
        Path к .env файлу
    """
    if is_app_bundle():
        # Для app bundle храним .env в пользовательской папке
        app_data_dir = get_app_data_dir()
        return app_data_dir / '.env'
    else:
        # В режиме разработки используем корень проекта
        return Path(__file__).parent.parent / '.env'


def get_resource_path(relative_path: str) -> Path:
    """
    Получает абсолютный путь к ресурсу внутри app bundle
    
    Args:
        relative_path: Относительный путь к ресурсу
        
    Returns:
        Path к ресурсу
    """
    if is_app_bundle():
        # В app bundle ресурсы находятся в Contents/Resources/
        bundle_dir = Path(sys.executable).parent.parent
        return bundle_dir / 'Resources' / relative_path
    else:
        # В режиме разработки используем обычные пути
        return Path(__file__).parent.parent / relative_path

def setup_user_config():
    """
    Настройка пользовательской конфигурации при первом запуске
    
    Returns:
        bool: True если это первый запуск, False если уже настроено
    """
    app_data_dir = get_app_data_dir()
    user_env_file = app_data_dir / '.env'
    
    # Проверяем, первый ли это запуск
    if user_env_file.exists():
        return False  # Уже настроено
    
    # Копируем шаблон .env в пользовательскую директорию
    env_template = get_resource_path('.env.template')
    
    if env_template.exists():
        import shutil
        shutil.copy2(env_template, user_env_file)
        print(f"✅ Создан файл конфигурации: {user_env_file}")
    else:
        # Создаем базовый .env файл если шаблона нет
        default_env_content = """# GoSilk Staff Configuration
EMD_API=https://api.emd.ru
EMD_SPACE=silk
EMD_TOKEN=
EMD_USER_ID=

# Optional Settings
NODE_ENV=production
DEBUG=false
"""
        user_env_file.write_text(default_env_content, encoding='utf-8')
        print(f"✅ Создан базовый файл конфигурации: {user_env_file}")
    
    return True  # Первый запуск

def get_node_executable():
    """
    Получение пути к исполняемому файлу Node.js
    
    Returns:
        str: Путь к node executable
    """
    if is_app_bundle():
        # В app bundle используем встроенный Node.js
        node_path = get_resource_path('embedded_node') / 'bin' / 'node'
        return str(node_path)
    else:
        # В режиме разработки используем системный Node.js
        return 'node' 