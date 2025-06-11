import pandas as pd
import os
from difflib import SequenceMatcher
from pathlib import Path
from datetime import datetime
from openpyxl.styles import PatternFill
import unicodedata
import re

# DEBUG: Добавляем логирование для отладки процесса сравнения файлов
# Импортируем логгер из pyqt_app
import sys
script_dir = Path(__file__).parent.parent
sys.path.append(str(script_dir))
from pyqt_app.logger_config import get_logger
debug_logger = get_logger("compare_files")

def normalize_filename(filename):
    """Нормализует имя файла для корректного сравнения"""
    if not filename or pd.isna(filename) or str(filename).strip() == '':
        return ''
    
    # Преобразуем в строку и убираем пробелы по краям
    filename = str(filename).strip()
    
    # Нормализация Unicode
    filename = unicodedata.normalize('NFKC', filename)
    
    # Обработка пробелов вокруг специальных символов
    # Убираем пробелы перед скобками, точками и другими спецсимволами
    filename = re.sub(r'\s*([\(\)\[\]\{\}\.,\-_])\s*', r'\1', filename)
    
    # Заменяем множественные пробелы на один
    filename = re.sub(r'\s+', ' ', filename)
    
    # Приводим к нижнему регистру
    filename = filename.lower()
    
    # Отдельно обрабатываем расширение файла
    name, ext = os.path.splitext(filename)
    if ext:
        # Убираем точку из расширения для сравнения
        ext = ext[1:] if ext.startswith('.') else ext
        # Убираем пробелы вокруг точки расширения
        return f"{name.strip()}.{ext.strip()}"
    
    return filename.strip()

def calculate_similarity(a, b):
    """Вычисляет процент сходства между двумя строками"""
    if not a or not b:
        return 0
    
    # Нормализуем строки перед сравнением
    a = normalize_filename(a)
    b = normalize_filename(b)
    
    # Разделяем имя и расширение
    a_name, a_ext = os.path.splitext(a)
    b_name, b_ext = os.path.splitext(b)
    
    # Если расширения разные, уменьшаем сходство
    if a_ext.lower() != b_ext.lower():
        return 0
    
    # Сравниваем только имена файлов без расширений
    similarity = SequenceMatcher(None, a_name, b_name).ratio() * 100
    
    return similarity

def find_closest_match(filename, file_list):
    """Находит самое похожее название файла и процент сходства"""
    if not filename or pd.isna(filename) or str(filename).strip() == '':
        return '', 0
    
    normalized_filename = normalize_filename(filename)
    if not normalized_filename:
        return '', 0
    
    # Выводим отладочную информацию
    print_debug_info(filename, normalized_filename)
    
    # Разделяем имя и расширение искомого файла
    filename_name, filename_ext = os.path.splitext(normalized_filename)
    
    max_similarity = 0
    closest_match = None
    closest_match_original = None
    
    for original_file in file_list:
        normalized_file = normalize_filename(original_file)
        # Проверяем расширение
        _, file_ext = os.path.splitext(normalized_file)
        
        # Если расширения разные, пропускаем файл
        if filename_ext.lower() != file_ext.lower():
            continue
            
        similarity = calculate_similarity(normalized_filename, normalized_file)
        if similarity > max_similarity:
            max_similarity = similarity
            closest_match = normalized_file
            closest_match_original = original_file
            
            # Выводим информацию о найденном совпадении
            print(f"\nНайдено лучшее совпадение:")
            print(f"Искомый файл     : '{filename}'")
            print(f"Нормализованный  : '{normalized_filename}'")
            print(f"Найденный файл   : '{original_file}'")
            print(f"Нормализованный  : '{normalized_file}'")
            print(f"Процент сходства : {similarity}%")
    
    return closest_match_original, max_similarity

def find_char_differences(str1, str2):
    """Находит различия между двумя строками"""
    # Нормализуем строки перед сравнением
    str1 = normalize_filename(str1)
    str2 = normalize_filename(str2)
    
    char_differences = []
    
    # Сравниваем символы
    for i, (c1, c2) in enumerate(zip(str1, str2)):
        if c1 != c2:
            # Показываем оригинальные символы для лучшего понимания различий
            char_differences.append(f"Позиция {i+1}: '{c1}' vs '{c2}'")
    
    # Проверяем разницу в длине
    if len(str1) != len(str2):
        min_len = min(len(str1), len(str2))
        # Показываем лишние символы
        if len(str1) > min_len:
            extra = str1[min_len:]
            char_differences.append(f"Лишние символы в первой строке: '{extra}'")
        if len(str2) > min_len:
            extra = str2[min_len:]
            char_differences.append(f"Лишние символы во второй строке: '{extra}'")
    
    return '; '.join(char_differences) if char_differences else ''

def compare_files_with_excel(excel_file_path=None, directory_path=None):
    """
    Сравнивает файлы из Excel с реальными файлами в директории
    
    Args:
        excel_file_path: Путь к Excel файлу (если не указан, берется из paths.json)
        directory_path: Путь к директории с файлами (если не указан, берется из paths.json)
    
    Returns:
        dict: Результат сравнения с ключами 'success', 'results_file', 'error_count', 'message'
    """
    debug_logger.info("🔍 Начинаем сравнение файлов с Excel")
    debug_logger.debug(f"📄 Excel файл: {excel_file_path}")
    debug_logger.debug(f"📁 Директория: {directory_path}")
    
    import json
    
    # Получаем абсолютный путь к директории скрипта
    script_dir = Path(__file__).parent.parent
    debug_logger.debug(f"📂 Директория скрипта: {script_dir}")
    
    # Если пути не переданы, загружаем из paths.json
    if not excel_file_path or not directory_path:
        debug_logger.info("🔄 Загружаем пути из paths.json")
        paths_file = script_dir / 'pyqt_app' / 'data' / 'paths.json'
        debug_logger.debug(f"📍 Путь к paths.json: {paths_file}")
        
        if os.path.exists(paths_file):
            debug_logger.success("✅ Файл paths.json найден")
            try:
                with open(paths_file, 'r', encoding='utf-8') as f:
                    paths_data = json.load(f)
                    debug_logger.debug(f"📊 Данные из paths.json: {paths_data}")
                    
                    if not excel_file_path:
                        excel_file_path = paths_data.get('excel_file_path')
                        debug_logger.debug(f"📄 Загружен Excel путь: {excel_file_path}")
                    if not directory_path:
                        directory_path = paths_data.get('directory_path')
                        debug_logger.debug(f"📁 Загружен путь директории: {directory_path}")
            except Exception as e:
                debug_logger.error(f"❌ Ошибка при загрузке paths.json: {str(e)}")
                return {
                    'success': False,
                    'message': f"Ошибка при загрузке paths.json: {str(e)}",
                    'results_file': None,
                    'error_count': 0
                }
        else:
            debug_logger.warning("⚠️ Файл paths.json не найден")
    
    # Проверяем наличие путей
    debug_logger.info("🔍 Проверяем наличие путей")
    if not excel_file_path:
        debug_logger.error("❌ Не указан путь к Excel файлу")
        return {
            'success': False,
            'message': "Не указан путь к Excel файлу",
            'results_file': None,
            'error_count': 0
        }
    
    if not directory_path:
        debug_logger.error("❌ Не указан путь к директории с файлами")
        return {
            'success': False,
            'message': "Не указан путь к директории с файлами",
            'results_file': None,
            'error_count': 0
        }
    
    debug_logger.info("🔍 Проверяем существование файлов")
    if not os.path.exists(excel_file_path):
        debug_logger.error(f"❌ Excel файл не найден: {excel_file_path}")
        return {
            'success': False,
            'message': f"Excel файл не найден: {excel_file_path}",
            'results_file': None,
            'error_count': 0
        }
        
    if not os.path.exists(directory_path):
        debug_logger.error(f"❌ Директория не найдена: {directory_path}")
        return {
            'success': False,
            'message': f"Директория не найдена: {directory_path}",
            'results_file': None,
            'error_count': 0
        }    
    
    debug_logger.success("✅ Все пути проверены и существуют")
    
    # Создаем директорию results, если её нет
    results_dir = script_dir / 'results'
    debug_logger.debug(f"📁 Директория результатов: {results_dir}")
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        debug_logger.info("📁 Создана директория для результатов")

    # Получаем список реальных файлов в директории
    debug_logger.info("📋 Получаем список файлов в директории")
    actual_files = [f for f in os.listdir(directory_path)]
    debug_logger.info(f"📊 Найдено {len(actual_files)} файлов в директории")
    debug_logger.debug(f"📝 Список файлов: {actual_files[:10]}...")  # Показываем только первые 10
    
    try:
        debug_logger.info("📖 Читаем Excel файл")
        # Читаем только Лист1 из Excel файла
        df = pd.read_excel(excel_file_path, sheet_name='Лист1', engine='openpyxl')
        debug_logger.success(f"✅ Excel файл прочитан, строк: {len(df)}")
    except Exception as e:        
        debug_logger.error(f"❌ Ошибка при чтении Excel файла: {str(e)}")
        return {
            'success': False,
            'message': f"Ошибка при чтении Excel файла: {str(e)}",
            'results_file': None,
            'error_count': 0
        }# Проверяем наличие необходимых столбцов
    required_columns = ['track (titel)', 'cover (titel)']
    if not all(col in df.columns for col in required_columns):
        return {
            'success': False,
            'message': f"В Excel файле отсутствуют необходимые столбцы: {required_columns}",
            'results_file': None,
            'error_count': 0
        }

    # Создаем списки для хранения результатов
    all_results = []

    # Обрабатываем каждую строку в Excel
    for index, row in df.iterrows():
        # Проверяем треки
        track_name = row['track (titel)']
        if pd.notna(track_name) and str(track_name).strip():
            closest_track, track_similarity = find_closest_match(track_name, actual_files)
            if track_similarity < 100:  # Если есть различия
                differences = find_char_differences(str(track_name), str(closest_track))
                all_results.append({
                    'Тип файла': 'Трек',
                    'Название в Excel': track_name,
                    'Найден в папке': closest_track if closest_track else 'Не найден',
                    'Ближайшее совпадение': closest_track if closest_track else '',
                    'Процент сходства': round(track_similarity, 2),
                    'Различия': differences
                })

        # Проверяем обложки
        cover_name = row['cover (titel)']
        if pd.notna(cover_name) and str(cover_name).strip():
            closest_cover, cover_similarity = find_closest_match(cover_name, actual_files)
            if cover_similarity < 100:  # Если есть различия
                differences = find_char_differences(str(cover_name), str(closest_cover))
                all_results.append({
                    'Тип файла': 'Обложка',
                    'Название в Excel': cover_name,
                    'Найден в папке': closest_cover if closest_cover else 'Не найден',
                    'Ближайшее совпадение': closest_cover if closest_cover else '',
                    'Процент сходства': round(cover_similarity, 2),
                    'Различия': differences
                })

    # Создаем DataFrame из результатов
    results_df = pd.DataFrame(all_results)
    
    # Создаем имя выходного файла с текущей датой и временем
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = results_dir / f"file_comparison_results_{timestamp}.xlsx"
    
    # Сохраняем результаты в новый Excel файл
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        results_df.to_excel(writer, index=False, sheet_name='Результаты')
        
        # Получаем рабочий лист для форматирования
        worksheet = writer.sheets['Результаты']
        
        # Форматирование: выделяем строки с низким процентом сходства
        red_fill = PatternFill(start_color='FFFF0000', end_color='FFFF0000', fill_type='solid')
        yellow_fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
        
        # Автоматическая ширина столбцов
        for column in worksheet.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2)
            worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
          # Выделяем строки цветом в зависимости от процента сходства
        for row in range(2, len(all_results) + 2):  # +2 because Excel is 1-based and we have header
            similarity = worksheet.cell(row=row, column=5).value  # Колонка с процентом сходства
            if similarity < 50:
                for col in range(1, 7):
                    worksheet.cell(row=row, column=col).fill = red_fill
            elif similarity < 80:
                for col in range(1, 7):
                    worksheet.cell(row=row, column=col).fill = yellow_fill
    
    error_count = len(all_results)
    success_message = f"Найдено {error_count} файлов с различиями" if error_count > 0 else "Все файлы соответствуют записям в Excel"
    
    return {
        'success': True,
        'message': success_message,
        'results_file': str(output_file),
        'error_count': error_count,
        'results_data': all_results    }


def print_debug_info(filename, normalized_filename):
    """Выводит отладочную информацию о нормализации файла"""
    print(f"\nИскомый файл: '{filename}'")
    print(f"Нормализованный файл: '{normalized_filename}'")


def compare_files_interactive():
    """Интерактивная версия для запуска из командной строки"""
    # Получаем абсолютный путь к директории скрипта
    script_dir = Path(__file__).parent.parent
    
    # Пути к файлам
    files_directory = script_dir / 'src' / 'apps' / 'release-parser-5' / 'files'
    excel_file = input("Введите путь к Excel файлу: ")
    
    result = compare_files_with_excel(excel_file, str(files_directory))
    
    if result['success']:
        print(f"\n{result['message']}")
        print(f"Результаты сохранены в файл: {result['results_file']}")
    else:
        print(f"Ошибка: {result['message']}")


if __name__ == "__main__":
    compare_files_interactive()
