#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
    QWidget, QFrame, QFileDialog, QScrollArea, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap, QColor

from .base_page import BasePage
from pyqt_app.resources.icons import get_excel_icon, get_folder_icon

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
        # Создаем контейнер с рамкой и тенью, который будет содержать все элементы
        main_container = QFrame()
        main_container.setObjectName("mainContainer")
        main_container.setStyleSheet("""
            #mainContainer {
                background-color: white;
                border-radius: 20px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        # Установка тени для контейнера через графический эффект
        # (В PyQt6 нужно использовать QGraphicsDropShadowEffect, 
        # но здесь для простоты используем черную рамку)
        main_container.setStyleSheet("""
            QFrame#mainContainer {
                background-color: white;
                border-radius: 20px;
                border: 1px solid #e0e0e0;
            }
        """)
        
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
        
        # Список выбранных файлов (видимый только после выбора директории)
        self.files_list_container = QFrame()
        self.files_list_container.setStyleSheet("""
            QFrame {
                background-color: #f5f0ff;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        files_list_layout = QVBoxLayout(self.files_list_container)
        
        # Заголовок для списка файлов
        files_list_title = QLabel("Выбрано файлов: 0")
        files_list_title.setStyleSheet("font-weight: bold; font-size: 16px;")
        files_list_layout.addWidget(files_list_title)
        
        # Список файлов
        self.files_list = QListWidget()
        self.files_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
            }
        """)
        files_list_layout.addWidget(self.files_list)
        
        # По умолчанию скрываем контейнер со списком файлов
        self.files_list_container.setVisible(False)
        
        # Добавляем контейнер со списком файлов
        container_layout.addWidget(self.files_list_container)
        
        # Добавляем разделительную линию
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: #e0e0e0;")
        separator.setFixedHeight(1)
        container_layout.addWidget(separator)
        
        # Добавляем растяжку, чтобы содержимое было в верхней части
        container_layout.addStretch()
        
        # Добавляем основной контейнер в layout страницы
        self.layout.addWidget(main_container)
        
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
            # Сохраняем путь к директории
            self.directory_path = directory
            
            # Имитируем загрузку и отображение списка файлов из директории
            import os
            
            # Очищаем текущий список
            self.files_list.clear()
            
            # Получаем список Excel файлов в директории
            excel_files = []
            try:
                for file in os.listdir(directory):
                    if file.endswith('.xlsx') or file.endswith('.xls'):
                        excel_files.append(file)
            except:
                pass
            
            # Заполняем список файлов
            for file in excel_files:
                self.files_list.addItem(file)
                
            # Обновляем заголовок со счетчиком файлов
            files_count_title = self.files_list_container.layout().itemAt(0).widget()
            files_count_title.setText(f"Выбрано файлов: {len(excel_files)}")
            
            # Показываем контейнер со списком файлов
            self.files_list_container.setVisible(len(excel_files) > 0) 