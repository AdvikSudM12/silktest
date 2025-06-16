"""
Диалог авторизации для GoSilk Staff
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QFrame, QWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPixmap
from loguru import logger as debug_logger


class AuthDialog(QDialog):
    """Диалог авторизации с паролем"""
    
    # Сигнал успешной авторизации
    authentication_successful = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_styles()
        
    def setup_ui(self):
        """Настройка интерфейса"""
        self.setWindowTitle("GoSilk Staff - Авторизация")
        self.setModal(True)
        self.setFixedSize(450, 350)
        
        # Устанавливаем иконку приложения (только для macOS)
        import sys
        if sys.platform == "darwin":
            from pyqt_app.resources.icons import get_app_icon
            self.setWindowIcon(get_app_icon())
        
        # Убираем кнопки закрытия окна
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowTitleHint)
        
        # Основной layout
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Заголовок приложения
        self.title_label = QLabel("🎵 GoSilk Staff")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        layout.addWidget(self.title_label)
        
        # Подзаголовок
        self.subtitle_label = QLabel("Система управления музыкальными релизами")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_font = QFont()
        subtitle_font.setPointSize(10)
        self.subtitle_label.setFont(subtitle_font)
        layout.addWidget(self.subtitle_label)
        
        # Разделитель
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        # Инструкция
        self.instruction_label = QLabel("🔐 Введите пароль для доступа:")
        self.instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction_font = QFont()
        instruction_font.setPointSize(11)
        instruction_font.setBold(True)
        self.instruction_label.setFont(instruction_font)
        layout.addWidget(self.instruction_label)
        
        # Поле ввода пароля
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Введите пароль...")
        self.password_input.returnPressed.connect(self.on_login_clicked)
        layout.addWidget(self.password_input)
        
        # Сообщение об ошибке (скрыто по умолчанию)
        self.error_label = QLabel("❌ Неверный пароль!")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setVisible(False)
        error_font = QFont()
        error_font.setPointSize(10)
        error_font.setBold(True)
        self.error_label.setFont(error_font)
        layout.addWidget(self.error_label)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("🚪 Выход")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)
        
        buttons_layout.addStretch()
        
        self.login_button = QPushButton("🔓 Войти")
        self.login_button.clicked.connect(self.on_login_clicked)
        self.login_button.setDefault(True)  # Кнопка по умолчанию
        buttons_layout.addWidget(self.login_button)
        
        layout.addLayout(buttons_layout)
        
        # Фокус на поле ввода
        self.password_input.setFocus()
        
    def setup_styles(self):
        """Настройка стилей в соответствии с дизайном приложения"""
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            
            QLabel {
                color: #333;
            }
            
            QLabel#title_label {
                color: #2196F3;
            }
            
            QLabel#subtitle_label {
                color: #666;
            }
            
            QLabel#instruction_label {
                color: #333;
            }
            
            QLabel#error_label {
                color: #f44336;
                background-color: #ffebee;
                border: 1px solid #f44336;
                border-radius: 6px;
                padding: 8px;
            }
            
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 8px;
                padding: 8px;
                font-size: 12px;
                background-color: #fff;
            }
            
            QLineEdit:focus {
                border-color: #2196F3;
            }
            
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 100px;
                font-size: 11px;
            }
            
            QPushButton:hover {
                background-color: #1976D2;
            }
            
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            
            QPushButton#cancel_button {
                background-color: #757575;
            }
            
            QPushButton#cancel_button:hover {
                background-color: #616161;
            }
            
            QPushButton#cancel_button:pressed {
                background-color: #424242;
            }
        """)
        
        # Устанавливаем имена объектов для стилей
        self.title_label.setObjectName("title_label")
        self.subtitle_label.setObjectName("subtitle_label")
        self.instruction_label.setObjectName("instruction_label")
        self.error_label.setObjectName("error_label")
        self.cancel_button.setObjectName("cancel_button")
        
    def check_password(self, password: str) -> bool:
        """Проверка пароля"""
        # Пока используем статичный пароль
        correct_password = "13579"
        return password == correct_password
        
    def on_login_clicked(self):
        """Обработчик нажатия кнопки входа"""
        password = self.password_input.text().strip()
        
        if not password:
            self.show_error("Введите пароль!")
            return
            
        if self.check_password(password):
            debug_logger.success("✅ Успешная авторизация")
            self.authentication_successful.emit()
            self.accept()
        else:
            debug_logger.warning("⚠️ Неверный пароль при авторизации")
            self.show_error("Неверный пароль!")
            self.password_input.clear()
            self.password_input.setFocus()
            
    def show_error(self, message: str):
        """Показывает сообщение об ошибке"""
        self.error_label.setText(f"❌ {message}")
        self.error_label.setVisible(True)
        
        # Скрываем ошибку через 3 секунды
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(3000, lambda: self.error_label.setVisible(False))
        
    def keyPressEvent(self, event):
        """Обработка нажатий клавиш"""
        # Блокируем Escape для предотвращения закрытия диалога
        if event.key() == Qt.Key.Key_Escape:
            return
        super().keyPressEvent(event) 