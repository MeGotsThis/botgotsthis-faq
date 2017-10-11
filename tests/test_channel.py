from asynctest.mock import patch

from lib.data.message import Message
from tests.unittest.base_channel import TestChannel
from tests.unittest.mock_class import StrContains

# Needs to be imported last
from .. import library
from .. import channel


class TestChannelFaq(TestChannel):
    @patch(library.__name__ + '.getGameFaq')
    @patch(library.__name__ + '.getFaq')
    async def test_faq(self, mock_faq, mock_gamefaq):
        self.permissions.moderator = False
        self.channel.twitchGame = 'Kappa'
        mock_faq.return_value = None
        mock_gamefaq.return_value = None
        self.assertIs(await channel.commandFaq(self.args), True)
        mock_faq.assert_called_once_with(self.database, self.channel.channel)
        mock_gamefaq.assert_called_once_with(
            self.database, self.channel.channel, self.channel.twitchGame)
        self.assertFalse(self.channel.send.called)

    @patch(library.__name__ + '.getGameFaq')
    @patch(library.__name__ + '.getFaq')
    async def test_faq_moderator(self, mock_faq, mock_gamefaq):
        self.permissions.moderator = True
        self.channel.twitchGame = 'Kappa'
        mock_faq.return_value = None
        mock_gamefaq.return_value = None
        self.assertIs(await channel.commandFaq(self.args), True)
        mock_faq.assert_called_once_with(self.database, self.channel.channel)
        mock_gamefaq.assert_called_once_with(
            self.database, self.channel.channel, self.channel.twitchGame)
        self.channel.send.assert_called_once_with(
            StrContains('No', '!setfaq', '!setgamefaq'))

    @patch(library.__name__ + '.getGameFaq')
    @patch(library.__name__ + '.getFaq')
    async def test_faq_faq(self, mock_faq, mock_gamefaq):
        self.permissions.moderator = False
        self.channel.twitchGame = 'Kappa'
        mock_faq.return_value = 'Kappa'
        mock_gamefaq.return_value = None
        self.assertIs(await channel.commandFaq(self.args), True)
        mock_faq.assert_called_once_with(self.database, self.channel.channel)
        self.assertFalse(mock_gamefaq.called)
        self.channel.send.assert_called_once_with(StrContains('FAQ', 'Kappa'))

    @patch(library.__name__ + '.getGameFaq')
    @patch(library.__name__ + '.getFaq')
    async def test_faq_gamefaq(self, mock_faq, mock_gamefaq):
        self.permissions.moderator = False
        self.channel.twitchGame = 'Kappa'
        mock_faq.return_value = None
        mock_gamefaq.return_value = 'Kappa'
        self.assertIs(await channel.commandFaq(self.args), True)
        mock_faq.assert_called_once_with(self.database, self.channel.channel)
        mock_gamefaq.assert_called_once_with(
            self.database, self.channel.channel, self.channel.twitchGame)
        self.channel.send.assert_called_once_with(StrContains('FAQ', 'Kappa'))

    @patch(library.__name__ + '.getGameFaq')
    @patch(library.__name__ + '.getFaq')
    async def test_faq_faq_gamefaq(self, mock_faq, mock_gamefaq):
        self.permissions.moderator = False
        self.channel.twitchGame = 'Kappa'
        mock_faq.return_value = 'Kappa'
        mock_gamefaq.return_value = 'FrankerZ'
        self.assertIs(await channel.commandFaq(self.args), True)
        mock_faq.assert_called_once_with(self.database, self.channel.channel)
        self.assertFalse(mock_gamefaq.called)
        self.channel.send.assert_called_once_with(StrContains('FAQ', 'Kappa'))

    @patch(library.__name__ + '.setGameFaq')
    @patch(library.__name__ + '.setFaq')
    async def test_setfaq_not_moderator(self, mock_faq, mock_gamefaq):
        self.permissionSet['moderator'] = False
        self.channel.twitchGame = 'Kappa'
        mock_faq.return_value = False
        mock_gamefaq.return_value = False
        message = Message('!setfaq Kappa')
        args = self.args._replace(message=message)
        self.assertIs(await channel.commandSetFaq(args), False)
        self.assertFalse(mock_faq.called)
        self.assertFalse(mock_gamefaq.called)
        self.assertFalse(self.channel.send.called)

    @patch(library.__name__ + '.setGameFaq')
    @patch(library.__name__ + '.setFaq')
    async def test_setfaq(self, mock_faq, mock_gamefaq):
        self.permissionSet['moderator'] = True
        self.channel.twitchGame = 'Kappa'
        mock_faq.return_value = True
        mock_gamefaq.return_value = False
        message = Message('!setfaq Kappa')
        args = self.args._replace(message=message)
        self.assertIs(await channel.commandSetFaq(args), True)
        mock_faq.assert_called_once_with(
            self.database, self.channel.channel, 'Kappa')
        self.assertFalse(mock_gamefaq.called)
        self.channel.send.assert_called_once_with(StrContains('FAQ', 'Kappa'))

    @patch(library.__name__ + '.setGameFaq')
    @patch(library.__name__ + '.setFaq')
    async def test_setfaq_empty(self, mock_faq, mock_gamefaq):
        self.permissionSet['moderator'] = True
        self.channel.twitchGame = 'Kappa'
        mock_faq.return_value = True
        mock_gamefaq.return_value = False
        message = Message('!setfaq')
        args = self.args._replace(message=message)
        self.assertIs(await channel.commandSetFaq(args), True)
        mock_faq.assert_called_once_with(
            self.database, self.channel.channel, '')
        self.assertFalse(mock_gamefaq.called)
        self.channel.send.assert_called_once_with(StrContains('FAQ', 'unset'))

    @patch(library.__name__ + '.setGameFaq')
    @patch(library.__name__ + '.setFaq')
    async def test_setfaq_error(self, mock_faq, mock_gamefaq):
        self.permissionSet['moderator'] = True
        self.channel.twitchGame = 'Kappa'
        mock_faq.return_value = False
        mock_gamefaq.return_value = False
        message = Message('!setfaq')
        args = self.args._replace(message=message)
        self.assertIs(await channel.commandSetFaq(args), True)
        mock_faq.assert_called_once_with(
            self.database, self.channel.channel, '')
        self.assertFalse(mock_gamefaq.called)
        self.channel.send.assert_called_once_with(StrContains('Error', 'FAQ'))
