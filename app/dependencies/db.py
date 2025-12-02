from users.infrastructure.database.db import db_helper


async def get_db():
    async with db_helper.session_dependency() as session:
        yield session
