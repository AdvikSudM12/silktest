#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QFrame, 
    QScrollArea, QWidget, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QResizeEvent

from .base_page import BasePage

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

class HelpPage(BasePage):
    """
    Страница помощи
    
    Содержит справочную информацию о работе с приложением
    """
    def __init__(self, parent=None):
        # Используем пустой заголовок, так как будем добавлять его вручную
        super().__init__("", parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Настройка элементов интерфейса страницы помощи"""
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
        
        # Основной контейнер с закругленными краями и тенью
        main_container = ContainerWithShadow()
        
        # Основной layout
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(10)  # Уменьшаем расстояние между элементами
        
        # 1. Добавляем заголовок "ПОМОЩЬ"
        main_title = QLabel("ПОМОЩЬ")
        main_title.setStyleSheet("""
            color: #6352EC;
            font-size: 40px;
            font-weight: bold;
            text-shadow: 2px 2px 3px rgba(0, 0, 0, 0.2);
        """)
        main_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(main_title)
        
        # 2. Добавляем секцию "КАК ПОЛЬЗОВАТЬСЯ ПРИЛОЖЕНИЕМ"
        self.add_section_title(main_layout, "КАК ПОЛЬЗОВАТЬСЯ ПРИЛОЖЕНИЕМ")
        
        # Добавляем полноразмерную линию под заголовком "КАК ПОЛЬЗОВАТЬСЯ ПРИЛОЖЕНИЕМ"
        section_line1 = QFrame()
        section_line1.setFrameShape(QFrame.Shape.HLine)
        section_line1.setFrameShadow(QFrame.Shadow.Sunken)
        section_line1.setStyleSheet("background-color: #e0e0e0;")
        section_line1.setFixedHeight(1)
        main_layout.addWidget(section_line1)
        
        # Добавляем контент для секции "КАК ПОЛЬЗОВАТЬСЯ ПРИЛОЖЕНИЕМ"
        self.add_usage_instructions_content(main_layout)
        
        # Добавляем секцию "ТРЕБОВАНИЯ К ФАЙЛАМ"
        self.add_section_title(main_layout, "ТРЕБОВАНИЯ К ФАЙЛАМ")
        
        # Добавляем полноразмерную линию под заголовком "ТРЕБОВАНИЯ К ФАЙЛАМ"
        section_line2 = QFrame()
        section_line2.setFrameShape(QFrame.Shape.HLine)
        section_line2.setFrameShadow(QFrame.Shadow.Sunken)
        section_line2.setStyleSheet("background-color: #e0e0e0;")
        section_line2.setFixedHeight(1)
        main_layout.addWidget(section_line2)
        
        # Добавляем контент для секции "ТРЕБОВАНИЯ К ФАЙЛАМ"
        self.add_file_requirements_content(main_layout)
        
        # Добавляем секцию "РЕШЕНИЕ ПРОБЛЕМ"
        self.add_section_title(main_layout, "РЕШЕНИЕ ПРОБЛЕМ")
        
        # Добавляем полноразмерную линию под заголовком "РЕШЕНИЕ ПРОБЛЕМ"
        section_line3 = QFrame()
        section_line3.setFrameShape(QFrame.Shape.HLine)
        section_line3.setFrameShadow(QFrame.Shadow.Sunken)
        section_line3.setStyleSheet("background-color: #e0e0e0;")
        section_line3.setFixedHeight(1)
        main_layout.addWidget(section_line3)
        
        # Добавляем контент для секции "РЕШЕНИЕ ПРОБЛЕМ"
        self.add_troubleshooting_content(main_layout)
        
        # Добавляем основной контейнер в layout прокручиваемого содержимого
        scroll_content_layout.addWidget(main_container)
        
        # Добавляем прокручиваемую область в основной layout страницы
        self.layout.addWidget(main_scroll_area)
        
        # Устанавливаем отступы для основного layout
        self.layout.setContentsMargins(20, 20, 20, 20)
    
    def add_section_title(self, parent_layout, title):
        """Добавляет заголовок раздела без разделительной линии"""
        # Заголовок раздела
        section_title = QLabel(title)
        section_title.setStyleSheet("""
            color: #6352EC;
            font-size: 22px;
            font-weight: bold;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
        """)
        parent_layout.addWidget(section_title)
    
    def add_usage_instructions(self, parent_layout):
        """Устаревший метод для обратной совместимости"""
        self.add_section_title(parent_layout, "КАК ПОЛЬЗОВАТЬСЯ ПРИЛОЖЕНИЕМ")
        self.add_usage_instructions_content(parent_layout)
    
    def add_usage_instructions_content(self, parent_layout):
        """Добавляет содержимое раздела с инструкциями по использованию приложения"""
        # Шаги использования приложения
        steps = [
            "Выберите Excel-файл с информацией о релизах.",
            "Выберите директорию с аудио-файлами и обложками.",
            "Нажмите кнопку \"Проверить файлы\" для валидации данных.",
            "В настройках введите \"Токен кабинета\" для авторизации.",
            "Нажмите кнопку \"Загрузить файлы\" для начала процесса загрузки."
        ]
        
        # Контейнер для всех шагов
        steps_container = QWidget()
        steps_layout = QVBoxLayout(steps_container)
        steps_layout.setContentsMargins(0, 10, 0, 0)  # Уменьшаем отступы
        steps_layout.setSpacing(10)  # Уменьшаем отступы между шагами
        
        # Добавляем шаги
        for i, step_text in enumerate(steps, 1):
            step_widget = self.create_numbered_step(i, step_text)
            steps_layout.addWidget(step_widget)
        
        parent_layout.addWidget(steps_container)
    
    def add_file_requirements(self, parent_layout):
        """Устаревший метод для обратной совместимости"""
        self.add_section_title(parent_layout, "ТРЕБОВАНИЯ К ФАЙЛАМ")
        self.add_file_requirements_content(parent_layout)
    
    def add_file_requirements_content(self, parent_layout):
        """Добавляет содержимое раздела с требованиями к файлам"""
        # Создаем контейнер для требований
        requirements_container = QWidget()
        requirements_layout = QVBoxLayout(requirements_container)
        requirements_layout.setContentsMargins(0, 10, 0, 0)  # Уменьшаем отступы
        requirements_layout.setSpacing(10)  # Уменьшаем отступы между блоками
        
        # 1. Блок с требованиями к Excel файлу
        excel_frame = QFrame()
        excel_frame.setStyleSheet("""
            background-color: #f0eaff;
            border-radius: 15px;
        """)
        excel_layout = QVBoxLayout(excel_frame)
        excel_layout.setContentsMargins(15, 10, 15, 10)  # Уменьшаем внутренние отступы
        excel_layout.setSpacing(5)  # Уменьшаем отступы между элементами
        
        # Заголовок блока
        excel_title = QLabel("Excel файл")
        excel_title.setStyleSheet("""
            font-weight: bold;
            font-size: 16px;
        """)
        excel_layout.addWidget(excel_title)
        
        # Текст требований
        excel_req = QLabel("Должен содержать следующие колонки:")
        excel_req.setStyleSheet("font-size: 14px;")
        excel_layout.addWidget(excel_req)
        
        # Создаем список требований
        columns = ["Название трека", "Исполнитель", "Альбом", "Жанр", "Дата релиза"]
        for column in columns:
            bullet_item = self.create_bullet_item(column, compact=True)
            excel_layout.addWidget(bullet_item)
        
        requirements_layout.addWidget(excel_frame)
        
        # 2. Блок с требованиями к аудиофайлам
        audio_frame = QFrame()
        audio_frame.setStyleSheet("""
            background-color: #f0eaff;
            border-radius: 15px;
        """)
        audio_layout = QVBoxLayout(audio_frame)
        audio_layout.setContentsMargins(15, 10, 15, 10)  # Уменьшаем внутренние отступы
        audio_layout.setSpacing(5)  # Уменьшаем отступы между элементами
        
        # Заголовок блока
        audio_title = QLabel("Аудиофайлы")
        audio_title.setStyleSheet("""
            font-weight: bold;
            font-size: 16px;
        """)
        audio_layout.addWidget(audio_title)
        
        # Текст требований
        audio_req = QLabel("Поддерживаются форматы MP3 и WAV. Имена файлов должны соответствовать данным в Excel.")
        audio_req.setStyleSheet("font-size: 14px;")
        audio_req.setWordWrap(True)
        audio_layout.addWidget(audio_req)
        
        requirements_layout.addWidget(audio_frame)
        
        parent_layout.addWidget(requirements_container)
    
    def add_troubleshooting(self, parent_layout):
        """Устаревший метод для обратной совместимости"""
        self.add_section_title(parent_layout, "РЕШЕНИЕ ПРОБЛЕМ")
        self.add_troubleshooting_content(parent_layout)
    
    def add_troubleshooting_content(self, parent_layout):
        """Добавляет содержимое раздела с решением проблем"""
        # Создаем контейнер для блоков с ошибками
        errors_container = QWidget()
        errors_layout = QVBoxLayout(errors_container)
        errors_layout.setContentsMargins(0, 10, 0, 0)  # Уменьшаем отступы
        errors_layout.setSpacing(10)  # Уменьшаем отступы между блоками
        
        # Список ошибок и их решений
        errors = [
            ("Ошибка авторизации", "Проверьте правильность токена кабинета в настройках."),
            ("Файлы не загружаются", "Убедитесь, что имена аудиофайлов соответствуют названиям треков в Excel файле."),
            ("Ошибка валидации", "Проверьте, что Excel файл содержит все необходимые колонки и данные.")
        ]
        
        # Добавляем блоки с ошибками
        for title, description in errors:
            error_frame = self.create_error_box(title, description)
            errors_layout.addWidget(error_frame)
        
        parent_layout.addWidget(errors_container)
    
    def create_error_box(self, title, description):
        """Создает блок с ошибкой и решением"""
        # Создаем фрейм с закругленными углами
        error_frame = QFrame()
        error_frame.setStyleSheet("""
            background-color: #f0eaff;
            border-radius: 15px;
        """)
        
        # Создаем layout для содержимого
        error_layout = QVBoxLayout(error_frame)
        error_layout.setContentsMargins(15, 10, 15, 10)  # Уменьшаем внутренние отступы
        error_layout.setSpacing(5)  # Уменьшаем отступы между элементами
        
        # Заголовок ошибки (красным цветом)
        error_title = QLabel(title)
        error_title.setStyleSheet("""
            color: #E85D75;
            font-weight: bold;
            font-size: 16px;
        """)
        error_layout.addWidget(error_title)
        
        # Описание решения
        error_desc = QLabel(description)
        error_desc.setStyleSheet("font-size: 14px;")
        error_desc.setWordWrap(True)
        error_layout.addWidget(error_desc)
        
        return error_frame
    
    def create_numbered_step(self, number, text):
        """Создает пронумерованный шаг с кружком и текстом"""
        # Контейнер для шага
        step_widget = QWidget()
        step_layout = QHBoxLayout(step_widget)
        step_layout.setContentsMargins(0, 0, 0, 0)
        step_layout.setSpacing(15)
        
        # Создаем круг с номером
        number_label = QLabel(str(number))
        number_label.setFixedSize(30, 30)
        number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        number_label.setStyleSheet("""
            background-color: #6352EC;
            color: white;
            border-radius: 15px;
            font-weight: bold;
            font-size: 14px;
        """)
        
        # Создаем текст шага
        text_label = QLabel(text)
        text_label.setWordWrap(True)
        text_label.setStyleSheet("""
            font-size: 14px;
        """)
        
        # Добавляем элементы в layout
        step_layout.addWidget(number_label)
        step_layout.addWidget(text_label, 1)
        
        return step_widget
    
    def create_bullet_item(self, text, compact=False):
        """Создает элемент списка с маркером-точкой"""
        # Контейнер для элемента
        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(0, 0, 0, 0)
        item_layout.setSpacing(10)
        
        # Создаем маркер (фиолетовая точка)
        bullet = QLabel("•")
        bullet.setStyleSheet("""
            color: #6352EC;
            font-size: 18px;
        """)
        
        # Создаем текст элемента
        text_label = QLabel(text)
        text_label.setStyleSheet("font-size: 14px;")
        
        # Добавляем элементы в layout
        item_layout.addWidget(bullet)
        item_layout.addWidget(text_label, 1)
        
        return item_widget 