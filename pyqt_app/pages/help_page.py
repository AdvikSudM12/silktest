#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QFrame, 
    QScrollArea, QWidget, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QResizeEvent

from .base_page import BasePage

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
        # Основной контейнер с закругленными краями
        main_container = QFrame()
        main_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        # Используем QVBoxLayout с минимальными отступами
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(10)  # Уменьшаем расстояние между элементами
        
        # 1. Добавляем заголовок "ПОМОЩЬ"
        main_title = QLabel("ПОМОЩЬ")
        main_title.setStyleSheet("""
            color: #6352EC;
            font-size: 32px;
            font-weight: bold;
        """)
        main_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(main_title)
        
        # Создаем контейнер для основного содержимого, чтобы он мог масштабироваться
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(10)
        
        # 2. Добавляем секцию "КАК ПОЛЬЗОВАТЬСЯ ПРИЛОЖЕНИЕМ"
        self.add_usage_instructions(content_layout)
        
        # 3. Добавляем секцию "ТРЕБОВАНИЯ К ФАЙЛАМ"
        self.add_file_requirements(content_layout)
        
        # 4. Добавляем секцию "РЕШЕНИЕ ПРОБЛЕМ"
        self.add_troubleshooting(content_layout)
        
        # Добавляем контент в основной layout с возможностью растягивания
        main_layout.addWidget(content_widget, 1)  # 1 = stretch factor
        
        # Создаем прокручиваемую область для контента (на случай, если все же не поместится)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setWidget(main_container)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # По умолчанию скрываем вертикальную полосу прокрутки, но оставляем возможность прокрутки при необходимости
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Устанавливаем политику размера для автоматического масштабирования
        main_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        content_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Добавляем прокручиваемую область в основной layout
        self.layout.addWidget(scroll_area)
        
        # Настраиваем обработку изменения размера
        self.resizeEvent = self.on_resize
    
    def on_resize(self, event: QResizeEvent):
        """Обработчик изменения размера окна"""
        # Вызываем базовый метод обработки изменения размера
        super().resizeEvent(event)
        
        # Здесь можно добавить дополнительную логику масштабирования при необходимости
        # Например, изменение размера шрифта в зависимости от размера окна
    
    def add_section_title(self, parent_layout, title):
        """Добавляет заголовок раздела с разделительной линией"""
        # Заголовок раздела (с уменьшенным размером)
        section_title = QLabel(title)
        section_title.setStyleSheet("""
            color: #6352EC;
            font-size: 18px;
            font-weight: bold;
        """)
        parent_layout.addWidget(section_title)
        
        # Разделительная линия с минимальными отступами
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: #e0e0e0;")
        separator.setFixedHeight(1)
        parent_layout.addWidget(separator)
    
    def add_usage_instructions(self, parent_layout):
        """Добавляет раздел с инструкциями по использованию приложения"""
        # Добавляем заголовок раздела с разделительной линией
        self.add_section_title(parent_layout, "КАК ПОЛЬЗОВАТЬСЯ ПРИЛОЖЕНИЕМ")
        
        # Шаги использования приложения
        steps = [
            "Выберите Excel-файл с информацией о релизах.",
            "Выберите директорию с аудио-файлами и обложками.",
            "Нажмите кнопку \"Проверить файлы\" для валидации данных.",
            "В настройках введите \"Токен кабинета\" для авторизации.",
            "Нажмите кнопку \"Загрузить файлы\" для начала процесса загрузки."
        ]
        
        # Создаем горизонтальный контейнер для компактного размещения шагов в две колонки
        steps_container = QWidget()
        steps_container_layout = QHBoxLayout(steps_container)
        steps_container_layout.setContentsMargins(0, 5, 0, 0)
        steps_container_layout.setSpacing(10)
        
        # Левая колонка (шаги 1-3)
        left_column = QWidget()
        left_layout = QVBoxLayout(left_column)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)
        
        # Правая колонка (шаги 4-5)
        right_column = QWidget()
        right_layout = QVBoxLayout(right_column)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)
        
        # Распределяем шаги по колонкам
        for i, step_text in enumerate(steps, 1):
            step_widget = self.create_numbered_step(i, step_text)
            if i <= 3:
                left_layout.addWidget(step_widget)
            else:
                right_layout.addWidget(step_widget)
        
        # Добавляем растяжку в конце каждой колонки
        left_layout.addStretch()
        right_layout.addStretch()
        
        # Добавляем колонки в контейнер
        steps_container_layout.addWidget(left_column)
        steps_container_layout.addWidget(right_column)
        
        parent_layout.addWidget(steps_container)
    
    def add_file_requirements(self, parent_layout):
        """Добавляет раздел с требованиями к файлам"""
        # Добавляем заголовок раздела с разделительной линией
        self.add_section_title(parent_layout, "ТРЕБОВАНИЯ К ФАЙЛАМ")
        
        # Создаем горизонтальный контейнер для размещения блоков рядом
        requirements_container = QWidget()
        requirements_layout = QHBoxLayout(requirements_container)
        requirements_layout.setContentsMargins(0, 5, 0, 0)
        requirements_layout.setSpacing(10)
        
        # 1. Блок с требованиями к Excel файлу
        excel_frame = QFrame()
        excel_frame.setStyleSheet("""
            background-color: #f5f0ff;
            border-radius: 10px;
        """)
        excel_layout = QVBoxLayout(excel_frame)
        excel_layout.setContentsMargins(15, 10, 15, 10)
        excel_layout.setSpacing(5)
        
        # Заголовок блока
        excel_title = QLabel("Excel файл")
        excel_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        excel_layout.addWidget(excel_title)
        
        # Текст с требованиями
        excel_desc = QLabel("Должен содержать следующие колонки:")
        excel_desc.setStyleSheet("font-size: 12px;")
        excel_layout.addWidget(excel_desc)
        
        # Список колонок Excel
        columns = [
            "Название трека", "Исполнитель", "Альбом", "Жанр", "Дата релиза"
        ]
        
        # Добавляем колонки с фиолетовыми маркерами
        for column in columns:
            bullet_widget = self.create_bullet_item(column, compact=True)
            excel_layout.addWidget(bullet_widget)
        
        # 2. Блок с требованиями к аудиофайлам
        audio_frame = QFrame()
        audio_frame.setStyleSheet("""
            background-color: #f5f0ff;
            border-radius: 10px;
        """)
        audio_layout = QVBoxLayout(audio_frame)
        audio_layout.setContentsMargins(15, 10, 15, 10)
        audio_layout.setSpacing(5)
        
        # Заголовок блока
        audio_title = QLabel("Аудиофайлы")
        audio_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        audio_layout.addWidget(audio_title)
        
        # Текст с требованиями
        audio_desc = QLabel("Поддерживаются форматы MP3 и WAV.\nИмена файлов должны соответствовать\nданным в Excel.")
        audio_desc.setStyleSheet("font-size: 12px;")
        audio_desc.setWordWrap(True)
        audio_layout.addWidget(audio_desc)
        
        # Добавляем растяжку в конце
        audio_layout.addStretch()
        
        # Добавляем блоки в контейнер
        requirements_layout.addWidget(excel_frame)
        requirements_layout.addWidget(audio_frame)
        
        parent_layout.addWidget(requirements_container)
    
    def add_troubleshooting(self, parent_layout):
        """Добавляет раздел с решением проблем"""
        # Добавляем заголовок раздела с разделительной линией
        self.add_section_title(parent_layout, "РЕШЕНИЕ ПРОБЛЕМ")
        
        # Список ошибок и их решений
        errors = [
            ("Ошибка авторизации", "Проверьте правильность токена кабинета в настройках."),
            ("Файлы не загружаются", "Убедитесь, что имена аудиофайлов соответствуют названиям треков в Excel файле."),
            ("Ошибка валидации", "Проверьте, что Excel файл содержит все необходимые колонки и данные.")
        ]
        
        # Создаем горизонтальный контейнер для размещения ошибок
        errors_container = QWidget()
        errors_layout = QHBoxLayout(errors_container)
        errors_layout.setContentsMargins(0, 5, 0, 0)
        errors_layout.setSpacing(10)
        
        # Распределяем ошибки по колонкам для компактности
        for i, (title, description) in enumerate(errors):
            error_frame = self.create_error_box(title, description)
            errors_layout.addWidget(error_frame)
        
        parent_layout.addWidget(errors_container)
    
    def create_error_box(self, title, description):
        """Создает блок с ошибкой и решением"""
        # Создаем фрейм с закругленными углами
        error_frame = QFrame()
        error_frame.setStyleSheet("""
            background-color: #f5f0ff;
            border-radius: 10px;
        """)
        
        # Создаем layout для содержимого
        error_layout = QVBoxLayout(error_frame)
        error_layout.setContentsMargins(15, 10, 15, 10)
        error_layout.setSpacing(5)
        
        # Заголовок ошибки (красным цветом)
        error_title = QLabel(title)
        error_title.setStyleSheet("""
            color: #E85D75;
            font-weight: bold;
            font-size: 14px;
        """)
        error_layout.addWidget(error_title)
        
        # Описание решения
        error_desc = QLabel(description)
        error_desc.setStyleSheet("font-size: 12px;")
        error_desc.setWordWrap(True)
        error_layout.addWidget(error_desc)
        
        return error_frame
    
    def create_numbered_step(self, number, text):
        """Создает пронумерованный шаг с кружком и текстом"""
        # Контейнер для шага
        step_widget = QWidget()
        step_layout = QHBoxLayout(step_widget)
        step_layout.setContentsMargins(0, 0, 0, 0)
        
        # Создаем круг с номером (уменьшенный размер)
        number_label = QLabel(str(number))
        number_label.setFixedSize(24, 24)  # Уменьшенный размер круга
        number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Центрируем текст
        number_label.setStyleSheet("""
            background-color: #6352EC;  /* Фиолетовый цвет фона */
            color: white;               /* Белый цвет текста */
            border-radius: 12px;        /* Круглая форма */
            font-weight: bold;          /* Жирный текст */
            font-size: 12px;            /* Меньший размер шрифта */
        """)
        
        # Создаем текст шага (без переносов строк)
        text_label = QLabel(text)
        text_label.setWordWrap(False)  # Запрещаем перенос текста
        text_label.setStyleSheet("""
            font-size: 12px;
            margin-left: 5px;
        """)
        
        # Добавляем элементы в layout
        step_layout.addWidget(number_label)
        step_layout.addWidget(text_label, 1)  # 1 - stretch factor
        step_layout.addStretch(10)  # Добавляем растяжку справа
        
        return step_widget
    
    def create_bullet_item(self, text, compact=False):
        """Создает элемент списка с маркером-точкой"""
        # Контейнер для элемента
        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)
        
        # Уменьшаем отступы для компактного режима
        if compact:
            item_layout.setContentsMargins(0, 0, 0, 0)
        else:
            item_layout.setContentsMargins(0, 2, 0, 2)
        
        # Создаем маркер (фиолетовая точка)
        bullet = QLabel("•")
        bullet.setStyleSheet(f"""
            color: #6352EC;
            font-size: {18 if compact else 24}px;
            min-width: {15 if compact else 20}px;
        """)
        bullet.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Создаем текст элемента
        text_label = QLabel(text)
        text_label.setWordWrap(False)  # Запрещаем перенос строк
        text_label.setStyleSheet(f"font-size: {12 if compact else 14}px;")
        
        # Добавляем элементы в layout
        item_layout.addWidget(bullet)
        item_layout.addWidget(text_label, 1)
        item_layout.addStretch(10)
        
        return item_widget 