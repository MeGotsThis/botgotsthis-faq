from datetime import timedelta
from typing import Optional  # noqa: F401

from lib.data import ChatCommandArgs
from lib.helper.chat import cooldown, permission
from . import library


@cooldown(timedelta(seconds=15), 'faq', 'moderator')
async def commandFaq(args: ChatCommandArgs) -> bool:
    faq: Optional[str] = await library.getFaq(args.database, args.chat.channel)

    if faq is None:
        faq = await library.getGameFaq(args.database, args.chat.channel,
                                       args.chat.twitchGame)

    if faq:
        args.chat.send(f'FAQ: {faq}')
    elif args.permissions.moderator:
        args.chat.send('''\
No FAQ was set. Use !setfaq or !setgamefaq to set a FAQ''')
    return True


@permission('moderator')
async def commandSetFaq(args: ChatCommandArgs) -> bool:
    result: bool = await library.setFaq(args.database, args.chat.channel,
                                        args.message.query)
    if result:
        if not args.message.query:
            args.chat.send('FAQ is now unset')
        else:
            args.chat.send(f'FAQ set as {args.message.query}')
    else:
        args.chat.send(f'Error setting FAQ')
    return True


@permission('moderator')
async def commandSetGameFaq(args: ChatCommandArgs) -> bool:
    if not args.chat.twitchGame:
        args.chat.send(f'''\
{args.chat.channel} needs to have a game set on Twitch before this command \
can be used''')

    result: bool = await library.setGameFaq(
        args.database, args.chat.channel, args.chat.twitchGame,
        args.message.query)
    if result:
        if not args.message.query:
            args.chat.send(f'''\
FAQ is now unset for the game "{args.chat.twitchGame}"''')
        else:
            args.chat.send(f'''\
FAQ set as {args.message.query} for the game "{args.chat.twitchGame}"''')
    else:
        args.chat.send(f'''\
Error setting FAQ for game "{args.chat.twitchGame}"''')
    return True
