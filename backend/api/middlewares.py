from typing import Any
from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.ext import Base
from config import get_current_config
from core.neo4j.connector import Neo4jDBConnector


engine = create_async_engine(get_current_config().DATABASE_URI, echo=True)
_base_model_session_ctx: ContextVar = ContextVar("session")


async def create_db_engine(app: Any, loop: Any) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def inject_session(request: Any) -> None:
    request.ctx.session = sessionmaker(engine, AsyncSession, expire_on_commit=False)()
    request.ctx.neo4j = Neo4jDBConnector("bolt://localhost:7687", "neo4j", "12345678")
    request.ctx.session_ctx_token = _base_model_session_ctx.set(request.ctx.session)


async def close_session(request: Any, response: Any) -> None:
    if hasattr(request.ctx, "session_ctx_token"):
        _base_model_session_ctx.reset(request.ctx.session_ctx_token)
        await request.ctx.session.close()
