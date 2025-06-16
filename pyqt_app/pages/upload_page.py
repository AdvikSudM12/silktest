#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
    QWidget, QFrame, QFileDialog, QScrollArea, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPixmap, QColor, QPainter, QPen

from .base_page import BasePage
from pyqt_app.resources.icons import get_excel_icon, get_folder_icon

# DEBUG: Добавляем логирование для отладки процесса проверки файлов
from ..logger_config import get_logger
debug_logger = get_logger("upload_page")

# Импорт сессионного менеджера данных
from ..session_data_manager import session_manager

# Импорты для асинхронной загрузки
from ..workers import UploadWorker, UpdateStatusWorker
from ..dialogs import UploadProgressDialog, UpdateStatusProgressDialog

class ContainerWithShadow(QFrame):
    """Кастомный виджет-контейнер с эффектом тени"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("containerWithShadow")
        self.setStyleSheet("""
            #containerWithShadow {
                background-color: white;
                border-radius: 20px;
                border-top: 1px solid #e0e0e0;
                border-left: 1px solid #e0e0e0;
                border-right: 4px solid #555555;
                border-bottom: 4px solid #555555;
            }
        """)

class UploadPage(BasePage):
    """
    Страница загрузки файлов
    
    Содержит интерфейс для загрузки файлов и запуска скриптов обработки
    """
    
    # Сигнал для передачи данных проверки на страницу аналитики
    comparison_completed = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        # Используем пустой заголовок, так как будем добавлять его вручную
        super().__init__("", parent)
        self.excel_file_path = None
        self.directory_path = None
        self.setup_ui()
        self.load_saved_paths()
        
    def setup_ui(self):
        """Настройка элементов интерфейса страницы загрузки"""
        # Установка белого фона для страницы
        self.setStyleSheet("background-color: white;")
        
        # Создаем основной scrollable контейнер для всего содержимого
        main_scroll_area = QScrollArea()
        main_scroll_area.setWidgetResizable(True)
        main_scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #d0d0d0;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: transparent;
            }
        """)
        
        # Создаем виджет для размещения всего содержимого
        scroll_content = QWidget()
        scroll_content_layout = QVBoxLayout(scroll_content)
        scroll_content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Устанавливаем виджет в прокручиваемую область
        main_scroll_area.setWidget(scroll_content)
        
        # Создаем контейнер с рамкой и тенью, который будет содержать все элементы
        main_container = ContainerWithShadow()
        
        # Создаем layout для контейнера
        container_layout = QVBoxLayout(main_container)
        container_layout.setContentsMargins(50, 30, 50, 30)
        container_layout.setSpacing(15)
        
        # Заголовок "GOSILK UPLOADER"
        title_label = QLabel("GOSILK UPLOADER")
        title_label.setStyleSheet("""
            font-size: 40px;
            font-weight: bold;
            color: #6352EC;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(title_label)
        
        # Добавляем отступ после заголовка
        container_layout.addSpacing(20)
        
        # 1. Выбор Excel файла
        # Контейнер для иконки и текста
        excel_header = QWidget()
        excel_header_layout = QHBoxLayout(excel_header)
        excel_header_layout.setContentsMargins(0, 0, 0, 0)
        excel_header_layout.setSpacing(10)
        
        # Иконка Excel (эмодзи документа в качестве запасного варианта)
        excel_icon_label = QLabel("📄")
        excel_icon_label.setStyleSheet("font-size: 24px;")
        
        # Текст-метка
        excel_text_label = QLabel("Выберите Excel файл")
        excel_text_label.setStyleSheet("""
            color: #6352EC;
            font-size: 16px;
            font-weight: bold;
        """)
        
        # Добавляем иконку и текст в контейнер
        excel_header_layout.addWidget(excel_icon_label)
        excel_header_layout.addWidget(excel_text_label)
        excel_header_layout.addStretch()
        
        # Добавляем контейнер с заголовком
        container_layout.addWidget(excel_header)
        
        # Кнопка выбора Excel
        excel_button = QPushButton("ВЫБРАТЬ EXCEL")
        excel_button.setStyleSheet("""
            QPushButton {
                background-color: #6352EC;
                color: white;
                border-radius: 15px;
                padding: 10px 20px;
                font-weight: bold;
                max-width: 200px;
                border: 1px solid #5143c9;
                border-right: 3px solid #473aad;
                border-bottom: 3px solid #473aad;
            }
            QPushButton:hover {
                background-color: #5143c9;
            }
            QPushButton:pressed {
                background-color: #473aad;
            }
        """)
        excel_button.setCursor(Qt.CursorShape.PointingHandCursor)
        excel_button.clicked.connect(self.select_excel_file)
        
        # Контейнер для кнопки с выравниванием по левому краю
        excel_button_container = QWidget()
        excel_button_layout = QHBoxLayout(excel_button_container)
        excel_button_layout.setContentsMargins(0, 0, 0, 0)
        excel_button_layout.addWidget(excel_button)
        excel_button_layout.addStretch()
        
        container_layout.addWidget(excel_button_container)
        
        # Отображаем имя выбранного файла - пустое изначально
        self.excel_filename_label = QLabel("")
        self.excel_filename_label.setStyleSheet("color: #333333; font-size: 14px;")
        self.excel_filename_label.setContentsMargins(0, 5, 0, 0)
        container_layout.addWidget(self.excel_filename_label)
        
        # Добавляем отступ перед следующим разделом
        container_layout.addSpacing(20)
        
        # 2. Выбор директории с файлами
        # Контейнер для иконки и текста
        folder_header = QWidget()
        folder_header_layout = QHBoxLayout(folder_header)
        folder_header_layout.setContentsMargins(0, 0, 0, 0)
        folder_header_layout.setSpacing(10)
        
        # Иконка папки (эмодзи папки в качестве запасного варианта)
        folder_icon_label = QLabel("📁")
        folder_icon_label.setStyleSheet("font-size: 24px;")
        
        # Текст-метка
        folder_text_label = QLabel("Выберите директорию с файлами")
        folder_text_label.setStyleSheet("""
            color: #6352EC;
            font-size: 16px;
            font-weight: bold;
        """)
        
        # Добавляем иконку и текст в контейнер
        folder_header_layout.addWidget(folder_icon_label)
        folder_header_layout.addWidget(folder_text_label)
        folder_header_layout.addStretch()
        
        # Добавляем контейнер с заголовком
        container_layout.addWidget(folder_header)
        
        # Кнопка выбора директории
        folder_button = QPushButton("ВЫБРАТЬ ДИРЕКТОРИЮ")
        folder_button.setStyleSheet("""
            QPushButton {
                background-color: #6352EC;
                color: white;
                border-radius: 15px;
                padding: 10px 20px;
                font-weight: bold;
                max-width: 250px;
                border: 1px solid #5143c9;
                border-right: 3px solid #473aad;
                border-bottom: 3px solid #473aad;
            }
            QPushButton:hover {
                background-color: #5143c9;
            }
            QPushButton:pressed {
                background-color: #473aad;
            }
        """)
        folder_button.setCursor(Qt.CursorShape.PointingHandCursor)
        folder_button.clicked.connect(self.select_directory)
        
        # Контейнер для кнопки с выравниванием по левому краю
        folder_button_container = QWidget()
        folder_button_layout = QHBoxLayout(folder_button_container)
        folder_button_layout.setContentsMargins(0, 0, 0, 0)
        folder_button_layout.addWidget(folder_button)
        folder_button_layout.addStretch()
        
        container_layout.addWidget(folder_button_container)
        
        # Создаем контейнер для списка файлов
        self.files_list_container = QFrame()
        self.files_list_container.setStyleSheet("""
            QFrame {
                background-color: #f0eaff;
                border-radius: 15px;
                border: 1px solid #e6e0ff;
                border-right: 4px solid #d7cdff;
                border-bottom: 4px solid #d7cdff;
            }
        """)
        self.files_list_container.setMinimumHeight(250)  # Устанавливаем минимальную высоту
        self.files_list_container.setMaximumHeight(300)  # Ограничиваем максимальную высоту
        files_list_layout = QVBoxLayout(self.files_list_container)
        files_list_layout.setContentsMargins(20, 20, 20, 20)
        
        # Заголовок для списка файлов
        self.files_list_title = QLabel("")
        self.files_list_title.setStyleSheet("font-weight: bold; font-size: 18px;")
        files_list_layout.addWidget(self.files_list_title)
        
        # Создаем прокручиваемую область для списка файлов
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #f0eaff;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #6352EC;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background-color: transparent;
            }
        """)
        
        # Контейнер для списка файлов
        files_list_widget = QWidget()
        files_list_widget.setStyleSheet("background-color: transparent;")
        files_list_widget_layout = QVBoxLayout(files_list_widget)
        files_list_widget_layout.setContentsMargins(0, 0, 0, 0)
        files_list_widget_layout.setSpacing(12)  # Увеличиваем расстояние между элементами
        
        # Список файлов
        self.files_list = QListWidget()
        self.files_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px 0;
            }
            QListWidget::item:hover {
                color: #6352EC;
            }
        """)
        files_list_widget_layout.addWidget(self.files_list)
        
        # Устанавливаем виджет в прокручиваемую область
        scroll_area.setWidget(files_list_widget)
        
        # Добавляем прокручиваемую область в контейнер
        files_list_layout.addWidget(scroll_area)
        
        # По умолчанию скрываем контейнер со списком файлов
        self.files_list_container.setVisible(False)
        
        # Добавляем контейнер со списком файлов
        container_layout.addWidget(self.files_list_container)
        
        # Кнопка "Проверьте файлы"
        check_files_header = QWidget()
        check_files_layout = QHBoxLayout(check_files_header)
        check_files_layout.setContentsMargins(0, 10, 0, 0)
        check_files_layout.setSpacing(10)
        
        # Иконка графика
        chart_icon_label = QLabel("📊")
        chart_icon_label.setStyleSheet("font-size: 24px;")
        
        # Текст-метка
        check_files_label = QLabel("Проверьте файлы")
        check_files_label.setStyleSheet("""
            color: #6352EC;
            font-size: 16px;
            font-weight: bold;
        """)
        
        # Добавляем иконку и текст в контейнер
        check_files_layout.addWidget(chart_icon_label)
        check_files_layout.addWidget(check_files_label)
        check_files_layout.addStretch()
        
        # Добавляем контейнер с заголовком
        container_layout.addWidget(check_files_header)
        
        # Кнопка проверки файлов
        check_files_button = QPushButton("ПРОВЕРИТЬ ФАЙЛЫ")
        check_files_button.setStyleSheet("""
            QPushButton {
                background-color: #6352EC;
                color: white;
                border-radius: 15px;
                padding: 10px 20px;
                font-weight: bold;
                max-width: 250px;
                border: 1px solid #5143c9;
                border-right: 3px solid #473aad;
                border-bottom: 3px solid #473aad;
            }
            QPushButton:hover {
                background-color: #5143c9;
            }
            QPushButton:pressed {
                background-color: #473aad;
            }
        """)
        check_files_button.setCursor(Qt.CursorShape.PointingHandCursor)
        check_files_button.clicked.connect(self.check_files)
        
        # Контейнер для кнопки с выравниванием по левому краю
        check_files_button_container = QWidget()
        check_files_button_layout = QHBoxLayout(check_files_button_container)
        check_files_button_layout.setContentsMargins(0, 0, 0, 0)
        check_files_button_layout.addWidget(check_files_button)
        check_files_button_layout.addStretch()
        
        container_layout.addWidget(check_files_button_container)
        
        # Метка количества файлов
        self.files_count_label = QLabel("Всего файлов: 0")
        self.files_count_label.setStyleSheet("color: #333333; font-size: 14px;")
        container_layout.addWidget(self.files_count_label)
        
        # Блок настроек
        settings_header = QWidget()
        settings_layout = QHBoxLayout(settings_header)
        settings_layout.setContentsMargins(0, 20, 0, 0)
        settings_layout.setSpacing(10)
        
        # Иконка замка
        lock_icon_label = QLabel("🔒")
        lock_icon_label.setStyleSheet("font-size: 24px;")
        
        # Текст-метка
        settings_label = QLabel("Настройки")
        settings_label.setStyleSheet("""
            color: #6352EC;
            font-size: 16px;
            font-weight: bold;
        """)
        
        # Добавляем иконку и текст в контейнер
        settings_layout.addWidget(lock_icon_label)
        settings_layout.addWidget(settings_label)
        settings_layout.addStretch()
        
        # Добавляем контейнер с заголовком
        container_layout.addWidget(settings_header)
        
        # Кнопка настроек
        settings_button = QPushButton("ОТКРЫТЬ НАСТРОЙКИ")
        settings_button.setStyleSheet("""
            QPushButton {
                background-color: #6352EC;
                color: white;
                border-radius: 15px;
                padding: 10px 20px;
                font-weight: bold;
                max-width: 250px;
                border: 1px solid #5143c9;
                border-right: 3px solid #473aad;
                border-bottom: 3px solid #473aad;
            }
            QPushButton:hover {
                background-color: #5143c9;
            }
            QPushButton:pressed {
                background-color: #473aad;
            }
        """)
        settings_button.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_button.clicked.connect(self.open_settings)
        
        # Контейнер для кнопки с выравниванием по левому краю
        settings_button_container = QWidget()
        settings_button_layout = QHBoxLayout(settings_button_container)
        settings_button_layout.setContentsMargins(0, 0, 0, 0)
        settings_button_layout.addWidget(settings_button)
        settings_button_layout.addStretch()
        
        container_layout.addWidget(settings_button_container)
        
        # Горизонтальная разделительная линия после настроек
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: #e0e0e0;")
        separator.setFixedHeight(1)
        container_layout.addWidget(separator)
        container_layout.addSpacing(20)
        
        # Контейнер для кнопок действий
        action_buttons_container = QWidget()
        action_buttons_layout = QHBoxLayout(action_buttons_container)
        action_buttons_layout.setContentsMargins(0, 0, 0, 0)
        action_buttons_layout.setSpacing(20)
        
        # Кнопка загрузки файлов
        self.upload_button = QPushButton("ЗАГРУЗИТЬ ФАЙЛЫ")
        self.upload_button.clicked.connect(self.upload_files)
        
        # Кнопка продолжения загрузки
        continue_button = QPushButton("ПРОДОЛЖИТЬ ЗАГРУЗКУ")
        continue_button.setStyleSheet("""
            QPushButton {
                background-color: #f7a440;
                color: white;
                border-radius: 15px;
                padding: 15px 25px;
                font-weight: bold;
                border: 1px solid #e69938;
                border-right: 4px solid #d68b31;
                border-bottom: 4px solid #d68b31;
            }
            QPushButton:hover {
                background-color: #e69938;
            }
            QPushButton:pressed {
                background-color: #d68b31;
            }
        """)
        continue_button.setCursor(Qt.CursorShape.PointingHandCursor)
        continue_button.clicked.connect(self.continue_upload)
        
        # Кнопка обновления статусов релизов
        update_status_button = QPushButton("ОТПРАВИТЬ НА FTP")
        update_status_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border-radius: 15px;
                padding: 15px 25px;
                font-weight: bold;
                border: 1px solid #F57C00;
                border-right: 4px solid #E65100;
                border-bottom: 4px solid #E65100;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
            QPushButton:pressed {
                background-color: #E65100;
            }
        """)
        update_status_button.setCursor(Qt.CursorShape.PointingHandCursor)
        update_status_button.clicked.connect(self.update_releases_statuses)
        
        # Добавляем кнопки в контейнер
        action_buttons_layout.addWidget(self.upload_button)
        action_buttons_layout.addWidget(continue_button)
        action_buttons_layout.addWidget(update_status_button)
        
        # Инициализируем кнопку загрузки в неактивном состоянии
        self.disable_upload_button()
        
        container_layout.addWidget(action_buttons_container)
        
        # Индикатор прогресса загрузки - изначально скрыт
        self.progress_container = QFrame()
        self.progress_container.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 15px;
                border-right: 3px solid #ced4da;
                border-bottom: 3px solid #ced4da;
            }
        """)
        progress_layout = QVBoxLayout(self.progress_container)
        progress_layout.setContentsMargins(20, 15, 20, 15)
        progress_layout.setSpacing(10)
        
        # Заголовок прогресса
        self.progress_title = QLabel("🚀 Загрузка релизов...")
        self.progress_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #495057;")
        
        # Индикатор прогресса
        from PyQt6.QtWidgets import QProgressBar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #dee2e6;
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
                color: #495057;
                background-color: #e9ecef;
            }
            QProgressBar::chunk {
                background-color: #19c790;
                border-radius: 6px;
            }
        """)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(0)  # Неопределенный прогресс
        
        # Текст статуса прогресса
        self.progress_status = QLabel("Подготовка к загрузке...")
        self.progress_status.setStyleSheet("font-size: 14px; color: #6c757d;")
        
        progress_layout.addWidget(self.progress_title)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_status)
        
        # По умолчанию скрываем контейнер прогресса
        self.progress_container.setVisible(False)
        
        container_layout.addWidget(self.progress_container)
        
        # Статус проверки - изначально скрыт
        self.status_container = QFrame()
        self.status_container.setStyleSheet("""
            QFrame {
                background-color: #e6ffe6;
                border: 1px solid #ccffcc;
                border-radius: 15px;
                border-right: 3px solid #b3ffb3;
                border-bottom: 3px solid #b3ffb3;
            }
        """)
        status_layout = QHBoxLayout(self.status_container)
        status_layout.setContentsMargins(15, 10, 15, 10)
        
        # Иконка статуса (по умолчанию - успех)
        self.status_icon = QLabel("✅")
        self.status_icon.setStyleSheet("font-size: 24px;")
        
        # Текст статуса
        self.status_label = QLabel("Проверка файлов успешно завершена. Все файлы найдены!")
        self.status_label.setStyleSheet("font-size: 14px;")
        
        status_layout.addWidget(self.status_icon)
        status_layout.addWidget(self.status_label, 1)
        
        # По умолчанию скрываем контейнер статуса
        self.status_container.setVisible(False)
        
        container_layout.addWidget(self.status_container)
        
        # Добавляем растяжку, чтобы содержимое было в верхней части
        container_layout.addStretch()
        
        # Добавляем основной контейнер в layout страницы
        scroll_content_layout.addWidget(main_container)
          # Добавляем прокручиваемую область в основной layout страницы
        self.layout.addWidget(main_scroll_area)
        
        # Устанавливаем отступы для основного layout
        self.layout.setContentsMargins(20, 20, 20, 20)
    
    def select_excel_file(self):
        """Обработчик выбора Excel файла"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите Excel файл",
            "",
            "Excel Files (*.xlsx *.xls)"
        )
        
        if file_name:
            # Сохраняем путь к файлу
            self.excel_file_path = file_name
            
            # Получаем только имя файла без пути и отображаем его
            import os
            file_basename = os.path.basename(file_name)
            self.excel_filename_label.setText(file_basename)
            
            # Сохраняем путь в файл
            self.save_paths()
    
    def select_directory(self):
        """Обработчик выбора директории с файлами"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Выберите директорию с файлами"
        )
        
        if directory:
            # Показываем статус загрузки
            self.show_status('loading', "Сканирование директории, пожалуйста подождите...")
              # Сохраняем путь к директории
            self.directory_path = directory
            
            # Очищаем текущий список
            self.files_list.clear()
            
            # Сохраняем путь в файл
            self.save_paths()
            
            # Получаем список всех файлов в директории
            import os
            files = []
            
            try:
                # Получаем все файлы в директории
                files = [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
            except Exception as e:
                debug_logger.error(f"❌ Ошибка при чтении директории: {e}")
                files = []
            
            # Заполняем список файлов
            for file in files:
                self.files_list.addItem(file)
                
            # Обновляем заголовок со счетчиком файлов
            self.files_list_title.setText(f"Выбрано файлов: {len(files)}")
            
            # Обновляем счетчик файлов в другом месте интерфейса
            self.files_count_label.setText(f"Всего файлов: {len(files)}")
            
            # Показываем контейнер со списком файлов только если есть файлы
            if files:
                self.files_list_container.setVisible(True)
                # Показываем статус проверки
                self.show_status('success', "Проверка файлов успешно завершена. Все файлы найдены!")
            else:
                # Если файлов нет, скрываем контейнер и показываем сообщение
                self.files_list_container.setVisible(False)
                self.show_status('warning', "В выбранной директории не найдены файлы. Пожалуйста, выберите другую директорию.")
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.warning(
                    self,
                    "Файлы не найдены",
                    f"В выбранной директории не найдены файлы.\nПожалуйста, выберите другую директорию."
                )

    def show_status(self, status_type, message):
        """
        Отображает статус операции
        
        Args:
            status_type (str): Тип статуса ('success', 'error', 'warning', 'info', 'loading')
            message (str): Сообщение для отображения
        """
        # Настраиваем стиль и иконку в зависимости от типа статуса
        if status_type == 'success':
            # Зеленый фон с галочкой
            self.status_container.setStyleSheet("""
                QFrame {
                    background-color: #e6ffe6;
                    border: 1px solid #ccffcc;
                    border-radius: 15px;
                    border-right: 3px solid #b3ffb3;
                    border-bottom: 3px solid #b3ffb3;
                }
            """)
            self.status_icon.setText("✅")
            self.status_icon.setStyleSheet("font-size: 24px;")
        
        elif status_type == 'error':
            # Красный фон с крестиком
            self.status_container.setStyleSheet("""
                QFrame {
                    background-color: #ffe6e6;
                    border: 1px solid #ffcccc;
                    border-radius: 15px;
                    border-right: 3px solid #ffb3b3;
                    border-bottom: 3px solid #ffb3b3;
                }
            """)
            self.status_icon.setText("❌")
            self.status_icon.setStyleSheet("font-size: 24px;")
        
        elif status_type == 'warning':
            # Желтый фон с восклицательным знаком
            self.status_container.setStyleSheet("""
                QFrame {
                    background-color: #fff9e6;
                    border: 1px solid #ffefcc;
                    border-radius: 15px;
                    border-right: 3px solid #ffe6b3;
                    border-bottom: 3px solid #ffe6b3;
                }
            """)
            self.status_icon.setText("⚠️")
            self.status_icon.setStyleSheet("font-size: 24px;")
        
        elif status_type == 'info':
            # Синий фон с информационной иконкой
            self.status_container.setStyleSheet("""
                QFrame {
                    background-color: #e6f2ff;
                    border: 1px solid #cce5ff;
                    border-radius: 15px;
                    border-right: 3px solid #b3d9ff;
                    border-bottom: 3px solid #b3d9ff;
                }
            """)
            self.status_icon.setText("ℹ️")
            self.status_icon.setStyleSheet("font-size: 24px;")
        
        elif status_type == 'loading':
            # Фиолетовый фон с индикатором загрузки
            self.status_container.setStyleSheet("""
                QFrame {
                    background-color: #f0eaff;
                    border: 1px solid #e6e0ff;
                    border-radius: 15px;
                    border-right: 3px solid #d7cdff;
                    border-bottom: 3px solid #d7cdff;
                }
            """)
            self.status_icon.setText("⏳")
            self.status_icon.setStyleSheet("font-size: 24px;")
        
        # Устанавливаем текст сообщения
        self.status_label.setText(message)
          # Показываем контейнер статуса
        self.status_container.setVisible(True)
    
    def hide_status(self):
        """Скрывает статус операции"""
        self.status_container.setVisible(False)

    def show_progress(self, title="🚀 Загрузка релизов...", status="Подготовка к загрузке..."):
        """
        Показывает индикатор прогресса
        
        Args:
            title (str): Заголовок прогресса
            status (str): Текст статуса
        """
        self.progress_title.setText(title)
        self.progress_status.setText(status)
        self.progress_container.setVisible(True)
        debug_logger.debug(f"📊 Показан прогресс: {title} - {status}")

    def update_progress(self, status):
        """
        Обновляет текст статуса прогресса
        
        Args:
            status (str): Новый текст статуса
        """
        self.progress_status.setText(status)
        debug_logger.debug(f"🔄 Обновлен прогресс: {status}")

    def hide_progress(self):
        """Скрывает индикатор прогресса"""
        self.progress_container.setVisible(False)
        debug_logger.debug("📊 Прогресс скрыт")

    def get_disabled_upload_button_style(self):
        """Возвращает стиль для неактивной кнопки загрузки"""
        return """
            QPushButton {
                background-color: #cccccc;
                color: #666666;
                border-radius: 15px;
                padding: 15px 25px;
                font-weight: bold;
                border: 1px solid #aaaaaa;
                border-right: 4px solid #999999;
                border-bottom: 4px solid #999999;
            }
            QPushButton:hover {
                background-color: #cccccc;
            }
        """

    def get_enabled_upload_button_style(self):
        """Возвращает стиль для активной кнопки загрузки"""
        return """
            QPushButton {
                background-color: #19c790;
                color: white;
                border-radius: 15px;
                padding: 15px 25px;
                font-weight: bold;
                border: 1px solid #17b683;
                border-right: 4px solid #149e72;
                border-bottom: 4px solid #149e72;
            }
            QPushButton:hover {
                background-color: #17b683;
            }
            QPushButton:pressed {
                background-color: #149e72;
            }
        """

    def disable_upload_button(self):
        """Делает кнопку загрузки неактивной (серой)"""
        self.upload_button.setEnabled(False)
        self.upload_button.setStyleSheet(self.get_disabled_upload_button_style())
        self.upload_button.setCursor(Qt.CursorShape.ForbiddenCursor)
        debug_logger.debug("🔒 Кнопка загрузки деактивирована")

    def enable_upload_button(self):
        """Делает кнопку загрузки активной (зеленой)"""
        self.upload_button.setEnabled(True)
        self.upload_button.setStyleSheet(self.get_enabled_upload_button_style())
        self.upload_button.setCursor(Qt.CursorShape.PointingHandCursor)
        debug_logger.debug("🔓 Кнопка загрузки активирована")

    def check_files(self):
        """Проверка файлов в выбранной директории с использованием интегрированных скриптов"""
        debug_logger.info("🔍 Началась проверка файлов")
        debug_logger.debug(f"Excel файл: {self.excel_file_path}")
        debug_logger.debug(f"Директория: {self.directory_path}")
        
        if not self.excel_file_path:
            debug_logger.warning("❌ Excel файл не выбран")
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Excel файл не выбран",
                "Пожалуйста, сначала выберите Excel файл."
            )
            return
            
        if not self.directory_path:
            debug_logger.warning("❌ Директория не выбрана")
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Директория не выбрана",
                "Пожалуйста, сначала выберите директорию с файлами."
            )
            return

        debug_logger.info("✅ Пути проверены, показываем статус загрузки")
        # Показываем статус загрузки
        self.show_status('loading', "Проверка файлов, пожалуйста подождите...")
        
        debug_logger.info("📦 Импортируем ScriptManager")
        # Используем ScriptManager для выполнения полного workflow
        from pyqt_app.script_manager import ScriptManager
        
        try:
            debug_logger.info("🏗️ Создаем экземпляр ScriptManager")
            script_manager = ScriptManager()
            
            debug_logger.info("🚀 Запускаем полный workflow проверки файлов")
            result = script_manager.run_complete_workflow()
            debug_logger.success(f"📊 Workflow завершен: {result.get('success', False)}")
            
            if result['success']:
                debug_logger.info("✅ Workflow выполнен успешно")
                if result.get('stage') == 'completed':
                    debug_logger.info("🎯 Workflow полностью завершен")
                    comparison_result = result.get('comparison_result', {})
                    excel_result = result.get('excel_result', {})
                    
                    error_count = comparison_result.get('error_count', 0)
                    debug_logger.info(f"📈 Количество ошибок: {error_count}")
                    
                    if error_count == 0:
                        debug_logger.success("🎉 Нет ошибок - все файлы соответствуют")
                        # Нет ошибок - все файлы соответствуют, активируем кнопку загрузки
                        self.enable_upload_button()
                        self.show_status('success', result['message'])
                        
                        # ИСПРАВЛЕНИЕ: добавляем отсутствующие вызовы
                        results_file = comparison_result.get('results_file', '')
                        debug_logger.info(f"📄 Файл результатов: {results_file}")
                        
                        # Предлагаем сохранить файл результатов даже при отсутствии ошибок
                        if results_file:
                            debug_logger.info("💾 Предлагаем сохранить файл результатов (без ошибок)")
                            self.offer_save_results_file(results_file, 0, 0)
                        
                        debug_logger.debug("🔄 Обновляем отображение файлов")
                        # Обновляем отображение файлов
                        self.update_files_display()
                        
                        debug_logger.debug("📡 Передаем данные на страницу аналитики")
                        # Передаем данные на страницу аналитики
                        self.comparison_completed.emit(comparison_result)
                        
                        # НОВОЕ: сохраняем в сессионные данные
                        debug_logger.debug("💾 Сохраняем данные в сессионное хранилище")
                        session_manager.save_comparison_result(
                            comparison_result=comparison_result,
                            excel_file_path=self.excel_file_path,
                            directory_path=self.directory_path
                        )
                        
                    else:
                        debug_logger.warning(f"⚠️ Найдены ошибки: {error_count}")
                        # Есть ошибки - кнопка загрузки остается неактивной
                        self.disable_upload_button()
                        # Показываем детали
                        moved_count = excel_result.get('moved_count', 0)
                        results_file = comparison_result.get('results_file', '')
                        
                        debug_logger.info(f"📝 Перенесено строк: {moved_count}")
                        debug_logger.info(f"📄 Файл результатов: {results_file}")
                        
                        warning_message = f"Найдено {error_count} файлов с ошибками. "
                        if moved_count > 0:
                            warning_message += f"Перенесено {moved_count} строк в лист ошибок. "
                        
                        self.show_status('warning', warning_message)
                        
                        # Предлагаем сохранить файл результатов
                        if results_file:
                            debug_logger.info("💾 Предлагаем сохранить файл результатов")
                            self.offer_save_results_file(results_file, error_count, moved_count)
                          
                        debug_logger.debug("🔄 Обновляем отображение файлов")
                        # Обновляем отображение файлов
                        self.update_files_display()
                        
                        debug_logger.debug("📡 Передаем данные на страницу аналитики")
                        # Передаем данные на страницу аналитики
                        self.comparison_completed.emit(comparison_result)
                        
                        # НОВОЕ: сохраняем в сессионные данные
                        debug_logger.debug("💾 Сохраняем данные в сессионное хранилище")
                        session_manager.save_comparison_result(
                            comparison_result=comparison_result,
                            excel_file_path=self.excel_file_path,
                            directory_path=self.directory_path
                        )
                        
                else:
                    debug_logger.info("ℹ️ Workflow завершен без обработки ошибок")
                    # Workflow завершен без обработки ошибок
                    self.show_status('info', result['message'])
                    self.update_files_display()
                    
                    # Передаем данные на страницу аналитики
                    self.comparison_completed.emit(comparison_result)
                    
                    # НОВОЕ: сохраняем в сессионные данные
                    debug_logger.debug("💾 Сохраняем данные в сессионное хранилище")
                    session_manager.save_comparison_result(
                        comparison_result=comparison_result,
                        excel_file_path=self.excel_file_path,
                        directory_path=self.directory_path
                    )
                    
            else:
                debug_logger.error("❌ Ошибка в выполнении workflow")
                # Ошибка в выполнении workflow - кнопка загрузки остается неактивной
                self.disable_upload_button()
                error_stage = result.get('stage', 'unknown')
                error_message = f"Ошибка на этапе '{error_stage}': {result['message']}"
                
                debug_logger.error(f"🚨 Этап ошибки: {error_stage}")
                debug_logger.error(f"📝 Сообщение ошибки: {result['message']}")
                
                self.show_status('error', error_message)
                
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.critical(
                    self,
                    "Ошибка проверки файлов",
                    error_message
                )
                
        except Exception as e:
            debug_logger.critical(f"💥 КРИТИЧЕСКАЯ ОШИБКА: {str(e)}")
            # Критическая ошибка - кнопка загрузки остается неактивной
            self.disable_upload_button()
            error_message = f"Неожиданная ошибка при проверке файлов: {str(e)}"
            self.show_status('error', error_message)
            
            import traceback
            full_traceback = traceback.format_exc()
            debug_logger.error(f"🔍 Полный traceback:\n{full_traceback}")
            
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(
                self,
                "Критическая ошибка",
                error_message
            )
        
        debug_logger.info("🏁 Завершение метода check_files")
    
    def update_files_display(self):
        """Обновляет отображение файлов в интерфейсе"""
        if self.directory_path:
            import os
            try:
                # Получаем все файлы в директории
                files = [file for file in os.listdir(self.directory_path) if os.path.isfile(os.path.join(self.directory_path, file))]
                
                # Обновляем счетчик файлов
                self.files_count_label.setText(f"Всего файлов: {len(files)}")
                
                # Показываем контейнер со списком файлов если есть файлы
                if files:
                    self.files_list_container.setVisible(True)
                    # Обновляем заголовок со счетчиком файлов
                    self.files_list_title.setText(f"Выбрано файлов: {len(files)}")
                    
                    # Очищаем и заполняем список файлов
                    self.files_list.clear()
                    for file in files:
                        self.files_list.addItem(file)
                else:
                    self.files_list_container.setVisible(False)
                    
            except Exception as e:
                debug_logger.error(f"❌ Ошибка при обновлении отображения файлов: {e}")
    
    def open_settings(self):
        """Открытие настроек приложения в отдельном окне"""
        # Импортируем диалог настроек
        from pyqt_app.pages.settings_page import SettingsDialog
          # Создаем и открываем диалоговое окно настроек
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec()
    
    def save_paths(self):
        """Сохранение выбранных путей в файл"""
        import json
        import os
        from datetime import datetime
        
        # Создаем директорию для данных, если её нет
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        os.makedirs(data_dir, exist_ok=True)
        
        paths_file = os.path.join(data_dir, "paths.json")
        
        # Создаем структуру данных для сохранения
        paths_data = {
            "excel_file_path": self.excel_file_path or "",
            "directory_path": self.directory_path or "",
            "last_updated": datetime.now().isoformat()
        }
        
        try:
            # Добавляем подробную диагностику
            debug_logger.debug(f"💾 Сохранение в файл: {paths_file}")
            debug_logger.debug(f"📊 Данные для сохранения: {paths_data}")
            debug_logger.debug(f"📁 Директория существует: {os.path.exists(data_dir)}")
            
            with open(paths_file, "w", encoding="utf-8") as f:
                json.dump(paths_data, f, ensure_ascii=False, indent=4)
                f.flush()  # Принудительно записываем на диск
                
            # Проверяем, что файл действительно записался
            if os.path.exists(paths_file):
                with open(paths_file, "r", encoding="utf-8") as f:
                    saved_data = json.load(f)
                    debug_logger.debug(f"🔍 Проверка записи: {saved_data}")
                    
            debug_logger.success(f"✅ Пути успешно сохранены: Excel={self.excel_file_path}, Directory={self.directory_path}")
            
        except Exception as e:
            debug_logger.error(f"❌ Ошибка при сохранении путей: {e}")
            import traceback
            debug_logger.error(f"🔍 Traceback: {traceback.format_exc()}")
    
    def load_saved_paths(self):
        """Загрузка сохраненных путей из файла"""
        import json
        import os
        
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        paths_file = os.path.join(data_dir, "paths.json")
        
        try:
            if os.path.exists(paths_file):
                with open(paths_file, "r", encoding="utf-8") as f:
                    paths_data = json.load(f)
                    
                # Загружаем Excel файл, если он существует
                excel_path = paths_data.get("excel_file_path", "")
                if excel_path and os.path.exists(excel_path):
                    self.excel_file_path = excel_path
                    file_basename = os.path.basename(excel_path)
                    self.excel_filename_label.setText(file_basename)
                    debug_logger.info(f"📄 Загружен Excel файл: {excel_path}")
                  # Загружаем директорию, если она существует  
                directory_path = paths_data.get("directory_path", "")
                if directory_path and os.path.exists(directory_path):
                    self.directory_path = directory_path
                    
                    # Автоматически загружаем файлы из директории
                    self.load_directory_files(directory_path)
                    debug_logger.info(f"📁 Загружена директория: {directory_path}")
                    
        except Exception as e:
            debug_logger.error(f"❌ Ошибка при загрузке путей: {e}")
    
    def load_directory_files(self, directory):
        """Загрузка файлов из указанной директории"""
        import os
        
        try:
            # Очищаем текущий список
            self.files_list.clear()
            
            # Получаем список всех файлов в директории
            files = [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
            
            # Заполняем список файлов
            for file in files:
                self.files_list.addItem(file)
                
            # Обновляем заголовок со счетчиком файлов
            self.files_list_title.setText(f"Выбрано файлов: {len(files)}")
            
            # Обновляем счетчик файлов в другом месте интерфейса
            self.files_count_label.setText(f"Всего файлов: {len(files)}")
            
            # Показываем контейнер со списком файлов только если есть файлы
            if files:
                self.files_list_container.setVisible(True)
                self.show_status('success', "Файлы из сохраненной директории загружены успешно!")
            else:
                self.files_list_container.setVisible(False)
                self.show_status('warning', "В сохраненной директории не найдены файлы.")
                
        except Exception as e:
            debug_logger.error(f"❌ Ошибка при загрузке файлов из директории: {e}")
            self.show_status('error', f"Ошибка при загрузке файлов: {e}")
    
    def upload_files(self):
        """Асинхронная загрузка файлов через TypeScript скрипт"""
        debug_logger.info("🚀 Начинаем асинхронную загрузку файлов")
        
        # Проверяем наличие необходимых данных
        if not self.excel_file_path or not self.directory_path:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Не все данные выбраны",
                "Пожалуйста, выберите Excel файл и директорию с файлами."
            )
            debug_logger.warning("⚠️ Не выбраны необходимые пути для загрузки")
            return
            
        debug_logger.info(f"📄 Excel файл: {self.excel_file_path}")
        debug_logger.info(f"📁 Директория: {self.directory_path}")
        
        try:
            # Импортируем ScriptManager
            from pyqt_app.script_manager import ScriptManager
            
            # Создаем экземпляр менеджера скриптов
            script_manager = ScriptManager()
            debug_logger.info("📦 ScriptManager инициализирован")
            
            # Создаем и настраиваем воркер
            self.upload_worker = UploadWorker(script_manager)
            
            # Создаем и показываем диалог прогресса
            self.progress_dialog = UploadProgressDialog(self)
            
            # Подключаем сигналы воркера к диалогу
            self.upload_worker.progress_updated.connect(self.progress_dialog.update_progress)
            self.upload_worker.progress_percent.connect(self.progress_dialog.update_progress_percent)
            self.upload_worker.stage_changed.connect(self.progress_dialog.update_stage)
            self.upload_worker.finished.connect(self.on_upload_finished)
            self.upload_worker.error_occurred.connect(self.progress_dialog.on_error)
            
            # Подключаем сигнал отмены от диалога к воркеру
            self.progress_dialog.cancel_requested.connect(self.upload_worker.cancel)
            
            # Запускаем воркер
            self.upload_worker.start()
            
            # Показываем диалог прогресса
            self.progress_dialog.show()
            
            debug_logger.info("🔄 Асинхронная загрузка запущена")
            
        except Exception as e:
            debug_logger.critical(f"💥 Критическая ошибка при запуске загрузки: {str(e)}")
            
            # Показываем диалог с критической ошибкой
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(
                self,
                "Критическая ошибка",
                f"💥 Произошла критическая ошибка:\n{str(e)}\n\nОбратитесь к разработчику."
            )
    
    def on_upload_finished(self, success: bool, message: str):
        """Обработка завершения загрузки"""
        debug_logger.info(f"🏁 Загрузка завершена: success={success}, message={message}")
        
        # Обновляем диалог прогресса
        self.progress_dialog.on_finished(success, message)
        
        # Обрабатываем результат в основном UI
        if success:
            debug_logger.success("🎉 Загрузка релизов завершена успешно!")
            self.show_status('success', message)
        else:
            debug_logger.error(f"❌ Ошибка загрузки: {message}")
            self.show_status('error', f"Ошибка: {message}")
            
        # Очищаем ссылки на воркер
        if hasattr(self, 'upload_worker'):
            self.upload_worker.deleteLater()
            delattr(self, 'upload_worker')
    
    def continue_upload(self):
        """Продолжение загрузки файлов"""
        # Показываем статус загрузки
        self.show_status('loading', "Продолжение загрузки, пожалуйста подождите...")
        
        # Здесь будет логика продолжения загрузки
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "Продолжение загрузки",
            "Продолжение загрузки файлов..."
        )
        
        # Для демонстрации - показываем информационный статус
        self.show_status('info', "Продолжение загрузки. Обработано 50% файлов...")
    
    def offer_save_results_file(self, source_file: str, error_count: int, moved_count: int):
        """
        Предлагает пользователю сохранить файл результатов в удобном месте
        
        Args:
            source_file: Путь к исходному файлу результатов
            error_count: Количество найденных ошибок
            moved_count: Количество перенесенных строк
        """
        from PyQt6.QtWidgets import QMessageBox, QFileDialog
        import os
        import shutil
        from datetime import datetime
        
        # Создаем информационное сообщение
        message = f"Проверка завершена!\n\n"
        message += f"🔍 Найдено ошибок: {error_count}\n"
        if moved_count > 0:
            message += f"📝 Перенесено строк в лист ошибок: {moved_count}\n"
        message += f"\nФайл с детальным отчетом готов к сохранению.\n"
        message += f"Хотите сохранить его в удобном для вас месте?"
        
        # Показываем диалог с вопросом
        reply = QMessageBox.question(
            self,
            "Сохранить отчет об ошибках",
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Получаем имя исходного файла
            source_filename = os.path.basename(source_file)
            name_without_ext = os.path.splitext(source_filename)[0]
            
            # Предлагаем сохранить с понятным именем
            suggested_filename = f"Отчет_об_ошибках_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
            
            # Открываем диалог сохранения файла
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "Сохранить отчет об ошибках",
                suggested_filename,
                "Excel Files (*.xlsx);;All Files (*)"
            )
            
            if save_path:
                try:
                    # Копируем файл в выбранное место
                    shutil.copy2(source_file, save_path)
                    
                    # Показываем сообщение об успехе
                    success_message = f"Отчет успешно сохранен:\n{save_path}\n\n"
                    success_message += f"📊 Файл содержит {error_count} записей с ошибками.\n"
                    success_message += f"Открыть файл сейчас?"
                    
                    reply = QMessageBox.question(
                        self,
                        "Файл сохранен",
                        success_message,
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                        QMessageBox.StandardButton.Yes
                    )
                    
                    # Если пользователь хочет открыть файл
                    if reply == QMessageBox.StandardButton.Yes:
                        self.open_file_in_system(save_path)
                    
                    # Обновляем статус
                    self.show_status('success', f"Отчет сохранен: {os.path.basename(save_path)}")
                    
                except Exception as e:
                    QMessageBox.critical(
                        self,
                        "Ошибка сохранения",
                        f"Не удалось сохранить файл:\n{str(e)}"
                    )
                    self.show_status('error', f"Ошибка сохранения файла: {str(e)}")
            else:
                # Пользователь отменил сохранение
                self.show_status('info', "Сохранение отчета отменено")
        else:
            # Пользователь не хочет сохранять
            self.show_status('info', f"Отчет доступен в: {os.path.basename(source_file)}")
    
    def open_file_in_system(self, file_path: str):
        """
        Открывает файл в системном приложении по умолчанию
        
        Args:
            file_path: Путь к файлу для открытия
        """
        import os
        import subprocess
        import platform
        
        try:
            if platform.system() == 'Windows':
                os.startfile(file_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.call(['open', file_path])
            else:  # Linux
                subprocess.call(['xdg-open', file_path])
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Не удалось открыть файл",
                f"Файл сохранен, но не удалось его открыть:\n{str(e)}\n\nПуть к файлу: {file_path}"
            )
    
    def update_releases_statuses(self):
        """Асинхронное обновление статусов релизов через TypeScript скрипт"""
        debug_logger.info("🔄 Начинаем асинхронное обновление статусов релизов")
        
        try:
            # Импортируем ScriptManager
            from pyqt_app.script_manager import ScriptManager
            
            # Создаем экземпляр менеджера скриптов
            script_manager = ScriptManager()
            debug_logger.info("📦 ScriptManager инициализирован для обновления статусов")
            
            # Создаем и настраиваем воркер
            self.update_status_worker = UpdateStatusWorker(script_manager)
            
            # Создаем и показываем диалог прогресса
            self.update_status_progress_dialog = UpdateStatusProgressDialog(self)
            
            # Подключаем сигналы воркера к диалогу
            self.update_status_worker.progress_updated.connect(self.update_status_progress_dialog.update_progress)
            self.update_status_worker.progress_percent.connect(self.update_status_progress_dialog.update_progress_percent)
            self.update_status_worker.stage_changed.connect(self.update_status_progress_dialog.update_stage)
            self.update_status_worker.finished.connect(self.on_update_status_finished)
            self.update_status_worker.error_occurred.connect(self.update_status_progress_dialog.on_error)
            
            # Подключаем сигнал отмены от диалога к воркеру
            self.update_status_progress_dialog.cancel_requested.connect(self.update_status_worker.cancel)
            
            # Запускаем воркер
            self.update_status_worker.start()
            
            # Показываем диалог прогресса
            self.update_status_progress_dialog.show()
            
            debug_logger.info("🔄 Асинхронное обновление статусов запущено")
            
        except Exception as e:
            debug_logger.critical(f"💥 Критическая ошибка при запуске обновления статусов: {str(e)}")
            
            # Показываем диалог с критической ошибкой
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(
                self,
                "Критическая ошибка",
                f"💥 Произошла критическая ошибка:\n{str(e)}\n\nОбратитесь к разработчику."
            )
    
    def on_update_status_finished(self, success: bool, message: str):
        """Обработка завершения обновления статусов"""
        debug_logger.info(f"🏁 Обновление статусов завершено: success={success}, message={message}")
        
        # Обновляем диалог прогресса
        self.update_status_progress_dialog.on_finished(success, message)
        
        # Обрабатываем результат в основном UI
        if success:
            debug_logger.success("🎉 Обновление статусов релизов завершено успешно!")
            self.show_status('success', message)
        else:
            debug_logger.error(f"❌ Ошибка обновления статусов: {message}")
            self.show_status('error', f"Ошибка: {message}")
            
        # Очищаем ссылки на воркер
        if hasattr(self, 'update_status_worker'):
            self.update_status_worker.deleteLater()
            delattr(self, 'update_status_worker')