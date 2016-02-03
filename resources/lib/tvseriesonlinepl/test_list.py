import unittest
import list


class IntegrationTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_happy_path(self):
        shows = list.shows().all()
        self.assertGreater(len(shows), 1, "There is at least one show found")

        episodes = list.episodes(shows[0].url).all()
        self.assertGreater(len(episodes), 1, "There is at least on episode found for the first show")

        player_sites = list.player_sites(episodes[0].url).all()
        self.assertGreater(len(player_sites), 1, "There is at least one player site found for the first episode")


if __name__ == '__main__':
    unittest.main()
