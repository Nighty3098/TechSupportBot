import asyncio
import datetime
import os
import sqlite3

from aiogram import types
from aiogram.types import Message

from config import bot, data, home_dir, logger
from db.check_data import get_data_url
from send_logs import send_log_to_dev


async def create_connection():
    """Creates connection to SQL DB"""
    tech_support_dir = os.path.join(home_dir, "TechSupport")

    if not os.path.exists(tech_support_dir):
        os.makedirs(tech_support_dir)
        logger.debug(f"Created directory: {tech_support_dir}")

    connection = None
    try:
        db_path = os.path.join(tech_support_dir, "TechSupport.db")
        connection = sqlite3.connect(db_path)
        logger.debug(f"Connected to SQL DB at {db_path}")
    except Exception as e:
        logger.error(f"Error '{e}' while connecting to SQL DB at {db_path}")

    return connection


async def create_table(connection):
    """Create table if not exists"""
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS bugs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        message TEXT,
        data TEXT,
        date TEXT
        )
        """
        )

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS suggestions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        message TEXT,
        data TEXT,
        date TEXT
        )
        """
        )

        connection.commit()
        connection.close()

        logger.debug(f"Table created successfully")
    except Exception as e:
        logger.error(f"Error '{e}' while creating table")


async def save_report_data(
    connection, username, message: types.Message, label, text_message
):
    """Saving reports to DB"""
    try:
        cursor = connection.cursor()

        files = await get_data_url(message)

        current_datetime = datetime.datetime.now()
        responsdate = current_datetime.strftime("%d-%m-%Y %H:%M:%S")

        if label == "BUG":
            cursor.execute(
                "INSERT INTO bugs (username, message, data, date) VALUES (?, ?, ?, ?)",
                (username, text_message, files, responsdate),
            )
        elif label == "SUGGESTION":
            cursor.execute(
                "INSERT INTO suggestions (username, message, data, date) VALUES (?, ?, ?, ?)",
                (username, text_message, files, responsdate),
            )
        else:
            raise ValueError("Invalid label")

        connection.commit()
        connection.close()

    except Exception as e:
        logger.error(f"Error '{e}' while saving report data")
