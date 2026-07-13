"""Planner sub-agent — decomposes research questions into sub-tasks."""

from datetime import datetime


class PlannerAgent:
    """Decomposes a research topic into structured sub-tasks."""

    def create_plan(self, topic: str, depth: str = "standard") -> dict:
        """
        Create a research plan with sub-tasks.

        Args:
            topic: Research question or topic.
            depth: "quick" (2 tasks), "standard" (4), "deep" (6+).

        Returns:
            Plan dict with sub-tasks.
        """
        depth_map = {"quick": 2, "standard": 4, "deep": 6}
        num_tasks = depth_map.get(depth, 4)

        # Generate sub-tasks based on topic decomposition
        base_tasks = [
            {"title": f"Overview of {topic}", "type": "overview",
             "search_query": f"{topic} overview summary 2026"},
            {"title": f"Key developments in {topic}", "type": "developments",
             "search_query": f"{topic} latest developments news"},
            {"title": f"Expert analysis of {topic}", "type": "analysis",
             "search_query": f"{topic} expert analysis opinion"},
            {"title": f"Future outlook for {topic}", "type": "outlook",
             "search_query": f"{topic} future predictions trends"},
            {"title": f"Regional impact of {topic}", "type": "regional",
             "search_query": f"{topic} India regional impact"},
            {"title": f"Comparative analysis of {topic}", "type": "comparative",
             "search_query": f"{topic} comparison alternatives"},
        ]

        sub_tasks = base_tasks[:num_tasks]

        return {
            "topic": topic,
            "depth": depth,
            "sub_tasks": sub_tasks,
            "created_at": datetime.now().isoformat(),
            "estimated_time_minutes": num_tasks * 2,
        }
