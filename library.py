from typing import Any, Optional, Tuple  # noqa: F401

import aioodbc.cursor  # noqa: F401

from lib.database import DatabaseMain


async def getFaq(channel: str) -> Optional[str]:
    db: DatabaseMain
    cursor: aioodbc.cursor.Cursor
    async with DatabaseMain.acquire() as db, await db.cursor() as cursor:
        query: str = 'SELECT faq FROM faq WHERE broadcaster=?'
        await cursor.execute(query, (channel,))
        return (await cursor.fetchone() or [None])[0]


async def getGameFaq(channel: str,
                     game: str) -> Optional[str]:
    db: DatabaseMain
    cursor: aioodbc.cursor.Cursor
    async with DatabaseMain.acquire() as db, await db.cursor() as cursor:
        query: str = '''
SELECT faq FROM faq_game WHERE broadcaster=? AND twitchGame=?'''
        await cursor.execute(query, (channel, game))
        return (await cursor.fetchone() or [None])[0]


async def setFaq(channel: str,
                 faq: str) -> bool:
    db: DatabaseMain
    cursor: aioodbc.cursor.Cursor
    async with DatabaseMain.acquire() as db, await db.cursor() as cursor:
        query: str
        params: Tuple[Any, ...]
        if not faq:
            query = 'DELETE FROM faq WHERE broadcaster=?'
            await cursor.execute(query, (channel,))
        else:
            if db.isSqlite:
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
        await db.commit()
    return True


async def setGameFaq(channel: str,
                     game: str,
                     faq: str) -> Optional[bool]:
    if not game:
        return None

    db: DatabaseMain
    cursor: aioodbc.cursor.Cursor
    async with DatabaseMain.acquire() as db, await db.cursor() as cursor:
        query: str
        params: Tuple[Any, ...]
        if not faq:
            query = 'DELETE FROM faq_game WHERE broadcaster=? AND twitchGame=?'
            params = channel, game
            await cursor.execute(query, params)
        else:
            if db.isSqlite:
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
        await db.commit()
    return True
