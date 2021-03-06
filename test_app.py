from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            # test that you're getting a template
            self.assertEqual(response.status_code, 200)
            self.assertIn("<title>Boggle</title>", html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.get("/api/new-game")
            json = response.json
    
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(json["gameId"], str)
            self.assertIsInstance(json["board"], list)
            self.assertIn(json["gameId"], games)
            # write a test for this route

    def test_api_score_word(self):
        with self.client as client: 
            response1 = client.get("/api/new-game")
            gameId = response1.json["gameId"]
            game = games[gameId]
            game.board = [['T', 'H', 'U', 'S', 'N'], ['O', 'P', 'E', 'A', 'A'], ['F', 'C', 'I', 'E', 'D'], ['I', 'G', 'E', 'A', 'I'], ['E', 'M', 'S', 'T', 'F']]
            
            print(game.board)

            # any failing assertion will cause test to fail
            test1 = client.post("/api/score-word", json={"gameId":gameId, "word":"pea"})
            result1 = test1.json["result"]
            self.assertEqual(result1, "ok")

            test2 = client.post("/api/score-word", json={"gameId":gameId, "word":"thusn"})
            result2 = test2.json["result"]
            self.assertEqual(result2, "not-word")

            test3 = client.post("/api/score-word", json={"gameId":gameId, "word":"caliphate"})
            result3 = test3.json["result"]
            self.assertEqual(result3, "not-on-board")


