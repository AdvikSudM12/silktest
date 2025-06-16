#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Файл для запуска приложения Silk Loader
Запускает GUI приложение
"""

import sys
from pyqt_app.main import MainWindow
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Установка стиля приложения
    app.setStyle("Fusion")
    
    try:
        # Создаем главное окно (авторизация происходит в конструкторе)
    window = MainWindow()
        
        # Если окно создано успешно, показываем его
    window.show()
    sys.exit(app.exec()) 
        
    except SystemExit:
        # Если авторизация была отменена, просто завершаем приложение
        sys.exit(0)
    except Exception as e:
        print(f"Ошибка при запуске приложения: {e}")
        sys.exit(1) 