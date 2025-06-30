from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)


from core import settings
from core.models import Base


class DatabaseManager:
    def __init__(self, db_url: str, db_echo: bool = False):
        self.engine = create_async_engine(
            url=db_url,
            echo=db_echo,
        )

        self.session_factory = async_sessionmaker(
            self.engine,
            autoflush=False,
            expire_on_commit=False,
        )

    async def create_tables(self):
        async with self.engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_scoped_dep(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()

    async def session_dep(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session


db_manager = DatabaseManager(
    db_url=settings.db_url,
)
