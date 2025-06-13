# GoSilk Staff - PyQt6 Desktop Application

Десктопное приложение для управления релизами на платформе EMD с интеграцией TypeScript скриптов.

## 🚀 Установка зависимостей

### Python зависимости (PyQt6 приложение):
```bash
pip install -r requirements.txt
```

### Node.js зависимости (TypeScript скрипты):
```bash
npm install
# или
yarn install
```

## 🎯 Запуск приложения

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

## 📁 Структура проекта

```
silk/
├── pyqt_app/                    # PyQt6 приложение
│   ├── workers/                 # Асинхронные воркеры
│   ├── dialogs/                 # Диалоги прогресса
│   ├── pages/                   # Страницы приложения
│   └── script_manager.py        # Менеджер TypeScript скриптов
├── src/apps/                    # TypeScript скрипты
│   ├── release-parser-5/        # Загрузка релизов
│   └── update-releases-shipment-statuses/  # Обновление статусов
├── main.py                      # Точка входа PyQt приложения
└── requirements.txt             # Python зависимости
```

## 🔧 Конфигурация

### Переменные окружения (.env):
```env
EMD_API=https://api.emd.ru
EMD_SPACE=your_workspace
EMD_TOKEN=your_jwt_token
EMD_USER_ID=your_user_id
```

### Путь к таблице релизов:
```
src/apps/release-parser-5/files/releases.xlsx
```
*Необходимо указать фактический путь к таблице с релизами*

## 🎨 Дизайн

Использует [Neobrutalism Components](https://github.com/ekmas/neobrutalism-components) для стилизации UI.

## 🛠️ Технологии

- **Frontend:** PyQt6, QThread
- **Backend:** TypeScript, Node.js
- **API:** EMD Platform REST API
- **Логирование:** loguru

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

---

*Обновлено: 19 декабря 2024*
