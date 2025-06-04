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
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 