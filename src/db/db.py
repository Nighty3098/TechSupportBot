import asyncio
import datetime
import os
import sqlite3
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Union

from aiogram import types

from config import bot, data, home_dir, logger
from db.check_data import get_data_url
from send_logs import send_log_to_dev

TABLE_MAPPING = {"bug": "bugs", "idea": "suggestions", "bugs": "bugs"}
DEFAULT_STATUS = "Not started"
DATE_FORMAT = "%d-%m-%Y %H:%M:%S"


@contextmanager
def db_cursor(connection: sqlite3.Connection):
    """A context manager for working with the cursor"""
    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        cursor.close()


async def create_connection() -> Optional[sqlite3.Connection]:
    """Creates a connection to the database"""
    tech_support_dir = os.path.join(home_dir, "TechSupport")
    os.makedirs(tech_support_dir, exist_ok=True)

    db_path = os.path.join(tech_support_dir, "TechSupport.db")
    try:
        conn = sqlite3.connect(db_path)
        logger.info(f"Connected to database: {db_path}")
        await create_table(conn)
        return conn
    except Exception as e:
        logger.error(f"Connection error: {e}")
        await send_log_to_dev()
        return None


async def create_table(connection: sqlite3.Connection) -> None:
    """Creates tables in the database"""
    ddl_queries = {
        "bugs": """
            CREATE TABLE IF NOT EXISTS bugs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                user_id TEXT NOT NULL,
                message TEXT NOT NULL,
                data TEXT,
                date TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """,
        "suggestions": """
            CREATE TABLE IF NOT EXISTS suggestions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                user_id TEXT NOT NULL,
                message TEXT NOT NULL,
                data TEXT,
                date TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """,
    }

    try:
        with db_cursor(connection) as cursor:
            for table_name, query in ddl_queries.items():
                cursor.execute(query)
                logger.debug(f"Table {table_name} verified")
        connection.commit()
    except Exception as e:
        logger.error(f"Table creation error: {e}")
        connection.rollback()
        raise


async def save_report_data(
    connection: sqlite3.Connection,
    username: str,
    user_id: str,
    message: types.Message,
    label: str,
) -> None:
    """Saves the report to the database"""
    label = label.upper()
    if label not in ("BUG", "SUGGESTION"):
        logger.error(f"Invalid label: {label}")
        raise ValueError("Invalid report label")

    table_name = "bugs" if label == "BUG" else "suggestions"
    content = message.text or message.caption or "No description provided."
    files = await get_data_url(message)
    date = datetime.datetime.now().strftime(DATE_FORMAT)

    try:
        with db_cursor(connection) as cursor:
            cursor.execute(
                f"""
                INSERT INTO {table_name} 
                    (username, user_id, message, data, date, status)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (username, user_id, content, files, date, DEFAULT_STATUS),
            )
            logger.info(
                "Report saved: User: %s, Type: %s, Chars: %d",
                username,
                label,
                len(content),
            )
        connection.commit()
    except Exception as e:
        logger.error("Failed to save report: %s", str(e))
        connection.rollback()
        await send_log_to_dev()
        raise


async def execute_query(
    connection: sqlite3.Connection, query: str, params: tuple, fetch_one: bool = False
) -> Optional[Union[tuple, List[tuple]]]:
    """Universal query execution function"""
    try:
        with db_cursor(connection) as cursor:
            cursor.execute(query, params)
            return cursor.fetchone() if fetch_one else cursor.fetchall()
    except Exception as e:
        logger.error("Query failed: %s\nQuery: %s\nParams: %s", str(e), query, params)
        await send_log_to_dev()
        return None


async def get_id_by_message(
    connection: sqlite3.Connection,
    message_value: str,
    date: str,
    user_id: str,
    category: str,
) -> Optional[int]:
    """Returns the message ID"""
    table_name = TABLE_MAPPING.get(category.lower())
    if not table_name:
        logger.error("Invalid category: %s", category)
        return None

    query = f"""
        SELECT id FROM {table_name}
        WHERE message = ? AND date = ? AND user_id = ?
    """
    result = await execute_query(
        connection, query, (message_value, date, user_id), fetch_one=True
    )
    return result[0] if result else None


async def update_ticket_status(
    connection: sqlite3.Connection, ticket_id: int, new_status: str, category: str
) -> bool:
    """Updates the ticket status"""
    table_name = TABLE_MAPPING.get(category.lower())
    if not table_name:
        logger.error("Invalid category: %s", category)
        return False

    query = f"UPDATE {table_name} SET status = ? WHERE id = ?"
    try:
        with db_cursor(connection) as cursor:
            cursor.execute(query, (new_status, ticket_id))
            connection.commit()
            logger.info(
                "Status updated: Ticket %d, New status: %s", ticket_id, new_status
            )
            return cursor.rowcount > 0
    except Exception as e:
        logger.error("Status update failed: %s", str(e))
        connection.rollback()
        return False


async def get_ticket_info(
    connection: sqlite3.Connection, ticket_id: int, category: str, field: str
) -> Optional[Any]:
    """A universal method for obtaining information about a ticket"""
    table_name = TABLE_MAPPING.get(category.lower())
    if not table_name or field not in ("user_id", "status"):
        logger.error("Invalid parameters: %s, %s", category, field)
        return None

    query = f"SELECT {field} FROM {table_name} WHERE id = ?"
    result = await execute_query(connection, query, (ticket_id,), fetch_one=True)
    return result[0] if result else None


async def get_user_id_by_message(
    connection: sqlite3.Connection, ticket_id: int, category: str
) -> Optional[int]:
    """Returns the user's ID by etiquette"""
    return await get_ticket_info(connection, ticket_id, category, "user_id")


async def get_ticket_status(
    connection: sqlite3.Connection, ticket_id: int, category: str
) -> Optional[str]:
    """Returns the ticket status"""
    return await get_ticket_info(connection, ticket_id, category, "status")


async def get_all_tickets(connection: sqlite3.Connection) -> List[Dict]:
    """Returns all tickets"""
    query = """
        SELECT 'bugs' as category, id, status, message, user_id, username FROM bugs
        UNION ALL
        SELECT 'suggestions' as category, id, status, message, user_id, username FROM suggestions
    """

    tickets = []
    results = await execute_query(connection, query, ())
    if results:
        for row in results:
            tickets.append(
                {
                    "category": row[0],
                    "id": row[1],
                    "status": row[2],
                    "message": row[3],
                    "user_id": row[4],
                    "username": row[5],
                }
            )
    return tickets
