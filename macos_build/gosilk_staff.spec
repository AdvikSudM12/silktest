# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

block_cipher = None

# Определяем базовую директорию (корень проекта)
base_dir = Path(__file__).parent.parent

# Основной файл запуска
python_files = [
    str(base_dir / 'run_app.py'),
]

# Дополнительные данные для включения в app bundle
datas = [
    # PyQt ресурсы и данные
    (str(base_dir / 'pyqt_app' / 'resources'), 'pyqt_app/resources'),
    (str(base_dir / 'pyqt_app' / 'data'), 'pyqt_app/data'),
    
    # Скомпилированный JavaScript из TypeScript
    (str(base_dir / 'src'), 'src'),
    
    # Критически важные Node.js модули
    (str(base_dir / 'node_modules' / 'ts-node'), 'node_modules/ts-node'),
    (str(base_dir / 'node_modules' / 'typescript'), 'node_modules/typescript'),
    (str(base_dir / 'node_modules' / 'axios'), 'node_modules/axios'),
    (str(base_dir / 'node_modules' / 'dotenv'), 'node_modules/dotenv'),
    (str(base_dir / 'node_modules' / 'dayjs'), 'node_modules/dayjs'),
    (str(base_dir / 'node_modules' / 'tus-js-client'), 'node_modules/tus-js-client'),
    (str(base_dir / 'node_modules' / 'convert-csv-to-json'), 'node_modules/convert-csv-to-json'),
    (str(base_dir / 'node_modules' / 'convert-excel-to-json'), 'node_modules/convert-excel-to-json'),
    (str(base_dir / 'node_modules' / 'tsconfig-paths'), 'node_modules/tsconfig-paths'),
    
    # Конфигурационные файлы
    (str(base_dir / 'package.json'), '.'),
    (str(base_dir / 'tsconfig.json'), '.'),
    
    # Python скрипты утилит
    (str(base_dir / 'scripts'), 'scripts'),
    
    # Шаблон конфигурации
    (str(base_dir / 'macos_build' / 'env_template.txt'), '.'),
]

# Скрытые импорты Python модулей
hiddenimports = [
    # PyQt6 основные модули
    'PyQt6.QtCore',
    'PyQt6.QtWidgets', 
    'PyQt6.QtGui',
    'PyQt6.QtWebEngineWidgets',
    
    # Логирование и утилиты
    'loguru',
    'pandas',
    'openpyxl',
    'xlsxwriter',
    
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
    icon=str(base_dir / 'pyqt_app' / 'resources' / 'icon.icns'),
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
    icon=str(base_dir / 'pyqt_app' / 'resources' / 'icon.icns'),
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