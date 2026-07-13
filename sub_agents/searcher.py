"""Searcher sub-agent — web search and information gathering."""

from datetime import datetime

try:
    from duckduckgo_search import DDGS
    DDG_AVAILABLE = True
except ImportError:
    DDG_AVAILABLE = False


class SearcherAgent:
    """Executes web searches and gathers information."""

    def search(self, query: str, max_results: int = 5) -> list[dict]:
        """
        Search for information on a query.

        Args:
            query: Search query string.
            max_results: Maximum results to return.

        Returns:
            List of finding dicts with title, url, body.
        """
        findings = []

        if DDG_AVAILABLE:
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.text(query, max_results=max_results))
                    for r in results:
                        findings.append({
                            "title": r.get("title", ""),
                            "url": r.get("href", ""),
                            "body": r.get("body", ""),
                            "source": "duckduckgo",
                            "found_at": datetime.now().isoformat(),
                        })
            except Exception as e:
                print(f"    ⚠ Search error: {e}")
                findings = self._mock_search(query, max_results)
        else:
            findings = self._mock_search(query, max_results)

        return findings

    def _mock_search(self, query: str, max_results: int) -> list[dict]:
        """Generate mock search results for demo purposes."""
        return [
            {
                "title": f"Result {i+1} for: {query[:40]}",
                "url": f"https://example.com/result-{i+1}",
                "body": f"This is a mock search result for '{query}'. "
                        f"Install duckduckgo-search for real web search.",
                "source": "mock",
                "found_at": datetime.now().isoformat(),
            }
            for i in range(min(max_results, 3))
        ]
