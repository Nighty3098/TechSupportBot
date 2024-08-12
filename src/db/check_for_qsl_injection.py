import re

from aiogram import types

from config import CHANNEL, bot, dp, logger

# Список паттернов для определения SQL-инъекций
SQL_INJECTION_PATTERNS = [
    r"\b(SELECT|UNION|INSERT|DELETE|UPDATE|DROP|OR|AND)\b",  # SQL ключевые слова
    r"(\b1=1\b|\b0=0\b)",  # Условия, часто используемые в инъекциях
    r"--",  # Комментарий в SQL
    r"#",  # Комментарий в SQL
    r"'",  # Одинарная кавычка
    r'"',  # Двойная кавычка
    r";",  # Точка с запятой
]


async def is_sql_injection_attempt(message_text, username):
    """Проверяет, является ли сообщение попыткой SQL-инъекции."""
    for pattern in SQL_INJECTION_PATTERNS:
        if re.search(pattern, message_text, re.IGNORECASE):
            logger.warning(
                f"SQL Injection attempt detected from user {username}: {message_text}"
            )
            await bot.send_message(
                CHANNEL,
                f"🚨 Warning: SQL Injection attempt detected from user @{username}: {message_text}",
            )

            return True
    return False
