# 📋 Подробный план разработки GoSilk Staff

## 🎯 Приоритет 1 - Критически важные задачи

### 1️⃣ **Авторизация**

#### **Задача:**
Реализовать единое окно авторизации с паролем, которое появляется до открытия основного интерфейса.

#### **Реализация:**

**Файлы для создания:**
- `silk/pyqt_app/dialogs/auth_dialog.py` - Новый диалог авторизации
- `silk/pyqt_app/auth_manager.py` - Менеджер авторизации

**Файлы для изменения:**
- `silk/pyqt_app/main.py` - MainWindow класс
  - **Функция:** `__init__()` - добавить проверку авторизации перед показом окна
  - **Почему:** Нужно показывать диалог авторизации до создания основного интерфейса

- `silk/run_app.py` - Точка входа приложения
  - **Функция:** `if __name__ == "__main__":` блок
  - **Почему:** Здесь происходит инициализация приложения, нужно добавить логику авторизации

**Структура реализации:**
```python
# auth_dialog.py
class AuthDialog(QDialog):
    def __init__(self):
        # Создать форму с полем пароля
        # Добавить кнопки "Войти" и "Отмена"
    
    def check_password(self, password: str) -> bool:
        # Проверка пароля (пока статичный)
        return password == "silk2024"

# auth_manager.py  
class AuthManager:
    def is_authenticated(self) -> bool:
        # Проверка состояния авторизации
    
    def authenticate(self) -> bool:
        # Показ диалога и процесс авторизации
```

---

### 2️⃣ **Иконка приложения**

#### **Задача:**
Добавить иконку приложения в заголовок окна и панель задач.

#### **Реализация:**

**Файлы для создания:**
- `silk/pyqt_app/resources/app_icon.ico` - Файл иконки приложения
- `silk/pyqt_app/resources/app_icon.png` - PNG версия иконки

**Файлы для изменения:**
- `silk/pyqt_app/main.py` - MainWindow класс
  - **Функция:** `__init__()` - добавить `self.setWindowIcon(QIcon("path/to/icon"))`
  - **Почему:** setWindowIcon устанавливает иконку для окна и панели задач

- `silk/pyqt_app/resources/icons.py` - Существующий файл иконок
  - **Функция:** Добавить `get_app_icon()` функцию
  - **Почему:** Централизованное управление иконками уже есть в проекте

**Структура реализации:**
```python
# В main.py __init__():
from pyqt_app.resources.icons import get_app_icon
self.setWindowIcon(get_app_icon())

# В icons.py:
def get_app_icon():
    return QIcon("pyqt_app/resources/app_icon.ico")
```

---

### 3️⃣ **Переименование кнопки**

#### **Задача:**
Изменить название кнопки "ОБНОВИТЬ СТАТУСЫ" на "ОТПРАВИТЬ НА FTP".

#### **Реализация:**

**Файлы для изменения:**
- `silk/pyqt_app/pages/upload_page.py` - UploadPage класс
  - **Строка:** 515 `update_status_button = QPushButton("ОБНОВИТЬ СТАТУСЫ")`
  - **Функция:** `setup_ui()` метод
  - **Почему:** Здесь создается кнопка обновления статусов

**Структура реализации:**
```python
# Изменить строку 515:
update_status_button = QPushButton("ОТПРАВИТЬ НА FTP")
```

---

## 🎯 Приоритет 2 - Функциональные улучшения

### 4️⃣ **Состояние кнопки загрузки**

#### **Задача:**
Реализовать логику: кнопка неактивна (серая) по умолчанию, активируется (зеленая) только после успешной проверки файлов.

#### **Реализация:**

**Файлы для изменения:**
- `silk/pyqt_app/pages/upload_page.py` - UploadPage класс
  - **Функция:** `setup_ui()` - изменить стили кнопки загрузки
  - **Функция:** `check_files()` (строка 831) - добавить активацию кнопки при успехе
  - **Функция:** `show_status()` (строка 714) - добавить логику состояния кнопки
  - **Почему:** Нужно связать результат проверки файлов с состоянием кнопки

**Структура реализации:**
```python
# В setup_ui() добавить состояние кнопки:
self.upload_button = upload_button
self.upload_button.setEnabled(False)  # По умолчанию неактивна

# В check_files() добавить:
if result['status'] == 'success':
    self.enable_upload_button()
else:
    self.disable_upload_button()

# Новые методы:
def enable_upload_button(self):
    self.upload_button.setEnabled(True)
    # Зеленый стиль

def disable_upload_button(self):
    self.upload_button.setEnabled(False)  
    # Серый стиль
```

---

### 5️⃣ **Кнопка "Продолжить загрузку"**

#### **Задача:**
Реализовать функционал: по умолчанию кнопка скрыта, появляется только если загрузка была прервана.

#### **Реализация:**

**Файлы для изменения:**
- `silk/pyqt_app/pages/upload_page.py` - UploadPage класс
  - **Функция:** `setup_ui()` - скрыть кнопку по умолчанию
  - **Функция:** `on_upload_finished()` (строка 1205) - логика показа кнопки при прерывании
  - **Почему:** Нужно проверять статус завершения загрузки

- `silk/pyqt_app/session_data_manager.py` - SessionDataManager класс
  - **Функция:** Добавить `has_interrupted_upload()` метод
  - **Функция:** Добавить `save_upload_state()` метод
  - **Почему:** Нужно отслеживать состояние загрузки между сессиями

**Структура реализации:**
```python
# В setup_ui() добавить:
self.continue_button = continue_button
self.continue_button.setVisible(False)  # Скрыта по умолчанию

# В on_upload_finished():
if not success and "interrupted" in message.lower():
    self.continue_button.setVisible(True)
    session_manager.save_upload_state(interrupted=True)

# В session_data_manager.py:
def has_interrupted_upload(self) -> bool:
    return self.session_data.get('upload_interrupted', False)
```

---

### 6️⃣ **Проверка файлов и обработка ошибок**

#### **Задача:**
Добавить возможность сохранения отчета при ошибках релиза и показывать точное местоположение ошибки в файле.

#### **Реализация:**

**Файлы для изменения:**
- `silk/pyqt_app/pages/upload_page.py` - UploadPage класс
  - **Функция:** `check_files()` (строка 831) - улучшить обработку ошибок
  - **Функция:** `offer_save_results_file()` (строка 1241) - расширить функционал
  - **Почему:** Здесь происходит проверка файлов и предложение сохранения

- `silk/scripts/compare_files.py` - Скрипт сравнения файлов
  - **Функция:** Основная логика сравнения - добавить детализацию ошибок
  - **Почему:** Этот скрипт генерирует отчет о проверке файлов

**Файлы для создания:**
- `silk/pyqt_app/dialogs/error_detail_dialog.py` - Диалог с детализацией ошибок

**Структура реализации:**
```python
# В check_files() добавить:
if result['status'] == 'error' and 'errors' in result:
    self.show_error_details(result['errors'])
    self.offer_error_report_save(result)

# Новые методы:
def show_error_details(self, errors: list):
    # Показать диалог с детализацией ошибок
    dialog = ErrorDetailDialog(errors)
    dialog.exec()

def offer_error_report_save(self, result: dict):
    # Предложить сохранить отчет об ошибках
```

---

### 7️⃣ **Настройка отправки**

#### **Задача:**
Добавить функционал выбора направления отправки (Zvonko или 1RPM).

#### **Реализация:**

**Файлы для изменения:**
- `silk/pyqt_app/pages/settings_page.py` - SettingsPage класс
  - **Функция:** `setup_ui()` - добавить радиокнопки выбора
  - **Функция:** `save_settings()` - сохранить выбор направления
  - **Почему:** Настройки логически должны быть на странице настроек

- `silk/pyqt_app/env_manager.py` - EnvManager класс
  - **Функция:** Добавить `get_upload_destination()` и `set_upload_destination()`
  - **Почему:** Направление отправки - это настройка окружения

**Структура реализации:**
```python
# В settings_page.py добавить:
# Группа радиокнопок
destination_group = QButtonGroup()
self.zvonko_radio = QRadioButton("Zvonko")
self.rpm_radio = QRadioButton("1RPM")
destination_group.addButton(self.zvonko_radio)
destination_group.addButton(self.rpm_radio)

# В env_manager.py:
def get_upload_destination(self) -> str:
    return self.config_data.get('upload_destination', 'zvonko')

def set_upload_destination(self, destination: str):
    self.config_data['upload_destination'] = destination
    self.save_config()
```

---

## 🎯 Приоритет 3 - Улучшения UI/UX

### 8️⃣ **Исправление шрифтов**

#### **Задача:**
Унифицировать шрифты в интерфейсе, заменить inline CSS на централизованные стили.

#### **Реализация:**

**Файлы для создания:**
- `silk/pyqt_app/styles/fonts.py` - Централизованные стили шрифтов
- `silk/pyqt_app/styles/theme.py` - Система тем

**Файлы для изменения:**
- `silk/pyqt_app/pages/upload_page.py` - множественные строки с font-size
  - **Строки:** 108, 127, 133, 153, 180, 196, 202, 222, 265, 307, 338, 344, 364, 391, 402, 408, 428, 476, 499, 522, 561, 571, 585, 612, 616, 735, 749, 763, 777, 791
  - **Почему:** Везде используются inline стили font-size

- `silk/pyqt_app/pages/settings_page.py` - строки с font-size
  - **Строки:** 96, 97, 121, 190, 191, 217, 238, 265, 309, 336
  - **Почему:** Inline стили нужно заменить на централизованные

- `silk/pyqt_app/pages/help_page.py` - строки с font-size
- `silk/pyqt_app/pages/analytics_page.py` - строки с font-size

**Структура реализации:**
```python
# fonts.py
class FontStyles:
    TITLE = QFont("Arial", 18, QFont.Weight.Bold)
    SUBTITLE = QFont("Arial", 14, QFont.Weight.Bold)
    BODY = QFont("Arial", 12)
    SMALL = QFont("Arial", 10)

# В каждой странице заменить:
# Было: setStyleSheet("font-size: 18px; font-weight: bold;")
# Стало: setFont(FontStyles.TITLE)
```

---

### 9️⃣ **Базовая поддержка тем**

#### **Задача:**
Создать систему переключения между светлой и темной темой.

#### **Реализация:**

**Файлы для создания:**
- `silk/pyqt_app/styles/themes.py` - Определение тем
- `silk/pyqt_app/theme_manager.py` - Менеджер тем

**Файлы для изменения:**
- `silk/pyqt_app/pages/settings_page.py` - SettingsPage класс
  - **Функция:** `setup_ui()` - добавить переключатель темы
  - **Почему:** Настройка темы логически должна быть в настройках

- `silk/pyqt_app/main.py` - MainWindow класс  
  - **Функция:** `__init__()` - инициализация менеджера тем
  - **Почему:** Главное окно должно управлять применением темы

**Структура реализации:**
```python
# themes.py
class LightTheme:
    BACKGROUND = "#ffffff"
    TEXT = "#333333"
    BUTTON = "#19c790"
    
class DarkTheme:
    BACKGROUND = "#2b2b2b"
    TEXT = "#ffffff" 
    BUTTON = "#17b683"

# theme_manager.py
class ThemeManager:
    def apply_theme(self, theme_name: str):
        # Применить тему ко всему приложению
```

---

### 🔟 **Финальный отчет с пользователем**

#### **Задача:**
Добавить тег пользователя в финальные отчеты приложения.

#### **Реализация:**

**Файлы для изменения:**
- `silk/pyqt_app/env_manager.py` - EnvManager класс
  - **Функция:** Добавить `get_current_user()` метод
  - **Почему:** Информация о пользователе хранится в переменных окружения

- `silk/pyqt_app/pages/upload_page.py` - UploadPage класс
  - **Функция:** `offer_save_results_file()` (строка 1241) - добавить пользователя в отчет
  - **Почему:** Здесь генерируются отчеты о загрузке

- `silk/pyqt_app/pages/analytics_page.py` - AnalyticsPage класс
  - **Функция:** Методы генерации отчетов - добавить информацию о пользователе
  - **Почему:** На странице аналитики тоже создаются отчеты

**Структура реализации:**
```python
# В env_manager.py:
def get_current_user(self) -> str:
    return self.config_data.get('current_user', 'Unknown User')

# В отчетах добавить:
report_header = f"Отчет создан: {datetime.now()}\nПользователь: {env_manager.get_current_user()}\n"
```

---

## 🎯 Приоритет 4 - Дополнительные улучшения

### 1️⃣1️⃣ **Адаптивный дизайн**

#### **Задача:**
Обеспечить адаптивность интерфейса под разные разрешения экрана.

#### **Реализация:**

**Файлы для изменения:**
- `silk/pyqt_app/main.py` - MainWindow класс
  - **Функция:** `__init__()` - установить минимальные размеры окна
  - **Функция:** Добавить `resizeEvent()` - обработчик изменения размера
  - **Почему:** Главное окно контролирует размеры всего приложения

- Все файлы страниц в `silk/pyqt_app/pages/`
  - **Функция:** `setup_ui()` - использовать responsive layouts
  - **Почему:** Каждая страница должна адаптироваться к размеру

**Структура реализации:**
```python
# В main.py:
self.setMinimumSize(800, 600)
self.resize(1200, 800)

def resizeEvent(self, event):
    # Адаптация компонентов под новый размер
    super().resizeEvent(event)
```

---

### 1️⃣2️⃣ **Общие улучшения дизайна**

#### **Задача:**
Улучшить общий дизайн интерфейса: единый стиль кнопок, отступы, hover-эффекты.

#### **Реализация:**

**Файлы для создания:**
- `silk/pyqt_app/styles/components.py` - Стили компонентов
- `silk/pyqt_app/styles/layout.py` - Стили макетов

**Файлы для изменения:**
- Все файлы страниц - унификация стилей кнопок и контейнеров
- `silk/pyqt_app/components.py` - TabBar класс
  - **Функция:** Стили вкладок - улучшить hover-эффекты
  - **Почему:** Панель вкладок - ключевой элемент навигации

**Структура реализации:**
```python
# components.py
class ButtonStyles:
    PRIMARY = """
        QPushButton {
            background-color: #19c790;
            border-radius: 15px;
            padding: 15px 25px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #17b683;
            transform: translateY(-2px);
        }
    """
```

---

## 📅 Рекомендуемый порядок выполнения

1. **Приоритет 1** (2-3 часа): Авторизация → Иконка → Переименование кнопки
2. **Приоритет 2** (3-4 часа): Состояние кнопок → Проверка файлов → Настройки
3. **Приоритет 3** (2-3 часа): Шрифты → Темы → Отчеты
4. **Приоритет 4** (1-2 часа): Адаптивность → Дизайн

## 🔗 Полезные ссылки на файлы

- [Главное окно](silk/pyqt_app/main.py) - Точка входа интерфейса
- [Страница загрузки](silk/pyqt_app/pages/upload_page.py) - Основная функциональность
- [Страница настроек](silk/pyqt_app/pages/settings_page.py) - Конфигурация
- [Менеджер окружения](silk/pyqt_app/env_manager.py) - Настройки приложения
- [Менеджер сессий](silk/pyqt_app/session_data_manager.py) - Состояние приложения
- [Компоненты](silk/pyqt_app/components.py) - UI компоненты
- [Иконки](silk/pyqt_app/resources/icons.py) - Ресурсы иконок 