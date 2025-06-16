# 🎵 GoSilk Staff - Система управления музыкальными релизами

> **Гибридное приложение для автоматизации процессов управления релизами на платформе EMD**

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Node.js](https://img.shields.io/badge/node-16+-green.svg)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-orange.svg)
![TypeScript](https://img.shields.io/badge/backend-TypeScript-blue.svg)

---

## 📖 Описание проекта

**GoSilk Staff** - это профессиональное решение для управления музыкальными релизами, разработанное для команды EMD. Приложение предоставляет удобный графический интерфейс для автоматизации процессов проверки, загрузки и мониторинга релизов.

### 🎯 Основные возможности

- **📁 Проверка файлов релизов** - автоматическое сравнение Excel файлов с содержимым папок
- **📊 Аналитика и отчетность** - детальные отчеты о состоянии релизов
- **🚀 Загрузка релизов** - интеграция с EMD API для автоматической загрузки
- **⚙️ Управление настройками** - гибкая конфигурация API токенов и параметров
- **🔄 Обновление статусов** - автоматическое обновление статусов релизов
- **🔐 Система авторизации** - защищенный доступ к функциональности

### 🏗️ Архитектура

Проект построен на **гибридной архитектуре**:
- **Frontend:** PyQt6 (Python) - современный графический интерфейс
- **Backend:** TypeScript/Node.js - серверная логика и API интеграция  
- **Утилиты:** Python скрипты - обработка файлов и данных

---

## 📂 Структура проекта

```
gosilk-staff/
├── 📁 pyqt_app/                    # GUI приложение (PyQt6)
│   ├── 📁 components/              # Компоненты интерфейса
│   ├── 📁 pages/                   # Страницы приложения
│   │   ├── upload_page.py          # Страница загрузки файлов
│   │   ├── analytics_page.py       # Страница аналитики
│   │   ├── settings_page.py        # Страница настроек
│   │   └── help_page.py           # Страница помощи
│   ├── 📁 dialogs/                # Диалоговые окна
│   ├── 📁 workers/                # Фоновые задачи
│   ├── 📁 resources/              # Ресурсы (иконки, стили)
│   ├── 📁 data/                   # Пользовательские данные
│   ├── main.py                    # Главное окно приложения
│   ├── env_manager.py             # Менеджер конфигурации
│   ├── session_data_manager.py    # Менеджер сессионных данных
│   └── script_manager.py          # Интеграция с TypeScript
├── 📁 src/                        # TypeScript backend
│   └── 📁 apps/                   # Приложения backend
│       ├── release-parser-5/      # Парсер релизов (этап 5)
│       ├── update-releases-shipment-statuses/  # Обновление статусов
│       └── ...                    # Другие микросервисы
├── 📁 scripts/                    # Python утилиты
│   ├── excel_operations.py        # Операции с Excel файлами
│   ├── compare_files.py          # Сравнение файлов
│   └── requirements.txt          # Зависимости утилит
├── 📁 macos_build/               # Сборка macOS приложения
│   ├── gosilk_staff.spec         # Конфигурация PyInstaller
│   ├── build_macos.sh            # Скрипт автоматической сборки
│   ├── resource_utils.py         # Утилиты для ресурсов
│   ├── node_runner.py            # Node.js runner для app bundle
│   └── README.md                 # Инструкция по сборке
├── 📁 setup/                     # Установка зависимостей
│   ├── install.py                # Автоматическая установка
│   ├── check_dependencies.py     # Проверка зависимостей
│   └── main.py                   # Главное меню установки
├── run_app.py                    # Точка входа в приложение
├── requirements.txt              # Python зависимости
├── package.json                  # Node.js зависимости
├── tsconfig.json                 # Конфигурация TypeScript
└── README.md                     # Данный файл
```

---

## 🚀 Способы запуска

### 💻 Режим разработки

#### 1️⃣ Автоматическая установка всех зависимостей

**🎯 Самый простой способ - одной командой:**
```bash
python setup_dependencies.py    # Windows: py setup_dependencies.py
```

Этот скрипт автоматически:
- ✅ Установит все Python зависимости (PyQt6, логирование, утилиты)
- ✅ Установит все Node.js зависимости (TypeScript, API клиенты)
- ✅ Проверит корректность установки
- ✅ Создаст подробный отчет о зависимостях

#### 2️⃣ Альтернативные способы

**Через меню setup:**
```bash
# Windows
cd setup/
python main.py    # или py main.py

# Linux/macOS  
cd setup/
./main.sh         # или python3 main.py
```

**Ручная установка (если нужна):**
```bash
# Python зависимости
pip install -r requirements.txt
pip install -r scripts/requirements.txt

# Node.js зависимости
npm install
```

#### 3️⃣ Запуск приложения

**Главное PyQt6 приложение:**
```bash
python run_app.py    # Windows: py run_app.py
```

**Отдельные TypeScript модули:**
```bash
# Парсер релизов (этап 5)  
npm run start:release-parser-5

# Обновление статусов релизов
npm run start:update-releases-shipment-statuses

# Другие модули (см. package.json)
npm run start:parse-users-to-table
```

**Python утилиты:**
```bash
cd scripts/

# Операции с Excel файлами
python excel_operations.py

# Сравнение файлов
python compare_files.py
```

---

### 🍎 Автономное macOS приложение

#### Сборка приложения

```bash
# Клонировать проект
git clone -b macos-build-test https://github.com/AdvikSudM12/silk.git
cd silk

# Автоматическая сборка
chmod +x macos_build/build_macos.sh
./macos_build/build_macos.sh

# Тестирование
open "dist/GoSilk Staff.app"

# Создание DMG для распространения
hdiutil create -volname 'GoSilk Staff' -srcfolder 'dist/GoSilk Staff.app' -ov -format UDZO 'GoSilk Staff v1.0.dmg'
```

#### Особенности автономного приложения

- **📁 Пользовательские данные:** `~/.gosilk_staff/` (настройки, .env, кеш)
- **📊 Логи:** `~/Library/Logs/GoSilk Staff/`
- **🔧 Node.js:** встроенный runtime, не требует системной установки
- **⚙️ Автоматическое определение режима:** app bundle vs разработка

---

## ⚙️ Конфигурация

### 🔑 API настройки

Создайте файл `.env` в корне проекта:

```env
# EMD API конфигурация
EMD_API=https://api.emd.ru
EMD_SPACE=silk
EMD_TOKEN=your_jwt_token_here
EMD_USER_ID=your_user_id_here

# Дополнительные настройки
NODE_ENV=production
DEBUG=false
```

### 📋 Получение токенов

1. **EMD_TOKEN** - JWT токен из личного кабинета EMD
2. **EMD_USER_ID** - ваш ID пользователя в системе EMD

### 🎛️ Управление настройками

Используйте встроенную **страницу "Настройки"** в приложении:
- Создание шаблонов токенов
- Быстрое переключение между аккаунтами
- Автоматическое обновление .env файла

---

## 📋 Системные требования

### Режим разработки
- **Python:** 3.8+
- **Node.js:** 16+
- **ОС:** Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **RAM:** 4GB+ рекомендуется
- **Место на диске:** 2GB+ (включая зависимости)

### macOS app bundle
- **macOS:** 10.14+ (Mojave или новее)
- **Архитектура:** x64 или arm64 (M1/M2)
- **RAM:** 4GB+ рекомендуется
- **Место на диске:** 500MB+ для приложения

---

## 🔧 Основные зависимости

### Python (requirements.txt)
```
PyQt6==6.9.0                # GUI фреймворк
loguru==0.7.2               # Логирование
pandas>=1.5.0               # Обработка данных
openpyxl>=3.0.0            # Работа с Excel
pyinstaller>=5.13.0        # Создание исполняемых файлов
```

### Node.js (package.json)
```json
{
  "axios": "^1.6.8",                    // HTTP клиент
  "dotenv": "^16.4.5",                  // Переменные окружения
  "convert-excel-to-json": "^1.7.0",    // Конвертация Excel
  "tus-js-client": "^4.1.0",           // Загрузка файлов
  "typescript": "^5.7.3"                // TypeScript компилятор
}
```

---

## 🎨 Интерфейс приложения

### 📱 Основные страницы

1. **🚀 ЗАГРУЗКА**
   - Выбор Excel файла и папки с релизами
   - Автоматическая проверка соответствия файлов
   - Загрузка релизов в EMD API

2. **📊 АНАЛИТИКА**
   - Детальная статистика по релизам
   - Отчеты об ошибках и расхождениях
   - Визуализация результатов проверки

3. **❓ ПОМОЩЬ**
   - Подробная инструкция по использованию
   - Требования к файлам
   - Советы по решению проблем

4. **⚙️ НАСТРОЙКИ**
   - Управление API токенами
   - Создание шаблонов конфигурации
   - Настройки приложения

---

## 🐛 Диагностика и решение проблем

### 📊 Логи приложения

**Режим разработки:**
```bash
# Логи находятся в
./pyqt_app/logs/app.log
```

**macOS app bundle:**
```bash
# Логи находятся в
~/Library/Logs/GoSilk\ Staff/app.log

# Просмотр логов в реальном времени
tail -f ~/Library/Logs/GoSilk\ Staff/app.log
```

### ⚠️ Типичные проблемы

1. **Ошибка авторизации API**
   - Проверьте правильность EMD_TOKEN
   - Убедитесь что токен не истек

2. **Проблемы с файлами**
   - Проверьте формат Excel файла
   - Убедитесь в наличии требуемых столбцов

3. **Ошибки Node.js модулей**
   - Переустановите зависимости: `npm install`
   - Проверьте версию Node.js: `node --version`

---

## 👥 Команда разработки

- **Backend TypeScript:** Готовые рабочие модули
- **GUI PyQt6:** Современный интерфейс пользователя  
- **Python утилиты:** Обработка файлов и данных
- **macOS сборка:** Автономное приложение для распространения

---

## 📞 Поддержка

Для получения помощи:

1. **📖 Встроенная справка** - используйте страницу "Помощь" в приложении
2. **📊 Логи** - проверьте файлы логов для диагностики
3. **🔧 Настройки** - используйте страницу "Настройки" для конфигурации

---

## 📄 Лицензия

MIT License - см. файл [LICENSE](LICENSE) для подробностей.

---

## 🎯 Быстрые команды

```bash
# Установка всех зависимостей
python setup_dependencies.py

# Запуск приложения
python run_app.py

# Сборка macOS приложения  
chmod +x macos_build/build_macos.sh && ./macos_build/build_macos.sh

# Проверка зависимостей
cd setup/ && python check_dependencies.py
```

---

**🎵 GoSilk Staff** - Ваш надежный помощник в управлении музыкальными релизами! 