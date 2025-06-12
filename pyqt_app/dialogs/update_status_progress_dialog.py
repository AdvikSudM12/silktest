"""
Диалог прогресса обновления статусов релизов
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QProgressBar, QTextEdit, QPushButton, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
from loguru import logger as debug_logger


class UpdateStatusProgressDialog(QDialog):
    """Диалог отображения прогресса обновления статусов релизов"""
    
    # Сигнал для запроса отмены
    cancel_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_styles()
        
    def setup_ui(self):
        """Настройка интерфейса"""
        self.setWindowTitle("Обновление статусов релизов")
        self.setModal(True)
        self.setFixedSize(600, 500)
        
        # Основной layout
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Заголовок
        self.title_label = QLabel("🔄 Обновление статусов релизов")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        layout.addWidget(self.title_label)
        
        # Текущая стадия
        self.stage_label = QLabel("Инициализация...")
        self.stage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stage_font = QFont()
        stage_font.setPointSize(10)
        self.stage_label.setFont(stage_font)
        layout.addWidget(self.stage_label)
        
        # Прогресс-бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)
        
        # Разделитель
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        # Лог выполнения
        log_label = QLabel("📋 Детальный лог:")
        log_font = QFont()
        log_font.setPointSize(10)
        log_font.setBold(True)
        log_label.setFont(log_font)
        layout.addWidget(log_label)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(250)
        
        # Настройка шрифта для лога
        log_font = QFont("Consolas", 9)
        if not log_font.exactMatch():
            log_font = QFont("Courier New", 9)
        self.log_text.setFont(log_font)
        
        layout.addWidget(self.log_text)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("🛑 Отменить")
        self.cancel_button.clicked.connect(self.on_cancel_clicked)
        buttons_layout.addWidget(self.cancel_button)
        
        buttons_layout.addStretch()
        
        self.close_button = QPushButton("✅ Закрыть")
        self.close_button.clicked.connect(self.accept)
        self.close_button.setEnabled(False)  # Включается после завершения
        buttons_layout.addWidget(self.close_button)
        
        layout.addLayout(buttons_layout)
        
    def setup_styles(self):
        """Настройка стилей"""
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            
            QLabel {
                color: #333;
            }
            
            QProgressBar {
                border: 2px solid #ddd;
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
                height: 25px;
            }
            
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FF9800, stop:1 #F57C00);
                border-radius: 6px;
            }
            
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: #fff;
                padding: 8px;
            }
            
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 100px;
            }
            
            QPushButton:hover {
                background-color: #1976D2;
            }
            
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            
            QPushButton:disabled {
                background-color: #ccc;
                color: #666;
            }
            
            QPushButton#cancel_button {
                background-color: #f44336;
            }
            
            QPushButton#cancel_button:hover {
                background-color: #d32f2f;
            }
        """)
        
        self.cancel_button.setObjectName("cancel_button")
        
    def update_progress(self, message: str):
        """Обновляет текстовый лог"""
        # Добавляем сообщение в лог
        self.log_text.append(message)
        
        # Автоскролл к последнему сообщению
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
        debug_logger.info(f"📊 Progress: {message}")
        
    def update_progress_percent(self, percent: int):
        """Обновляет прогресс-бар"""
        self.progress_bar.setValue(percent)
        debug_logger.info(f"📈 Progress: {percent}%")
        
    def update_stage(self, stage: str):
        """Обновляет текущую стадию"""
        stage_messages = {
            "init": "🔧 Инициализация...",
            "api_check": "🔍 Проверка API...",
            "api_test": "🌐 Тестирование подключения...",
            "fetching": "📥 Получение релизов...",
            "backup": "💾 Создание резервной копии...",
            "updating": "🔄 Обновление статусов...",
            "completed": "✅ Обновление завершено!",
            "report": "📊 Формирование отчета...",
            "error": "❌ Ошибка выполнения",
            "cancelled": "🛑 Операция отменена"
        }
        
        message = stage_messages.get(stage, f"🔄 {stage}")
        self.stage_label.setText(message)
        debug_logger.info(f"🎭 Stage: {stage} -> {message}")
        
    def on_cancel_clicked(self):
        """Обработка нажатия кнопки отмены"""
        debug_logger.warning("🛑 Пользователь запросил отмену обновления статусов")
        self.cancel_requested.emit()
        self.cancel_button.setEnabled(False)
        self.cancel_button.setText("⏳ Отмена...")
        
    def on_finished(self, success: bool, message: str):
        """Обработка завершения операции"""
        debug_logger.info(f"🏁 Обновление статусов завершено: success={success}")
        
        # Отключаем кнопку отмены и включаем кнопку закрытия
        self.cancel_button.setEnabled(False)
        self.close_button.setEnabled(True)
        
        # Обновляем заголовок в зависимости от результата
        if success:
            self.title_label.setText("✅ Статусы релизов успешно обновлены!")
            self.title_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
            self.stage_label.setText("🎉 Операция завершена успешно")
            self.progress_bar.setValue(100)
        else:
            self.title_label.setText("❌ Ошибка обновления статусов")
            self.title_label.setStyleSheet("color: #f44336; font-weight: bold;")
            self.stage_label.setText("💥 Операция завершена с ошибкой")
            
        # Добавляем финальное сообщение в лог
        self.update_progress(f"🏁 РЕЗУЛЬТАТ: {message}")
        
    def on_error(self, error_message: str):
        """Обработка ошибки"""
        debug_logger.error(f"💥 Ошибка обновления статусов: {error_message}")
        self.update_progress(f"💥 ОШИБКА: {error_message}")
        self.on_finished(False, error_message)
        
    def closeEvent(self, event):
        """Обработка закрытия диалога"""
        # Если операция еще выполняется, предупреждаем пользователя
        if self.cancel_button.isEnabled():
            from PyQt6.QtWidgets import QMessageBox
            reply = QMessageBox.question(
                self,
                "Подтверждение закрытия",
                "Обновление статусов еще выполняется.\nВы действительно хотите закрыть окно и отменить операцию?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.cancel_requested.emit()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept() 