"""
Список запросов к Wolfram Alpha.

10 обязательных из методички + 5 дополнительных на выбор.
Каждый запрос — словарь с полями:
  - id:       короткий идентификатор (для имени файла)
  - category: категория (математика, факт, химия и т.д.)
  - text:     сам текст запроса к Wolfram Alpha
"""

QUERIES = [
    # === 10 обязательных из методички ===
    {
        "id": "01_math_integral",
        "category": "Математика",
        "text": "integrate x^2 sin^3 x dx",
    },
    {
        "id": "02_fact_population",
        "category": "Фактология",
        "text": "population of Russia 2024",
    },
    {
        "id": "03_chem_molar_mass",
        "category": "Химия",
        "text": "molar mass of H2SO4",
    },
    {
        "id": "04_phys_kinetic_energy",
        "category": "Физика",
        "text": "kinetic energy of 5kg object at 10m/s",
    },
    {
        "id": "05_geo_distance",
        "category": "География",
        "text": "distance between Moscow and Saint Petersburg",
    },
    {
        "id": "06_fin_currency",
        "category": "Финансы",
        "text": "100 USD to RUB",
    },
    {
        "id": "07_time_kazan",
        "category": "Время",
        "text": "current time in Kazan",
    },
    {
        "id": "08_astro_mars",
        "category": "Астрономия",
        "text": "distance to Mars",
    },
    {
        "id": "09_med_bmi",
        "category": "Медицина",
        "text": "body mass index 180cm 75kg",
    },
    {
        "id": "10_lang_translate",
        "category": "Лингвистика",
        "text": "translate hello to Russian",
    },

    # === 5 дополнительных на выбор ===
    {
        "id": "11_math_derivative",
        "category": "Математика",
        "text": "derivative of x^3 * ln(x)",
    },
    {
        "id": "12_chem_reaction",
        "category": "Химия",
        "text": "balance chemical equation C3H8 + O2 -> CO2 + H2O",
    },
    {
        "id": "13_phys_speed_of_light",
        "category": "Физика",
        "text": "speed of light in km/s",
    },
    {
        "id": "14_geo_capital",
        "category": "География",
        "text": "capital of Australia",
    },
    {
        "id": "15_astro_sun_mass",
        "category": "Астрономия",
        "text": "mass of the Sun",
    },
]
