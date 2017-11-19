from .. import library


class TestDatabaseFaq:
    POOL_SIZE = 2

    async def setUpInsert(self):
        await self.execute('''
INSERT INTO faq VALUES ('megotsthis', 'Kappa')
''')
        await self.execute('''
INSERT INTO faq_game VALUES ('megotsthis', 'Kappa', 'Keepo')
''')

    async def tearDown(self):
        if self.database.isPostgres:
            await self.database.connection.rollback()
        await self.execute(['''DROP TABLE faq''',
                            '''DROP TABLE faq_game'''])
        await super().tearDown()

    async def test_get_faq(self):
        self.assertEqual(
            await library.getFaq('megotsthis'), 'Kappa')

    async def test_get_faq_empty(self):
        self.assertIsNone(await library.getFaq('botgotsthis'))

    async def test_get_game_faq(self):
        self.assertEqual(
            await library.getGameFaq('megotsthis', 'Kappa'),
            'Keepo')

    async def test_get_game_faq_empty(self):
        self.assertIsNone(
            await library.getGameFaq('botgotsthis', 'Kappa'))
        self.assertIsNone(
            await library.getGameFaq('megotsthis', 'Keepo'))

    async def test_set_faq(self):
        self.assertTrue(
            await library.setFaq('botgotsthis', 'FrankerZ'))
        self.assertCountEqual(await self.rows('SELECT * FROM faq'),
                              [('megotsthis', 'Kappa'),
                               ('botgotsthis', 'FrankerZ')])

    async def test_set_faq_replace(self):
        self.assertTrue(
            await library.setFaq('megotsthis', 'FrankerZ'))
        self.assertCountEqual(await self.rows('SELECT * FROM faq'),
                              [('megotsthis', 'FrankerZ'),
                               ])

    async def test_set_faq_empty(self):
        self.assertTrue(
            await library.setFaq('megotsthis', ''))
        self.assertCountEqual(await self.rows('SELECT * FROM faq'), [])

    async def test_set_game_faq(self):
        self.assertTrue(
            await library.setGameFaq('megotsthis', 'Keepo', 'KappaPride'))
        self.assertTrue(
            await library.setGameFaq('botgotsthis', 'Kappa', 'FrankerZ'))
        self.assertCountEqual(await self.rows('SELECT * FROM faq_game'),
                              [('megotsthis', 'Kappa', 'Keepo'),
                               ('megotsthis', 'Keepo', 'KappaPride'),
                               ('botgotsthis', 'Kappa', 'FrankerZ')])

    async def test_set_game_faq_replace(self):
        self.assertTrue(
            await library.setGameFaq('megotsthis', 'Kappa', 'FrankerZ'))
        self.assertCountEqual(await self.rows('SELECT * FROM faq_game'),
                              [('megotsthis', 'Kappa', 'FrankerZ'),
                               ])

    async def test_set_game_faq_empty(self):
        self.assertTrue(
            await library.setGameFaq('megotsthis', 'Kappa', ''))
        self.assertCountEqual(await self.rows('SELECT * FROM faq_game'), [])
