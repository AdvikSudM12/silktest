import os
import pandas as pd
from openpyxl import load_workbook
import json
from pathlib import Path
from datetime import datetime

# DEBUG: Добавляем логирование для отладки обработки Excel
import sys
script_dir = Path(__file__).parent.parent
sys.path.append(str(script_dir))
from pyqt_app.logger_config import get_logger
debug_logger = get_logger("excel_operations")

def process_excel_errors(excel_file_path=None, error_file_path=None):
    """
    Обрабатывает ошибки из файла сравнения и переносит проблемные строки в отдельный лист
    
    Args:
        excel_file_path: Путь к основному Excel файлу
        error_file_path: Путь к файлу с результатами сравнения
    
    Returns:
        dict: Результат обработки с ключами 'success', 'message', 'moved_count'
    """
    debug_logger.info("📝 Начинаем обработку Excel ошибок")
    debug_logger.debug(f"📄 Основной Excel: {excel_file_path}")
    debug_logger.debug(f"📊 Файл ошибок: {error_file_path}")
    
    # Получаем абсолютный путь к директории скрипта
    script_dir = Path(__file__).parent.parent
    debug_logger.debug(f"📂 Директория скрипта: {script_dir}")
    
    # Если пути не переданы, загружаем из paths.json
    if not excel_file_path:
        paths_file = script_dir / 'pyqt_app' / 'data' / 'paths.json'
        if os.path.exists(paths_file):
            try:
                with open(paths_file, 'r', encoding='utf-8') as f:
                    paths_data = json.load(f)
                    excel_file_path = paths_data.get('excel_file_path')
            except Exception as e:
                return {
                    'success': False,
                    'message': f"Ошибка при загрузке paths.json: {str(e)}",
                    'moved_count': 0
                }
    
    # Если файл с ошибками не указан, ищем последний в папке results
    if not error_file_path:
        results_dir = script_dir / 'results'
        if os.path.exists(results_dir):
            # Ищем последний файл с результатами сравнения
            error_files = [f for f in os.listdir(results_dir) if f.startswith('file_comparison_results_') and f.endswith('.xlsx')]
            if error_files:
                error_files.sort(reverse=True)  # Сортируем по убыванию (последний файл первый)
                error_file_path = results_dir / error_files[0]
    
    # Проверяем наличие файлов
    if not excel_file_path or not os.path.exists(excel_file_path):
        return {
            'success': False,
            'message': f"Основной Excel файл не найден: {excel_file_path}",
            'moved_count': 0
        }
    
    if not error_file_path or not os.path.exists(error_file_path):        return {
            'success': False,
            'message': f"Файл с ошибками не найден: {error_file_path}",
            'moved_count': 0
        }

    try:
        # Читаем файл с ошибками с помощью pandas
        error_df = pd.read_excel(error_file_path, sheet_name='Результаты')
        
        # Собираем список названий треков с ошибками
        error_tracks = set()
        for _, row in error_df.iterrows():
            if pd.notna(row['Название в Excel']):  # Проверяем, что значение не NaN
                track_name = str(row['Название в Excel']).strip()
                error_tracks.add(track_name)
        
        if len(error_tracks) == 0:
            return {
                'success': True,
                'message': "Не найдено треков с ошибками для обработки",
                'moved_count': 0
            }
        
        # Открываем основной файл
        main_wb = load_workbook(excel_file_path)
        if "Лист1" not in main_wb.sheetnames:
            return {
                'success': False,
                'message': "Лист 'Лист1' не найден в основном файле",
                'moved_count': 0
            }
        
        main_sheet = main_wb["Лист1"]
        
        # Создаем имя листа с текущей датой
        current_date = datetime.now().strftime("%d.%m.%y")
        error_sheet_name = f"Ошибки_загрузки_{current_date}"
        
        # Создаем или очищаем лист для ошибок
        if error_sheet_name in main_wb.sheetnames:
            main_wb.remove(main_wb[error_sheet_name])
        error_sheet_new = main_wb.create_sheet(error_sheet_name)
          # Копируем заголовки
        headers = [cell.value for cell in main_sheet[1]]
        error_sheet_new.append(headers)
        
        # Перебираем строки и переносим только те, что есть в списке ошибок
        rows_to_delete = []
        
        for row_idx, row in enumerate(main_sheet.iter_rows(min_row=2, values_only=True), start=2):
            if row[0]:
                current_track = str(row[0]).strip()
                # Проверяем, есть ли текущий трек в списке ошибок
                if current_track in error_tracks:
                    error_sheet_new.append(row)
                    rows_to_delete.append(row_idx)
        
        # Удаляем строки с конца, чтобы не сбить нумерацию
        for row_idx in reversed(rows_to_delete):
            main_sheet.delete_rows(row_idx)
        
        # Сохраняем изменения
        main_wb.save(excel_file_path)
        
        return {
            'success': True,
            'message': f"Операция успешно выполнена! Перенесено {len(rows_to_delete)} строк с ошибками в лист '{error_sheet_name}'",
            'moved_count': len(rows_to_delete),
            'error_sheet_name': error_sheet_name
        }

    except Exception as e:
        return {
            'success': False,
            'message': f"Произошла ошибка: {str(e)}",
            'moved_count': 0
        }


def process_excel_errors_interactive():
    """Интерактивная версия для запуска из командной строки"""
    main_file = input("Введите путь к основному Excel файлу: ")
    error_file = input("Введите путь к файлу с ошибками (или нажмите Enter для автопоиска): ")
    
    if not error_file.strip():
        error_file = None
    
    result = process_excel_errors(main_file, error_file)
    
    if result['success']:
        print(f"\n{result['message']}")
    else:
        print(f"Ошибка: {result['message']}")


if __name__ == "__main__":
    process_excel_errors_interactive()
