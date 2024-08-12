import re

from aiogram import types

from config import CHANNEL, bot, dp, logger

# List of patterns to define SQL injections
SQL_INJECTION_PATTERNS = [
    r"\b(SELECT|UNION|INSERT|DELETE|UPDATE|DROP|OR|AND)\b",  # SQL keywords
    r"(\b1=1\b|\b0=0\b)",  # Conditions commonly used in injections
    r"--",  # Comment in SQL
    r"#",  # Comment in SQL
    r"'",  # Single inverted comma
    r'"',  # Double inverted comma
    r";",  # Semicolon
]


async def is_sql_injection_attempt(message_text, username):
    """Checks if the message is an SQL injection attempt."""
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
