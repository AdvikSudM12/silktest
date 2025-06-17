#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Централизованный менеджер путей для приложения GoSilk Staff
Автоматически определяет правильные пути в зависимости от режима запуска:
- Development mode: локальные пути
- macOS app bundle: пользовательские директории macOS
"""

import os
from pathlib import Path
from typing import Union

# Попытка импорта resource_utils для macOS app bundle поддержки
try:
    from macos_build.resource_utils import (
        get_app_data_dir, 
        get_logs_dir, 
        get_env_file_path as macos_get_env_file_path,
        is_app_bundle
    )
    MACOS_BUILD_AVAILABLE = True
except ImportError:
    # В режиме разработки macos_build модули могут быть недоступны
    MACOS_BUILD_AVAILABLE = False


def get_data_directory() -> Path:
    """
    Получает директорию для пользовательских данных приложения
    
    Returns:
        Path к директории данных:
        - App bundle: ~/.gosilk_staff/
        - Development: pyqt_app/data/
    """
    if MACOS_BUILD_AVAILABLE and is_app_bundle():
        # App bundle режим - пользовательские данные
        return get_app_data_dir()
    else:
        # Режим разработки - локальная папка data
        data_dir = Path(__file__).parent / "data"
        data_dir.mkdir(exist_ok=True)
        return data_dir


def get_logs_directory() -> Path:
    """
    Получает директорию для логов приложения
    
    Returns:
        Path к директории логов:
        - App bundle: ~/Library/Logs/GoSilk Staff/
        - Development: pyqt_app/logs/
    """
    if MACOS_BUILD_AVAILABLE and is_app_bundle():
        # App bundle режим - стандартная папка логов macOS
        return get_logs_dir()
    else:
        # Режим разработки - локальная папка logs
        logs_dir = Path(__file__).parent / "logs"
        logs_dir.mkdir(exist_ok=True)
        return logs_dir


def get_results_directory() -> Path:
    """
    Получает директорию для результатов работы приложения
    
    Returns:
        Path к директории результатов:
        - App bundle: ~/.gosilk_staff/results/
        - Development: results/
    """
    if MACOS_BUILD_AVAILABLE and is_app_bundle():
        # App bundle режим - results в пользовательских данных
        results_dir = get_app_data_dir() / "results"
        results_dir.mkdir(exist_ok=True)
        return results_dir
    else:
        # Режим разработки - корневая папка results
        results_dir = Path(__file__).parent.parent / "results"
        results_dir.mkdir(exist_ok=True)
        return results_dir


def get_env_file_path() -> Path:
    """
    Получает путь к .env файлу
    
    Returns:
        Path к .env файлу:
        - App bundle: ~/.gosilk_staff/.env
        - Development: .env в корне проекта
    """
    if MACOS_BUILD_AVAILABLE and is_app_bundle():
        # App bundle режим - используем функцию из resource_utils
        return macos_get_env_file_path()
    else:
        # Режим разработки - .env в корне проекта
        return Path(__file__).parent.parent / ".env"


def get_project_root() -> Path:
    """
    Получает корневую директорию проекта
    
    Returns:
        Path к корневой директории проекта
    """
    return Path(__file__).parent.parent


# Дополнительные utility функции для удобства

def ensure_directory_exists(path: Union[str, Path]) -> Path:
    """
    Гарантирует существование директории
    
    Args:
        path: Путь к директории
        
    Returns:
        Path объект к директории
    """
    path_obj = Path(path)
    path_obj.mkdir(parents=True, exist_ok=True)
    return path_obj


def get_file_in_data_dir(filename: str) -> Path:
    """
    Получает путь к файлу в директории данных
    
    Args:
        filename: Имя файла
        
    Returns:
        Path к файлу в директории данных
    """
    return get_data_directory() / filename


def get_file_in_results_dir(filename: str) -> Path:
    """
    Получает путь к файлу в директории результатов
    
    Args:
        filename: Имя файла
        
    Returns:
        Path к файлу в директории результатов
    """
    return get_results_directory() / filename


def is_development_mode() -> bool:
    """
    Определяет, запущено ли приложение в режиме разработки
    
    Returns:
        True если режим разработки, False если app bundle
    """
    if not MACOS_BUILD_AVAILABLE:
        return True
    return not is_app_bundle()


# Константы для часто используемых файлов
PATHS_JSON_FILE = "paths.json"
CONFIG_JSON_FILE = "config.json"
TEMPLATES_JSON_FILE = "templates.json"
SESSION_ANALYTICS_FILE = "session_analytics.json"
UPLOAD_STATE_FILE = "upload_state.json"
LOG_FILE_NAME = "file_check_debug.log"


def get_paths_json_path() -> Path:
    """Получает путь к файлу paths.json"""
    return get_file_in_data_dir(PATHS_JSON_FILE)


def get_config_json_path() -> Path:
    """Получает путь к файлу config.json"""
    return get_file_in_data_dir(CONFIG_JSON_FILE)


def get_templates_json_path() -> Path:
    """Получает путь к файлу templates.json"""
    return get_file_in_data_dir(TEMPLATES_JSON_FILE)


def get_session_analytics_path() -> Path:
    """Получает путь к файлу session_analytics.json"""
    return get_file_in_data_dir(SESSION_ANALYTICS_FILE)


def get_upload_state_path() -> Path:
    """Получает путь к файлу upload_state.json"""
    return get_file_in_data_dir(UPLOAD_STATE_FILE)


def get_log_file_path() -> Path:
    """Получает путь к основному файлу логов"""
    return get_logs_directory() / LOG_FILE_NAME


# Alias для совместимости
def get_config_file_path(filename: str) -> Path:
    """Alias для get_file_in_data_dir для совместимости"""
    return get_file_in_data_dir(filename)


def get_data_file_path(filename: str) -> Path:
    """Получает путь к файлу в директории данных (alias для get_file_in_data_dir)"""
    return get_file_in_data_dir(filename)


def get_results_directory_path() -> Path:
    """Получает путь к директории результатов (alias для get_results_directory)"""
    return get_results_directory()


# Диагностическая функция для отладки
def get_paths_info() -> dict:
    """
    Получает информацию о всех используемых путях для диагностики
    
    Returns:
        Словарь с информацией о путях
    """
    return {
        "mode": "app_bundle" if (MACOS_BUILD_AVAILABLE and is_app_bundle()) else "development",
        "macos_build_available": MACOS_BUILD_AVAILABLE,
        "data_directory": str(get_data_directory()),
        "logs_directory": str(get_logs_directory()),
        "results_directory": str(get_results_directory()),
        "env_file": str(get_env_file_path()),
        "project_root": str(get_project_root()),
        "paths_json": str(get_paths_json_path()),
        "config_json": str(get_config_json_path()),
        "log_file": str(get_log_file_path())
    } 