#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
    QWidget, QFrame, QComboBox, QLineEdit, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import tempfile
import os
from datetime import datetime

from .base_page import BasePage

class ContainerWithShadow(QFrame):
    """Кастомный виджет-контейнер с эффектом тени"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("containerWithShadow")
        self.setStyleSheet("""
            #containerWithShadow {
                background-color: white;
                border-radius: 20px;
                border-top: 1px solid #e0e0e0;
                border-left: 1px solid #e0e0e0;
                border-right: 4px solid #555555;
                border-bottom: 4px solid #555555;
            }
        """)

class SettingsPage(BasePage):
    """
    Страница настроек
    
    Содержит настройки приложения и конфигурацию скриптов
    """
    def __init__(self, parent=None):
        # Используем пустой заголовок, так как будем добавлять его вручную
        super().__init__("", parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Настройка элементов интерфейса страницы настроек"""
        # Установка белого фона для страницы
        self.setStyleSheet("background-color: white;")
        
        # Создаем основной scrollable контейнер для всего содержимого
        main_scroll_area = QScrollArea()
        main_scroll_area.setWidgetResizable(True)
        main_scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #d0d0d0;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: transparent;
            }
        """)
        
        # Создаем виджет для размещения всего содержимого
        scroll_content = QWidget()
        scroll_content_layout = QVBoxLayout(scroll_content)
        scroll_content_layout.setContentsMargins(20, 20, 20, 20)
        scroll_content_layout.setSpacing(15)
        
        # Добавляем отступ перед заголовком
        scroll_content_layout.addSpacing(10)
        
        # Добавляем заголовок "Настройки" в верхней части страницы
        title_label = QLabel("НАСТРОЙКИ")
        title_label.setStyleSheet("""
            font-size: 40px;
            font-weight: bold;
            color: #6352EC;
            margin-bottom: 15px;
            text-shadow: 2px 2px 3px rgba(0, 0, 0, 0.2);
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_content_layout.addWidget(title_label)
        
        # Добавляем горизонтальную линию под заголовком
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: #e0e0e0;")
        separator.setFixedHeight(1)
        scroll_content_layout.addWidget(separator)
        scroll_content_layout.addSpacing(20)
        
        # Создаем контейнер для настроек с тенью
        settings_container = ContainerWithShadow()
        container_layout = QVBoxLayout(settings_container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(15)
        
        # Выпадающий список шаблонов токенов
        template_label = QLabel("Шаблон токенов")
        template_label.setStyleSheet("font-size: 14px;")
        container_layout.addWidget(template_label)
        
        # Создаем контейнер для комбобокса и кнопки добавления
        template_selector_container = QWidget()
        template_selector_layout = QHBoxLayout(template_selector_container)
        template_selector_layout.setContentsMargins(0, 0, 0, 0)
        template_selector_layout.setSpacing(10)
        
        # Комбобокс для выбора шаблона
        self.template_combo = QComboBox()
        
        # Создаем временный SVG файл для стрелки
        svg_data = '''
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
          <path fill="#6352EC" d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
        </svg>
        '''
        
        temp_arrow_file = os.path.join(tempfile.gettempdir(), "down_arrow.svg")
        with open(temp_arrow_file, "w") as f:
            f.write(svg_data)
        
        # Преобразуем путь для использования в CSS (заменяем обратные слеши на прямые)
        css_path = temp_arrow_file.replace('\\', '/')
        
        self.template_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 15px;
                padding: 8px 15px;
                min-height: 40px;
                background-color: white;
                selection-background-color: #e6e0ff;
                selection-color: #333333;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 30px;
                border-left-width: 0px;
                border-top-right-radius: 15px;
                border-bottom-right-radius: 15px;
                margin-right: 10px;
            }
            QComboBox::down-arrow {
                image: url(""" + css_path + """);
                width: 16px;
                height: 16px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                border-radius: 8px;
                selection-background-color: #e6e0ff;
                background-color: white;
                padding: 5px;
            }
        """)
        
        # Кнопка добавления шаблона
        delete_template_button = QPushButton("×")  # Символ × для удаления
        delete_template_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5252;
                color: white;
                border-radius: 15px;
                padding: 5px 10px;
                font-weight: bold;
                font-size: 18px;
                min-width: 40px;
                min-height: 40px;
                border: 1px solid #ff3939;
                border-right: 2px solid #e60000;
                border-bottom: 2px solid #e60000;
            }
            QPushButton:hover {
                background-color: #ff3939;
            }
            QPushButton:pressed {
                background-color: #e60000;
            }
        """)
        delete_template_button.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_template_button.clicked.connect(self.delete_current_template)
        
        # Добавляем комбобокс и кнопку в контейнер
        template_selector_layout.addWidget(self.template_combo, 1)  # 1 - растягивать по доступному пространству
        template_selector_layout.addWidget(delete_template_button)
        
        # Добавляем контейнер с комбобоксом и кнопкой в основной layout
        container_layout.addWidget(template_selector_container)
        
        # Токен кабинета (User ID)
        user_id_label = QLabel("Токен кабинета (User ID)")
        user_id_label.setStyleSheet("font-size: 14px; margin-top: 15px;")
        container_layout.addWidget(user_id_label)
        
        self.user_id_input = QLineEdit()
        self.user_id_input.setPlaceholderText("Введите токен кабинета")
        self.user_id_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 15px;
                padding: 8px 15px;
                min-height: 40px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #6352EC;
            }
        """)
        container_layout.addWidget(self.user_id_input)
        
        # API Токен (JWT)
        jwt_label = QLabel("API Токен (JWT)")
        jwt_label.setStyleSheet("font-size: 14px; margin-top: 15px;")
        container_layout.addWidget(jwt_label)
        
        self.jwt_input = QLineEdit()
        self.jwt_input.setPlaceholderText("Введите API токен")
        self.jwt_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 15px;
                padding: 8px 15px;
                min-height: 40px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #6352EC;
            }
        """)
        container_layout.addWidget(self.jwt_input)
        
        # Кнопка "СОХРАНИТЬ КАК ШАБЛОН"
        save_template_button = QPushButton("СОХРАНИТЬ КАК ШАБЛОН")
        save_template_button.setStyleSheet("""
            QPushButton {
                background-color: #6352EC;
                color: white;
                border-radius: 15px;
                padding: 10px 20px;
                font-weight: bold;
                max-width: 250px;
                border: 1px solid #5143c9;
                border-right: 3px solid #473aad;
                border-bottom: 3px solid #473aad;
            }
            QPushButton:hover {
                background-color: #5143c9;
            }
            QPushButton:pressed {
                background-color: #473aad;
            }
        """)
        save_template_button.setCursor(Qt.CursorShape.PointingHandCursor)
        save_template_button.clicked.connect(self.save_as_template)
        
        # Контейнер для кнопки с выравниванием по левому краю
        save_template_container = QWidget()
        save_template_layout = QHBoxLayout(save_template_container)
        save_template_layout.setContentsMargins(0, 15, 0, 0)
        save_template_layout.addWidget(save_template_button)
        save_template_layout.addStretch()
        
        container_layout.addWidget(save_template_container)
        
        # Добавляем основной контейнер настроек в layout
        scroll_content_layout.addWidget(settings_container)
        
        # Контейнер с кнопками внизу страницы
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 20, 0, 0)
        
        # Добавляем растягивающийся элемент слева для выравнивания кнопок по правому краю
        buttons_layout.addStretch()
        
        # Кнопка "ОТМЕНА"
        cancel_button = QPushButton("ОТМЕНА")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5252;
                color: white;
                border-radius: 15px;
                padding: 15px 25px;
                font-weight: bold;
                border: 1px solid #ff3939;
                border-right: 4px solid #e60000;
                border-bottom: 4px solid #e60000;
            }
            QPushButton:hover {
                background-color: #ff3939;
            }
            QPushButton:pressed {
                background-color: #e60000;
            }
        """)
        cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_button.clicked.connect(self.cancel_settings)
        buttons_layout.addWidget(cancel_button)
        
        # Добавляем небольшой отступ между кнопками
        buttons_layout.addSpacing(20)
        
        # Кнопка "СОХРАНИТЬ"
        save_button = QPushButton("СОХРАНИТЬ")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #6352EC;
                color: white;
                border-radius: 15px;
                padding: 15px 25px;
                font-weight: bold;
                border: 1px solid #5143c9;
                border-right: 4px solid #473aad;
                border-bottom: 4px solid #473aad;
            }
            QPushButton:hover {
                background-color: #5143c9;
            }
            QPushButton:pressed {
                background-color: #473aad;
            }
        """)
        save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        save_button.clicked.connect(self.save_settings)
        buttons_layout.addWidget(save_button)
        
        # Добавляем контейнер с кнопками
        scroll_content_layout.addWidget(buttons_container)
        
        # Устанавливаем контент в scrollable контейнер
        main_scroll_area.setWidget(scroll_content)
        self.layout.addWidget(main_scroll_area)
        
        # Заполняем комбобокс тестовыми данными (в реальном приложении данные будут загружаться из файла или БД)
        self.load_templates()
        
    def load_templates(self):
        """Загрузка шаблонов токенов"""
        # Добавляем пустой элемент для выбора нового шаблона
        self.template_combo.addItem("Создать новый шаблон...")
        
        # Загрузка из JSON файла
        try:
            import json
            import os
            
            templates_path = os.path.join(os.path.dirname(__file__), "..", "data", "templates.json")
            if os.path.exists(templates_path):
                with open(templates_path, "r", encoding="utf-8") as f:
                    templates = json.load(f)
                    for template_name in templates:
                        self.template_combo.addItem(template_name)
        except Exception as e:
            print(f"Ошибка при загрузке шаблонов: {e}")
        
        # Подключаем обработчик изменения выбора
        self.template_combo.currentIndexChanged.connect(self.template_changed)
    
    def template_changed(self, index):
        """Обработчик изменения выбора шаблона"""
        if index == 0:  # "Создать новый шаблон..."
            # Очищаем поля
            self.user_id_input.clear()
            self.jwt_input.clear()
        else:
            # Загрузка данных шаблона из JSON файла
            import json
            import os
            
            template_name = self.template_combo.currentText()
            templates_path = os.path.join(os.path.dirname(__file__), "..", "data", "templates.json")
            
            try:
                if os.path.exists(templates_path):
                    with open(templates_path, "r", encoding="utf-8") as f:
                        templates = json.load(f)
                        if template_name in templates:
                            template_data = templates[template_name]
                            self.user_id_input.setText(template_data.get("user_id", ""))
                            self.jwt_input.setText(template_data.get("jwt", ""))
            except Exception as e:
                print(f"Ошибка при загрузке данных шаблона: {e}")
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.warning(
                    self,
                    "Ошибка загрузки",
                    f"Не удалось загрузить шаблон: {str(e)}"
                )
    
    def save_as_template(self):
        """Сохранение текущих токенов как шаблон"""
        # Получаем значения из полей
        user_id = self.user_id_input.text().strip()
        jwt = self.jwt_input.text().strip()
        
        # Проверяем, что поля не пустые
        if not user_id or not jwt:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Недостаточно данных",
                "Пожалуйста, заполните оба поля: токен кабинета и API токен."
            )
            return
        
        # Используем токен кабинета (ID) в качестве имени шаблона
        template_name = user_id
        
        # Сохранение в JSON файл
        import json
        import os
        
        # Создаем директорию для данных, если её нет
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        os.makedirs(data_dir, exist_ok=True)
        
        templates_path = os.path.join(data_dir, "templates.json")
        
        # Загружаем существующие шаблоны или создаем новый словарь
        templates = {}
        if os.path.exists(templates_path):
            try:
                with open(templates_path, "r", encoding="utf-8") as f:
                    templates = json.load(f)
            except:
                templates = {}
        
        # Добавляем или обновляем шаблон
        templates[template_name] = {
            "user_id": user_id,
            "jwt": jwt
        }
        
        # Сохраняем обновленные шаблоны
        try:
            with open(templates_path, "w", encoding="utf-8") as f:
                json.dump(templates, f, ensure_ascii=False, indent=4)
                
            # Обновляем список шаблонов в комбобоксе
            current_index = self.template_combo.currentIndex()
            self.template_combo.blockSignals(True)
            self.template_combo.clear()
            self.template_combo.addItem("Создать новый шаблон...")
            
            # Добавляем все шаблоны
            for name in templates:
                self.template_combo.addItem(name)
                
            # Выбираем текущий шаблон
            new_index = self.template_combo.findText(template_name)
            if new_index >= 0:
                self.template_combo.setCurrentIndex(new_index)
            else:
                self.template_combo.setCurrentIndex(current_index)
            self.template_combo.blockSignals(False)
                
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(
                self,
                "Ошибка сохранения",
                f"Не удалось сохранить шаблон: {str(e)}"
            )
            return
        
        # Показываем сообщение об успешном сохранении
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "Сохранение шаблона",
            f"Шаблон '{template_name}' успешно сохранен."
        )
    
    def save_settings(self):
        """Сохранение настроек"""
        # Получаем значения из полей
        user_id = self.user_id_input.text().strip()
        jwt = self.jwt_input.text().strip()
        
        # Проверяем, что поля не пустые
        if not user_id or not jwt:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Недостаточно данных",
                "Пожалуйста, заполните оба поля: токен кабинета и API токен."
            )
            return
        
        # Сохраняем текущие настройки в файл конфигурации
        import json
        import os
        
        # Создаем директорию для данных, если её нет
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        os.makedirs(data_dir, exist_ok=True)
        
        config_path = os.path.join(data_dir, "config.json")
        
        # Создаем или обновляем конфигурационный файл
        config = {
            "user_id": user_id,
            "jwt": jwt,
            "last_updated": datetime.now().isoformat()
        }
        
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
                
            # Показываем сообщение об успешном сохранении
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(
                self,
                "Сохранение настроек",
                "Настройки успешно сохранены."
            )
            
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(
                self,
                "Ошибка сохранения",
                f"Не удалось сохранить настройки: {str(e)}"
            )
    
    def cancel_settings(self):
        """Отмена изменений"""
        # Возвращаемся на предыдущую страницу
        main_window = self.window()
        main_window.content_stack.setCurrentIndex(0)  # Переход на страницу загрузки

    def delete_current_template(self):
        """Удаление текущего выбранного шаблона"""
        # Получаем текущий выбранный шаблон
        current_index = self.template_combo.currentIndex()
        if current_index <= 0:  # Если выбран первый элемент ("Создать новый шаблон...")
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Предупреждение",
                "Выберите шаблон для удаления"
            )
            return
        
        template_name = self.template_combo.currentText()
        
        # Запрашиваем подтверждение
        from PyQt6.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить шаблон '{template_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.No:
            return
        
        # Удаляем шаблон из JSON файла
        import json
        import os
        
        templates_path = os.path.join(os.path.dirname(__file__), "..", "data", "templates.json")
        
        # Загружаем существующие шаблоны
        if os.path.exists(templates_path):
            try:
                with open(templates_path, "r", encoding="utf-8") as f:
                    templates = json.load(f)
                
                # Удаляем шаблон
                if template_name in templates:
                    del templates[template_name]
                
                # Сохраняем обновленные шаблоны
                with open(templates_path, "w", encoding="utf-8") as f:
                    json.dump(templates, f, ensure_ascii=False, indent=4)
                
                # Обновляем список шаблонов в комбобоксе
                self.template_combo.blockSignals(True)
                self.template_combo.clear()
                self.template_combo.addItem("Создать новый шаблон...")
                
                # Добавляем все шаблоны
                for name in templates:
                    self.template_combo.addItem(name)
                
                # Выбираем первый элемент
                self.template_combo.setCurrentIndex(0)
                self.template_combo.blockSignals(False)
                
                # Очищаем поля ввода
                self.user_id_input.clear()
                self.jwt_input.clear()
                
                # Показываем сообщение об успешном удалении
                QMessageBox.information(
                    self,
                    "Шаблон удален",
                    f"Шаблон '{template_name}' успешно удален."
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Ошибка удаления",
                    f"Не удалось удалить шаблон: {str(e)}"
                )
        else:
            QMessageBox.warning(
                self,
                "Файл не найден",
                "Файл шаблонов не найден."
            )