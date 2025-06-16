"""
Менеджер авторизации для GoSilk Staff
"""

from PyQt6.QtWidgets import QApplication
from pyqt_app.dialogs.auth_dialog import AuthDialog
from loguru import logger as debug_logger


class AuthManager:
    """Менеджер авторизации приложения"""
    
    def __init__(self):
        self._is_authenticated = False
        
    def is_authenticated(self) -> bool:
        """Проверка состояния авторизации"""
        return self._is_authenticated
        
    def authenticate(self, parent=None) -> bool:
        """
        Показывает диалог авторизации и выполняет процесс авторизации
        
        Args:
            parent: Родительский виджет для диалога
            
        Returns:
            bool: True если авторизация успешна, False если отменена
        """
        debug_logger.info("🔐 Запуск процесса авторизации")
        
        # Создаем диалог авторизации
        auth_dialog = AuthDialog(parent)
        
        # Показываем диалог и ждем результата
        result = auth_dialog.exec()
        
        if result == AuthDialog.DialogCode.Accepted:
            self._is_authenticated = True
            debug_logger.success("✅ Авторизация успешно завершена")
            return True
        else:
            self._is_authenticated = False
            debug_logger.info("🚪 Авторизация отменена пользователем")
            return False
            
    def logout(self):
        """Выход из системы"""
        self._is_authenticated = False
        debug_logger.info("🚪 Пользователь вышел из системы")
        
    def require_authentication(self, parent=None) -> bool:
        """
        Требует авторизации. Если пользователь не авторизован, показывает диалог.
        
        Args:
            parent: Родительский виджет для диалога
            
        Returns:
            bool: True если пользователь авторизован, False если отказался
        """
        if self.is_authenticated():
            return True
            
        return self.authenticate(parent)


# Глобальный экземпляр менеджера авторизации
auth_manager = AuthManager() 