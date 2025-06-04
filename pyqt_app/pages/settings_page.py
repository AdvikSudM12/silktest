#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

from .base_page import BasePage

class SettingsPage(BasePage):
    """
    Страница настроек
    
    Содержит настройки приложения и конфигурацию скриптов
    """
    def __init__(self, parent=None):
        super().__init__("Настройки приложения", parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Настройка элементов интерфейса страницы настроек"""
        # Временное сообщение-заглушка
        placeholder = QLabel("Здесь будут настройки приложения")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(placeholder)
        
        # Здесь будут добавлены элементы управления настройками
        self.layout.addStretch() 