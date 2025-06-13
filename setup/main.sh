#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo
echo "=========================================="
echo "  🎯 SILK PROJECT - УПРАВЛЕНИЕ ЗАВИСИМОСТЯМИ"
echo "=========================================="
echo

# Переходим в директорию скрипта
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Функция проверки команды
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Ищем Python
PYTHON_CMD=""
for cmd in python3 python py; do
    if command_exists "$cmd"; then
        PYTHON_CMD="$cmd"
        break
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo -e "${RED}❌ Python не найден!${NC}"
    echo "Установите Python:"
    echo "  Ubuntu/Debian: sudo apt install python3"
    echo "  CentOS/RHEL: sudo yum install python3"
    echo "  macOS: brew install python3"
    echo
    exit 1
fi

echo -e "${GREEN}✅ Найден Python: $PYTHON_CMD${NC}"
echo

# Запускаем главный скрипт
echo -e "${BLUE}🚀 Запуск главного меню...${NC}"
echo
"$PYTHON_CMD" main.py

echo
echo -e "${YELLOW}Нажмите Enter для выхода...${NC}"
read 