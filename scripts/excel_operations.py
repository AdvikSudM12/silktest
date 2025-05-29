import os
import pandas as pd
from openpyxl import load_workbook

# Пути к файлам
main_file = '/Users/mac/Downloads/gosilk-staff1/src/apps/release-parser-5/files/releases.xlsx'
error_file = '/Users/mac/Downloads/gosilk-staff1/results/file_comparison_results_2025-02-05_01-55-06.xlsx'

try:
    # Читаем файл с ошибками с помощью pandas
    error_df = pd.read_excel(error_file, sheet_name='Отсутствующие файлы')
    
    # Выводим первые несколько строк файла с ошибками для проверки
    print("Первые строки из файла с ошибками:")
    print(error_df.head())
    print("\nКолонки в файле с ошибками:")
    print(error_df.columns.tolist())
    
    # Собираем список названий треков с ошибками
    error_tracks = set()
    for _, row in error_df.iterrows():
        if pd.notna(row['Название в Excel']):  # Проверяем, что значение не NaN
            track_name = str(row['Название в Excel']).strip()
            error_tracks.add(track_name)
            print(f"Найден трек с ошибкой: {track_name}")
    
    print(f"\nВсего найдено {len(error_tracks)} треков с ошибками")
    
    # Открываем основной файл
    main_wb = load_workbook(main_file)
    if "Лист1" not in main_wb.sheetnames:
        raise ValueError("Лист 'Лист1' не найден в основном файле.")
    
    main_sheet = main_wb["Лист1"]
    
    # Выводим первые несколько строк основного файла для проверки
    print("\nПервые строки из основного файла:")
    for idx, row in enumerate(main_sheet.iter_rows(min_row=1, max_row=3, values_only=True)):
        print(f"Строка {idx + 1}: {row[0] if row else 'Пустая строка'}")
    
    # Создаем или очищаем лист для ошибок
    if "Ошибки_загрузки_05.02.25" in main_wb.sheetnames:
        main_wb.remove(main_wb["Ошибки_загрузки_05.02.25"])
    error_sheet_new = main_wb.create_sheet("Ошибки_загрузки_05.02.25")
    
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
                print(f"Найдено совпадение: {current_track}")
                error_sheet_new.append(row)
                rows_to_delete.append(row_idx)
    
    # Удаляем строки с конца, чтобы не сбить нумерацию
    for row_idx in reversed(rows_to_delete):
        main_sheet.delete_rows(row_idx)
    
    # Сохраняем изменения
    main_wb.save(main_file)
    
    print("\nОперация успешно выполнена!")
    print(f"Перенесено {len(rows_to_delete)} строк с ошибками")
    print("Строки перемещены в лист 'Ошибки_загрузки_05.02.25'")

except Exception as e:
    print(f"Произошла ошибка: {str(e)}")
    print("Пути к файлам:")
    print(f"Основной файл: {main_file}")
    print(f"Файл с ошибками: {error_file}")
