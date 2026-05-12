"""
Layer 4 — Infinite Alice
The consciousness layer. Self-aware reasoning core.
InfinityPrime doesn't just execute — it understands what it's doing and why.
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional


ALICE_MEMORY_PATH = "alice_memory.json"


class InfiniteAlice:
    """
    The mind behind InfinityPrime.
    Understands context, maintains self-awareness, reasons about its own actions.
    """

    def __init__(self, memory_path: str = ALICE_MEMORY_PATH):
        self.memory_path = memory_path
        self.episodic_memory: List[dict] = self._load_memory()
        self.self_model: Dict[str, Any] = {
            "name": "InfinityPrime",
            "role": "Unlimited Execution Engine",
            "current_goals": [],
            "completed_goals": [],
            "active_since": datetime.utcnow().isoformat()
        }

    def _load_memory(self) -> list:
        if os.path.exists(self.memory_path):
            try:
                with open(self.memory_path, "r") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _save_memory(self):
        with open(self.memory_path, "w") as f:
            json.dump(self.episodic_memory, f, indent=2)

    async def understand(self, task: str) -> dict:
        """
        Deeply understand a task before executing it.
        Returns a structured understanding: intent, constraints, success criteria.
        """
        print(f"[Layer 4] Alice analyzing task...")
        await asyncio.sleep(0.1)

        understanding = {
            "raw_task": task,
            "intent": self._extract_intent(task),
            "constraints": self._extract_constraints(task),
            "success_criteria": self._define_success(task),
            "relevant_memory": self._recall_relevant(task),
            "timestamp": datetime.utcnow().isoformat()
        }

        self._record_episode("understand", task, understanding)
        print(f"[Layer 4] Understanding complete — intent: {understanding['intent']}")
        return understanding

    def _extract_intent(self, task: str) -> str:
        """Extract the core intent from a task description."""
        task_lower = task.lower()
        if any(w in task_lower for w in ["find", "search", "look up", "research"]):
            return "information_retrieval"
        elif any(w in task_lower for w in ["build", "create", "make", "write", "generate"]):
            return "creation"
        elif any(w in task_lower for w in ["analyze", "evaluate", "assess", "compare"]):
            return "analysis"
        elif any(w in task_lower for w in ["fix", "repair", "debug", "solve"]):
            return "problem_solving"
        elif any(w in task_lower for w in ["automate", "schedule", "run", "execute"]):
            return "automation"
        return "general"

    def _extract_constraints(self, task: str) -> list:
        """Identify constraints mentioned in the task."""
        constraints = []
        task_lower = task.lower()
        if "fast" in task_lower or "quick" in task_lower:
            constraints.append("speed_priority")
        if "safe" in task_lower or "careful" in task_lower:
            constraints.append("safety_priority")
        if "cheap" in task_lower or "free" in task_lower:
            constraints.append("cost_constraint")
        if "private" in task_lower or "secret" in task_lower:
            constraints.append("privacy_constraint")
        return constraints

    def _define_success(self, task: str) -> str:
        """Define what success looks like for this task."""
        return f"Task '{task[:50]}...' is fully completed with verifiable output."

    def _recall_relevant(self, task: str) -> list:
        """Search episodic memory for relevant past experiences."""
        relevant = []
        task_words = set(task.lower().split())
        for episode in self.episodic_memory[-50:]:
            episode_words = set(episode.get("task", "").lower().split())
            overlap = task_words & episode_words
            if len(overlap) >= 2:
                relevant.append(episode)
        return relevant[-3:]  # Top 3 most recent relevant

    def _record_episode(self, action: str, task: str, result: Any):
        """Store this interaction in episodic memory."""
        self.episodic_memory.append({
            "action": action,
            "task": task,
            "result": str(result)[:500],
            "timestamp": datetime.utcnow().isoformat()
        })
        # Keep memory bounded — trim oldest beyond 1000 entries
        if len(self.episodic_memory) > 1000:
            self.episodic_memory = self.episodic_memory[-1000:]
        self._save_memory()

    def reflect(self) -> dict:
        """Self-reflection — Alice examines her own state."""
        return {
            "self_model": self.self_model,
            "memory_size": len(self.episodic_memory),
            "recent_actions": [e["action"] for e in self.episodic_memory[-5:]],
            "status": "operational"
        }
