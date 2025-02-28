import asyncio
import datetime
import os
import sqlite3

from aiogram import types

from config import bot, data, home_dir, logger
from db.check_data import get_data_url
from send_logs import send_log_to_dev


async def create_connection():
    """Creates connection to SQL DB"""
    tech_support_dir = os.path.join(home_dir, "TechSupport")

    if not os.path.exists(tech_support_dir):
        os.makedirs(tech_support_dir)
        logger.info(f"Created directory: {tech_support_dir}")

    db_path = os.path.join(tech_support_dir, "TechSupport.db")
    try:
        connection = sqlite3.connect(db_path)
        logger.info(f"Connected to SQL DB at {db_path}")
        return connection
    except Exception as e:
        logger.error(f"Error '{e}' while connecting to SQL DB at {db_path}")
        return None


async def create_table(connection):
    """Create tables if they do not exist"""
    try:
        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS bugs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            user_id TEXT,
            message TEXT,
            data TEXT,
            date TEXT,
            status TEXT
            )"""
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS suggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            user_id TEXT,
            message TEXT,
            data TEXT,
            date TEXT,
            status TEXT
            )"""
        )
        connection.commit()
        logger.info("Tables created successfully")
    except Exception as e:
        logger.error(f"Error '{e}' while creating tables")


async def save_report_data(
    connection, username: str, user_id: str, message: types.Message, label: str
):
    """Saving reports to DB"""
    cursor = connection.cursor()
    files = await get_data_url(message)
    current_datetime = datetime.datetime.now()
    responsdate = current_datetime.strftime("%d-%m-%Y %H:%M:%S")

    text_message = message.text or message.caption or "No description provided."

    if label in ["BUG", "SUGGESTION"]:
        table_name = "bugs" if label == "BUG" else "suggestions"
        cursor.execute(
            f"INSERT INTO {table_name} (username, user_id, message, data, date, status) VALUES (?, ?, ?, ?, ?, ?)",
            (username, user_id, text_message, files, responsdate, "Not started"),
        )
    else:
        raise ValueError("Invalid label")

    connection.commit()


async def get_id_by_message(
    connection, message_value: str, date: str, user_id: str, category: str
):
    cursor = connection.cursor()
    table_name = {"bug": "bugs", "idea": "suggestions", "bugs": "bugs"}.get(
        category.lower()
    )

    if table_name is None:
        logger.error(f"Invalid category: {category}")
        return None

    logger.info(
        f"Getting id from {table_name} where message = ?, date = ?, user_id = ?"
    )

    try:
        cursor.execute(
            f"SELECT id FROM {table_name} WHERE message = ? AND date = ? AND user_id = ?",
            (message_value, date, user_id),
        )
        result = cursor.fetchone()
        logger.info(f"Query result: {result}")
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        await send_log_to_dev()
        return None

    return result[0] if result else None


async def update_ticket_status(
    connection, ticket_id: int, new_status: str, category: str
):
    cursor = connection.cursor()
    table_name = {"bug": "bugs", "idea": "suggestions", "bugs": "bugs"}.get(
        category.lower()
    )

    if table_name is None:
        logger.error(f"Invalid category: {category}")
        await send_log_to_dev()
        return False

    logger.info(
        f"Updating status for {table_name} with id = '{ticket_id}' to '{new_status}'"
    )

    try:
        cursor.execute(
            f"UPDATE {table_name} SET status = ? WHERE id = ?", (new_status, ticket_id)
        )
        connection.commit()
        logger.info(
            f"Updated status for {table_name} with id = '{ticket_id}' to '{new_status}'"
        )
    except Exception as e:
        logger.error(f"Error updating ticket status: {e}")
        await send_log_to_dev()
        return False

    return True


async def get_user_id_by_message(connection, ticket_id: str, category: str):
    cursor = connection.cursor()
    table_name = {"bug": "bugs", "idea": "suggestions", "bugs": "bugs"}.get(
        category.lower()
    )

    if table_name is None:
        logger.error(f"Invalid category: {category}")
        return None

    logger.info(f"Getting user_id from {table_name} where id = ?")

    try:
        cursor.execute(f"SELECT user_id FROM {table_name} WHERE id = ?", (ticket_id,))
        result = cursor.fetchone()
        logger.info(f"Query result: {result}")
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        await send_log_to_dev()
        return None

    return result[0] if result else None


async def get_ticket_status(connection, ticket_id: str, category: str):
    cursor = connection.cursor()
    table_name = {"bug": "bugs", "idea": "suggestions", "bugs": "bugs"}.get(
        category.lower()
    )

    if table_name is None:
        logger.error(f"Invalid category: {category}")
        return None

    logger.info(f"Getting status from {table_name} where id = ?")

    try:
        cursor.execute(f"SELECT status FROM {table_name} WHERE id = ?", (ticket_id,))
        result = cursor.fetchone()
        logger.info(f"Query result: {result}")

        if result:
            return result[0]
        else:
            logger.warning(f"No status found for ticket id: {ticket_id}")
            return None
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        await send_log_to_dev()
        return None


async def get_all_tickets(connection):
    tickets = []
    queries = {
        "bugs": "SELECT id, status, message, user_id, username FROM bugs",
        "suggestions": "SELECT id, status, message, user_id, username FROM suggestions",
    }

    try:
        for category, query in queries.items():
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()

            for row in results:
                ticket_id, status, message, user_id, username = row
                tickets.append(
                    {
                        "id": ticket_id,
                        "category": category,
                        "status": status,
                        "message": message,
                        "user_id": user_id,
                        "username": username,
                    }
                )

    except Exception as e:
        logger.error(f"Error fetching tickets: {e}")
        await send_log_to_dev()

    return tickets
