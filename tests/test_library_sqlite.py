import os

from tests.database.postgres.test_database import TestPostgres
from .base_library import TestDatabaseFaq


class TestLibraryFaqSqlite(TestDatabaseFaq, TestPostgres):
    async def setUp(self):
        await super().setUp()
        sqlFile = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'database-sqlite.sql')
        with open(sqlFile) as f:
            await self.execute(f.read())
        await self.setUpInsert()
