# 🍎 Сборка macOS приложения GoSilk Staff

## 📁 Описание файлов

- `gosilk_staff.spec` - конфигурация PyInstaller для создания .app bundle
- `node_runner.py` - wrapper для запуска Node.js в автономном приложении
- `resource_utils.py` - утилиты для работы с путями ресурсов
- `build_macos.sh` - автоматический скрипт сборки
- `env_template.txt` - шаблон конфигурации для пользователей

## 🚀 Полная инструкция сборки

### Шаг 1: Подготовка окружения

```bash
# 1. Клонировать проект
git clone <project_repo>
cd silk

# 2. Проверить наличие зависимостей
node --version    # Должен быть 16+
python3 --version # Должен быть 3.8+
```

### Шаг 2: Автоматическая сборка

```bash
# Запустить автоматическую сборку  
chmod +x macos_build/build_macos.sh
./macos_build/build_macos.sh
```

Скрипт автоматически:
- Установит все Python зависимости
- Установит Node.js зависимости
- Скомпилирует TypeScript
- Скачает встроенный Node.js runtime
- Соберет приложение через PyInstaller
- Создаст готовый .app bundle

### Шаг 3: Тестирование

```bash
# Запустить готовое приложение
open "dist/GoSilk Staff.app"
```

### Шаг 4: Создание установочного файла

```bash
# Создать DMG для распространения
hdiutil create -volname 'GoSilk Staff' -srcfolder 'dist/GoSilk Staff.app' -ov -format UDZO 'GoSilk Staff v1.0.dmg'
```

## 📦 Результат

После успешной сборки:
- **Приложение:** `dist/GoSilk Staff.app` - автономное macOS приложение
- **Размер:** ~300-400MB
- **Установочный файл:** `GoSilk Staff v1.0.dmg` - готов к распространению
- **Включает все зависимости:** Python, PyQt6, Node.js, TypeScript модули

## ✅ Особенности автономного приложения

- **Автоматическое определение режима:** app bundle vs разработка
- **Пользовательские данные:** `~/.gosilk_staff/` (настройки, .env, кеш)
- **Логи приложения:** `~/Library/Logs/GoSilk Staff/`
- **Встроенный Node.js:** не требует системной установки
- **Полная автономность:** работает без дополнительных зависимостей

## 🔧 Устранение проблем

Если приложение не запускается:

```bash
# Логи PyQt приложения
tail -f ~/Library/Logs/GoSilk\ Staff/app.log

# Логи системы macOS
tail -f /var/log/system.log | grep "GoSilk Staff"

# Проверка прав доступа
ls -la "dist/GoSilk Staff.app/Contents/MacOS/"
```

## 📋 Требования

- **macOS:** 10.14+ (Mojave или новее)
- **Python:** 3.8+
- **Node.js:** 16+
- **Архитектура:** x64 или arm64 (M1/M2)

## 🎯 Структура готового приложения

```
GoSilk Staff.app/
├── Contents/
│   ├── MacOS/GoSilk Staff           # Исполняемый файл
│   ├── Resources/                   # Ресурсы приложения
│   │   ├── pyqt_app/               # GUI компоненты
│   │   ├── scripts/                # Python утилиты
│   │   ├── src/                    # JavaScript из TypeScript
│   │   ├── node_modules/           # Node.js зависимости
│   │   ├── embedded_node/          # Встроенный Node.js
│   │   └── .env.template           # Шаблон конфигурации
│   └── Info.plist                  # Метаданные приложения
``` 