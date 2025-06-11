#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime
from typing import Dict, Optional, Any
from pathlib import Path

# DEBUG: импорт логгера для системы отладки - нужно будет удалить позже
from .logger_config import get_logger
debug_logger = get_logger("session_data_manager")


class SessionDataManager:
    """
    Менеджер сессионных данных для аналитики
    
    Хранит данные только во время работы приложения.
    Данные удаляются при закрытии приложения.
    """
    
    def __init__(self):
        """Инициализация менеджера сессионных данных"""
        # Определяем путь к файлу сессионных данных
        self.data_dir = Path(__file__).parent / "data"
        self.session_file = self.data_dir / "session_analytics.json"
        
        # Создаем директорию если её нет
        self.data_dir.mkdir(exist_ok=True)
        
        debug_logger.info(f"🚀 SessionDataManager инициализирован")
        debug_logger.debug(f"📁 Директория данных: {self.data_dir}")
        debug_logger.debug(f"📄 Файл сессии: {self.session_file}")
        
        # Очищаем все старые сессионные данные при запуске (создает пустые файлы)
        self.clear_all_session_data()
    
    def save_comparison_result(self, comparison_result: Dict[str, Any], 
                             excel_file_path: str = "", 
                             directory_path: str = "") -> bool:
        """
        Сохраняет результат сравнения файлов в сессионные данные
        
        Args:
            comparison_result: Результат сравнения файлов
            excel_file_path: Путь к Excel файлу  
            directory_path: Путь к директории с файлами
            
        Returns:
            True если сохранение успешно, False если ошибка
        """
        try:
            debug_logger.info("💾 Сохраняем результат сравнения в сессионные данные")
            
            # Получаем пути из paths.json если не переданы
            if not excel_file_path or not directory_path:
                excel_file_path, directory_path = self._get_paths_from_config()
            
            # Формируем структуру сессионных данных
            session_data = {
                "timestamp": datetime.now().isoformat(),
                "excel_file_path": excel_file_path,
                "directory_path": directory_path,
                "comparison_result": comparison_result,
                "analytics_summary": self._create_analytics_summary(comparison_result)
            }
            
            debug_logger.debug(f"📊 Структура данных: {list(session_data.keys())}")
            debug_logger.debug(f"📈 Количество ошибок: {comparison_result.get('error_count', 0)}")
            debug_logger.debug(f"📄 Файл результатов: {comparison_result.get('results_file', 'Нет')}")
            
            # Сохраняем в файл
            with open(self.session_file, "w", encoding="utf-8") as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
            
            debug_logger.success("✅ Сессионные данные успешно сохранены")
            return True
            
        except Exception as e:
            debug_logger.error(f"❌ Ошибка при сохранении сессионных данных: {e}")
            return False
    
    def get_latest_analytics_data(self) -> Optional[Dict[str, Any]]:
        """
        Получает последние данные аналитики из сессии
        
        Returns:
            Словарь с данными аналитики или None если данных нет
        """
        try:
            if not self.session_file.exists():
                debug_logger.warning("⚠️ Файл сессионных данных не найден")
                return None
            
            debug_logger.info("📖 Читаем сессионные данные аналитики")
            
            with open(self.session_file, "r", encoding="utf-8") as f:
                session_data = json.load(f)
            
            # Проверяем что файл не пустой
            if not session_data or len(session_data) == 0:
                debug_logger.warning("📭 Файл сессионных данных пустой")
                return None
            
            debug_logger.success("✅ Сессионные данные успешно загружены")
            debug_logger.debug(f"📅 Дата создания: {session_data.get('timestamp', 'Неизвестно')}")
            
            return session_data
            
        except Exception as e:
            debug_logger.error(f"❌ Ошибка при чтении сессионных данных: {e}")
            return None
    
    def clear_session_data(self) -> bool:
        """
        Очищает сессионные данные (перезаписывает пустыми данными)
        
        Returns:
            True если очистка успешна
        """
        try:
            # Создаем пустую структуру данных
            empty_session_data = {}
            
            # Перезаписываем файл пустыми данными вместо удаления
            with open(self.session_file, "w", encoding="utf-8") as f:
                json.dump(empty_session_data, f, ensure_ascii=False, indent=2)
            
            debug_logger.info("🗑️ Сессионные данные очищены (файл перезаписан)")
            return True
            
        except Exception as e:
            debug_logger.error(f"❌ Ошибка при очистке сессионных данных: {e}")
            return False
    
    def clear_session_paths(self) -> bool:
        """
        Очищает сессионные пути (перезаписывает пустыми данными)
        
        Returns:
            True если очистка успешна
        """
        try:
            # Создаем пустую структуру путей
            empty_paths_data = {
                "excel_file_path": "",
                "directory_path": "",
                "last_updated": ""
            }
            
            paths_file = self.data_dir / "paths.json"
            
            # Перезаписываем файл пустыми данными вместо удаления
            with open(paths_file, "w", encoding="utf-8") as f:
                json.dump(empty_paths_data, f, ensure_ascii=False, indent=2)
            
            debug_logger.info("📁 Сессионные пути очищены (файл перезаписан)")
            return True
            
        except Exception as e:
            debug_logger.error(f"❌ Ошибка при очистке путей: {e}")
            return False
    
    def clear_all_session_data(self) -> bool:
        """
        Очищает все сессионные данные (аналитика + пути)
        
        Returns:
            True если очистка успешна
        """
        analytics_cleared = self.clear_session_data()
        paths_cleared = self.clear_session_paths()
        
        if analytics_cleared and paths_cleared:
            debug_logger.success("✅ Все сессионные данные успешно очищены")
            return True
        else:
            debug_logger.warning("⚠️ Частичная очистка сессионных данных")
            return False
    
    def has_analytics_data(self) -> bool:
        """
        Проверяет наличие данных аналитики в сессии
        
        Returns:
            True если данные есть
        """
        try:
            if not self.session_file.exists():
                return False
            
            # Проверяем что файл не пустой
            with open(self.session_file, "r", encoding="utf-8") as f:
                session_data = json.load(f)
            
            # Файл считается пустым если это пустой словарь или None
            return bool(session_data and len(session_data) > 0)
            
        except Exception:
            return False
    
    def _get_paths_from_config(self) -> tuple[str, str]:
        """
        Получает пути из конфигурационного файла paths.json
        
        Returns:
            Кортеж (excel_path, directory_path)
        """
        try:
            paths_file = self.data_dir / "paths.json"
            if paths_file.exists():
                with open(paths_file, "r", encoding="utf-8") as f:
                    paths_data = json.load(f)
                    
                excel_path = paths_data.get("excel_file_path", "")
                directory_path = paths_data.get("directory_path", "")
                
                # Проверяем что пути не пустые
                if not excel_path or not directory_path:
                    debug_logger.debug("📭 Пути в файле пустые")
                    return "", ""
                    
                return excel_path, directory_path
            return "", ""
            
        except Exception as e:
            debug_logger.error(f"❌ Ошибка при чтении paths.json: {e}")
            return "", ""
    
    def _create_analytics_summary(self, comparison_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Создает краткую сводку для аналитики
        
        Args:
            comparison_result: Результат сравнения файлов
            
        Returns:
            Словарь с аналитической сводкой
        """
        try:
            error_count = comparison_result.get('error_count', 0)
            results_data = comparison_result.get('results_data', [])
            
            # Подсчитываем статистику по типам файлов
            audio_errors = len([r for r in results_data if r.get('Тип файла') == 'Трек'])
            cover_errors = len([r for r in results_data if r.get('Тип файла') == 'Обложка'])
            
            summary = {
                "total_errors": error_count,
                "audio_errors": audio_errors,
                "cover_errors": cover_errors,
                "has_errors": error_count > 0,
                "results_file": comparison_result.get('results_file', ''),
                "success": comparison_result.get('success', False),
                "message": comparison_result.get('message', '')
            }
            
            debug_logger.debug(f"📊 Аналитическая сводка: ошибок={error_count}, аудио={audio_errors}, обложки={cover_errors}")
            
            return summary
            
        except Exception as e:
            debug_logger.error(f"❌ Ошибка при создании аналитической сводки: {e}")
            return {
                "total_errors": 0,
                "audio_errors": 0, 
                "cover_errors": 0,
                "has_errors": False,
                "results_file": "",
                "success": False,
                "message": "Ошибка при создании сводки"
            }


# Глобальный экземпляр для использования во всем приложении
session_manager = SessionDataManager() 