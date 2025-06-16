# 📁 Какие пути тестируются в Complete Pipeline

## 🔍 Автоматически определяемые пути (через `resource_utils.py`):

### 📊 **Development Mode** (как на Windows при разработке):
```python
# Эти пути тестируются в pipeline (он запускается в dev mode):
is_app_bundle() = False  # ❌ не app bundle

get_app_data_dir() = 
  /Users/runner/work/silk/silk/pyqt_app/data/

get_logs_dir() = 
  /Users/runner/work/silk/silk/pyqt_app/logs/

get_resource_path("test.txt") = 
  /Users/runner/work/silk/silk/test.txt

get_env_file_path() = 
  /Users/runner/work/silk/silk/.env
```

### 🏗️ **App Bundle Mode** (НЕ тестируется, но код есть):
```python
# Эти пути НЕ тестируются в pipeline:
is_app_bundle() = True  # ✅ app bundle

get_app_data_dir() = 
  ~/.gosilk_staff/

get_logs_dir() = 
  ~/Library/Logs/GoSilk Staff/

get_resource_path("test.txt") = 
  GoSilk Staff.app/Contents/Resources/test.txt

get_env_file_path() = 
  ~/.gosilk_staff/.env
```

## 📂 Статичные пути которые проверяются:

### ✅ **Проектные директории:**
- `run_app.py` - главный файл
- `pyqt_app/__init__.py` - Python модуль
- `macos_build/__init__.py` - macOS модуль
- `requirements.txt` - Python зависимости
- `package.json` - Node.js конфигурация

### ✅ **Python компоненты:**
- `pyqt_app/requirements.txt` - дополнительные зависимости
- `pyqt_app/resources/icon.icns` - иконка приложения
- `pyqt_app/resources/` - папка ресурсов
- `pyqt_app/data/` - папка данных (создается при тестах)
- `pyqt_app/logs/` - папка логов (создается при тестах)

### ✅ **Scripts и TypeScript:**
- `scripts/*.py` - все Python скрипты
- `scripts/requirements.txt` - зависимости скриптов
- `src/apps/*/` - TypeScript приложения
- `src/apps/*/index.ts` - точки входа приложений
- `tsconfig.json` - TypeScript конфигурация

### ✅ **Сборка:**
- `macos_build/gosilk_staff.spec` - PyInstaller спецификация
- `dist/` - результаты сборки
- `dist/*.app` - собранное приложение
- `dist/*.dmg` - установочный файл

## ⚠️ **Пути которые НЕ тестируются:**

### ❌ **Windows специфичные:**
```python
# Этот код существует, но НЕ выполняется:
if platform.system() == 'Windows':
    # Windows пути с обратными слешами \
    # Windows команды (py вместо python3)
    # Windows логика в setup/ модулях
```

### ❌ **App Bundle пути:**
- `~/.gosilk_staff/` - пользовательские данные в app bundle mode
- `~/Library/Logs/GoSilk Staff/` - логи в app bundle mode  
- `.app/Contents/Resources/` - ресурсы внутри bundle
- `.app/Contents/MacOS/` - исполняемые файлы

## 🧪 Что тестируется в каждой директории:

### 📁 **pyqt_app/data/** (создается и проверяется):
- Создание директории
- Права доступа
- Возможность записи

### 📁 **pyqt_app/logs/** (создается и проверяется):
- Создание директории с подпапками
- Права доступа
- Возможность записи

### 📁 **pyqt_app/resources/**:
- Существование иконки (`icon.icns`)
- Размер файлов
- Формат иконки
- Количество ресурсов

### 📁 **scripts/**:
- Синтаксис всех `.py` файлов
- Реальное выполнение скриптов
- Импорты и зависимости
- Функциональные тесты (для `compare_files.py`)

### 📁 **src/apps/**:
- Существование TypeScript приложений
- Компиляция `.ts` файлов
- Соответствие `package.json` и файловой системы
- Структура каждого приложения

## 💡 **Выводы:**

### ✅ **Хорошо протестировано:**
- **Development mode пути** (как на Windows при разработке)
- **Создание и доступ к директориям**
- **Работа с ресурсами и файлами**
- **Выполнение скриптов**

### ❌ **НЕ протестировано:**
- **App bundle пути** (реальное поведение в .app)
- **Windows специфичные пути**
- **Кроссплатформенные различия**
- **Поведение на Windows**

**Итог:** Pipeline тестирует пути в development mode на macOS, что примерно соответствует Windows разработке, но НЕ тестирует финальные app bundle пути и Windows специфику. 