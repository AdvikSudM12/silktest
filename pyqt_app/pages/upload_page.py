#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
    QWidget, QFrame, QFileDialog, QScrollArea, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap, QColor, QPainter, QPen

from .base_page import BasePage
from pyqt_app.resources.icons import get_excel_icon, get_folder_icon

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
    def __init__(self, parent=None):
        # Используем пустой заголовок, так как будем добавлять его вручную
        super().__init__("", parent)
        self.excel_file_path = None
        self.directory_path = None
        self.setup_ui()
        
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
        upload_button = QPushButton("ЗАГРУЗИТЬ ФАЙЛЫ")
        upload_button.setStyleSheet("""
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
        """)
        upload_button.setCursor(Qt.CursorShape.PointingHandCursor)
        upload_button.clicked.connect(self.upload_files)
        
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
        
        # Добавляем кнопки в контейнер
        action_buttons_layout.addWidget(upload_button)
        action_buttons_layout.addWidget(continue_button)
        
        container_layout.addWidget(action_buttons_container)
        
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
            
            # Получаем список всех файлов в директории
            import os
            files = []
            
            try:
                # Получаем все файлы в директории
                files = [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
            except Exception as e:
                print(f"Ошибка при чтении директории: {e}")
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
    
    def check_files(self):
        """Проверка файлов в выбранной директории"""
        if not self.directory_path:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Директория не выбрана",
                "Пожалуйста, сначала выберите директорию с файлами."
            )
            return
        
        # Показываем статус загрузки
        self.show_status('loading', "Проверка файлов, пожалуйста подождите...")
            
        # Получаем список всех файлов в директории
        import os
        files = []
        
        try:
            # Получаем все файлы в директории
            files = [file for file in os.listdir(self.directory_path) if os.path.isfile(os.path.join(self.directory_path, file))]
        except Exception as e:
            print(f"Ошибка при чтении директории: {e}")
            files = []
        
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
        
        # Показываем соответствующий статус проверки
        if files:
            self.show_status('success', "Проверка файлов успешно завершена. Все файлы найдены!")
        else:
            self.show_status('error', "Файлы не найдены. Пожалуйста, проверьте выбранную директорию.")
    
    def open_settings(self):
        """Открытие настроек приложения"""
        # Переключение на страницу настроек
        # Получаем доступ к главному окну и переключаемся на вкладку настроек
        main_window = self.window()
        # Индекс 3 соответствует странице настроек в стеке
        main_window.content_stack.setCurrentIndex(3)
        main_window.tab_bar.buttons[3].setChecked(True)
    
    def upload_files(self):
        """Загрузка файлов для обработки"""
        if not self.excel_file_path or not self.directory_path:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Не все данные выбраны",
                "Пожалуйста, выберите Excel файл и директорию с файлами."
            )
            return
            
        # Показываем статус загрузки
        self.show_status('loading', "Загрузка файлов, пожалуйста подождите...")
            
        # Здесь будет логика загрузки файлов и интеграции с бэкендом
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "Загрузка файлов",
            "Начата загрузка файлов для обработки..."
        )
        
        # Для демонстрации - показываем успешный статус через 1 секунду
        # В реальном приложении этот статус будет обновляться по мере выполнения операции
        import time
        time.sleep(1)
        self.show_status('success', "Загрузка файлов успешно выполнена!")
    
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
        
        # Для демонстрации - показываем информационный статус через 1 секунду
        import time
        time.sleep(1)
        self.show_status('info', "Продолжение загрузки. Обработано 50% файлов...") 