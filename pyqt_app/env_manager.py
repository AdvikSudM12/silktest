#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Менеджер для автоматического создания и обновления .env файла
на основе выбранных шаблонов токенов из templates.json
"""

import os
import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

# DEBUG: импорт логгера для системы отладки
from .logger_config import get_logger
debug_logger = get_logger("env_manager")

class EnvManager:
    """Класс для управления .env файлом с токенами из templates.json"""
    
    def __init__(self):
        """Инициализация менеджера"""
        # Определяем пути к файлам
        self.root_dir = Path(__file__).parent.parent  # Корень проекта
        self.data_dir = Path(__file__).parent / "data"
        self.templates_file = self.data_dir / "templates.json"
        self.config_file = self.data_dir / "config.json"
        self.env_file = self.root_dir / ".env"
        
        debug_logger.info("🏗️ Инициализация EnvManager")
        debug_logger.debug(f"📁 Корневая директория: {self.root_dir}")
        debug_logger.debug(f"📄 Файл .env: {self.env_file}")
        debug_logger.debug(f"📊 Файл templates.json: {self.templates_file}")
        
        # Создаем директорию data если её нет
        self.data_dir.mkdir(exist_ok=True)
        
        # Базовая структура .env файла (статичные настройки)
        self.base_env_structure = {
            "EMD_API": "https://api.emd.cloud",
            "EMD_SPACE": "silk",
            "EMD_HEADER_TOKEN": "Authorization",
            "EMD_TOKEN": "",  # Будет заполняться из templates
            "EMD_USER_ID": "",  # Будет заполняться из templates
            "DAYS_GONE_FOR_START_SITES": "14"
        }
    
    def load_templates(self) -> Dict:
        """Загружает шаблоны из templates.json"""
        try:
            if self.templates_file.exists():
                with open(self.templates_file, 'r', encoding='utf-8') as f:
                    templates = json.load(f)
                debug_logger.debug(f"📊 Загружено шаблонов: {len(templates)}")
                return templates
            else:
                debug_logger.warning("⚠️ Файл templates.json не найден")
                return {}
        except Exception as e:
            debug_logger.error(f"❌ Ошибка загрузки templates.json: {e}")
            return {}
    
    def load_current_config(self) -> Dict:
        """Загружает текущую конфигурацию из config.json"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                debug_logger.debug(f"🔧 Загружена текущая конфигурация")
                return config
            else:
                debug_logger.warning("⚠️ Файл config.json не найден")
                return {}
        except Exception as e:
            debug_logger.error(f"❌ Ошибка загрузки config.json: {e}")
            return {}
    
    def create_env_file(self, user_id: str = "", jwt_token: str = "") -> bool:
        """
        Создает или обновляет .env файл с указанными токенами
        
        Args:
            user_id: ID пользователя
            jwt_token: JWT токен
            
        Returns:
            True если файл успешно создан/обновлен
        """
        try:
            debug_logger.info("📝 Создаем/обновляем .env файл")
            debug_logger.debug(f"👤 User ID: {user_id}")
            debug_logger.debug(f"🔑 JWT Token: {'***' if jwt_token else 'пустой'}")
            
            # Создаем содержимое .env файла
            env_content = f"""# API Configuration - автоматически обновляется из PyQt
# Последнее обновление: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

EMD_API={self.base_env_structure['EMD_API']}
EMD_SPACE={self.base_env_structure['EMD_SPACE']}
EMD_HEADER_TOKEN={self.base_env_structure['EMD_HEADER_TOKEN']}
EMD_TOKEN={jwt_token}
EMD_USER_ID={user_id}

# Other settings
DAYS_GONE_FOR_START_SITES={self.base_env_structure['DAYS_GONE_FOR_START_SITES']}
"""
            
            # Записываем файл
            with open(self.env_file, 'w', encoding='utf-8') as f:
                f.write(env_content)
            
            debug_logger.success("✅ Файл .env успешно обновлен")
            return True
            
        except Exception as e:
            debug_logger.error(f"❌ Ошибка создания .env файла: {e}")
            return False
    
    def update_env_from_template(self, template_name: str) -> bool:
        """
        Обновляет .env файл токенами из указанного шаблона
        
        Args:
            template_name: Имя шаблона из templates.json
            
        Returns:
            True если успешно обновлен
        """
        debug_logger.info(f"🔄 Обновляем .env из шаблона: {template_name}")
        
        templates = self.load_templates()
        
        if template_name not in templates:
            debug_logger.error(f"❌ Шаблон '{template_name}' не найден")
            return False
        
        template_data = templates[template_name]
        user_id = template_data.get('user_id', '')
        jwt_token = template_data.get('jwt', '')
        
        debug_logger.info(f"📊 Данные шаблона: user_id={user_id}")
        
        return self.create_env_file(user_id, jwt_token)
    
    def update_env_from_current_config(self) -> bool:
        """
        Обновляет .env файл из текущей конфигурации (config.json)
        
        Returns:
            True если успешно обновлен
        """
        debug_logger.info("🔄 Обновляем .env из текущей конфигурации")
        
        config = self.load_current_config()
        
        if not config:
            debug_logger.warning("⚠️ Конфигурация пуста, создаем .env с пустыми токенами")
            return self.create_env_file()
        
        user_id = config.get('user_id', '')
        jwt_token = config.get('jwt', '')
        
        debug_logger.info(f"📊 Данные конфигурации: user_id={user_id}")
        
        return self.create_env_file(user_id, jwt_token)
    
    def save_last_selected_template(self, template_name: str) -> bool:
        """
        Сохраняет данные выбранного шаблона в config.json
        КОПИРУЕТ user_id и jwt из templates.json в config.json
        
        Args:
            template_name: Имя выбранного шаблона
            
        Returns:
            True если успешно сохранен
        """
        try:
            debug_logger.info(f"💾 Сохраняем данные шаблона '{template_name}' в config.json")
            
            # Загружаем данные шаблона из templates.json
            templates = self.load_templates()
            if template_name not in templates:
                debug_logger.error(f"❌ Шаблон '{template_name}' не найден")
                return False
            
            template_data = templates[template_name]
            user_id = template_data.get('user_id', '')
            jwt_token = template_data.get('jwt', '')
            
            debug_logger.info(f"📊 Копируем данные: user_id={user_id}")
            
            # Загружаем текущую конфигурацию
            config = self.load_current_config()
            
            # Обновляем ВСЕ поля в config.json
            config['user_id'] = user_id                    # НОВОЕ: копируем данные
            config['jwt'] = jwt_token                      # НОВОЕ: копируем данные  
            config['last_selected_template'] = template_name
            config['last_updated'] = datetime.now().isoformat()
            
            # Сохраняем обновленную конфигурацию
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            
            debug_logger.success("✅ Данные шаблона сохранены в config.json")
            return True
            
        except Exception as e:
            debug_logger.error(f"❌ Ошибка сохранения данных шаблона: {e}")
            return False
    
    def get_last_selected_template(self) -> Optional[str]:
        """
        Получает имя последнего выбранного шаблона
        
        Returns:
            Имя последнего шаблона или None
        """
        config = self.load_current_config()
        last_template = config.get('last_selected_template')
        
        debug_logger.debug(f"📋 Последний выбранный шаблон: {last_template}")
        return last_template
    
    def initialize_env_with_last_template(self) -> bool:
        """
        Инициализирует .env файл с данными из config.json
        ВСЕГДА использует данные из config.json (новая логика)
        
        Returns:
            True если успешно инициализирован
        """
        debug_logger.info("🚀 Инициализация .env файла из config.json")
        
        config = self.load_current_config()
        
        if not config:
            debug_logger.warning("⚠️ config.json не найден, создаем пустой .env")
            return self.create_env_file()
        
        user_id = config.get('user_id', '')
        jwt_token = config.get('jwt', '')
        last_template = config.get('last_selected_template', '')
        
        debug_logger.info(f"📊 Загружаем из config.json: user_id={user_id}, шаблон={last_template}")
        
        return self.create_env_file(user_id, jwt_token)
    
    def initialize_env_on_startup(self) -> bool:
        """
        Инициализирует .env файл при запуске приложения
        ВСЕГДА использует данные из config.json
        
        Returns:
            True если успешно инициализирован
        """
        debug_logger.info("🚀 Инициализация .env файла при запуске")
        
        config = self.load_current_config()
        
        if not config:
            debug_logger.warning("⚠️ config.json не найден, создаем пустой .env")
            return self.create_env_file()
        
        user_id = config.get('user_id', '')
        jwt_token = config.get('jwt', '')
        
        debug_logger.info(f"📊 Загружаем из config.json: user_id={user_id}")
        
        return self.create_env_file(user_id, jwt_token)
    
    def get_available_templates(self) -> list:
        """
        Получает список доступных шаблонов
        
        Returns:
            Список названий шаблонов
        """
        templates = self.load_templates()
        template_names = list(templates.keys())
        debug_logger.debug(f"📋 Доступные шаблоны: {template_names}")
        return template_names
    
    def get_env_status(self) -> Dict:
        """
        Получает статус .env файла
        
        Returns:
            Словарь с информацией о состоянии .env файла
        """
        status = {
            "exists": self.env_file.exists(),
            "path": str(self.env_file),
            "templates_count": len(self.load_templates()),
            "has_config": self.config_file.exists()
        }
        
        debug_logger.debug(f"📊 Статус .env: {status}")
        return status

# Глобальный экземпляр менеджера
env_manager = EnvManager() 