# -*- mode: python ; coding: utf-8 -*-

import os
import shutil
from pathlib import Path

block_cipher = None

# Определяем базовую директорию (корень проекта)
# В PyInstaller контексте используем os.getcwd() вместо __file__
base_dir = Path(os.getcwd())

# Находим Node.js runtime для встраивания
def find_node_runtime():
    """Находит Node.js исполняемые файлы для включения в bundle"""
    node_files = {}
    
    # Ищем основные исполняемые файлы Node.js
    node_executable = shutil.which('node')
    npm_executable = shutil.which('npm')
    npx_executable = shutil.which('npx')
    
    if node_executable:
        node_files['node'] = node_executable
        print(f"✅ Найден Node.js: {node_executable}")
    else:
        print("❌ Node.js не найден в системе")
        
    if npm_executable:
        node_files['npm'] = npm_executable
        print(f"✅ Найден npm: {npm_executable}")
        
    if npx_executable:
        node_files['npx'] = npx_executable
        print(f"✅ Найден npx: {npx_executable}")
    
    return node_files

# Получаем Node.js runtime
node_runtime = find_node_runtime()

# Основной файл запуска
python_files = [
    str(base_dir / 'run_app.py'),
]

# Функция для безопасного добавления .bin файлов
def add_bin_files():
    """Добавляет критичные исполняемые файлы из node_modules/.bin"""
    bin_files = []
    bin_dir = base_dir / 'node_modules' / '.bin'
    
    # Критичные исполняемые файлы для TypeScript
    critical_bins = ['ts-node', 'tsc', 'ts-node-esm', 'ts-node-script']
    
    for bin_name in critical_bins:
        bin_file = bin_dir / bin_name
        if bin_file.exists():
            # Добавляем как отдельный файл, а не директорию
            bin_files.append((str(bin_file), f'node_modules_bin/{bin_name}'))
            print(f"   ✅ Включен {bin_name}")
    
    return bin_files

# Дополнительные данные для включения в app bundle
datas = [
    # PyQt ресурсы и данные
    (str(base_dir / 'pyqt_app' / 'resources'), 'pyqt_app/resources'),
    (str(base_dir / 'pyqt_app' / 'data'), 'pyqt_app/data'),
    
    # Скомпилированный JavaScript из TypeScript
    (str(base_dir / 'src'), 'src'),
    
    # Конфигурационные файлы
    (str(base_dir / 'package.json'), '.'),
    (str(base_dir / 'tsconfig.json'), '.'),
    
    # Python скрипты утилит
    (str(base_dir / 'scripts'), 'scripts'),
    
    # Шаблон конфигурации
    (str(base_dir / 'macos_build' / 'env_template.txt'), '.'),
]

# Режим включения Node.js модулей
INCLUDE_ALL_NODE_MODULES = True  # Измените на True для включения всех модулей

if INCLUDE_ALL_NODE_MODULES:
    print("📦 Включаем ВСЕ Node.js модули (может быть медленно и занимать много места)...")
    node_modules_path = base_dir / 'node_modules'
    if node_modules_path.exists():
        # Включаем node_modules, но исключаем проблемные вложенные структуры
        print("🔧 Копируем node_modules с исключением проблемных путей...")
        
        # Создаем безопасную копию node_modules без глубокой вложенности
        import shutil
        import tempfile
        import os
        
        # Создаем временную директорию для "плоской" версии node_modules
        temp_node_modules = base_dir / 'temp_node_modules'
        if temp_node_modules.exists():
            shutil.rmtree(temp_node_modules)
        temp_node_modules.mkdir()
        
        # Копируем только первый уровень модулей
        for item in node_modules_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                try:
                    dest_path = temp_node_modules / item.name
                    # Копируем только основную структуру, избегая глубокой вложенности
                    shutil.copytree(item, dest_path, ignore=shutil.ignore_patterns('node_modules'))
                    print(f"   ✅ Скопирован {item.name}")
                except Exception as e:
                    print(f"   ⚠️ Пропущен {item.name}: {e}")
        
        datas.append((str(temp_node_modules), 'node_modules'))
        print(f"   ✅ Включена оптимизированная папка node_modules")
else:
    # Автоматически добавляем только нужные Node.js модули
    print("📦 Определяем необходимые Node.js модули...")
    try:
        # Попробуем автоматическое определение
        node_modules = get_required_node_modules()
        datas.extend(node_modules)
    except Exception as e:
        print(f"⚠️ Автоматическое определение не удалось: {e}")
        # Fallback к ручному списку
        node_modules = get_manual_node_modules()
        datas.extend(node_modules)

# Добавляем критичные исполняемые файлы из .bin
print("🔧 Включаем критичные исполняемые файлы из node_modules/.bin:")
datas.extend(add_bin_files())

# Добавляем Node.js runtime в bundle (встраиваем полностью)
if node_runtime:
    print("🚀 Включаем Node.js runtime в app bundle:")
    
    # Создаем директорию node/bin в bundle
    if 'node' in node_runtime:
        datas.append((node_runtime['node'], 'node/bin/'))
        print(f"   ✅ node -> node/bin/node")
    
    if 'npm' in node_runtime:
        datas.append((node_runtime['npm'], 'node/bin/'))
        print(f"   ✅ npm -> node/bin/npm")
        
    if 'npx' in node_runtime:
        datas.append((node_runtime['npx'], 'node/bin/'))
        print(f"   ✅ npx -> node/bin/npx")
else:
    print("⚠️ Node.js runtime не найден - приложение будет зависеть от системного Node.js")

# Скрытые импорты Python модулей
hiddenimports = [
    # PyQt6 основные модули
    'PyQt6.QtCore',
    'PyQt6.QtWidgets', 
    'PyQt6.QtGui',
    
    # Логирование и утилиты
    'loguru',
    'pandas',
    'openpyxl',
    
    # Стандартные библиотеки
    'pathlib',
    'subprocess',
    'json',
    'sys',
    'os',
    'shutil',
    'datetime',
    'urllib',
    'ssl',
    
    # Для работы с Excel и CSV
    'csv',
    'xml',
    'xml.etree',
    'xml.etree.ElementTree',
]

# Функция для автоматического определения нужных Node.js модулей
def get_required_node_modules():
    """Автоматически определяет необходимые Node.js модули из package.json"""
    import json
    
    required_modules = []
    package_json_path = base_dir / 'package.json'
    
    if package_json_path.exists():
        try:
            with open(package_json_path, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
            
            # Получаем зависимости из package.json
            dependencies = package_data.get('dependencies', {})
            dev_dependencies = package_data.get('devDependencies', {})
            
            # Объединяем все зависимости
            all_deps = {**dependencies, **dev_dependencies}
            
            print("🔍 Автоматическое определение Node.js модулей:")
            
            for module_name in all_deps.keys():
                module_path = base_dir / 'node_modules' / module_name
                if module_path.exists():
                    required_modules.append((str(module_path), f'node_modules/{module_name}'))
                    print(f"   ✅ {module_name}")
                else:
                    print(f"   ⚠️ {module_name} (не найден)")
            
            print(f"📊 Найдено модулей: {len(required_modules)} из {len(all_deps)}")
            
        except Exception as e:
            print(f"❌ Ошибка чтения package.json: {e}")
            # Fallback к ручному списку
            return get_manual_node_modules()
    
    return required_modules

def get_manual_node_modules():
    """Ручной список критичных Node.js модулей (fallback)"""
    manual_modules = [
        'ts-node', 'typescript', 'axios', 'dotenv', 'dayjs',
        'tus-js-client', 'convert-csv-to-json', 'convert-excel-to-json',
        'tsconfig-paths'
    ]
    
    modules = []
    print("🔧 Используем ручной список модулей:")
    
    for module_name in manual_modules:
        module_path = base_dir / 'node_modules' / module_name
        if module_path.exists():
            modules.append((str(module_path), f'node_modules/{module_name}'))
            print(f"   ✅ {module_name}")
        else:
            print(f"   ❌ {module_name} (не найден)")
    
    return modules

a = Analysis(
    python_files,
    pathex=[str(base_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Проверяем наличие иконки
icon_path = base_dir / 'pyqt_app' / 'resources' / 'icon.icns'
app_icon = str(icon_path) if icon_path.exists() else None

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GoSilk Staff',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Отключаем консоль для GUI приложения
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=app_icon,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GoSilk Staff',
)

# Создание macOS app bundle
app = BUNDLE(
    coll,
    name='GoSilk Staff.app',
    icon=app_icon,
    bundle_identifier='com.emd.gosilk-staff',
    version='1.0.0',
    info_plist={
        'CFBundleName': 'GoSilk Staff',
        'CFBundleDisplayName': 'GoSilk Staff',
        'CFBundleIdentifier': 'com.emd.gosilk-staff',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSMinimumSystemVersion': '10.14',
        'NSHighResolutionCapable': True,
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'Excel Files',
                'CFBundleTypeExtensions': ['xlsx', 'xls'],
                'CFBundleTypeRole': 'Editor'
            }
        ],
    },
)

# Очищаем временную папку после сборки
print("🧹 Очистка временных файлов...")
temp_node_modules = base_dir / 'temp_node_modules'
if temp_node_modules.exists():
    import shutil
    shutil.rmtree(temp_node_modules)
    print("   ✅ Временная папка temp_node_modules удалена")

# ВАЖНО: После сборки нужно сделать Node.js исполняемые файлы исполняемыми
# chmod +x "GoSilk Staff.app/Contents/Resources/node/bin/*"
print("💡 После сборки не забудьте выполнить:")
print('   chmod +x "GoSilk Staff.app/Contents/Resources/node/bin/"*') 