import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from setproctitle import setproctitle

from src.config import TOKEN
from src.handlers import register_handlers
from src.db.database import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

async def main():
    try:
        await init_db()
        
        bot = Bot(
            token=TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2)
        )
        dp = Dispatcher()
        
        register_handlers(dp)
        
        logger.info("Starting bot...")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setproctitle("TechSupportBot")
    asyncio.run(main())
