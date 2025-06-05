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
                background-color: #f5f0ff;
                border-radius: 10px;
            }
        """)
        files_list_layout = QVBoxLayout(self.files_list_container)
        files_list_layout.setContentsMargins(15, 15, 15, 15)
        
        # Заголовок для списка файлов
        self.files_list_title = QLabel("")
        self.files_list_title.setStyleSheet("font-weight: bold; font-size: 16px;")
        files_list_layout.addWidget(self.files_list_title)
        
        # Создаем прокручиваемую область для списка файлов
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)
        
        # Контейнер для списка файлов
        files_list_widget = QWidget()
        files_list_widget.setStyleSheet("background-color: transparent;")
        files_list_widget_layout = QVBoxLayout(files_list_widget)
        files_list_widget_layout.setContentsMargins(0, 0, 0, 0)
        files_list_widget_layout.setSpacing(8)
        
        # Список файлов
        self.files_list = QListWidget()
        self.files_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
            }
            QListWidget::item {
                padding: 5px 0;
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
            
            # Очищаем текущий список
            self.files_list.clear()
            
            # Получаем список Excel файлов в директории
            import os
            excel_files = []
            
            try:
                # Получаем все файлы в директории
                all_files = os.listdir(directory)
                
                # Фильтруем только Excel файлы
                excel_files = [file for file in all_files if file.endswith('.xlsx') or file.endswith('.xls')]
            except Exception as e:
                print(f"Ошибка при чтении директории: {e}")
                excel_files = []
            
            # Заполняем список файлов
            for file in excel_files:
                self.files_list.addItem(file)
                
            # Обновляем заголовок со счетчиком файлов
            self.files_list_title.setText(f"Выбрано файлов: {len(excel_files)}")
            
            # Показываем контейнер со списком файлов только если есть файлы
            if excel_files:
                self.files_list_container.setVisible(True)
            else:
                # Если файлов нет, скрываем контейнер и показываем сообщение
                self.files_list_container.setVisible(False)
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.warning(
                    self,
                    "Файлы не найдены",
                    f"В выбранной директории не найдены Excel файлы.\nПожалуйста, выберите другую директорию."
                ) 