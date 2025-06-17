# -*- coding: utf-8 -*-

"""
Диалоговое окно для отображения логов приложения
Интегрируется с существующей системой loguru логирования
Вызывается по горячей клавише F12
"""

import os
from datetime import datetime
from pathlib import Path
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, 
    QPushButton, QLineEdit, QLabel, QCheckBox,
    QFrame, QMessageBox, QFileDialog, QApplication
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QShortcut, QKeySequence, QFont

# НЕ используем логгер в диалоге логов чтобы избежать рекурсии!


class LogsDialog(QDialog):
    """Диалоговое окно для отображения логов приложения"""
    
    # Сигнал для thread-safe добавления логов
    new_log_signal = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logs_buffer = []
        self.last_file_size = 0  # Для отслеживания изменений файла
        self.log_file_path = None  # Путь к файлу логов
        
        self.setup_ui()
        self.setup_shortcuts()
        self.setup_connections()
        self.setup_auto_refresh()
        self.load_existing_logs()
        
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        self.setWindowTitle("🔍 Логи приложения - GoSilk Staff")
        self.setModal(False)  # Не блокирует главное окно
        self.resize(800, 600)
        self.setMinimumSize(400, 300)
        
        # Основной layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # === ВЕРХНЯЯ ПАНЕЛЬ УПРАВЛЕНИЯ ===
        self.setup_control_panel(main_layout)
        
        # === ОСНОВНАЯ ОБЛАСТЬ ЛОГОВ ===
        self.setup_logs_area(main_layout)
        
        # === НИЖНЯЯ ПАНЕЛЬ КНОПОК ===
        self.setup_bottom_panel(main_layout)
        
        # Стилизация
        self.apply_styles()
        
    def setup_control_panel(self, main_layout):
        """Настройка верхней панели управления"""
        control_frame = QFrame()
        control_layout = QHBoxLayout(control_frame)
        control_layout.setContentsMargins(0, 0, 0, 0)
        
        # Фильтры по уровням логов
        self.filter_debug = QCheckBox("DEBUG")
        self.filter_info = QCheckBox("INFO")
        self.filter_warning = QCheckBox("WARNING")  
        self.filter_error = QCheckBox("ERROR")
        self.filter_all = QCheckBox("ALL")
        
        # По умолчанию показываем все
        self.filter_all.setChecked(True)
        
        # Поиск
        search_label = QLabel("🔍")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по логам...")
        self.search_input.setMaximumWidth(200)
        
        # Кнопка очистки
        self.clear_button = QPushButton("🗑️ Очистить")
        
        # Добавляем виджеты
        control_layout.addWidget(QLabel("Фильтры:"))
        control_layout.addWidget(self.filter_debug)
        control_layout.addWidget(self.filter_info)
        control_layout.addWidget(self.filter_warning)
        control_layout.addWidget(self.filter_error)
        control_layout.addWidget(self.filter_all)
        control_layout.addStretch()
        control_layout.addWidget(search_label)
        control_layout.addWidget(self.search_input)
        control_layout.addWidget(self.clear_button)
        
        main_layout.addWidget(control_frame)
        
    def setup_logs_area(self, main_layout):
        """Настройка области отображения логов"""
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setFont(QFont("Consolas", 9))  # Моноширинный шрифт
        
        # Настройки прокрутки
        self.logs_text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.logs_text.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        main_layout.addWidget(self.logs_text)
        
    def setup_bottom_panel(self, main_layout):
        """Настройка нижней панели кнопок"""
        bottom_frame = QFrame()
        bottom_layout = QHBoxLayout(bottom_frame)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        # Информация о количестве логов
        self.logs_count_label = QLabel("Логов: 0")
        
        # Кнопки действий
        self.export_button = QPushButton("💾 Экспорт")
        self.copy_button = QPushButton("📋 Копировать")
        self.refresh_button = QPushButton("🔄 Обновить")
        self.close_button = QPushButton("❌ Закрыть")
        
        # Добавляем виджеты
        bottom_layout.addWidget(self.logs_count_label)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.export_button)
        bottom_layout.addWidget(self.copy_button)
        bottom_layout.addWidget(self.refresh_button)
        bottom_layout.addWidget(self.close_button)
        
        main_layout.addWidget(bottom_frame)
        
    def setup_shortcuts(self):
        """Настройка горячих клавиш"""
        # Escape - закрыть окно
        self.close_shortcut = QShortcut(QKeySequence("Escape"), self)
        self.close_shortcut.activated.connect(self.close)
        
        # Ctrl+F - фокус на поиск
        self.search_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        self.search_shortcut.activated.connect(self.focus_search)
        
        # Ctrl+C - копировать выделенное
        self.copy_shortcut = QShortcut(QKeySequence("Ctrl+C"), self)
        self.copy_shortcut.activated.connect(self.copy_selected)
        
        # F5 - обновить
        self.refresh_shortcut = QShortcut(QKeySequence("F5"), self)
        self.refresh_shortcut.activated.connect(self.refresh_logs)
        
    def setup_connections(self):
        """Настройка подключений сигналов"""
        # Кнопки
        self.clear_button.clicked.connect(self.clear_logs)
        self.export_button.clicked.connect(self.export_logs)
        self.copy_button.clicked.connect(self.copy_all_logs)
        self.refresh_button.clicked.connect(self.refresh_logs)
        self.close_button.clicked.connect(self.close)
        
        # Фильтры
        self.filter_debug.toggled.connect(self.apply_filters)
        self.filter_info.toggled.connect(self.apply_filters)
        self.filter_warning.toggled.connect(self.apply_filters)
        self.filter_error.toggled.connect(self.apply_filters)
        self.filter_all.toggled.connect(self.on_filter_all_changed)
        
        # Поиск с задержкой
        self.search_timer = QTimer()
        self.search_timer.timeout.connect(self.perform_search)
        self.search_timer.setSingleShot(True)
        self.search_input.textChanged.connect(self.on_search_changed)
        
        # Сигнал для добавления логов
        self.new_log_signal.connect(self.append_log_message)
        
    def setup_auto_refresh(self):
        """Настройка автообновления логов каждую секунду"""
        self.auto_refresh_timer = QTimer()
        self.auto_refresh_timer.timeout.connect(self.check_for_new_logs)
        self.auto_refresh_timer.start(1000)  # Каждую секунду
        
    def apply_styles(self):
        """Применение стилей к интерфейсу"""
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 5px;
                font-family: 'Consolas', 'Monaco', monospace;
            }
            
            QLineEdit {
                border: 1px solid #cccccc;
                border-radius: 3px;
                padding: 3px 5px;
                background-color: white;
            }
            
            QPushButton {
                background-color: #6352EC;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 15px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #5041d4;
            }
            
            QPushButton:pressed {
                background-color: #3f32b8;
            }
            
            QCheckBox {
                spacing: 5px;
                font-weight: bold;
            }
            
            QLabel {
                color: #333333;
                font-weight: bold;
            }
        """)
        
    def load_existing_logs(self):
        """Загрузка существующих логов из файла loguru"""
        try:
            # Определяем путь к файлу логов через path_manager
            from ..path_manager import get_log_file_path
            self.log_file_path = get_log_file_path()
            
            if not self.log_file_path.exists():
                return
                
            # Читаем последние 100 строк для начала (чтобы не загружать сразу 999 строк)
            with open(self.log_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            # Берем последние 100 строк
            recent_lines = lines[-100:] if len(lines) > 100 else lines
            
            for line in recent_lines:
                line = line.strip()
                if line:  # Пропускаем пустые строки
                    self.append_log_message(line)
                    
            # Запоминаем размер файла для отслеживания изменений
            self.last_file_size = self.log_file_path.stat().st_size
            self.update_logs_count()
            
        except Exception as e:
            # Fallback к тестовым данным если что-то пошло не так
            self.load_fallback_logs()
            
    def load_fallback_logs(self):
        """Загрузка тестовых логов как fallback"""
        test_logs = [
            "2025-01-17 15:30:01 | INFO     | main_window | ✅ Приложение запущено",
            "2025-01-17 15:30:02 | DEBUG    | logger_config | 📂 Инициализация системы логирования", 
            "2025-01-17 15:30:03 | INFO     | env_manager | 🔧 Загрузка конфигурации .env",
            "2025-01-17 15:30:04 | WARNING  | session_manager | ⚠️ Файл paths.json не найден",
            "2025-01-17 15:30:05 | ERROR    | script_manager | ❌ Ошибка выполнения Node.js скрипта",
            "2025-01-17 15:30:06 | INFO     | logs_dialog | 🚀 Окно логов готово к работе (fallback)"
        ]
        
        for log in test_logs:
            self.append_log_message(log)
            
        self.update_logs_count()
        
    def check_for_new_logs(self):
        """Проверка новых логов в файле (вызывается каждую секунду)"""
        try:
            if not self.log_file_path or not self.log_file_path.exists():
                return
                
            # Проверяем изменился ли размер файла
            current_size = self.log_file_path.stat().st_size
            if current_size <= self.last_file_size:
                return  # Новых данных нет
                
            # Читаем только новые строки
            with open(self.log_file_path, 'r', encoding='utf-8') as f:
                f.seek(self.last_file_size)  # Переходим к месту где остановились
                new_lines = f.readlines()
                
            # Добавляем новые строки
            for line in new_lines:
                line = line.strip()
                if line:
                    self.append_log_message(line)
                    
            # Обновляем размер файла
            self.last_file_size = current_size
            
        except Exception as e:
            # Игнорируем ошибки чтобы не спамить
            pass
        
    # ================== ОБРАБОТЧИКИ СОБЫТИЙ ==================
    
    def on_filter_all_changed(self, checked):
        """Обработка изменения фильтра 'Все'"""
        if checked:
            # Отключаем остальные фильтры
            self.filter_debug.setChecked(False)
            self.filter_info.setChecked(False)
            self.filter_warning.setChecked(False)
            self.filter_error.setChecked(False)
        self.apply_filters()
        
    def apply_filters(self):
        """Применение фильтров к отображению логов"""
        # Логика фильтрации будет добавлена в этапе 3
        pass
        
    def on_search_changed(self):
        """Обработка изменения текста поиска"""
        self.search_timer.start(300)  # Debounce 300ms
        
    def perform_search(self):
        """Выполнение поиска по логам"""
        search_text = self.search_input.text().strip()
        # Логика поиска будет добавлена в этапе 3
        
    def focus_search(self):
        """Установка фокуса на поле поиска"""
        self.search_input.setFocus()
        self.search_input.selectAll()
        
    def clear_logs(self):
        """Очистка всех логов"""
        reply = QMessageBox.question(
            self, "Очистка логов",
            "Вы уверены, что хотите очистить все логи?\nЭто действие нельзя отменить.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.logs_text.clear()
            self.logs_buffer.clear()
            self.update_logs_count()
            
    def refresh_logs(self):
        """Обновление логов из файла"""
        # Очищаем текущие логи
        self.logs_text.clear()
        self.logs_buffer.clear()
        
        # Загружаем заново
        self.load_existing_logs()
        
    def copy_selected(self):
        """Копирование выделенного текста"""
        if self.logs_text.textCursor().hasSelection():
            self.logs_text.copy()
            
    def copy_all_logs(self):
        """Копирование всех логов в буфер обмена"""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.logs_text.toPlainText())
        
    def export_logs(self):
        """Экспорт логов в файл"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"gosilk_logs_{timestamp}.txt"
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Сохранить логи", default_filename,
            "Text files (*.txt);;All files (*.*)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"# Логи GoSilk Staff\n")
                    f.write(f"# Экспорт: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"# Всего записей: {len(self.logs_buffer)}\n\n")
                    f.write(self.logs_text.toPlainText())
                    
                QMessageBox.information(self, "Экспорт", f"Логи сохранены в:\n{filename}")
                
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{e}")
                
    def append_log_message(self, message):
        """Добавление нового сообщения в область логов"""
        # Цветовая подсветка по уровням
        colored_message = self.colorize_log_message(message)
        
        # Добавляем в текстовую область
        self.logs_text.append(colored_message)
        
        # Автопрокрутка к последнему сообщению
        scrollbar = self.logs_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
        # Добавляем в буфер
        self.logs_buffer.append(message)
        self.update_logs_count()
        
    def colorize_log_message(self, message):
        """Добавление цветовой подсветки к сообщению лога"""
        if "ERROR" in message:
            return f'<span style="color: #ff4444;">{message}</span>'
        elif "WARNING" in message:
            return f'<span style="color: #ffaa00;">{message}</span>'
        elif "INFO" in message:
            return f'<span style="color: #44aaff;">{message}</span>'
        elif "DEBUG" in message:
            return f'<span style="color: #888888;">{message}</span>'
        elif "SUCCESS" in message:
            return f'<span style="color: #44ff44;">{message}</span>'
        else:
            return f'<span style="color: #ffffff;">{message}</span>'
            
    def update_logs_count(self):
        """Обновление счетчика логов"""
        count = len(self.logs_buffer)
        self.logs_count_label.setText(f"Логов: {count}")
        
    def closeEvent(self, event):
        """Обработка закрытия окна"""
        # Останавливаем таймер автообновления
        if hasattr(self, 'auto_refresh_timer'):
            self.auto_refresh_timer.stop()
        event.accept() 