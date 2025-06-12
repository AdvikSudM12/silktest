#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Конфигурация логирования для отладки процесса проверки файлов
Использует библиотеку loguru для красивого и информативного логирования
"""

import sys
import os
from loguru import logger
from pathlib import Path

# Глобальный флаг для предотвращения дублирования инициализации
_LOGGER_INITIALIZED = False

def setup_debug_logging():
    """
    Настраивает логирование для отладки процесса проверки файлов
    
    Создает два вывода:
    1. В консоль - с цветовым кодированием
    2. В файл - подробные логи для анализа
    """
    global _LOGGER_INITIALIZED
    
    # Проверяем, не настроено ли уже логирование
    if _LOGGER_INITIALIZED:
        return logger
    
    # Удаляем все существующие обработчики loguru (избегаем дублирования)
    logger.remove()
    
    # Создаем директорию для логов
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    # Формат для консоли (цветной и краткий)
    console_format = (
        "<green>{time:HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    # Формат для файла (подробный)
    file_format = (
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
        "{level: <8} | "
        "{name}:{function}:{line} | "
        "{message}"
    )
    
    # Добавляем вывод в консоль (только INFO и выше для чистоты)
    logger.add(
        sys.stderr,
        format=console_format,
        level="INFO",  # Изменили с DEBUG на INFO для консоли
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    # Добавляем вывод в файл (с ротацией)
    logger.add(
        log_dir / "file_check_debug.log",
        format=file_format,
        level="DEBUG",
        rotation="10 MB",
        retention="7 days",
        compression="zip",
        backtrace=True,
        diagnose=True
    )
    
    # Отмечаем, что логирование настроено
    _LOGGER_INITIALIZED = True
    
    logger.info("🚀 Логирование настроено для отладки проверки файлов")
    logger.info(f"📁 Логи сохраняются в: {log_dir / 'file_check_debug.log'}")
    
    return logger

def get_logger(name: str):
    """
    Получает настроенный логгер для модуля
    
    Args:
        name: Имя модуля/файла
    
    Returns:
        Настроенный логгер
    """
    return logger.bind(name=name)

# Автоматически настраиваем логирование при импорте
# (защита от множественной инициализации)
setup_debug_logging() 