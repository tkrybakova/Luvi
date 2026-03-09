import unittest

from command_router import CommandRouter


class CommandRouterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.router = CommandRouter()

    def test_search_file_is_system_intent(self) -> None:
        self.assertEqual(self.router.route("search file budget.xlsx"), "system")

    def test_screen_intent(self) -> None:
        self.assertEqual(self.router.route("what is on my screen"), "screen")

    def test_web_search_intent(self) -> None:
        self.assertEqual(self.router.route("search latest ai news"), "web_search")


if __name__ == "__main__":
    unittest.main()
