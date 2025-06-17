#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFrame, 
    QPushButton, QScrollArea, QGridLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPainter, QPen, QColor
from datetime import datetime
import json
import os
import pandas as pd

# DEBUG: импорт логгера для системы отладки - нужно будет удалить позже
from ..logger_config import get_logger
debug_logger = get_logger("analytics_page")

# Импорт сессионного менеджера данных
from ..session_data_manager import session_manager

from .base_page import BasePage

class AnalyticsCard(QFrame):
    """Карточка для отображения аналитических данных"""
    def __init__(self, title: str, value: str, color: str = "#6352EC", parent=None):
        super().__init__(parent)
        self.setObjectName("analyticsCard")
        self.setup_ui(title, value, color)
        
    def setup_ui(self, title: str, value: str, color: str):
        """Настройка UI карточки"""
        self.setStyleSheet(f"""
            #analyticsCard {{
                background-color: white;
                border-radius: 15px;
                border: 1px solid #e0e0e0;
                border-right: 3px solid {color};
                border-bottom: 3px solid {color};
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(8)
        
        # Заголовок
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            color: {color};
            font-size: 14px;
            font-weight: bold;
        """)
        layout.addWidget(title_label)
        
        # Значение
        value_label = QLabel(value)
        value_label.setStyleSheet("""
            color: #333333;
            font-size: 24px;
            font-weight: bold;
        """)
        layout.addWidget(value_label)

class AnalyticsPage(BasePage):
    """
    Страница аналитики
    
    Отображает отчет о проверке файлов на основе данных из скриптов
    """
    
    # Сигнал для обновления данных
    update_analytics = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__("", parent)  # Пустой заголовок, добавим свой
        self.analytics_data = None
        self.setup_ui()
        self.load_analytics_data()
        
    def setup_ui(self):
        """Настройка элементов интерфейса страницы аналитики"""
        # Установка белого фона
        self.setStyleSheet("background-color: white;")
        
        # Создаем основной scrollable контейнер
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
        scroll_content_layout.setContentsMargins(40, 30, 40, 30)
        scroll_content_layout.setSpacing(30)
        
        # Заголовок страницы с эффектом
        title_label = QLabel("АНАЛИТИКА")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 48px;
            font-weight: bold;
            color: #6352EC;
            margin: 20px 0;
        """)
        scroll_content_layout.addWidget(title_label)
        
        # Раздел "Отчет о проверке"
        self.setup_report_section(scroll_content_layout)
        
        # Устанавливаем виджет в прокручиваемую область
        main_scroll_area.setWidget(scroll_content)
        
        # Добавляем прокручиваемую область в основной layout страницы
        self.layout.addWidget(main_scroll_area)
        
    def setup_report_section(self, parent_layout):
        """Настройка раздела отчета о проверке"""
        # Заголовок секции с иконкой
        section_header = QWidget()
        section_layout = QHBoxLayout(section_header)
        section_layout.setContentsMargins(0, 0, 0, 10)
        section_layout.setSpacing(10)
        
        # Иконка отчета
        report_icon = QLabel("📊")
        report_icon.setStyleSheet("font-size: 24px;")
        
        # Заголовок
        section_title = QLabel("Отчет о проверке")
        section_title.setStyleSheet("""
            color: #6352EC;
            font-size: 20px;
            font-weight: bold;
        """)
        
        section_layout.addWidget(report_icon)
        section_layout.addWidget(section_title)
        section_layout.addStretch()
        
        parent_layout.addWidget(section_header)
        
        # Основной контейнер отчета
        self.report_container = QFrame()
        self.report_container.setObjectName("reportContainer")
        self.report_container.setStyleSheet("""
            #reportContainer {
                background-color: #f8f7ff;
                border-radius: 20px;
                border: 1px solid #e6e0ff;
                border-right: 4px solid #d7cdff;
                border-bottom: 4px solid #d7cdff;
            }
        """)
        
        self.report_layout = QVBoxLayout(self.report_container)
        self.report_layout.setContentsMargins(30, 25, 30, 25)
        self.report_layout.setSpacing(20)
        
        # Информация об отчете
        self.setup_report_info()
        
        # Статистика в виде карточек
        self.setup_statistics_cards()
        
        # Результат проверки
        self.setup_result_section()
        
        # Кнопка сохранения отчета
        self.setup_save_button()
        
        parent_layout.addWidget(self.report_container)
        
    def setup_report_info(self):
        """Настройка информации об отчете"""
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(8)
        
        # Заголовок отчета
        report_title = QLabel("Отчет о проверке файлов для загрузки")
        report_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #333333;
        """)
        info_layout.addWidget(report_title)
        
        # Дата отчета
        self.date_label = QLabel(f"Дата: {datetime.now().strftime('%d.%m.%Y')}")
        self.date_label.setStyleSheet("""
            font-size: 14px;
            color: #666666;
        """)
        info_layout.addWidget(self.date_label)
        
        self.report_layout.addWidget(info_widget)
        
    def setup_statistics_cards(self):
        """Настройка карточек со статистикой"""
        # Контейнер для карточек
        cards_container = QWidget()
        cards_layout = QGridLayout(cards_container)
        cards_layout.setContentsMargins(0, 10, 0, 10)
        cards_layout.setSpacing(15)
        
        # Создаем карточки с данными
        self.releases_card = AnalyticsCard("Всего релизов из Excel:", "0", "#6352EC")
        self.tracks_card = AnalyticsCard("Всего треков в Excel:", "0", "#19c790")
        self.covers_card = AnalyticsCard("Всего обложек в Excel:", "0", "#f7a440")
        
        self.found_audio_card = AnalyticsCard("Найдено аудио файлов:", "0 из 0", "#8B7FFF")
        self.found_covers_card = AnalyticsCard("Найдено файлов обложек:", "0 из 0", "#17b683")
        
        # Размещаем карточки в сетке
        cards_layout.addWidget(self.releases_card, 0, 0)
        cards_layout.addWidget(self.tracks_card, 0, 1)
        cards_layout.addWidget(self.covers_card, 0, 2)
        
        cards_layout.addWidget(self.found_audio_card, 1, 0)
        cards_layout.addWidget(self.found_covers_card, 1, 1)
        
        # Пустая ячейка для симметрии
        empty_widget = QWidget()
        cards_layout.addWidget(empty_widget, 1, 2)
        
        self.report_layout.addWidget(cards_container)
        
    def setup_result_section(self):
        """Настройка секции результата"""
        # Контейнер результата
        self.result_container = QFrame()
        self.result_container.setStyleSheet("""
            QFrame {
                background-color: #e6ffe6;
                border: 1px solid #ccffcc;
                border-radius: 15px;
                border-right: 3px solid #b3ffb3;
                border-bottom: 3px solid #b3ffb3;
                padding: 15px;
            }
        """)
        
        result_layout = QHBoxLayout(self.result_container)
        result_layout.setContentsMargins(20, 15, 20, 15)
        result_layout.setSpacing(15)
        
        # Иконка результата
        self.result_icon = QLabel("✅")
        self.result_icon.setStyleSheet("font-size: 24px;")
        
        # Текст результата
        self.result_text = QLabel("Данные не загружены. Выполните проверку файлов.")
        self.result_text.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #333333;
        """)
        
        result_layout.addWidget(self.result_icon)
        result_layout.addWidget(self.result_text, 1)
        
        self.report_layout.addWidget(self.result_container)
        
    def setup_save_button(self):
        """Настройка кнопки сохранения отчета"""
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 10, 0, 0)
        
        self.save_button = QPushButton("СОХРАНИТЬ ОТЧЕТ")
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #6352EC;
                color: white;
                border-radius: 15px;
                padding: 12px 30px;
                font-weight: bold;
                font-size: 14px;
                border: 1px solid #5143c9;
                border-right: 3px solid #473aad;
                border-bottom: 3px solid #473aad;
                max-width: 200px;
            }
            QPushButton:hover {
                background-color: #5143c9;
            }
            QPushButton:pressed {
                background-color: #473aad;
            }
            QPushButton:disabled {                background-color: #cccccc;
                color: #888888;
                border: 1px solid #bbbbbb;
                border-right: 3px solid #aaaaaa;
                border-bottom: 3px solid #aaaaaa;
            }
        """)
        self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_button.clicked.connect(self.save_report)
        self.save_button.setEnabled(False)  # Изначально отключена
        
        button_layout.addWidget(self.save_button)
        button_layout.addStretch()
        
        self.report_layout.addWidget(button_container)
        
    def load_analytics_data(self):
        """Загрузка данных аналитики из сессионного хранилища или последнего отчета"""
        try:
            debug_logger.info("📊 Загружаем данные аналитики")
            
            # ПРИОРИТЕТ 1: Проверяем сессионные данные
            if session_manager.has_analytics_data():
                debug_logger.info("✅ Найдены сессионные данные аналитики")
                session_data = session_manager.get_latest_analytics_data()
                if session_data:
                    self.load_from_session_data(session_data)
                    return
            
            debug_logger.info("⚠️ Сессионные данные не найдены, ищем файлы results")
            
            # ПРИОРИТЕТ 2: Ищем файлы в папке results (старый метод)
            results_dir = os.path.join(os.path.dirname(__file__), "..", "..", "results")
            
            if os.path.exists(results_dir):
                # Ищем последний файл с результатами
                result_files = [f for f in os.listdir(results_dir) 
                              if f.startswith('file_comparison_results_') and f.endswith('.xlsx')]
                
                if result_files:
                    result_files.sort(reverse=True)  # Сортируем по убыванию (последний файл первый)
                    latest_file = result_files[0]
                    
                    debug_logger.info(f"📄 Найден файл результатов: {latest_file}")
                    
                    # Извлекаем дату из имени файла
                    date_part = latest_file.replace('file_comparison_results_', '').replace('.xlsx', '')
                    formatted_date = date_part.replace('_', ' ').replace('-', '.')
                    self.date_label.setText(f"Дата: {formatted_date}")
                    
                    # Пытаемся загрузить данные из Excel файла
                    self.load_excel_data(os.path.join(results_dir, latest_file))
                    return
            
            debug_logger.warning("⚠️ Нет данных для аналитики, показываем пустое состояние")
            # ПРИОРИТЕТ 3: Показываем пустое состояние
            self.show_empty_state()
                    
        except Exception as e:
            debug_logger.error(f"❌ Ошибка при загрузке данных аналитики: {e}")
            self.show_empty_state()
    
    def load_from_session_data(self, session_data: dict):
        """Загружает данные аналитики из сессионного хранилища"""
        try:
            debug_logger.info("📋 Загружаем данные из сессионного хранилища")
            
            comparison_result = session_data.get('comparison_result', {})
            analytics_summary = session_data.get('analytics_summary', {})
            timestamp = session_data.get('timestamp', '')
            
            # Обновляем дату
            if timestamp:
                from datetime import datetime
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00') if timestamp.endswith('Z') else timestamp)
                formatted_date = dt.strftime('%d.%m.%Y %H:%M')
                self.date_label.setText(f"Дата: {formatted_date}")
            
            # Используем существующий метод для обновления UI
            self.update_from_comparison_result(comparison_result)
            
            debug_logger.success("✅ Данные из сессии успешно загружены")
            
        except Exception as e:
            debug_logger.error(f"❌ Ошибка при загрузке из сессии: {e}")
            # Fallback к пустому состоянию
            self.show_empty_state()
    
    def show_empty_state(self):
        """Показывает пустое состояние когда нет данных для аналитики"""
        # Показываем пустые значения
        self.update_analytics_display({
            'total_releases': 0,
            'total_tracks': 0,
            'total_covers': 0,
            'found_audio': "— из —",
            'found_covers': "— из —", 
            'all_found': False
        })
        
        # Специальное оформление для пустого состояния
        self.result_container.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border: 1px solid #e0e0e0;
                border-radius: 15px;
                border-right: 3px solid #cccccc;
                border-bottom: 3px solid #cccccc;
                padding: 15px;
            }
        """)
        self.result_icon.setText("📊")
        self.result_text.setText("Нет данных для отображения. Перейдите на страницу 'Загрузка' и выполните проверку файлов.")
        
        # Обновляем дату
        self.date_label.setText("Дата: —")
        
        # Кнопка остается неактивной
        self.save_button.setEnabled(False)
            
    def load_excel_data(self, file_path: str):
        """Загрузка данных из Excel файла"""
        try:
            # Читаем файл результатов
            df = pd.read_excel(file_path, sheet_name='Результаты')
            
            # Подсчитываем статистику
            total_errors = len(df)
            audio_errors = len(df[df['Тип файла'] == 'Трек'])
            cover_errors = len(df[df['Тип файла'] == 'Обложка'])
              # Обновляем данные с реальной статистикой из Excel
            excel_stats = self.get_excel_statistics()
            self.update_analytics_display({
                'total_releases': excel_stats['total_releases'],
                'total_tracks': excel_stats['total_tracks'],   
                'total_covers': excel_stats['total_covers'],
                'found_audio': f"{excel_stats['total_tracks'] - audio_errors} из {excel_stats['total_tracks']}",
                'found_covers': f"{excel_stats['total_covers'] - cover_errors} из {excel_stats['total_covers']}",
                'all_found': total_errors == 0
            })
            
            self.analytics_data = {
                'file_path': file_path,
                'total_errors': total_errors,
                'audio_errors': audio_errors,
                'cover_errors': cover_errors
            }
            
            # Активируем кнопку сохранения
            self.save_button.setEnabled(True)
            
        except Exception as e:
            debug_logger.error(f"❌ Ошибка при чтении Excel файла: {e}")
            
    def update_analytics_display(self, data: dict):
        """Обновление отображения аналитических данных"""
        # Обновляем карточки
        self.releases_card.findChild(QLabel).setText("Всего релизов из Excel:")
        self.releases_card.findChildren(QLabel)[1].setText(str(data['total_releases']))
        
        self.tracks_card.findChildren(QLabel)[1].setText(str(data['total_tracks']))
        self.covers_card.findChildren(QLabel)[1].setText(str(data['total_covers']))
        
        self.found_audio_card.findChildren(QLabel)[1].setText(data['found_audio'])
        self.found_covers_card.findChildren(QLabel)[1].setText(data['found_covers'])
        
        # Обновляем результат
        if data['all_found']:
            self.result_container.setStyleSheet("""
                QFrame {
                    background-color: #e6ffe6;
                    border: 1px solid #ccffcc;
                    border-radius: 15px;
                    border-right: 3px solid #b3ffb3;
                    border-bottom: 3px solid #b3ffb3;
                    padding: 15px;
                }
            """)
            self.result_icon.setText("✅")
            self.result_text.setText("Все файлы из Excel найдены успешно!")
        else:
            self.result_container.setStyleSheet("""
                QFrame {
                    background-color: #fff9e6;
                    border: 1px solid #ffefcc;
                    border-radius: 15px;
                    border-right: 3px solid #ffe6b3;
                    border-bottom: 3px solid #ffe6b3;
                    padding: 15px;
                }
            """)
            self.result_icon.setText("⚠️")
            self.result_text.setText("Обнаружены проблемы с файлами. Проверьте отчет.")
            
    def update_from_comparison_result(self, comparison_result: dict):
        """Обновление данных на основе результатов сравнения файлов"""
        if not comparison_result:
            return
            
        # Извлекаем данные из результата сравнения
        error_count = comparison_result.get('error_count', 0)
        results_data = comparison_result.get('results_data', [])
          # Подсчитываем статистику
        audio_errors = len([r for r in results_data if r.get('Тип файла') == 'Трек'])
        cover_errors = len([r for r in results_data if r.get('Тип файла') == 'Обложка'])
        
        # Получаем реальную статистику из Excel файла
        excel_stats = self.get_excel_statistics()
        total_tracks = excel_stats['total_tracks']
        total_covers = excel_stats['total_covers']
        total_releases = excel_stats['total_releases']
        
        # Обновляем отображение
        self.update_analytics_display({
            'total_releases': total_releases,
            'total_tracks': total_tracks,
            'total_covers': total_covers,
            'found_audio': f"{total_tracks - audio_errors} из {total_tracks}",
            'found_covers': f"{total_covers - cover_errors} из {total_covers}",
            'all_found': error_count == 0
        })
        
        # Сохраняем данные
        self.analytics_data = {
            'total_errors': error_count,
            'audio_errors': audio_errors,
            'cover_errors': cover_errors,
            'results_file': comparison_result.get('results_file', '')
        }
        
        # Активируем кнопку сохранения
        self.save_button.setEnabled(True)
        
        # Обновляем дату
        self.date_label.setText(f"Дата: {datetime.now().strftime('%d.%m.%Y')}")
        
    def save_report(self):
        """Сохранение отчета аналитики"""
        from PyQt6.QtWidgets import QMessageBox, QFileDialog
        import shutil
        
        if not self.analytics_data:
            QMessageBox.warning(self, "Нет данных", "Нет данных для сохранения отчета.")
            return
            
        # Диалог сохранения файла
        suggested_filename = f"Аналитический_отчет_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
        
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить аналитический отчет",
            suggested_filename,
            "Excel Files (*.xlsx);;All Files (*)"
        )
        
        if save_path:
            try:
                # Если есть файл результатов, копируем его
                results_file = self.analytics_data.get('results_file')
                if results_file and os.path.exists(results_file):
                    shutil.copy2(results_file, save_path)
                    
                    QMessageBox.information(
                        self,
                        "Отчет сохранен",
                        f"Аналитический отчет сохранен:\n{save_path}"
                    )
                else:
                    QMessageBox.warning(
                        self,
                        "Файл не найден",
                        "Исходный файл результатов не найден."
                    )
                    
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Ошибка сохранения",
                    f"Не удалось сохранить отчет:\n{str(e)}"
                )
                
    def get_excel_statistics(self):
        """Получение реальной статистики из Excel файла"""
        try:
            # Читаем paths.json для получения пути к Excel файлу
            from ..path_manager import get_config_file_path
            paths_file = str(get_config_file_path('paths.json'))
            if os.path.exists(paths_file):
                with open(paths_file, 'r', encoding='utf-8') as f:
                    paths_data = json.load(f)
                    excel_path = paths_data.get('excel_file_path', '')
                    
                if excel_path and os.path.exists(excel_path):
                    # Читаем Excel файл
                    df = pd.read_excel(excel_path)
                    
                    # Подсчитываем статистику
                    total_releases = len(df) if not df.empty else 0
                    # Подсчитываем треки (предполагаем, что каждый релиз может иметь несколько треков)
                    # Если есть колонка с количеством треков - используем её, иначе считаем по 1 треку на релиз
                    if 'Треки' in df.columns:
                        total_tracks = df['Треки'].sum()
                    elif 'Количество треков' in df.columns:
                        total_tracks = df['Количество треков'].sum()
                    else:
                        # В нашем случае каждая строка = 1 трек (колонка 'track (titel)')
                        total_tracks = total_releases  # 1 трек на релиз
                    
                    # Обложки обычно = количеству релизов
                    total_covers = total_releases
                    
                    return {
                        'total_releases': total_releases,
                        'total_tracks': total_tracks,
                        'total_covers': total_covers
                    }
            
            # Возвращаем нули если не удалось прочитать Excel
            return {
                'total_releases': 0,
                'total_tracks': 0,
                'total_covers': 0
            }
            
        except Exception as e:
            debug_logger.error(f"❌ Ошибка при чтении Excel статистики: {e}")
            # Возвращаем нули в случае ошибки
            return {
                'total_releases': 0,
                'total_tracks': 0,
                'total_covers': 0
            }