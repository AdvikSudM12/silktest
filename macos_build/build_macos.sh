#!/bin/bash
set -e

# 🍎 Автоматическая сборка GoSilk Staff для macOS
echo "🍎 Начинаем сборку GoSilk Staff для macOS..."

# Переходим в корневую папку проекта
cd "$(dirname "$0")/.."

# 1. Проверка зависимостей
echo ""
echo "📦 Проверка зависимостей..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js не найден. Установите Node.js 16+ и повторите попытку"
    exit 1
fi

if ! command -v python3 &> /dev/null && ! command -v py &> /dev/null; then
    echo "❌ Python не найден. Установите Python 3.8+ и повторите попытку"
    exit 1
fi

# Определяем команду Python
if command -v py &> /dev/null; then
    PYTHON_CMD="py"
else
    PYTHON_CMD="python3"
fi

echo "✅ Node.js: $(node --version)"
echo "✅ Python: $($PYTHON_CMD --version)"

# 2. Установка Python зависимостей
echo ""
echo "🐍 Установка Python зависимостей..."
$PYTHON_CMD -m pip install --upgrade pip
$PYTHON_CMD -m pip install pyinstaller
$PYTHON_CMD -m pip install -r requirements.txt

# Проверяем наличие дополнительных requirements файлов
if [ -f "pyqt_app/requirements.txt" ]; then
    $PYTHON_CMD -m pip install -r pyqt_app/requirements.txt
fi

if [ -f "scripts/requirements.txt" ]; then
    $PYTHON_CMD -m pip install -r scripts/requirements.txt
fi

# 3. Установка Node.js зависимостей
echo ""
echo "📦 Установка Node.js зависимостей..."
if [ ! -d "node_modules" ]; then
    npm install
else
    echo "✅ node_modules уже существует"
fi

# 4. Компиляция TypeScript
echo ""
echo "🔨 Компиляция TypeScript в JavaScript..."
if [ -f "tsconfig.json" ]; then
    npx tsc
    echo "✅ TypeScript скомпилирован"
else
    echo "⚠️  tsconfig.json не найден, пропускаем компиляцию TypeScript"
fi

# 5. Скачивание Node.js runtime для встраивания
echo ""
echo "⬇️ Подготовка Node.js runtime..."
if [ ! -d "embedded_node" ]; then
    echo "Скачиваем Node.js runtime для macOS..."
    
    # Определяем архитектуру
    if [[ $(uname -m) == "arm64" ]]; then
        NODE_ARCH="arm64"
        NODE_URL="https://nodejs.org/dist/v18.18.0/node-v18.18.0-darwin-arm64.tar.gz"
        NODE_FOLDER="node-v18.18.0-darwin-arm64"
    else
        NODE_ARCH="x64"
        NODE_URL="https://nodejs.org/dist/v18.18.0/node-v18.18.0-darwin-x64.tar.gz"
        NODE_FOLDER="node-v18.18.0-darwin-x64"
    fi
    
    echo "Архитектура: $NODE_ARCH"
    curl -o node-runtime.tar.gz "$NODE_URL"
    tar -xzf node-runtime.tar.gz
    mv "$NODE_FOLDER" embedded_node
    rm node-runtime.tar.gz
    echo "✅ Node.js runtime подготовлен"
else
    echo "✅ embedded_node уже существует"
fi

# 6. Обновляем .spec файл чтобы он указывал на правильную папку env_template
echo ""
echo "🔧 Обновляем конфигурацию сборки..."
sed -i '' 's|macos_build/.env.template|macos_build/env_template.txt|g' macos_build/gosilk_staff.spec

# 7. Сборка через PyInstaller
echo ""
echo "🔨 Сборка приложения через PyInstaller..."
pyinstaller macos_build/gosilk_staff.spec --clean

# 8. Копирование Node.js runtime в app bundle
echo ""
echo "📋 Копирование Node.js runtime в app bundle..."
cp -r embedded_node "dist/GoSilk Staff.app/Contents/Resources/"
chmod +x "dist/GoSilk Staff.app/Contents/Resources/embedded_node/bin/node"

# 9. Копирование шаблона конфигурации
echo ""
echo "⚙️ Копирование шаблона конфигурации..."
cp macos_build/env_template.txt "dist/GoSilk Staff.app/Contents/Resources/.env.template"

# 10. Проверка результата
echo ""
echo "🔍 Проверка готового приложения..."
if [ -d "dist/GoSilk Staff.app" ]; then
    APP_SIZE=$(du -sh "dist/GoSilk Staff.app" | cut -f1)
    echo "✅ Приложение создано успешно!"
    echo "📦 Размер: $APP_SIZE"
    echo "📁 Путь: dist/GoSilk Staff.app"
    echo ""
    echo "🚀 Для запуска выполните:"
    echo "   open 'dist/GoSilk Staff.app'"
    echo ""
    echo "📋 Для создания DMG образа выполните:"
    echo "   hdiutil create -volname 'GoSilk Staff' -srcfolder 'dist/GoSilk Staff.app' -ov -format UDZO 'GoSilk Staff v1.0.dmg'"
else
    echo "❌ Ошибка сборки! Приложение не создано."
    exit 1
fi

echo ""
echo "🎉 Сборка завершена успешно!" 