Лабораторная работа №1. Интеграция Wolfram Alpha API

Описание

Программа подключается к Wolfram Alpha Full Results API и выполняет 15 запросов (10 обязательных из методички + 5 дополнительных). Полные JSON-ответы и извлечённые ключевые данные сохраняются в файлы, ведётся лог выполнения.

Требования

- Python 3.9+
- Аккаунт Wolfram ID и AppID

Установка

1. Перейти в папку проекта:

cd sppr_lab1_wolfram

2. Создать и активировать виртуальное окружение:

python3 -m venv venv
source venv/bin/activate

3. Установить зависимости:

pip install -r requirements.txt

4. Создать config.json из шаблона:

cp config.example.json config.json

5. Открыть config.json и вставить свой AppID в поле app_id.

Запуск

python3 main.py

Программа:

1. Читает конфиг и ключ.
2. Последовательно выполняет 15 запросов к Wolfram Alpha.
3. Сохраняет полные ответы в results/full/<id>.json.
4. Сохраняет извлечённые данные в results/extracted/<id>.txt.
5. Пишет сводку в results/summary.txt и лог в run.log.

Структура проекта

sppr_lab1_wolfram/
    config.json
    config.example.json
    logger.py
    wolfram_client.py
    queries.py
    main.py
    requirements.txt
    results/
        full/
        extracted/
        summary.txt
    run.log
    README.md

Архитектура

- logger.py — единый логгер (файл + консоль).
- wolfram_client.py — класс WolframClient:
    - query() — HTTP GET с обработкой сетевых ошибок и retry;
    - extract_primary() — главный ответ (с fallback, если primary не помечен);
    - extract_plaintext() — все текстовые блоки.
- queries.py — декларативный список запросов.
- main.py — оркестрация, сохранение, сводка.

Список запросов

1. Математика — integrate x^2 sin^3 x dx
2. Фактология — population of Russia 2024
3. Химия — molar mass of H2SO4
4. Физика — kinetic energy of 5kg object at 10m/s
5. География — distance between Moscow and Saint Petersburg
6. Финансы — 100 USD to RUB
7. Время — current time in Kazan
8. Астрономия — distance to Mars
9. Медицина — body mass index 180cm 75kg
10. Лингвистика — translate hello to Russian
11. Математика — derivative of x^3 * ln(x)
12. Химия — balance chemical equation C3H8 + O2 -> CO2 + H2O
13. Физика — speed of light in km/s
14. География — capital of Australia
15. Астрономия — mass of the Sun
