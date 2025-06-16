# 🚀 GitHub Actions для GoSilk Staff

Автоматическая сборка macOS приложения через GitHub Actions.

## 📦 Что настроено

### 1. 🍎 Build macOS App (`build-macos.yml`)
**Полная сборка macOS приложения с созданием DMG**

**Триггеры:**
- ✅ Push в ветки `main`, `macos-build-test`
- ✅ Создание тегов `v*` (например, `v1.0.0`)
- ✅ Pull Request в `main`
- ✅ Ручной запуск через GitHub UI

**Что делает:**
- 🐍 Устанавливает Python 3.11 + все зависимости
- 📦 Устанавливает Node.js 18 + npm зависимости  
- 🔨 Компилирует TypeScript в JavaScript
- ⬇️ Скачивает Node.js runtime для встраивания
- 🔨 Собирает через PyInstaller
- 📦 Создает готовый DMG файл
- 🔺 Загружает артефакты (App + DMG)
- 🚀 Создает GitHub Release (только для тегов)

### 2. 🧪 Test Build (`test-build.yml`)
**Быстрая проверка без создания артефактов**

**Триггеры:**
- ✅ Pull Request в `main`, `macos-build-test`
- ❌ Игнорирует изменения в `.md`, `docs/`, `.gitignore`

**Что делает:**
- 🔍 Проверяет Python/Node.js зависимости
- 🔨 Тестирует TypeScript компиляцию
- 📋 Проверяет структуру проекта
- ✅ Валидирует PyInstaller spec

## 🚀 Как использовать

### Автоматическая сборка при коммите
```bash
# 1. Сделайте изменения и закоммитьте
git add .
git commit -m "feat: новая функция"

# 2. Запушьте в main или macos-build-test
git push origin main

# 3. Откройте GitHub Actions tab для отслеживания
# https://github.com/AdvikSudM12/silk/actions
```

### Создание релиза с готовым DMG
```bash
# 1. Создайте тег версии
git tag v1.0.0
git push origin v1.0.0

# 2. GitHub Actions автоматически:
#    - Соберет приложение
#    - Создаст DMG файл  
#    - Создаст GitHub Release
#    - Прикрепит DMG к релизу
```

### Ручной запуск сборки
1. Откройте [GitHub Actions](https://github.com/AdvikSudM12/silk/actions)
2. Выберите workflow "🍎 Build macOS App"  
3. Нажмите "Run workflow"
4. Выберите ветку и нажмите "Run workflow"

## 📥 Где скачать готовые файлы

### Из Artifacts (временные сборки)
1. Откройте конкретный [workflow run](https://github.com/AdvikSudM12/silk/actions)
2. Прокрутите вниз до секции "Artifacts"
3. Скачайте:
   - `GoSilk-Staff-macOS-App` - готовое .app приложение
   - `GoSilk-Staff-macOS-DMG` - установочный DMG файл
   - `Release-Notes` - описание сборки

### Из Releases (стабильные версии)
1. Откройте [Releases](https://github.com/AdvikSudM12/silk/releases)
2. Выберите нужную версию
3. Скачайте DMG файл из Assets

## 🔧 Результат сборки

### Готовые файлы:
- **📱 GoSilk Staff.app** - автономное macOS приложение
- **📦 GoSilk-Staff-v1.0.0-macOS.dmg** - установочный файл
- **📋 release-notes.md** - описание сборки

### Характеристики:
- **📏 Размер app:** ~350-400MB
- **📏 Размер DMG:** ~300-350MB  
- **🏗️ Архитектуры:** x64 + arm64 (M1/M2)
- **📱 Совместимость:** macOS 10.14+

### Включено в app bundle:
- ✅ Python runtime + PyQt6
- ✅ Node.js runtime + TypeScript
- ✅ Все зависимости проекта
- ✅ Готовность к распространению

## ⚡ Время сборки

- **🧪 Test Build:** ~3-5 минут
- **🍎 Full Build:** ~15-20 минут

## 🔍 Отслеживание сборки

### GitHub Actions UI
1. Откройте [Actions tab](https://github.com/AdvikSudM12/silk/actions)
2. Выберите нужный workflow run
3. Кликните на джобу "build-macos"
4. Смотрите логи в реальном времени

### Ключевые этапы:
1. **📥 Checkout** - загрузка кода
2. **🐍 Python Setup** - установка Python + pip зависимости
3. **📦 Node.js Setup** - установка Node.js + npm зависимости  
4. **🔨 TypeScript** - компиляция TS → JS
5. **⬇️ Node.js Runtime** - скачивание embedded runtime
6. **🔨 PyInstaller** - сборка Python → .app
7. **📦 DMG Creation** - создание установочного файла
8. **🔺 Upload** - загрузка артефактов

## ❌ Troubleshooting

### Сборка падает на этапе Python dependencies
```bash
# Проверьте requirements.txt локально:
pip install -r requirements.txt
pip install -r pyqt_app/requirements.txt
pip install -r scripts/requirements.txt
```

### Сборка падает на этапе TypeScript
```bash
# Проверьте TypeScript локально:
npm install
npx tsc --noEmit
```

### Сборка падает на этапе PyInstaller  
```bash
# Проверьте spec файл локально:
python -m py_compile macos_build/gosilk_staff.spec
```

### DMG не создается
- Проверьте, что .app bundle создался в `dist/`
- Убедитесь, что нет проблем с правами доступа

## 🎯 Быстрые команды

```bash
# Создать релиз
git tag v1.0.0 && git push origin v1.0.0

# Запустить тест локально  
npm run build && python -c "import run_app"

# Проверить GitHub Actions
open https://github.com/AdvikSudM12/silk/actions

# Скачать последнюю сборку
open https://github.com/AdvikSudM12/silk/releases/latest
```

---

**🎵 Теперь каждый push автоматически проверяет сборку, а каждый тег создает готовый DMG! 🚀** 