"""
Точка входа лабораторной работы №1.

Выполняет 15 запросов к Wolfram Alpha Full Results API,
сохраняет полные и извлечённые ответы, ведёт лог.
"""
import json
import sys
from pathlib import Path

import requests

from logger import setup_logger
from queries import QUERIES
from wolfram_client import WolframClient, WolframAPIError


# Пути проекта
BASE_DIR = Path(__file__).parent
CONFIG_PATH = BASE_DIR / "config.json"
RESULTS_FULL = BASE_DIR / "results" / "full"
RESULTS_EXTRACTED = BASE_DIR / "results" / "extracted"


def load_config(path: Path) -> dict:
    """Загружает конфиг из JSON."""
    if not path.exists():
        raise FileNotFoundError(
            f"Не найден файл конфигурации: {path}\n"
            f"Скопируйте config.example.json в config.json и вставьте AppID."
        )
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict) -> None:
    """Сохраняет словарь в JSON-файл с отступами."""
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_text(path: Path, lines: list[str]) -> None:
    """Сохраняет список строк в текстовый файл."""
    with path.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main() -> int:
    log = setup_logger()
    log.info("=" * 60)
    log.info("Лабораторная работа №1: Wolfram Alpha API")
    log.info("=" * 60)

    # 1. Готовим папки
    RESULTS_FULL.mkdir(parents=True, exist_ok=True)
    RESULTS_EXTRACTED.mkdir(parents=True, exist_ok=True)

    # 2. Читаем конфиг
    try:
        config = load_config(CONFIG_PATH)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        log.error("Ошибка конфигурации: %s", e)
        return 1

    # 3. Создаём клиент
    client = WolframClient(
        app_id=config["app_id"],
        timeout=config.get("timeout", 10),
    )

    # 4. Проходим по всем запросам
    summary = []
    ok_count = 0
    error_count = 0

    for i, q in enumerate(QUERIES, start=1):
        log.info("[%d/%d] %s: %s", i, len(QUERIES), q["category"], q["text"])
        try:
            data = client.query(q["text"])

            # Сохраняем полный ответ
            full_path = RESULTS_FULL / f"{q['id']}.json"
            save_json(full_path, data)

            # Извлекаем ключевые данные
            primary = client.extract_primary(data)
            all_texts = client.extract_plaintext(data)

            extracted_lines = [
                f"Категория: {q['category']}",
                f"Запрос:    {q['text']}",
                "",
                "--- Главный ответ ---",
                primary if primary else "(не найден)",
                "",
                "--- Все текстовые блоки ---",
                *all_texts,
            ]

            extracted_path = RESULTS_EXTRACTED / f"{q['id']}.txt"
            save_text(extracted_path, extracted_lines)

            log.info("    ✓ primary: %s", primary[:80] if primary else "(пусто)")
            summary.append((q["id"], "OK", primary[:60]))
            ok_count += 1

        except WolframAPIError as e:
            log.error("    ✗ Ошибка API: %s", e)
            summary.append((q["id"], "API_ERROR", str(e)[:60]))
            error_count += 1

        except requests.RequestException as e:
            log.error("    ✗ Сетевая ошибка: %s", e)
            summary.append((q["id"], "NET_ERROR", str(e)[:60]))
            error_count += 1

        except Exception as e:  # noqa: BLE001
            log.exception("    ✗ Непредвиденная ошибка: %s", e)
            summary.append((q["id"], "UNKNOWN", str(e)[:60]))
            error_count += 1

    # 5. Итоговая сводка
    log.info("=" * 60)
    log.info("ИТОГО: успешно %d, с ошибками %d, всего %d",
             ok_count, error_count, len(QUERIES))
    log.info("Полные ответы:    %s", RESULTS_FULL)
    log.info("Извлечённые данные: %s", RESULTS_EXTRACTED)
    log.info("=" * 60)

    # Сохраняем сводку
    summary_path = BASE_DIR / "results" / "summary.txt"
    save_text(
        summary_path,
        [f"{qid:25s} | {status:10s} | {note}" for qid, status, note in summary],
    )
    log.info("Сводка сохранена: %s", summary_path)

    return 0 if error_count == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
