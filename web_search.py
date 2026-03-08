"""Web-search utilities for Luvi."""

from duckduckgo_search import DDGS

import config


class WebSearch:
    """Performs web search and returns digestible results."""

    def search(self, query: str, limit: int = config.SEARCH_RESULTS_LIMIT) -> list[dict]:
        """Return DuckDuckGo text results, or an empty list on failure."""
        try:
            with DDGS() as ddgs:
                return list(ddgs.text(query, max_results=limit))
        except Exception:
            return []

    def format_results(self, results: list[dict]) -> str:
        lines = []
        for idx, item in enumerate(results, start=1):
            lines.append(
                f"{idx}. {item.get('title', 'No title')}\n"
                f"   URL: {item.get('href', '')}\n"
                f"   Snippet: {item.get('body', '')}"
            )
        return "\n\n".join(lines)
