#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Пакет страниц приложения Silk Loader

Содержит классы для всех страниц приложения:
- UploadPage: страница загрузки файлов
- AnalyticsPage: страница аналитики
- HelpPage: страница помощи
- SettingsPage: страница настроек
"""

from .base_page import BasePage
from .upload_page import UploadPage
from .analytics_page import AnalyticsPage
from .help_page import HelpPage
from .settings_page import SettingsPage

__all__ = [
    'BasePage',
    'UploadPage', 
    'AnalyticsPage', 
    'HelpPage', 
    'SettingsPage'
] 