#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QPushButton, QWidget, QHBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal

class TabButton(QPushButton):
    """
    Кастомная кнопка для табов навигации
    
    Представляет собой кнопку с возможностью переключения состояния (активная/неактивная)
    и специальным стилем оформления для создания табов в верхней части приложения.
    """
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setMinimumHeight(40)
        self.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        
        # Стиль для кнопки
        self.setStyleSheet("""
            QPushButton {
                border: none;
                border-bottom: 3px solid transparent;
                background-color: transparent;
                color: #333333;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #6352EC;
            }
            QPushButton:checked {
                color: #6352EC;
                border-bottom: 3px solid #6352EC;
            }
        """)


class TabBar(QWidget):
    """
    Панель вкладок для навигации по приложению
    
    Содержит группу TabButton и управляет их состоянием,
    а также сигнализирует о переключении между вкладками.
    """
    # Сигнал, который будет испускаться при переключении вкладки
    tabChanged = pyqtSignal(int)
    
    def __init__(self, tabs_list, parent=None):
        """
        Инициализация панели вкладок
        
        Args:
            tabs_list (list): Список названий вкладок
            parent: Родительский виджет
        """
        super().__init__(parent)
        
        # Настройка внешнего вида
        self.setStyleSheet("""
            background-color: white;
            border-bottom: 1px solid #e0e0e0;
        """)
        
        # Создаем layout для размещения вкладок
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        
        # Список кнопок вкладок
        self.buttons = []
        
        # Создаем кнопки для каждой вкладки
        for i, tab_name in enumerate(tabs_list):
            button = TabButton(tab_name)
            button.setMinimumWidth(150)
            button.clicked.connect(lambda checked, idx=i: self.on_tab_clicked(idx))
            self.buttons.append(button)
            self.layout.addWidget(button)
        
        # Добавляем растягивающийся элемент справа
        self.layout.addStretch()
        
        # По умолчанию выбираем первую вкладку
        if self.buttons:
            self.set_active_tab(0)
    
    def set_active_tab(self, index):
        """
        Устанавливает активную вкладку
        
        Args:
            index (int): Индекс активной вкладки
        """
        if 0 <= index < len(self.buttons):
            # Сбрасываем состояние всех кнопок
            for button in self.buttons:
                button.setChecked(False)
            
            # Активируем нужную кнопку
            self.buttons[index].setChecked(True)
            
            # Испускаем сигнал о смене вкладки
            self.tabChanged.emit(index)
    
    def on_tab_clicked(self, index):
        """
        Обработчик нажатия на вкладку
        
        Args:
            index (int): Индекс нажатой вкладки
        """
        self.set_active_tab(index) 