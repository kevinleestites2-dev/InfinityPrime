"""
Layer 3 — Infinite Knowledge
Powered by GPT Researcher architecture.
Never stops learning. Never forgets. Grows indefinitely.
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Optional


KNOWLEDGE_STORE_PATH = "knowledge_store.json"


class InfiniteKnowledge:
    """
    Autonomous research engine.
    Any topic, any depth. Knowledge compounds over time.
    """

    def __init__(self, llm_provider: str = "openai", store_path: str = KNOWLEDGE_STORE_PATH):
        self.llm_provider = llm_provider
        self.store_path = store_path
        self.memory: dict = self._load_store()

    def _load_store(self) -> dict:
        if os.path.exists(self.store_path):
            try:
                with open(self.store_path, "r") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_store(self):
        with open(self.store_path, "w") as f:
            json.dump(self.memory, f, indent=2)

    async def research(self, query: str, depth: int = 2) -> str:
        """
        Research a topic. Checks memory first, then runs deep research.
        Stores results for future use — knowledge compounds.
        """
        key = query.strip().lower()

        if key in self.memory:
            age_hours = self._age_hours(self.memory[key]["timestamp"])
            if age_hours < 24:
                print(f"[Layer 3] Cache hit for: '{query}' ({age_hours:.1f}h old)")
                return self.memory[key]["content"]

        print(f"[Layer 3] Researching: '{query}' (depth={depth})...")
        result = await self._deep_research(query, depth)

        self.memory[key] = {
            "content": result,
            "timestamp": datetime.utcnow().isoformat(),
            "query": query
        }
        self._save_store()
        print(f"[Layer 3] Knowledge stored. Store size: {len(self.memory)} entries.")
        return result

    async def _deep_research(self, query: str, depth: int) -> str:
        """
        GPT Researcher-style pipeline:
        1. Generate sub-queries
        2. Search each sub-query
        3. Synthesize into a report
        """
        sub_queries = self._generate_sub_queries(query, depth)
        findings = []

        for sq in sub_queries:
            finding = await self._search(sq)
            findings.append(finding)
            await asyncio.sleep(0.1)

        report = self._synthesize(query, findings)
        return report

    def _generate_sub_queries(self, query: str, depth: int) -> list:
        """Break the main query into focused sub-queries."""
        base = [
            f"What is {query}?",
            f"How does {query} work?",
            f"Latest developments in {query}",
        ]
        if depth >= 2:
            base += [
                f"Best practices for {query}",
                f"Common problems with {query} and solutions",
            ]
        if depth >= 3:
            base += [
                f"Future of {query}",
                f"Expert opinions on {query}",
            ]
        return base

    async def _search(self, sub_query: str) -> str:
        """
        Search layer — in production, hits web search APIs.
        Plug in: Tavily, Serper, Bing, DuckDuckGo.
        """
        await asyncio.sleep(0.05)
        return f"[SEARCH RESULT] {sub_query} — data pending live search integration."

    def _synthesize(self, query: str, findings: list) -> str:
        return (
            f"Research Report: {query}\n"
            f"Generated: {datetime.utcnow().isoformat()}\n\n"
            + "\n".join(f"- {f}" for f in findings)
        )

    def _age_hours(self, timestamp_str: str) -> float:
        try:
            ts = datetime.fromisoformat(timestamp_str)
            return (datetime.utcnow() - ts).total_seconds() / 3600
        except Exception:
            return 9999

    def forget(self, query: str):
        """Force re-research on next call."""
        key = query.strip().lower()
        if key in self.memory:
            del self.memory[key]
            self._save_store()
            print(f"[Layer 3] Forgot: '{query}'")

    def stats(self) -> dict:
        return {
            "entries": len(self.memory),
            "queries": list(self.memory.keys())
        }
