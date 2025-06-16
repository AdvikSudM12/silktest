
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

```

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

7️⃣ Настройка отправки
Задача:
Добавить функционал выбора направления отправки (Zvonko или 1RPM).

Реализация:
Файлы для изменения:

silk/pyqt_app/pages/settings_page.py - SettingsPage класс

Функция: setup_ui() - добавить радиокнопки выбора
Функция: save_settings() - сохранить выбор направления
Почему: Настройки логически должны быть на странице настроек
silk/pyqt_app/env_manager.py - EnvManager класс

Функция: Добавить get_upload_destination() и set_upload_destination()
Почему: Направление отправки - это настройка окружения
Структура реализации:

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