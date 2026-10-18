# Переводы сюжета Arknights — ru_RU

Русские переводы сценариев для Zoot Archive. Один CSV = одна глава (level) сценария.

## Структура

```
translation/ru_RU/
├── <episode>/                      # папка = ID эпизода/главы в игре
│   └── <storyBaseName>_<translator>.csv
├── episodes.json                   # снимок структуры (файлы и переводчики по эпизодам)
└── README.md
```

`<episode>` — это ID эпизода из игровых данных, ровно как в пути сценария:
`main`, `a001`, `act47side`, `act15d5`, `act10mini`, `st`, `spst`, `ui`, `guide`.
Сейчас 79 папок и 1756 CSV. В корне `ru_RU/` CSV больше не лежат.

`<storyBaseName>` — базовое имя сценария без расширения (последний сегмент пути
`.../activities/act19side/level/act19side_sub-1-1.txt` → `act19side_sub-1-1`).

`<translator>` — ник переводчика из реестра приложения: `neksi0762`, `num4ar`,
`naoshka_v`, `ilarhion`, `frostymisery17`, `nep0num`. Исторический алиас `neponum`
в приложении нормализуется в `nep0num`.

## Формат CSV

```
ID,Character,Original Text,Reference,Translation
__translator__,,Translator,,nep0num
__language__,,Language,en_US,ru_RU
__episode__,,Episode ID,,act19side          # необязательно, заполняется для side-историй
__chapter__,,Chapter Name,activities/...,困心
char-1,？？？,？？？,???,???
char-2,赏金猎人,赏金猎人,Bounty Hunter,Охотник за головами
line-1,阿米娅,阿米娅,Amiya,Амия
```

- Строки `__translator__` и `__language__` обязательны — по ним приложение определяет
  профиль переводчика.
- Пустая ячейка `Translation` означает «ещё не переведено»: приложение показывает
  оригинал.
- Первая колонка (`ID`) — ключ сопоставления со сценарием: `char-N` — реплики персонажа,
  `line-N` — обычный текст. Менять её нельзя, иначе перевод перестанет применяться.

## Как приложение ищет файл

`Zoot Archive` строит список кандидатов в `src/utils/translationPaths.ts`
(`getTranslationCsvCandidates`) и проверяет их по порядку:

1. `translation/ru_RU/<episode>/<storyBaseName>_<translator>.csv` — текущая раскладка;
2. `translation/ru_RU/<storyBaseName>_<translator>.csv` — старый плоский путь;
3. те же два пути без суффикса переводчика (общественный перевод).

Плоский фолбэк нужен, потому что Discord-бот до сих пор заливает новые файлы в корень
языковой папки. Новые файлы можно класть в папку эпизода — приложение найдёт их и так,
и по старому пути.

## Правила для контрибьюторов

1. Кладите файл в папку своего эпизода, имя не меняйте: `<storyBaseName>_<translator>.csv`.
2. Не трогайте чужие файлы: один переводчик — один файл на главу.
3. Терминология — только по канону из `glossary.json` этого репозитория
   (человекочитаемая сводка решений — `ASSISTANT/lore/glossary.md`,
   приложение дополнительно держит `ARKNIGHTS_CANONICAL_GLOSSARY`).
4. Не переводите `ID`-колонку и служебные `__*__`-строки.
5. Мёртвые дубли (файл без строк `line-`) удаляйте отдельным коммитом.
6. Тире — `—`, кавычки — « », обращение на «Вы» с большой буквы, ё обязательна,
   многоточие — `...` (ровно три точки).

## Порядок правки эпизода (инструменты в `tools/`)

```bash
python3 tools/normalize_csv.py <эпизод> --apply     # невидимые символы, пробелы, тире, многоточия
python3 tools/apply_glossary.py <эпизод> --names --unquote \
    --terms infected,knights_treasure,village_dewville,surzahar_language --apply
python3 tools/apply_patch.py <эпизод> --apply       # точечные правки текста
python3 tools/collect_names.py --episode <эпизод>  # аудит подписей говорящих
```

- `normalize_csv.py` и `apply_glossary.py` правят **только** колонку `Translation`
  и подписи `char-N`; CN/EN/ID не трогаются. CRLF-окончания строк сохраняются.
- `apply_glossary.py` без `--names`/`--unquote` применяет только термины.
- `tools/patches/<эпизод>.py` — список правок текста: `(файл, ID строки, было, стало)`.
  Если «было» не найдено, патч падает с конфликтом и этот файл не записывается.
  Повторный запуск безопасен: уже применённые правки считаются успехом.
- `glossary.json` — машинный канон: `terms` (термины), `names.entries` (подписи говорящих).

## Проверка после правок

```bash
# в клоне Zoot-ARCHIVE
npx tsx scripts/verify_translation_paths.ts /путь/к/zoot-data
```

Скрипт обязан напечатать `Не найдено загрузчиком: 0`.