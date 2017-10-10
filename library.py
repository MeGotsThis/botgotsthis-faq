from typing import Any, Optional, Tuple  # noqa: F401

import aioodbc.cursor  # noqa: F401

from lib.database import DatabaseMain


async def getFaq(database: DatabaseMain,
                 channel: str) -> Optional[str]:
    cursor: aioodbc.cursor.Cursor
    async with await database.cursor() as cursor:
        query: str = 'SELECT faq FROM faq WHERE broadcaster=?'
        await cursor.execute(query, (channel,))
        return (await cursor.fetchone() or [None])[0]


async def getGameFaq(database: DatabaseMain,
                     channel: str,
                     game: str) -> Optional[str]:
    cursor: aioodbc.cursor.Cursor
    async with await database.cursor() as cursor:
        query: str = '''
SELECT faq FROM faq_game WHERE broadcaster=? AND twitchGame=?'''
        await cursor.execute(query, (channel, game))
        return (await cursor.fetchone() or [None])[0]


async def setFaq(database: DatabaseMain,
                 channel: str,
                 faq: str) -> bool:
    cursor: aioodbc.cursor.Cursor
    async with await database.cursor() as cursor:
        query: str
        params: Tuple[Any, ...]
        if not faq:
            query = 'DELETE FROM faq WHERE broadcaster=?'
            await cursor.execute(query, (channel,))
        else:
            if database.isSqlite:
                query = 'REPLACE INTO faq (broadcaster, faq) VALUES (?, ?)'
                params = channel, faq
            else:
                query = '''\
INSERT INTO faq (broadcaster, faq) VALUES (?, ?)
    ON CONFLICT ON CONSTRAINT faq_pkey
    DO UPDATE SET faq=?
'''
                params = channel, faq, faq
            await cursor.execute(query, params)
        await database.commit()
    return True


async def setGameFaq(database: DatabaseMain,
                     channel: str,
                     game: str,
                     faq: str) -> Optional[bool]:
    if not game:
        return None

    cursor: aioodbc.cursor.Cursor
    async with await database.cursor() as cursor:
        query: str
        params: Tuple[Any, ...]
        if not faq:
            query = 'DELETE FROM faq_game WHERE broadcaster=? AND twitchGame=?'
            params = channel, game
            await cursor.execute(query, params)
        else:
            if database.isSqlite:
                query = '''
REPLACE INTO faq_game (broadcaster, twitchGame, faq) VALUES (?, ?, ?)
'''
                params = channel, game, faq
            else:
                query = '''\
INSERT INTO faq_game (broadcaster, twitchGame, faq) VALUES (?, ?, ?)
    ON CONFLICT ON CONSTRAINT faq_game_pkey
    DO UPDATE SET faq=?
'''
                params = channel, game, faq, faq
            await cursor.execute(query, params)
        await database.commit()
    return True
