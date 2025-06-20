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

# Импорт для поддержки macOS app bundle
try:
    from macos_build.node_runner import NodeRunner
    MACOS_BUILD_AVAILABLE = True
except ImportError:
    # В режиме разработки macos_build модули могут быть недоступны
    MACOS_BUILD_AVAILABLE = False
    NodeRunner = None

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
        
        # Инициализация Node.js runner для macOS app bundle
        if MACOS_BUILD_AVAILABLE and NodeRunner:
            self.node_runner = NodeRunner()
            debug_logger.debug("🍎 Инициализирован NodeRunner для app bundle")
        else:
            self.node_runner = None
            debug_logger.debug("💻 Использование стандартного subprocess для Node.js")
          
        # Добавляем директорию проекта в sys.path для корректного импорта
        if self.root_dir not in sys.path:
            sys.path.append(self.root_dir)
            debug_logger.debug(f"➕ Добавлена директория в sys.path: {self.root_dir}")
        
        debug_logger.success("✅ ScriptManager инициализирован")
    
    def _run_typescript_script(self, script_relative_path: str, description: str) -> Dict[str, Any]:
        """
        Универсальная функция для запуска TypeScript скриптов
        
        Args:
            script_relative_path: Относительный путь к скрипту от root_dir
            description: Описание скрипта для логирования
            
        Returns:
            Результат выполнения скрипта
        """
        debug_logger.info(f"🔧 Запуск {description}")
        
        try:
            # Путь к скрипту
            script_path = os.path.join(self.root_dir, script_relative_path)
            debug_logger.debug(f"📂 Путь к скрипту: {script_path}")
            
            # Проверяем существование скрипта
            index_file = os.path.join(script_path, 'index.ts')
            if not os.path.exists(index_file):
                debug_logger.error(f"❌ Файл скрипта не найден: {index_file}")
                return {
                    'success': False,
                    'message': f"Скрипт {description} не найден: {index_file}"
                }
            
            debug_logger.success(f"✅ Скрипт {description} найден")
            
            # Проверяем наличие .env файла с токенами
            from .path_manager import get_env_file_path
            env_file = str(get_env_file_path())
            if not os.path.exists(env_file):
                debug_logger.error("❌ Файл .env не найден")
                return {
                    'success': False,
                    'message': "Файл .env с токенами не найден. Настройте токены в разделе НАСТРОЙКИ."
                }
            
            debug_logger.success("✅ Файл .env найден")
            
            # Используем node_runner если доступен, иначе стандартный subprocess
            if self.node_runner:
                debug_logger.info("🍎 Использование встроенного Node.js runner")
                result = self.node_runner.run_typescript_script(script_path, env_file)
                
                if result['success']:
                    debug_logger.success(f"🎉 {description} завершен успешно!")
                    return {
                        'success': True,
                        'message': f"{description} успешно завершен",
                        'output': result.get('output', ''),
                        'stage': 'completed'
                    }
                else:
                    debug_logger.error(f"❌ Ошибка {description}: {result.get('message', 'Unknown error')}")
                    return {
                        'success': False,
                        'message': f"Ошибка при выполнении {description}: {result.get('message', 'Unknown error')}",
                        'stage': 'failed'
                    }
            else:
                # Fallback к стандартному subprocess
                debug_logger.info("💻 Использование стандартного subprocess для Node.js")
                return self._run_typescript_subprocess(script_path, description, env_file)
                
        except Exception as e:
            debug_logger.critical(f"💥 Критическая ошибка при выполнении {description}: {str(e)}")
            import traceback
            debug_logger.error(f"🔍 Traceback: {traceback.format_exc()}")
            return {
                'success': False,
                'message': f"Критическая ошибка при выполнении {description}: {str(e)}",
                'stage': 'critical_error'
            }
    
    def _run_typescript_subprocess(self, script_path: str, description: str, env_file: str) -> Dict[str, Any]:
        """
        Запуск TypeScript скрипта через стандартный subprocess
        """
        import subprocess
        import shutil
        
        debug_logger.info("🔧 Запуск TypeScript скрипта через Node.js")
        
        # Команда для запуска скрипта с полным путем для Windows
        npx_path = shutil.which('npx')
        if npx_path:
            cmd = [npx_path, 'ts-node', 'index.ts']
            debug_logger.debug(f"🔍 Найден npx: {npx_path}")
        else:
            # Fallback: пробуем через cmd
            cmd = ['cmd', '/c', 'npx', 'ts-node', 'index.ts']
            debug_logger.warning("⚠️ npx не найден, используем cmd /c")
        
        debug_logger.debug(f"💻 Команда: {' '.join(cmd)}")
        debug_logger.debug(f"📁 Рабочая директория: {script_path}")
        
        # Подготавливаем переменные окружения
        env = os.environ.copy()  # Копируем текущие переменные окружения
        
        # Загружаем переменные из .env файла
        if os.path.exists(env_file):
            debug_logger.info("📄 Загружаем переменные из .env файла")
            try:
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            env[key.strip()] = value.strip()
                            debug_logger.debug(f"🔧 Переменная: {key.strip()}={'***' if 'TOKEN' in key else value.strip()}")
                debug_logger.success("✅ Переменные окружения загружены из .env")
                
                # Проверяем ключевые переменные
                key_vars = ['EMD_API', 'EMD_SPACE', 'EMD_TOKEN', 'EMD_USER_ID']
                debug_logger.info("🔍 Проверка ключевых переменных:")
                for var in key_vars:
                    if var in env:
                        display_value = '***скрыто***' if 'TOKEN' in var else env[var]
                        debug_logger.success(f"✅ {var}: {display_value}")
                    else:
                        debug_logger.error(f"❌ {var}: отсутствует")
                        
            except Exception as e:
                debug_logger.error(f"❌ Ошибка загрузки .env: {e}")
        else:
            debug_logger.warning("⚠️ Файл .env не найден")
        
        # Запускаем процесс с переменными окружения
        process = subprocess.Popen(
            cmd,
            cwd=script_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            env=env  # Передаем переменные окружения
        )
        
        debug_logger.info(f"⏳ Ожидание завершения {description}...")
        
        # Ждем завершения процесса
        stdout, stderr = process.communicate()
        
        debug_logger.debug(f"📤 STDOUT: {stdout}")
        if stderr:
            debug_logger.warning(f"⚠️ STDERR: {stderr}")
        
        # Проверяем код возврата
        if process.returncode == 0:
            debug_logger.success(f"🎉 {description} завершен успешно!")
            return {
                'success': True,
                'message': f"{description} успешно завершен",
                'output': stdout,
                'stage': 'completed'
            }
        else:
            debug_logger.error(f"❌ Ошибка {description}, код возврата: {process.returncode}")
            return {
                'success': False,
                'message': f"Ошибка при выполнении {description}: {stderr or stdout}",
                'error_code': process.returncode,
                'stage': 'failed'
            }

    def load_paths_from_json(self) -> Dict[str, str]:
        """
        Загружает сохраненные пути из paths.json
        
        Returns:
            Словарь с путями или пустой словарь в случае ошибки
        """
        from .path_manager import get_config_file_path
        paths_file = str(get_config_file_path('paths.json'))
        if os.path.exists(paths_file):
            try:
                with open(paths_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                debug_logger.error(f"❌ Ошибка при загрузке paths.json: {str(e)}")
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
        
        # Проверяем количество ошибок
        error_count = comparison_result.get('error_count', 0)
        debug_logger.info(f"📈 Найдено ошибок: {error_count}")
        
        # Workflow завершен успешно - compare_files.py уже создал полный отчет
        debug_logger.success("🎊 Полный workflow завершен успешно!")
        
        if error_count == 0:
            message = "Все файлы соответствуют записям в Excel."
        else:
            message = f"Проверка завершена. Найдено {error_count} файлов с ошибками."
        
        return {
            'success': True,
            'message': message,
            'stage': 'completed',
            'comparison_result': comparison_result,
            'excel_result': {'moved_count': 0}  # Заглушка для совместимости
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
            debug_logger.error(f"❌ Скрипт {script_name} не найден в {self.scripts_dir}")
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
            debug_logger.error(f"❌ Ошибка при загрузке скрипта {script_name}: {str(e)}")
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
            debug_logger.error(f"❌ Функция {function_name} не найдена в скрипте {script_name}")
            return False
        
        function = getattr(module, function_name)
        if not callable(function):
            debug_logger.error(f"❌ {function_name} не является функцией в скрипте {script_name}")
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
            debug_logger.error(f"❌ Функция {function_key} не зарегистрирована")
            return None
        
        try:
            return self.available_functions[function_key](*args, **kwargs)
        except Exception as e:
            debug_logger.error(f"❌ Ошибка при вызове функции {function_key}: {str(e)}")
            return None
    
    def check_nodejs_dependencies(self) -> Dict[str, Any]:
        """
        Проверяет наличие Node.js и ts-node для запуска TypeScript скриптов
        
        Returns:
            Результат проверки зависимостей
        """
        debug_logger.info("🔍 Проверка зависимостей Node.js")
        
        try:
            import subprocess
            
            # Проверяем Node.js
            try:
                result = subprocess.run(['node', '--version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    node_version = result.stdout.strip()
                    debug_logger.success(f"✅ Node.js найден: {node_version}")
                else:
                    debug_logger.error("❌ Node.js не найден")
                    return {
                        'success': False,
                        'message': "Node.js не установлен. Установите Node.js для загрузки релизов.",
                        'missing': ['nodejs']
                    }
            except (subprocess.TimeoutExpired, FileNotFoundError):
                debug_logger.error("❌ Node.js не найден или недоступен")
                return {
                    'success': False,
                    'message': "Node.js не найден. Установите Node.js для загрузки релизов.",
                    'missing': ['nodejs']
                }
            
            # Проверяем ts-node через npx (не требует глобальной установки)
            try:
                result = subprocess.run(['npx', 'ts-node', '--version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    ts_node_version = result.stdout.strip()
                    debug_logger.success(f"✅ ts-node доступен через npx: {ts_node_version}")
                else:
                    debug_logger.warning("⚠️ ts-node недоступен через npx")
                    return {
                        'success': False,
                        'message': "ts-node недоступен. Проверьте установку Node.js и npm.",
                        'missing': ['ts-node']
                    }
            except (subprocess.TimeoutExpired, FileNotFoundError):
                debug_logger.warning("⚠️ npx или ts-node недоступны")
                return {
                    'success': False,
                    'message': "npx или ts-node недоступны. Проверьте установку Node.js.",
                    'missing': ['ts-node']
                }
            
            debug_logger.success("🎉 Все зависимости Node.js найдены")
            return {
                'success': True,
                'message': "Все зависимости Node.js доступны",
                'node_version': node_version,
                'ts_node_version': ts_node_version
            }
            
        except Exception as e:
            debug_logger.error(f"❌ Ошибка проверки зависимостей: {str(e)}")
            return {
                'success': False,
                'message': f"Ошибка проверки зависимостей: {str(e)}",
                'error': str(e)
            }

    def run_release_upload(self) -> Dict[str, Any]:
        """
        Запускает загрузку релизов через TypeScript скрипт release-parser-5
        
        Returns:
            Результат загрузки релизов
        """
        debug_logger.info("🚀 Запуск загрузки релизов")
        
        # Загружаем пути из paths.json
        paths = self.load_paths_from_json()
        if not paths:
            debug_logger.error("❌ Пути не настроены")
            return {
                'success': False,
                'message': "Пути к папкам не настроены. Настройте пути в разделе UPLOAD."
            }
        
        debug_logger.success(f"✅ Пути загружены: {list(paths.keys())}")
        
        # Используем универсальную функцию для запуска TypeScript
        return self._run_typescript_script(
            os.path.join('src', 'apps', 'release-parser-5'),
            "загрузки релизов"
        )

    def run_update_releases_statuses(self) -> Dict[str, Any]:
        """
        Запускает обновление статусов релизов через TypeScript скрипт update-releases-shipment-statuses
        
        Returns:
            Результат обновления статусов релизов
        """
        debug_logger.info("🔄 Запуск обновления статусов релизов")
        
        # Используем универсальную функцию для запуска TypeScript
        return self._run_typescript_script(
            os.path.join('src', 'apps', 'update-releases-shipment-statuses'),
            "обновления статусов релизов"
        )


# Пример использования
if __name__ == "__main__":
    manager = ScriptManager()
    debug_logger.info(f"📋 Доступные скрипты: {manager.get_available_scripts()}")
    
    # Пример загрузки и вызова функции из скрипта
    # manager.register_function("compare_files.py", "compare_two_files")
    # result = manager.call_function("compare_files.compare_two_files", "file1.txt", "file2.txt")
