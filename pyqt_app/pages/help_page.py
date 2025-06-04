#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

from .base_page import BasePage

class HelpPage(BasePage):
    """
    Страница помощи
    
    Содержит справочную информацию о работе с приложением
    """
    def __init__(self, parent=None):
        super().__init__("Помощь", parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Настройка элементов интерфейса страницы помощи"""
        # Временное сообщение-заглушка
        placeholder = QLabel("Здесь будет отображаться справочная информация")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(placeholder)
        
        # Здесь будут добавлены элементы справочной информации
        self.layout.addStretch() 