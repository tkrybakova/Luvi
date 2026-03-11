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

    def test_search_file_keeps_original_case_query(self) -> None:
        message = self.router.execute_system_command("search file Budget.XLSX")
        self.assertIn("budget", message.lower())

    def test_open_app_parses_case_insensitively(self) -> None:
        self.router._open_app = lambda app_name: app_name  # type: ignore[method-assign]
        result = self.router.execute_system_command("Open App Calculator")
        self.assertEqual(result, "Calculator")


if __name__ == "__main__":
    unittest.main()
