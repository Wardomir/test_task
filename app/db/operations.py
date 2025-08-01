from typing import Dict, Any
from sqlmodel import Session, SQLModel, create_engine

from app.config import DATABASE_URL, logger
from app.db.models import NylasMessage
from app.metrics.metrics import track_db_write


engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


async def store_messages_in_db(data: Dict[str, Any], submitter: str = "system") -> int:
    message = NylasMessage(submitter=submitter, data=data)
    
    try:
        with Session(engine) as session:
            session.add(message)
            session.commit()
            session.refresh(message)
            
            track_db_write()
            logger.info(f"Successfully stored message data with ID: {message.id}")
            return message.id
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise e