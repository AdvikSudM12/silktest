#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import importlib.util
import json
from typing import Dict, Any, Callable, List, Optional
from pathlib import Path

# DEBUG: Добавляем логирование для отладки ScriptManager
from pyqt_app.logger_config import get_logger
debug_logger = get_logger("script_manager")

class ScriptManager:
    """
    Класс для управления и интеграции существующих скриптов проекта
    """
    def __init__(self, scripts_dir: str = None):
        """
        Инициализация менеджера скриптов
        
        Args:
            scripts_dir: Директория со скриптами (по умолчанию - папка scripts в корне проекта)
        """
        debug_logger.info("🏗️ Инициализация ScriptManager")
        
        # Определяем корневую директорию проекта (относительно текущего файла)
        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        debug_logger.debug(f"📁 Корневая директория: {self.root_dir}")
        
        # Директория со скриптами
        self.scripts_dir = scripts_dir or os.path.join(self.root_dir, 'scripts')
        debug_logger.debug(f"📂 Директория скриптов: {self.scripts_dir}")
        
        # Словарь загруженных модулей
        self.loaded_modules: Dict[str, Any] = {}
        
        # Словарь доступных функций из скриптов
        self.available_functions: Dict[str, Callable] = {}
          
        # Добавляем директорию проекта в sys.path для корректного импорта
        if self.root_dir not in sys.path:
            sys.path.append(self.root_dir)
            debug_logger.debug(f"➕ Добавлена директория в sys.path: {self.root_dir}")
        
        debug_logger.success("✅ ScriptManager инициализирован")
    
    def load_paths_from_json(self) -> Dict[str, str]:
        """
        Загружает сохраненные пути из paths.json
        
        Returns:
            Словарь с путями или пустой словарь в случае ошибки
        """
        paths_file = os.path.join(self.root_dir, 'pyqt_app', 'data', 'paths.json')
        if os.path.exists(paths_file):
            try:
                with open(paths_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Ошибка при загрузке paths.json: {str(e)}")
        return {}
    
    def run_file_comparison(self) -> Dict[str, Any]:
        """
        Запускает сравнение файлов с использованием сохраненных путей
        
        Returns:
            Результат сравнения файлов
        """
        debug_logger.info("📋 Начинаем сравнение файлов")
        
        # Загружаем модуль compare_files
        debug_logger.debug("📦 Загружаем модуль compare_files.py")
        module = self.load_script('compare_files.py')
        if not module:
            debug_logger.error("❌ Не удалось загрузить модуль compare_files.py")
            return {
                'success': False,
                'message': "Не удалось загрузить модуль compare_files.py"
            }
        
        debug_logger.success("✅ Модуль compare_files.py загружен")
        
        # Получаем функцию сравнения
        debug_logger.debug("🔍 Ищем функцию compare_files_with_excel")
        if not hasattr(module, 'compare_files_with_excel'):
            debug_logger.error("❌ Функция compare_files_with_excel не найдена")
            return {
                'success': False,
                'message': "Функция compare_files_with_excel не найдена в модуле"
            }
        
        debug_logger.success("✅ Функция compare_files_with_excel найдена")
        
        # Вызываем функцию сравнения
        try:
            debug_logger.info("🚀 Запускаем функцию сравнения файлов")
            compare_function = getattr(module, 'compare_files_with_excel')
            result = compare_function()
            debug_logger.success(f"📊 Сравнение завершено: {result.get('success', False)}")
            return result
        except Exception as e:
            debug_logger.critical(f"💥 Критическая ошибка при сравнении: {str(e)}")
            import traceback
            debug_logger.error(f"🔍 Traceback: {traceback.format_exc()}")
            return {
                'success': False,
                'message': f"Ошибка при выполнении сравнения файлов: {str(e)}"
            }
    
    def run_excel_processing(self, error_file_path: str = None) -> Dict[str, Any]:
        """
        Запускает обработку Excel файла с ошибками
        
        Args:
            error_file_path: Путь к файлу с результатами сравнения
        
        Returns:
            Результат обработки Excel файла
        """
        # Загружаем модуль excel_operations
        module = self.load_script('excel_operations.py')
        if not module:
            return {
                'success': False,
                'message': "Не удалось загрузить модуль excel_operations.py"
            }
        
        # Получаем функцию обработки
        if not hasattr(module, 'process_excel_errors'):
            return {
                'success': False,
                'message': "Функция process_excel_errors не найдена в модуле"
            }
        
        # Вызываем функцию обработки
        try:
            process_function = getattr(module, 'process_excel_errors')
            return process_function(error_file_path=error_file_path)
        except Exception as e:
            return {
                'success': False,
                'message': f"Ошибка при обработке Excel файла: {str(e)}"
            }
    
    def run_complete_workflow(self) -> Dict[str, Any]:
        """
        Выполняет полный workflow: сравнение файлов → обработка ошибок
        
        Returns:
            Результат выполнения полного workflow
        """
        debug_logger.info("🚀 Запуск полного workflow")
        
        # Этап 1: Сравнение файлов
        debug_logger.info("📋 Этап 1: Сравнение файлов")
        comparison_result = self.run_file_comparison()
        debug_logger.debug(f"📊 Результат сравнения: {comparison_result.get('success', False)}")
        
        if not comparison_result['success']:
            debug_logger.error(f"❌ Ошибка сравнения файлов: {comparison_result['message']}")
            return {
                'success': False,
                'message': f"Ошибка на этапе сравнения файлов: {comparison_result['message']}",
                'stage': 'comparison'
            }
        
        # Проверяем, есть ли ошибки для обработки
        error_count = comparison_result.get('error_count', 0)
        debug_logger.info(f"📈 Найдено ошибок для обработки: {error_count}")
        
        if error_count == 0:
            debug_logger.success("🎉 Нет ошибок - workflow завершен успешно")
            return {
                'success': True,
                'message': "Все файлы соответствуют записям в Excel. Обработка ошибок не требуется.",
                'stage': 'completed',
                'comparison_result': comparison_result
            }
        
        # Этап 2: Обработка ошибок в Excel
        debug_logger.info("📝 Этап 2: Обработка ошибок в Excel")
        results_file = comparison_result.get('results_file')
        debug_logger.debug(f"📄 Файл результатов: {results_file}")
        
        excel_result = self.run_excel_processing(results_file)
        debug_logger.debug(f"📊 Результат обработки Excel: {excel_result.get('success', False)}")
        
        if not excel_result['success']:
            debug_logger.error(f"❌ Ошибка обработки Excel: {excel_result['message']}")
            return {
                'success': False,
                'message': f"Ошибка на этапе обработки Excel: {excel_result['message']}",
                'stage': 'excel_processing',
                'comparison_result': comparison_result
            }
        
        debug_logger.success("🎊 Полный workflow завершен успешно!")
        return {
            'success': True,
            'message': f"Workflow выполнен успешно! {comparison_result['message']} {excel_result['message']}",
            'stage': 'completed',
            'comparison_result': comparison_result,
            'excel_result': excel_result
        }
    
    def load_script(self, script_name: str) -> Optional[Any]:
        """
        Загружает скрипт по имени файла
        
        Args:
            script_name: Имя файла скрипта (с расширением .py)
            
        Returns:
            Загруженный модуль или None в случае ошибки
        """
        if script_name in self.loaded_modules:
            return self.loaded_modules[script_name]
        
        script_path = os.path.join(self.scripts_dir, script_name)
        
        if not os.path.exists(script_path):
            print(f"Ошибка: Скрипт {script_name} не найден в {self.scripts_dir}")
            return None
        
        try:
            # Загружаем модуль
            spec = importlib.util.spec_from_file_location(script_name.replace('.py', ''), script_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.loaded_modules[script_name] = module
                return module
        except Exception as e:
            print(f"Ошибка при загрузке скрипта {script_name}: {str(e)}")
            return None
    
    def get_available_scripts(self) -> List[str]:
        """
        Получает список доступных скриптов в директории scripts
        
        Returns:
            Список имен файлов скриптов
        """
        if not os.path.exists(self.scripts_dir):
            return []
        
        return [f for f in os.listdir(self.scripts_dir) if f.endswith('.py')]
    
    def register_function(self, script_name: str, function_name: str) -> bool:
        """
        Регистрирует функцию из скрипта для использования в приложении
        
        Args:
            script_name: Имя файла скрипта
            function_name: Имя функции в скрипте
            
        Returns:
            True если функция успешно зарегистрирована, иначе False
        """
        module = self.load_script(script_name)
        if not module:
            return False
        
        if not hasattr(module, function_name):
            print(f"Ошибка: Функция {function_name} не найдена в скрипте {script_name}")
            return False
        
        function = getattr(module, function_name)
        if not callable(function):
            print(f"Ошибка: {function_name} не является функцией в скрипте {script_name}")
            return False
        
        # Регистрируем функцию с уникальным именем
        key = f"{script_name.replace('.py', '')}.{function_name}"
        self.available_functions[key] = function
        return True
    
    def call_function(self, function_key: str, *args, **kwargs) -> Any:
        """
        Вызывает зарегистрированную функцию
        
        Args:
            function_key: Ключ функции в формате "script_name.function_name"
            *args, **kwargs: Аргументы для передачи в функцию
            
        Returns:
            Результат выполнения функции
        """
        if function_key not in self.available_functions:
            print(f"Ошибка: Функция {function_key} не зарегистрирована")
            return None
        
        try:
            return self.available_functions[function_key](*args, **kwargs)
        except Exception as e:
            print(f"Ошибка при вызове функции {function_key}: {str(e)}")
            return None


# Пример использования
if __name__ == "__main__":
    manager = ScriptManager()
    print("Доступные скрипты:", manager.get_available_scripts())
    
    # Пример загрузки и вызова функции из скрипта
    # manager.register_function("compare_files.py", "compare_two_files")
    # result = manager.call_function("compare_files.compare_two_files", "file1.txt", "file2.txt")
