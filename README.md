# GoSilk Staff - PyQt6 Desktop Application

Десктопное приложение для управления релизами на платформе EMD с интеграцией TypeScript скриптов.

## 🛠️ Системные требования

**⚠️ Установите ДО запуска проекта:**

### 🐍 Python 3.8+
**Windows:**
1. Скачайте с https://python.org/downloads/
2. ⚠️ **Обязательно** отметьте "Add Python to PATH" при установке
3. Проверьте: `py --version` в cmd/PowerShell

**macOS:**
```bash
# Через Homebrew (рекомендуется):
brew install python3

# Или скачайте с https://python.org/downloads/
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install python3 python3-pip
```

### 📦 Node.js 16+ 
**Все ОС:**
1. Скачайте **LTS версию** с https://nodejs.org/
2. Установите (npm включен автоматически)
3. Проверьте: `node --version` и `npm --version`

### ✅ Проверка готовности:
```bash
# Должны работать все команды:
py --version          # или python3 --version
node --version  
npm --version
```

## ⚡ Быстрый старт

**Все команды выполняются из корня проекта (папка `silk/`):**

1. **Установите зависимости:** `py setup_dependencies.py` (выберите пункт 2)
2. **Запустите приложение:** `py run_app.py`

## 🚀 Установка зависимостей

### 🎯 Автоматическая установка (Рекомендуется)

**Выполните из корня проекта (папка `silk/`):**

```bash
# Windows
py setup_dependencies.py

# macOS/Linux  
python3 setup_dependencies.py
```

В меню выберите:
- **1** - Проверить зависимости (диагностика)
- **2** - Установить зависимости (автоматическая установка всего)

### 📋 Что устанавливается автоматически

**Python зависимости:**
- PyQt6 - GUI приложение
- loguru - Логирование 
- pandas - Обработка данных
- openpyxl - Работа с Excel

**Node.js зависимости:**
- typescript, ts-node - TypeScript поддержка
- axios - HTTP запросы к API
- dotenv - Переменные окружения
- И другие из package.json

### 🔧 Ручная установка (если нужно)

**Выполните из корня проекта (папка `silk/`):**

```bash
# Python зависимости
pip install -r requirements.txt
pip install -r scripts/requirements.txt

# Node.js зависимости
npm install
# или
yarn install
```

## 🎯 Запуск приложения

**Все команды выполняются из корня проекта (папка `silk/`):**

### Основное PyQt6 приложение:
```bash
py run_app.py
```

### Прямой запуск TypeScript скриптов:

#### Обновление статусов релизов:
```bash
npm run start:update-releases-shipment-statuses
# или
yarn start:update-releases-shipment-statuses
```
*Переключает статусы релизов с 'new' на 'moderation' для отгрузки на FTP партнера*

#### Загрузка релизов:
```bash
npm run start:release-parser-5  
# или
yarn start:release-parser-5
```
*Парсит релизы из папки и загружает их в EMD Cloud с метаданными*

#### Сверка файлов:
```bash
py compare_files.py
```
*Сверяет названия файлов с таблицей релизов*

### 📂 Размещение файлов для обработки:

- **Таблица релизов:** `src/apps/release-parser-5/files/releases.xlsx`
- **Аудио файлы для загрузки:** Укажите путь в таблице релизов
- **Переменные окружения:** `.env` в корне проекта

## 📁 Структура проекта

```
silk/
├── setup/                       # 🔧 Система установки зависимостей
│   ├── main.py                  # Главное меню установки
│   ├── main.bat                 # Windows launcher
│   ├── main.sh                  # Linux/macOS launcher
│   ├── install.py               # Установочный скрипт
│   ├── check_dependencies.py    # Проверка зависимостей
│   └── README.md                # Документация установки
├── pyqt_app/                    # PyQt6 приложение
│   ├── workers/                 # Асинхронные воркеры
│   ├── dialogs/                 # Диалоги прогресса
│   ├── pages/                   # Страницы приложения
│   └── script_manager.py        # Менеджер TypeScript скриптов
├── src/apps/                    # TypeScript скрипты
│   ├── release-parser-5/        # Загрузка релизов
│   └── update-releases-shipment-statuses/  # Обновление статусов
├── setup_dependencies.py        # 🚀 Launcher системы установки
├── run_app.py                   # Запуск PyQt приложения
└── requirements.txt             # Python зависимости
```

## 🔧 Конфигурация

### Переменные окружения (.env):

**🚀 Автоматическое создание и настройка:**
- При **первом запуске** приложения файл `.env` создается автоматически в корне проекта
- Приложение **само заполняет** файл нужными данными
- ✅ **Если приложение запускалось хотя бы раз - настройка уже готова!**

**🔧 Ручное создание (только если нужно ДО первого запуска):**

Создайте файл `silk/.env` с содержимом:
```env
# EMD Platform API Configuration
EMD_API=https://api.emd.one/api              # URL API EMD платформы
EMD_SPACE=silk                               # Название workspace в EMD
EMD_HEADER_TOKEN=token                       # Заголовок токена для авторизации
EMD_TOKEN=                                   # JWT токен доступа к API
EMD_USER_ID=                                 # ID пользователя в системе EMD

# Application Settings
DAYS_GONE_FOR_START_SITES=14                 # Количество дней для запуска сайтов
```

**📝 Когда нужно редактировать:**
- Нужно переключиться на другой workspace
- Приложение еще ни разу не запускалось

### Путь к таблице релизов:
**Поместите файл Excel в:**
```
к таблице: silk/src/apps/release-parser-5/files/releases.xlsx
к файлам: silk/src/apps/release-parser-5/files
```


## 🛠️ Технологии

- **Frontend:** PyQt6, QThread
- **Backend:** TypeScript, Node.js  
- **API:** EMD Platform REST API
- **Логирование:** loguru
- **Системы:** Windows, macOS, Linux

## 📋 Функциональность

### PyQt6 приложение:
- ✅ Асинхронная загрузка релизов
- ✅ Обновление статусов релизов  
- ✅ Real-time прогресс операций
- ✅ Обработка ошибок и уведомления
- ✅ Интуитивный пользовательский интерфейс

### TypeScript скрипты:
- ✅ Парсинг аудио файлов (MP3, WAV, FLAC)
- ✅ Извлечение метаданных
- ✅ Интеграция с EMD API
- ✅ Создание резервных копий
- ✅ Детальное логирование

## 🔍 Проверка установки

**Для диагностики проблем с зависимостями выполните из корня проекта (папка `silk`):**

```bash
py setup_dependencies.py
```
*Выберите пункт 1 - "Проверить зависимости" для получения подробного отчета*

---

*Обновлено: 19 декабря 2024*
