#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QStackedWidget)
from PyQt6.QtCore import Qt

# Импортируем наши компоненты
from components import TabBar
from pages import UploadPage, AnalyticsPage, HelpPage, SettingsPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Silk Loader Application")
        self.resize(900, 700)
        
        # Устанавливаем светлый фон для всего приложения
        self.setStyleSheet("background-color: white;")
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Создаем список названий вкладок
        tabs = ["ЗАГРУЗКА", "АНАЛИТИКА", "ПОМОЩЬ", "НАСТРОЙКИ"]
        
        # Создаем панель вкладок и подключаем сигнал изменения
        self.tab_bar = TabBar(tabs)
        self.tab_bar.tabChanged.connect(self.change_tab)
        main_layout.addWidget(self.tab_bar)
        
        # Создаем стек виджетов для содержимого вкладок
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)
        
        # Создаем страницы для вкладок
        self.setup_pages()
        
        # Устанавливаем активную вкладку АНАЛИТИКА как на скриншоте
        self.tab_bar.set_active_tab(1)
    
    def setup_pages(self):
        """Создание и настройка страниц для каждой вкладки"""
        # Создаем экземпляры страниц
        self.upload_page = UploadPage()
        self.analytics_page = AnalyticsPage()
        self.help_page = HelpPage()
        self.settings_page = SettingsPage()
        
        # Добавляем страницы в стек
        self.content_stack.addWidget(self.upload_page)
        self.content_stack.addWidget(self.analytics_page)
        self.content_stack.addWidget(self.help_page)
        self.content_stack.addWidget(self.settings_page)
    
    def change_tab(self, index):
        """Обработчик переключения вкладок"""
        # Переключаем содержимое вкладки
        self.content_stack.setCurrentIndex(index)
        
    def connect_scripts(self):
        """Метод для интеграции существующих скриптов проекта"""
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Установка стиля приложения
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
