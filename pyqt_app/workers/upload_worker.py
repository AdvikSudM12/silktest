"""
Воркер для асинхронной загрузки релизов
"""

import os
import re
import subprocess
import shutil
from typing import Dict, Any
from PyQt6.QtCore import QThread, pyqtSignal
from loguru import logger as debug_logger


class UploadWorker(QThread):
    """Воркер для асинхронной загрузки релизов в отдельном потоке"""
    
    # Сигналы для связи с UI
    progress_updated = pyqtSignal(str)      # Обновление текстового лога
    progress_percent = pyqtSignal(int)      # Обновление процента (0-100)
    stage_changed = pyqtSignal(str)         # Изменение стадии (init, api_check, parsing, uploading, etc.)
    finished = pyqtSignal(bool, str)        # Завершение (success, message)
    error_occurred = pyqtSignal(str)        # Ошибка
    
    def __init__(self, script_manager, initial_iteration=0):
        super().__init__()
        self.script_manager = script_manager
        self.initial_iteration = initial_iteration
        self.is_cancelled = False
        
    def cancel(self):
        """Отмена операции"""
        self.is_cancelled = True
        debug_logger.warning("🛑 Запрос на отмену загрузки")
        
    def emit_progress(self, message: str, stage: str = None):
        """Отправляет сообщение прогресса в UI и консоль"""
        # Дублируем в консоль
        print(f"[UPLOAD] {message}")
        debug_logger.info(f"📤 {message}")
        
        # Отправляем в UI
        self.progress_updated.emit(message)
        
        if stage:
            self.stage_changed.emit(stage)
            
    def parse_progress_line(self, line: str) -> int:
        """Парсит строку прогресса и извлекает процент"""
        try:
            # Ищем паттерн: [██████░░░░] 33% (1/3)
            progress_match = re.search(r'(\d+)%\s*\((\d+)/(\d+)\)', line)
            if progress_match:
                percent = int(progress_match.group(1))
                current = int(progress_match.group(2))
                total = int(progress_match.group(3))
                
                # Дополнительно отправляем информацию о стадии
                self.emit_progress(f"Обработка релиза {current} из {total}", "uploading")
                return percent
                
            # Ищем паттерн загрузки файлов: [#####=====] 50%
            file_progress_match = re.search(r'\[([#=]+[░=]*)\]\s*(\d+)%', line)
            if file_progress_match:
                return int(file_progress_match.group(2))
                
        except Exception as e:
            debug_logger.warning(f"⚠️ Ошибка парсинга прогресса: {e}")
            
        return None
        
    def parse_stage_from_line(self, line: str) -> str:
        """Определяет стадию выполнения по строке лога"""
        if "🚀 ЗАПУСК ЗАГРУЗКИ РЕЛИЗОВ" in line:
            return "init"
        elif "Проверка конфигурации API" in line:
            return "api_check"
        elif "Тестирование API подключения" in line:
            return "api_test"
        elif "Парсинг данных релизов" in line:
            return "parsing"
        elif "Проверка наличия аудиофайлов" in line:
            return "file_check"
        elif "Начинаем загрузку релизов" in line:
            return "uploading"
        elif "ЗАГРУЗКА РЕЛИЗОВ ЗАВЕРШЕНА" in line:
            return "completed"
        elif "ОТЧЕТ О ЗАГРУЗКЕ" in line:
            return "report"
        else:
            return None
            
    def run(self):
        """Основной метод выполнения в отдельном потоке"""
        try:
            self.emit_progress("🚀 Инициализация загрузки релизов...", "init")
            
            if self.is_cancelled:
                return
                
            # Подготовка к запуску скрипта
            script_path = os.path.join(
                self.script_manager.root_dir, 
                'src', 'apps', 'release-parser-5'
            )
            
            # Проверяем существование скрипта
            index_file = os.path.join(script_path, 'index.ts')
            if not os.path.exists(index_file):
                self.error_occurred.emit(f"Скрипт не найден: {index_file}")
                return
                
            self.emit_progress("✅ Скрипт найден", "init")
            
            # Подготавливаем переменные окружения
            env = os.environ.copy()
            env_file = os.path.join(self.script_manager.root_dir, '.env')
            
            if os.path.exists(env_file):
                self.emit_progress("📄 Загрузка переменных окружения...", "init")
                try:
                    with open(env_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#') and '=' in line:
                                key, value = line.split('=', 1)
                                env[key.strip()] = value.strip()
                    self.emit_progress("✅ Переменные окружения загружены", "init")
                except Exception as e:
                    self.error_occurred.emit(f"Ошибка загрузки .env: {e}")
                    return
            else:
                self.error_occurred.emit("Файл .env не найден")
                return
                
            if self.is_cancelled:
                return
                
            # Подготавливаем команду
            npx_path = shutil.which('npx')
            if npx_path:
                cmd = [npx_path, 'ts-node', 'index.ts']
            else:
                cmd = ['cmd', '/c', 'npx', 'ts-node', 'index.ts']
            
            # Добавляем параметр initial_iteration если нужно продолжить загрузку
            if self.initial_iteration > 0:
                cmd.extend(['--initial-iteration', str(self.initial_iteration)])
                self.emit_progress(f"🔄 Продолжение загрузки с итерации: {self.initial_iteration}", "init")
                
            self.emit_progress(f"🔧 Запуск команды: {' '.join(cmd)}", "init")
            
            # Запускаем процесс
            process = subprocess.Popen(
                cmd,
                cwd=script_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # Объединяем stderr с stdout
                text=True,
                encoding='utf-8',
                env=env,
                bufsize=1,  # Построчная буферизация
                universal_newlines=True
            )
            
            self.emit_progress("⏳ Процесс запущен, ожидание вывода...", "running")
            
            # Читаем вывод в реальном времени
            current_progress = 0
            
            try:
                while True:
                    if self.is_cancelled:
                        process.terminate()
                        self.emit_progress("🛑 Операция отменена пользователем", "cancelled")
                        self.finished.emit(False, "Операция отменена")
                        return
                        
                    output = process.stdout.readline()
                    
                    if output == '' and process.poll() is not None:
                        break
                        
                    if output:
                        line = output.strip()
                        
                        # Отправляем строку в UI
                        self.emit_progress(line)
                        
                        # Парсим прогресс
                        progress = self.parse_progress_line(line)
                        if progress is not None and progress != current_progress:
                            current_progress = progress
                            self.progress_percent.emit(progress)
                            
                        # Определяем стадию
                        stage = self.parse_stage_from_line(line)
                        if stage:
                            self.stage_changed.emit(stage)
                            
            except Exception as e:
                self.error_occurred.emit(f"Ошибка чтения вывода: {e}")
                return
                
            # Ждем завершения процесса
            return_code = process.wait()
            
            if return_code == 0:
                self.emit_progress("🎉 Загрузка завершена успешно!", "completed")
                self.progress_percent.emit(100)
                self.finished.emit(True, "Релизы успешно загружены")
            else:
                self.emit_progress(f"❌ Ошибка загрузки, код: {return_code}", "error")
                self.finished.emit(False, f"Ошибка загрузки, код возврата: {return_code}")
                
        except Exception as e:
            debug_logger.error(f"💥 Критическая ошибка в воркере: {e}")
            self.error_occurred.emit(f"Критическая ошибка: {e}")
            self.finished.emit(False, f"Критическая ошибка: {e}") 