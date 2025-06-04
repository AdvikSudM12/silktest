#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

from .base_page import BasePage

class UploadPage(BasePage):
    """
    Страница загрузки файлов
    
    Содержит интерфейс для загрузки файлов и запуска скриптов обработки
    """
    def __init__(self, parent=None):
        super().__init__("Загрузка файлов", parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Настройка элементов интерфейса страницы загрузки"""
        # Временное сообщение-заглушка
        placeholder = QLabel("Здесь будет интерфейс загрузки файлов")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(placeholder)
        
        # Здесь будут добавлены элементы управления для загрузки файлов
        self.layout.addStretch() 