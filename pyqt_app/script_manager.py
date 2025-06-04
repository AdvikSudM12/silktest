#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import importlib.util
from typing import Dict, Any, Callable, List, Optional

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
        # Определяем корневую директорию проекта (относительно текущего файла)
        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        
        # Директория со скриптами
        self.scripts_dir = scripts_dir or os.path.join(self.root_dir, 'scripts')
        
        # Словарь загруженных модулей
        self.loaded_modules: Dict[str, Any] = {}
        
        # Словарь доступных функций из скриптов
        self.available_functions: Dict[str, Callable] = {}
        
        # Добавляем директорию проекта в sys.path для корректного импорта
        if self.root_dir not in sys.path:
            sys.path.append(self.root_dir)
    
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
