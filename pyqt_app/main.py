#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QStackedWidget)
from PyQt6.QtCore import Qt

# Импортируем наши компоненты
from pyqt_app.components import TabBar
from pyqt_app.pages import UploadPage, AnalyticsPage, HelpPage, SettingsPage

# Импорт сессионного менеджера для очистки при закрытии
from pyqt_app.session_data_manager import session_manager

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
        
        # Устанавливаем активную вкладку ЗАГРУЗКА (индекс 0)
        self.tab_bar.set_active_tab(0)
    
    def setup_pages(self):
        """Создание и настройка страниц для каждой вкладки"""
        # Создаем экземпляры страниц
        self.upload_page = UploadPage()
        self.analytics_page = AnalyticsPage()
        self.help_page = HelpPage()
        self.settings_page = SettingsPage()
        
        # Связываем страницы для передачи данных
        self.connect_pages()
          # Добавляем страницы в стек
        self.content_stack.addWidget(self.upload_page)
        self.content_stack.addWidget(self.analytics_page)
        self.content_stack.addWidget(self.help_page)
        self.content_stack.addWidget(self.settings_page)
    
    def connect_pages(self):
        """Связывание страниц для передачи данных"""
        # Связываем сигнал завершения проверки файлов с обновлением аналитики
        self.upload_page.comparison_completed.connect(
            self.analytics_page.update_from_comparison_result
        )
    
    def change_tab(self, index):
        """Обработчик переключения вкладок"""
        # Переключаем содержимое вкладки
        self.content_stack.setCurrentIndex(index)
        
    def connect_scripts(self):
        """Метод для интеграции существующих скриптов проекта"""
        pass
    
    def closeEvent(self, event):
        """Обработчик закрытия приложения - очищаем сессионные данные"""
        try:
            # Очищаем все сессионные данные при закрытии приложения
            session_manager.clear_all_session_data()
            print("🗑️ Все сессионные данные очищены при закрытии приложения")
        except Exception as e:
            print(f"⚠️ Ошибка при очистке сессионных данных: {e}")
        
        # Принимаем событие закрытия
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Установка стиля приложения
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
