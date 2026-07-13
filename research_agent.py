"""
DeerFlow Research Agent
========================
A long-horizon research agent inspired by ByteDance's DeerFlow architecture,
implementing the "agents as an organisation" pattern with sub-agents, memory,
skills, and context engineering.

Sub-Agents:
  1. Planner   — Decomposes research questions into sub-tasks
  2. Searcher  — Executes web searches and gathers information
  3. Analyzer  — Synthesizes findings into structured analysis

Usage:
  python research_agent.py "Your research question here"
  python research_agent.py --topic "AI regulation in India" --depth deep
  python research_agent.py --resume session_id
"""

import os
import json
import uuid
import argparse
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

from sub_agents.planner import PlannerAgent
from sub_agents.searcher import SearcherAgent
from sub_agents.analyzer import AnalyzerAgent
from memory.context_store import ContextStore

load_dotenv()


class ResearchAgent:
    """
    Long-horizon research agent with sub-agent orchestration,
    persistent memory, and context engineering.
    """

    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or str(uuid.uuid4())[:8]
        self.memory = ContextStore(session_id=self.session_id)
        self.planner = PlannerAgent()
        self.searcher = SearcherAgent()
        self.analyzer = AnalyzerAgent()
        self.output_dir = f"./output/{self.session_id}"
        os.makedirs(self.output_dir, exist_ok=True)

    def research(
        self,
        topic: str,
        depth: str = "standard",
        max_sources: int = 10,
    ) -> dict:
        """
        Execute a full research pipeline on a topic.

        Args:
            topic: Research question or topic.
            depth: "quick", "standard", or "deep".
            max_sources: Maximum sources to search.

        Returns:
            Research report dict.
        """
        print(f"\n{'═' * 60}")
        print(f"🦌  DeerFlow Research Agent — Session {self.session_id}")
        print(f"{'═' * 60}")
        print(f"  Topic: {topic}")
        print(f"  Depth: {depth}")
        print(f"  Max sources: {max_sources}")
        print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Store initial context
        self.memory.store("topic", topic)
        self.memory.store("depth", depth)
        self.memory.store("started_at", datetime.now().isoformat())

        # Phase 1: Planning
        print(f"\n📋 Phase 1: Research Planning")
        print("─" * 40)

        plan = self.planner.create_plan(topic, depth=depth)
        self.memory.store("plan", plan)

        print(f"  ✓ Generated {len(plan['sub_tasks'])} sub-tasks")
        for i, task in enumerate(plan["sub_tasks"], 1):
            print(f"    {i}. {task['title']}")

        # Phase 2: Search & Gather
        print(f"\n🔍 Phase 2: Searching & Gathering")
        print("─" * 40)

        all_findings = []
        for task in plan["sub_tasks"]:
            print(f"\n  📌 Task: {task['title']}")
            findings = self.searcher.search(
                query=task["search_query"],
                max_results=max_sources // len(plan["sub_tasks"]),
            )
            task["findings"] = findings
            all_findings.extend(findings)
            print(f"     ✓ Found {len(findings)} relevant sources")

        self.memory.store("findings", all_findings)
        print(f"\n  Total findings: {len(all_findings)}")

        # Phase 3: Analysis & Synthesis
        print(f"\n🧠 Phase 3: Analysis & Synthesis")
        print("─" * 40)

        report = self.analyzer.analyze(
            topic=topic,
            plan=plan,
            findings=all_findings,
            depth=depth,
        )
        self.memory.store("report", report)

        # Save report
        report_path = f"{self.output_dir}/report.md"
        with open(report_path, "w") as f:
            f.write(report["markdown"])
        print(f"  ✓ Report saved to: {report_path}")

        # Save full session data
        session_path = f"{self.output_dir}/session.json"
        session_data = {
            "session_id": self.session_id,
            "topic": topic,
            "depth": depth,
            "plan": plan,
            "findings_count": len(all_findings),
            "report_summary": report.get("summary", ""),
            "completed_at": datetime.now().isoformat(),
        }
        with open(session_path, "w") as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)

        # Summary
        print(f"\n{'═' * 60}")
        print(f"✅  Research Complete — Session {self.session_id}")
        print(f"{'═' * 60}")
        print(f"  Sub-tasks completed: {len(plan['sub_tasks'])}")
        print(f"  Sources gathered: {len(all_findings)}")
        print(f"  Report: {report_path}")
        print(f"  Session: {session_path}")

        return report

    def resume(self) -> Optional[dict]:
        """Resume a previous research session from memory."""
        topic = self.memory.recall("topic")
        if not topic:
            print(f"⚠ No session found for {self.session_id}")
            return None

        print(f"♻ Resuming session {self.session_id}: {topic}")
        plan = self.memory.recall("plan")
        findings = self.memory.recall("findings")

        if plan and not findings:
            return self.research(topic, depth=self.memory.recall("depth") or "standard")

        if findings and not self.memory.recall("report"):
            report = self.analyzer.analyze(
                topic=topic,
                plan=plan,
                findings=findings,
            )
            self.memory.store("report", report)
            return report

        return self.memory.recall("report")


def main():
    parser = argparse.ArgumentParser(
        description="DeerFlow Research Agent — Long-Horizon Research Pipeline"
    )
    parser.add_argument(
        "topic", nargs="?",
        default="Latest AI developments in India and Andhra Pradesh",
        help="Research topic or question"
    )
    parser.add_argument("--depth", choices=["quick", "standard", "deep"],
                        default="standard", help="Research depth")
    parser.add_argument("--max-sources", type=int, default=10, help="Max sources")
    parser.add_argument("--resume", type=str, default=None, help="Resume session ID")
    args = parser.parse_args()

    if args.resume:
        agent = ResearchAgent(session_id=args.resume)
        agent.resume()
    else:
        agent = ResearchAgent()
        agent.research(
            topic=args.topic,
            depth=args.depth,
            max_sources=args.max_sources,
        )


if __name__ == "__main__":
    main()
