#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt

class BasePage(QWidget):
    """
    Базовый класс для всех страниц приложения
    
    Устанавливает общие элементы стиля и структуры страниц
    """
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        
        # Основной layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)
        
        # Заголовок страницы (если указан)
        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                font-size: 18px;
                font-weight: bold;
                color: #333333;
                margin-bottom: 10px;
            """)
            self.layout.addWidget(title_label)
            
        # Линия-разделитель под заголовком
        if title:
            separator = QFrame()
            separator.setFrameShape(QFrame.Shape.HLine)
            separator.setFrameShadow(QFrame.Shadow.Sunken)
            separator.setStyleSheet("background-color: #e0e0e0;")
            separator.setMaximumHeight(1)
            self.layout.addWidget(separator)
            
        # Настройка внешнего вида
        self.setStyleSheet("""
            background-color: white;
        """)
        
    def setup_ui(self):
        """
        Метод для настройки UI страницы
        
        Должен быть переопределен в дочерних классах
        """
        pass 