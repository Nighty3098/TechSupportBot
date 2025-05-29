from datetime import datetime
from typing import List, Optional, Union

from aiogram import types
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from config import logger
from db.check_data import get_data_url
from db.models import Bug, Suggestion
from send_logs import send_log_to_dev

TABLE_MAPPING = {"bug": Bug, "suggestion": Suggestion, "bugs": Bug}
DEFAULT_STATUS = "Not started"


async def save_report_data(
    session: AsyncSession,
    username: str,
    user_id: str,
    message: types.Message,
    label: str,
) -> None:
    label = label.upper()
    if label not in ("BUG", "SUGGESTION"):
        logger.error(f"Invalid label: {label}")
        raise ValueError("Invalid report label")

    model = Bug if label == "BUG" else Suggestion
    content = message.text or message.caption or "No description provided."
    files = await get_data_url(message)
    date = datetime.now()

    try:
        new_report = model(
            username=username,
            user_id=user_id,
            message=content,
            data=files,
            date=date,
            status=DEFAULT_STATUS,
        )
        session.add(new_report)
        await session.commit()
        logger.info(
            "Report saved: User: %s, Type: %s, Chars: %d",
            username,
            label,
            len(content),
        )
    except Exception as e:
        logger.error("Failed to save report: %s", str(e))
        await session.rollback()
        await send_log_to_dev()
        raise


async def get_id_by_message(
    session: AsyncSession,
    message_value: str,
    date: datetime,
    user_id: str,
    category: str,
) -> Optional[int]:
    model = TABLE_MAPPING.get(category.lower())
    if not model:
        logger.error("Invalid category: %s", category)
        return None

    query = select(model.id).where(
        model.message == message_value,
        model.date == date,
        model.user_id == user_id,
    )
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def update_ticket_status(
    session: AsyncSession, ticket_id: int, new_status: str, category: str
) -> bool:
    model = TABLE_MAPPING.get(category.lower())
    if not model:
        logger.error("Invalid category: %s", category)
        return False

    try:
        query = (
            update(model)
            .where(model.id == ticket_id)
            .values(status=new_status)
        )
        result = await session.execute(query)
        await session.commit()
        logger.info(
            "Status updated: Ticket %d, New status: %s", ticket_id, new_status
        )
        return result.rowcount > 0
    except Exception as e:
        logger.error("Status update failed: %s", str(e))
        await session.rollback()
        return False


async def get_ticket_info(
    session: AsyncSession, ticket_id: int, category: str, field: str
) -> Optional[Union[str, int]]:
    model = TABLE_MAPPING.get(category.lower())
    if not model or field not in ("user_id", "status"):
        logger.error("Invalid parameters: %s, %s", category, field)
        return None

    query = select(getattr(model, field)).where(model.id == ticket_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_user_id_by_message(
    session: AsyncSession, ticket_id: int, category: str
) -> Optional[str]:
    return await get_ticket_info(session, ticket_id, category, "user_id")


async def get_ticket_status(
    session: AsyncSession, ticket_id: int, category: str
) -> Optional[str]:
    return await get_ticket_info(session, ticket_id, category, "status")


async def get_all_tickets(session: AsyncSession) -> List[dict]:
    tickets = []
    
    bug_query = select(Bug)
    bug_results = await session.execute(bug_query)
    for bug in bug_results.scalars():
        tickets.append({
            "category": "bugs",
            "id": bug.id,
            "status": bug.status,
            "message": bug.message,
            "user_id": bug.user_id,
            "username": bug.username,
        })
    
    suggestion_query = select(Suggestion)
    suggestion_results = await session.execute(suggestion_query)
    for suggestion in suggestion_results.scalars():
        tickets.append({
            "category": "suggestions",
            "id": suggestion.id,
            "status": suggestion.status,
            "message": suggestion.message,
            "user_id": suggestion.user_id,
            "username": suggestion.username,
        })
    
    return tickets 
