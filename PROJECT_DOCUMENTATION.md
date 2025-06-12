# 📋 GoSilk Staff - Полная документация проекта

## 🎯 Описание проекта

**GoSilk Staff** - это комплексное приложение для автоматизации загрузки и управления музыкальными релизами на платформе EMD. Проект состоит из PyQt6 графического интерфейса и TypeScript backend скриптов для работы с API.

---

## 🏗️ Архитектура проекта

```
GoSilk Staff
├── 🖥️ Frontend (PyQt6)     - Графический интерфейс пользователя
├── 🔧 Backend (TypeScript)  - Скрипты для работы с API
├── 🐍 Scripts (Python)     - Утилиты для обработки данных
└── ⚙️ Configuration        - Настройки и переменные окружения
```

---

## 📁 Структура проекта

```
silk/
├── 📱 pyqt_app/                    # PyQt6 приложение
│   ├── 🏠 main.py                  # Точка входа приложения
│   ├── 📄 pages/                   # Страницы интерфейса
│   │   ├── upload_page.py          # Страница загрузки релизов
│   │   ├── analytics_page.py       # Страница аналитики
│   │   ├── settings_page.py        # Страница настроек
│   │   └── base_page.py           # Базовый класс страниц
│   ├── 🔄 workers/                 # Асинхронные воркеры
│   │   ├── upload_worker.py        # Воркер загрузки релизов
│   │   └── update_status_worker.py # Воркер обновления статусов
│   ├── 💬 dialogs/                 # Диалоговые окна
│   │   ├── upload_progress_dialog.py        # Диалог прогресса загрузки
│   │   └── update_status_progress_dialog.py # Диалог прогресса обновления
│   ├── 🔧 script_manager.py        # Менеджер TypeScript скриптов
│   ├── 📊 session_data_manager.py  # Менеджер сессионных данных
│   ├── 🌍 env_manager.py           # Менеджер переменных окружения
│   ├── 📝 logger_config.py         # Конфигурация логирования
│   └── 📦 data/                    # Данные приложения
│       └── paths.json              # Сохраненные пути
├── 🚀 src/                         # TypeScript backend
│   ├── 📱 apps/                    # Основные приложения
│   │   ├── 📤 release-parser-5/    # Главный парсер релизов
│   │   │   ├── index.ts            # Основной скрипт загрузки
│   │   │   ├── 📁 files/           # Excel файлы и медиа
│   │   │   └── 🛠️ utils/           # Утилиты загрузки
│   │   ├── 🔄 update-releases-shipment-statuses/ # Обновление статусов
│   │   │   ├── index.ts            # Скрипт обновления статусов
│   │   │   └── 📁 files/           # Резервные копии
│   │   └── 🧪 test/                # Тестовые версии скриптов
│   ├── ⚙️ configs/                 # Конфигурационные файлы
│   │   ├── api.ts                  # Настройки API
│   │   ├── countries-codes.ts      # Коды стран
│   │   └── release.ts              # Конфигурация релизов
│   └── 🛠️ tools/                   # Вспомогательные инструменты
│       ├── table.ts                # Работа с таблицами API
│       └── flow.ts                 # Управление потоками
├── 🐍 scripts/                     # Python утилиты
│   ├── compare_files.py            # Сравнение файлов с Excel
│   ├── excel_operations.py         # Операции с Excel файлами
│   └── requirements.txt            # Python зависимости
├── 📋 package.json                 # Node.js зависимости и скрипты
├── 🔧 tsconfig.json               # Конфигурация TypeScript
├── 🌍 .env                        # Переменные окружения
└── 📚 docs/                       # Документация
    └── СКРИПТЫ_И_ЗАВИСИМОСТИ.md  # Описание скриптов
```

---

## 🔧 Технологический стек

### Frontend (PyQt6)
- **PyQt6** - Графический интерфейс
- **loguru** - Логирование
- **QThread** - Асинхронные операции

### Backend (TypeScript/Node.js)
- **TypeScript** - Основной язык backend
- **ts-node** - Выполнение TypeScript
- **axios** - HTTP клиент для API
- **dotenv** - Управление переменными окружения
- **dayjs** - Работа с датами
- **tus-js-client** - Загрузка файлов

### Утилиты (Python)
- **pandas** - Обработка Excel файлов
- **openpyxl** - Работа с Excel
- **pathlib** - Работа с путями

---

## 🌍 Переменные окружения

### Файл `.env`
```env
# API Configuration
EMD_API=https://api.emd.ru
EMD_SPACE=silk
EMD_TOKEN=your_jwt_token_here
EMD_USER_ID=your_user_id_here

# Optional Settings
NODE_ENV=production
DEBUG=false
```

### Описание переменных
- **EMD_API** - URL API платформы EMD
- **EMD_SPACE** - Название пространства (workspace)
- **EMD_TOKEN** - JWT токен для авторизации
- **EMD_USER_ID** - ID пользователя в системе

### Как используются переменные

#### В PyQt приложении:
1. **env_manager.py** - Загружает переменные из .env
2. **script_manager.py** - Передает переменные в subprocess
3. **settings_page.py** - Позволяет редактировать токены

#### В TypeScript скриптах:
1. **dotenv.config()** - Загружает переменные в process.env
2. **src/configs/api.ts** - Использует переменные для настройки API
3. **src/tools/table.ts** - Использует токены для авторизации

---

## 📊 Поток данных

### 1. Загрузка релизов (release-parser-5)
```
Excel файл → PyQt UI → UploadWorker → TypeScript скрипт → EMD API
     ↓
Медиа файлы → Загрузка через tus-js-client → EMD Cloud Storage
     ↓
Метаданные → Создание записей в таблице releases → EMD Database
```

### 2. Обновление статусов (update-releases-shipment-statuses)
```
PyQt UI → UpdateStatusWorker → TypeScript скрипт → EMD API
    ↓
Получение релизов со статусом 'new' → Создание backup.json
    ↓
Обновление shouldUploadReleaseToZvonko: true → Изменение статуса на 'moderation'
```

### 3. Сравнение файлов (compare_files.py)
```
Excel файл + Директория с файлами → Python скрипт → Анализ соответствия
    ↓
Создание отчета с ошибками → Сохранение в Excel → Отображение в PyQt UI
```

---

## 🔄 Асинхронная архитектура

### PyQt6 Threading Model
```
Main UI Thread (PyQt6)
    ├── UploadWorker (QThread)          # Загрузка релизов
    ├── UpdateStatusWorker (QThread)    # Обновление статусов
    └── ComparisonWorker (QThread)      # Сравнение файлов
            ↓
    subprocess.Popen → TypeScript/Python скрипты
            ↓
    Real-time stdout/stderr → UI updates через signals/slots
```

### Сигналы и слоты
- **progress_updated** - Обновление текстового лога
- **progress_percent** - Обновление прогресс-бара (0-100%)
- **stage_changed** - Изменение стадии выполнения
- **finished** - Завершение операции (success/failure)
- **error_occurred** - Обработка ошибок

---

## 🗄️ Управление данными

### Конфигурационные файлы

#### pyqt_app/data/paths.json
```json
{
    "excel_file_path": "C:/path/to/releases.xlsx",
    "directory_path": "C:/path/to/media/files",
    "last_updated": "2024-01-15T10:30:00Z"
}
```

#### src/configs/api.ts
```typescript
export default {
    api_url: process.env.EMD_API,
    space: process.env.EMD_SPACE,
    token: process.env.EMD_TOKEN,
    user_id: process.env.EMD_USER_ID
}
```

### Сессионные данные
- **session_data_manager.py** - Управляет временными данными сессии
- **Хранение результатов** - Результаты операций сохраняются для аналитики
- **Кэширование путей** - Последние выбранные пути сохраняются

---

## 🚀 Скрипты и команды

### NPM Scripts (package.json)
```json
{
    "scripts": {
        "start:release-parser-5": "ts-node ./src/apps/release-parser-5",
        "start:update-releases-shipment-statuses": "ts-node ./src/apps/update-releases-shipment-statuses"
    }
}
```

### Запуск через PyQt
```python
# Команда формируется в script_manager.py
cmd = [npx_path, 'ts-node', 'index.ts']

# Выполняется в рабочей директории скрипта
process = subprocess.Popen(cmd, cwd=script_path, env=env)
```

---

## 🔐 Безопасность

### Токены и авторизация
- **JWT токены** хранятся в .env файле
- **Маскирование** токенов в логах (показывается как ***)
- **Проверка токенов** перед запуском скриптов

### Обработка ошибок
- **Детальное логирование** всех операций
- **Graceful degradation** при ошибках API
- **Пользовательские уведомления** об ошибках

---

## 📈 Мониторинг и логирование

### Логирование в PyQt
```python
from loguru import logger as debug_logger

debug_logger.info("📤 Информационное сообщение")
debug_logger.success("✅ Успешная операция") 
debug_logger.warning("⚠️ Предупреждение")
debug_logger.error("❌ Ошибка")
debug_logger.critical("💥 Критическая ошибка")
```

### Логирование в TypeScript
```typescript
console.log('Get rows from "releases" table in "silk" space is success ✅')
console.log('Backup is created ✅')
console.log('Flow completed ✅')
```

---

## 🔧 Установка и настройка

### 1. Установка зависимостей
```bash
# Node.js зависимости
npm install

# Python зависимости  
pip install -r scripts/requirements.txt

# PyQt6
pip install PyQt6 loguru
```

### 2. Настройка окружения
```bash
# Создать .env файл
cp .env.example .env

# Заполнить переменные
EMD_API=https://api.emd.ru
EMD_SPACE=your_space
EMD_TOKEN=your_token
EMD_USER_ID=your_user_id
```

### 3. Запуск приложения
```bash
# Запуск PyQt приложения
py pyqt_app/main.py

# Или прямой запуск скриптов
npm run start:release-parser-5
npm run start:update-releases-shipment-statuses
```

---

## 🧪 Тестирование

### Тестовые скрипты
- **src/apps/test/** - Тестовые версии основных скриптов
- **Изолированная среда** - Тестирование без влияния на продакшн
- **Отладочные логи** - Расширенное логирование для диагностики

### Проверка работоспособности
1. **API подключение** - Тестирование доступности EMD API
2. **Загрузка файлов** - Проверка загрузки медиа файлов
3. **Обработка данных** - Валидация Excel файлов

---

## 🔄 Workflow процессов

### Полный цикл загрузки релиза
1. **Подготовка данных** - Заполнение Excel файла с метаданными
2. **Размещение файлов** - Копирование медиа файлов в директорию
3. **Проверка соответствия** - Сравнение файлов с Excel (compare_files.py)
4. **Загрузка релизов** - Запуск release-parser-5 через PyQt
5. **Обновление статусов** - Перевод релизов в статус модерации
6. **Мониторинг** - Отслеживание результатов через UI

### Обработка ошибок
1. **Автоматическое обнаружение** - Парсинг ошибок из вывода скриптов
2. **Пользовательские уведомления** - Отображение ошибок в UI
3. **Логирование** - Сохранение детальной информации об ошибках
4. **Восстановление** - Возможность повторного запуска операций

---

## 📚 API интеграция

### EMD Platform API
- **Базовый URL**: https://api.emd.ru
- **Авторизация**: JWT Bearer токен
- **Основные эндпоинты**:
  - `GET /tables/{tableName}/rows` - Получение записей
  - `POST /tables/{tableName}/rows` - Создание записей  
  - `PUT /tables/{tableName}/rows/{id}` - Обновление записей
  - `POST /files/upload` - Загрузка файлов

### Структура данных релиза
```typescript
interface Release {
    name: string;           // Название релиза
    status: 'new' | 'moderation' | 'published';
    tracks: Track[];        // Массив треков
    cover: MediaFile;       // Обложка
    genre: string;          // Жанр
    label: string;          // Лейбл
    dateStartSites: string; // Дата публикации
    shouldUploadReleaseToZvonko: boolean; // Флаг для FTP
}
```

---

## 🎯 Планы развития

### Ближайшие улучшения
- **FTP интеграция** - Автоматическая отправка на FTP партнера
- **Batch операции** - Массовая обработка релизов
- **Расширенная аналитика** - Детальные отчеты и статистика

### Долгосрочные цели
- **Web интерфейс** - Дополнительный веб-интерфейс
- **API расширения** - Собственное API для интеграций
- **Автоматизация** - Полностью автоматический pipeline

---

## 👥 Команда и поддержка

### Разработка
- **Frontend**: PyQt6 + Python
- **Backend**: TypeScript + Node.js  
- **Интеграция**: EMD Platform API

### Поддержка
- **Логирование**: Детальные логи всех операций
- **Мониторинг**: Real-time отслеживание процессов
- **Диагностика**: Автоматическое обнаружение проблем

---

*Документация обновлена: 2024-12-19*
*Версия проекта: 1.0.0* 