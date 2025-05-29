# silk-stuff

To install dependencies:

```bash
bun install
```

To run:

```bash
bun run app.ts
```

This project was created using `bun init` in bun v1.0.0. [Bun](https://bun.sh) is a fast all-in-one JavaScript runtime.

yarn start:update-releases-shipment-statuses // Переключаем свичи у релизов на этапе new, чтобы отгрузить на ФТП партнера и переносим релиз на этап moderation
yarn start:release-parser-5 // Проверяется наличие файлов из таблицы для отправки релизов и отгружаются в EMD Cloud собирая метаданные релиза из таблицы в формате подходящем для EMD Cloud
python3 compare_files.py // Запуск скрипта сверки названий файлов с таблицей
/Users/mac/Downloads/GoSilk Loader/gosilk-staff1/src/apps/release-parser-5/files/releases.xlsx // локальный путь к таблице с релизами, необходимо указывать адрес фактического нахождения таблицы с релизами
