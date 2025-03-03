import re
from typing import List, Pattern

from aiogram import types

from config import CHANNEL, bot, dp, logger

SQL_INJECTION_PATTERNS: List[Pattern[str]] = [
    re.compile(r"\b(SELECT|UNION|INSERT|DELETE|UPDATE|DROP|OR|AND)\b", re.IGNORECASE),  # SQL keywords
    re.compile(r"(\b1=1\b|\b0=0\b)", re.IGNORECASE),  # Conditions commonly used in injections
    re.compile(r"--"),  # Comment in SQL
    re.compile(r"#"),  # Comment in SQL
    re.compile(r"'"),  # Single inverted comma
    re.compile(r'"'),  # Double inverted comma
    re.compile(r";"),  # Semicolon
]

async def is_sql_injection_attempt(message_text: str, username: str) -> bool:
    """
    Checks if the message is an SQL injection attempt.

    Args:
        message_text (str): The text of the message to check.
        username (str): The username of the sender.

    Returns:
        bool: True if an SQL injection attempt is detected, otherwise False.
    """
    for pattern in SQL_INJECTION_PATTERNS:
        if pattern.search(message_text):
            logger.warning(
                f"SQL Injection attempt detected from user {username}: {message_text}"
            )
            await bot.send_message(
                CHANNEL,
                f"🚨 Warning: SQL Injection attempt detected from user @{username}: {message_text}",
            )
            return True
    return False
