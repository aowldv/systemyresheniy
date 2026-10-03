"""
Модуль для работы с Wolfram Alpha Full Results API.

Инкапсулирует HTTP-запросы, обработку ошибок и извлечение
ключевых данных из JSON-ответа.
"""
import json
import logging
from typing import Any

import requests

logger = logging.getLogger("wolfram_lab")


class WolframAPIError(Exception):
    """Исключение для ошибок на стороне Wolfram Alpha API."""
    pass


class WolframClient:
    """Клиент для работы с Wolfram Alpha Full Results API."""

    BASE_URL = "https://api.wolframalpha.com/v2/query"

    def __init__(self, app_id: str, timeout: int = 10):
        """
        :param app_id: AppID из личного кабинета Wolfram
        :param timeout: таймаут HTTP-запроса в секундах
        """
        if not app_id:
            raise ValueError("AppID не может быть пустым")
        self.app_id = app_id
        self.timeout = timeout

    def query(self, input_text: str) -> dict[str, Any]:
        """
        Выполняет один запрос к Wolfram Alpha.

        :param input_text: текст запроса (например, "integrate x^2 sin^3 x dx")
        :return: распарсенный JSON-ответ API
        :raises WolframAPIError: если API вернул ошибку
        :raises requests.RequestException: при сетевой ошибке
        """
        params = {
            "input": input_text,
            "format": "plaintext",   # просим текстовый формат ответа
            "output": "json",        # ответ в JSON
            "appid": self.app_id,
        }

        logger.debug("Отправка запроса: %s", input_text)

        try:
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=self.timeout,
            )
        except requests.RequestException as e:
            logger.error("Сетевая ошибка при запросе '%s': %s", input_text, e)
            raise

        # Проверка HTTP-статуса
        if response.status_code != 200:
            raise WolframAPIError(
                f"HTTP {response.status_code}: {response.text[:200]}"
            )

        try:
            data = response.json()
        except json.JSONDecodeError as e:
            raise WolframAPIError(f"Не удалось распарсить JSON: {e}")

        # Wolfram может вернуть success=false с описанием ошибки
        query_result = data.get("queryresult", {})
        if not query_result.get("success", False):
            error_msg = query_result.get("error", {}).get("msg", "unknown error")
            logger.warning("API вернул success=false: %s", error_msg)

        return data

    @staticmethod
    def extract_plaintext(data: dict[str, Any]) -> list[str]:
        """
        Извлекает все plaintext-строки из ответа API.

        Wolfram разбивает ответ на "pods" (блоки), внутри каждого — "subpods".
        Нам нужны текстовые значения subpod'ов.

        :param data: JSON-ответ от API
        :return: список строк с ответами
        """
        result: list[str] = []
        query_result = data.get("queryresult", {})
        pods = query_result.get("pods", [])

        for pod in pods:
            pod_title = pod.get("title", "")
            for subpod in pod.get("subpods", []):
                text = subpod.get("plaintext", "").strip()
                if text:
                    result.append(f"[{pod_title}] {text}")

        return result

    @staticmethod
    @staticmethod
    def extract_primary(data: dict[str, Any]) -> str:
        """
        Извлекает главный (primary) ответ, если он есть.
        Если primary-блока нет — возвращает первый непустой plaintext
        (fallback для запросов вроде "translate ...", где Wolfram
        не помечает блок как primary, но данные есть).
        """
        query_result = data.get("queryresult", {})
        pods = query_result.get("pods", [])

        # 1) Ищем блок с флагом primary
        for pod in pods:
            if pod.get("primary", False):
                for subpod in pod.get("subpods", []):
                    text = subpod.get("plaintext", "").strip()
                    if text:
                        return text

        # 2) Fallback: берём первый непустой plaintext
        #    (пропускаем блок "Input interpretation" — это эхо запроса)
        for pod in pods:
            title = pod.get("title", "").lower()
            if "input interpretation" in title:
                continue
            for subpod in pod.get("subpods", []):
                text = subpod.get("plaintext", "").strip()
                if text:
                    return text

        return ""
