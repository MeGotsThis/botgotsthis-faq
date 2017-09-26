from datetime import timedelta
from typing import Any, Optional, Tuple  # noqa: F401

import aioodbc.cursor  # noqa: F401

from lib.data import ChatCommandArgs
from lib.helper.chat import cooldown, permission


@cooldown(timedelta(seconds=15), 'faq', 'moderator')
async def commandFaq(args: ChatCommandArgs) -> bool:
    cursor: aioodbc.cursor.Cursor
    async with await args.database.cursor() as cursor:
        query: str
        faqRow: Optional[Tuple[str]]
        faq: Optional[str]

        query = 'SELECT faq FROM faq WHERE broadcaster=?'
        await cursor.execute(query, (args.chat.channel,))
        faqRow = await cursor.fetchone()
        faq = (faqRow or [None])[0]

        if faq is None:
            query = '''
SELECT faq FROM faq_game WHERE broadcaster=? AND twitchGame=?'''
            params = args.chat.channel, args.chat.twitchGame
            await cursor.execute(query, params)
            faqRow = await cursor.fetchone()
            faq = (faqRow or [None])[0]

    if faq:
        args.chat.send(f'FAQ: {faq}')
    elif args.permissions.moderator:
        args.chat.send('''\
No FAQ was set. Use !setfaq or !setgamefaq to set a FAQ''')
    return True


@permission('moderator')
async def commandSetFaq(args: ChatCommandArgs) -> bool:
    cursor: aioodbc.cursor.Cursor
    async with await args.database.cursor() as cursor:
        query: str
        params: Tuple[Any, ...]
        if not args.message.query:
            query = 'DELETE FROM faq WHERE broadcaster=?'
            await cursor.execute(query, (args.chat.channel,))
            args.chat.send('FAQ is now unset')
        else:
            if args.database.isSqlite:
                query = 'REPLACE INTO faq (broadcaster, faq) VALUES (?, ?)'
                params = args.chat.channel, args.message.query
            else:
                query = '''\
INSERT INTO faq (broadcaster, faq) VALUES (?, ?)
    ON CONFLICT ON CONSTRAINT faq_pkey
    DO UPDATE SET faq=?
'''
                params = (args.chat.channel, args.message.query,
                          args.message.query)
            await cursor.execute(query, params)
            args.chat.send(f'FAQ set as {args.message.query}')
        await args.database.commit()
    return True


@permission('moderator')
async def commandSetGameFaq(args: ChatCommandArgs) -> bool:
    if not args.chat.twitchGame:
        args.chat.send(args.chat.channel + ' needs to have a game set on '
                       'Twitch before this command can be used')

    cursor: aioodbc.cursor.Cursor
    async with await args.database.cursor() as cursor:
        query: str
        params: Tuple[Any, ...]
        if not args.message.query:
            query = 'DELETE FROM faq_game WHERE broadcaster=? AND twitchGame=?'
            params = args.chat.channel, args.chat.twitchGame
            await cursor.execute(query, params)
            args.chat.send(f'''\
FAQ is now unset for the game "{args.chat.twitchGame}"''')
        else:
            if args.database.isSqlite:
                query = '''
REPLACE INTO faq_game (broadcaster, twitchGame, faq) VALUES (?, ?, ?)
'''
                params = (args.chat.channel, args.chat.twitchGame,
                          args.message.query)
            else:
                query = '''\
INSERT INTO faq_game (broadcaster, twitchGame, faq) VALUES (?, ?, ?)
    ON CONFLICT ON CONSTRAINT faq_game_pkey
    DO UPDATE SET faq=?
'''
                params = (args.chat.channel, args.chat.twitchGame,
                          args.message.query, args.message.query)
            await cursor.execute(query, params)
            args.chat.send(f'''\
FAQ set as {args.message.query} for the game "{args.chat.twitchGame}"''')
        await args.database.commit()
    return True
