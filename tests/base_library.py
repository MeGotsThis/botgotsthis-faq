import encodings

from .. import library

# Fix for running: python -m unittest discover -s ./pkg -t ./ -p test_*.py
encodings.search_function('utf-16le')


class TestDatabaseFaq:
    async def setUpInsert(self):
        await self.execute('''
INSERT INTO faq VALUES ('megotsthis', 'Kappa')
''')
        await self.execute('''
INSERT INTO faq_game VALUES ('megotsthis', 'Kappa', 'Keepo')
''')

    async def tearDown(self):
        await self.execute(['''DROP TABLE faq''',
                            '''DROP TABLE faq_game'''])
        await super().tearDown()

    async def test_get_faq(self):
        self.assertEqual(
            await library.getFaq(self.database, 'megotsthis'), 'Kappa')

    async def test_get_faq_empty(self):
        self.assertIsNone(await library.getFaq(self.database, 'botgotsthis'))

    async def test_get_game_faq(self):
        self.assertEqual(
            await library.getGameFaq(self.database, 'megotsthis', 'Kappa'),
            'Keepo')

    async def test_get_game_faq_empty(self):
        self.assertIsNone(
            await library.getGameFaq(self.database, 'botgotsthis', 'Kappa'))
        self.assertIsNone(
            await library.getGameFaq(self.database, 'megotsthis', 'Keepo'))

    async def test_set_faq(self):
        self.assertTrue(
            await library.setFaq(self.database, 'botgotsthis', 'FrankerZ'))
        self.assertCountEqual(await self.rows('SELECT * FROM faq'),
                              [('megotsthis', 'Kappa'),
                               ('botgotsthis', 'FrankerZ')])

    async def test_set_faq_replace(self):
        self.assertTrue(
            await library.setFaq(self.database, 'megotsthis', 'FrankerZ'))
        self.assertCountEqual(await self.rows('SELECT * FROM faq'),
                              [('megotsthis', 'FrankerZ'),])

    async def test_set_faq_empty(self):
        self.assertTrue(
            await library.setFaq(self.database, 'megotsthis', ''))
        self.assertCountEqual(await self.rows('SELECT * FROM faq'), [])

    async def test_set_game_faq(self):
        self.assertTrue(
            await library.setGameFaq(self.database, 'megotsthis', 'Keepo',
                                     'KappaPride'))
        self.assertTrue(
            await library.setGameFaq(self.database, 'botgotsthis', 'Kappa',
                                     'FrankerZ'))
        self.assertCountEqual(await self.rows('SELECT * FROM faq_game'),
                              [('megotsthis', 'Kappa', 'Keepo'),
                               ('megotsthis', 'Keepo', 'KappaPride'),
                               ('botgotsthis', 'Kappa', 'FrankerZ')])

    async def test_set_game_faq_replace(self):
        self.assertTrue(
            await library.setGameFaq(self.database, 'megotsthis', 'Kappa',
                                     'FrankerZ'))
        self.assertCountEqual(await self.rows('SELECT * FROM faq_game'),
                              [('megotsthis', 'Kappa', 'FrankerZ'),])

    async def test_set_game_faq_empty(self):
        self.assertTrue(
            await library.setGameFaq(self.database, 'megotsthis', 'Kappa', ''))
        self.assertCountEqual(await self.rows('SELECT * FROM faq_game'), [])
