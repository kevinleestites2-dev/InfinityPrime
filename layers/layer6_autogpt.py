"""
Layer 6 — AutoGPT Loop
Self-directed autonomous execution.
Sets its own goals, breaks them into steps, executes, evaluates, iterates.
No human intervention required.
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional


AUTOGPT_LOG_PATH = "autogpt_log.json"


class AutoGPTLoop:
    """
    Self-directed goal execution engine.
    Feed it a task → it figures out the goals → hands them to the Swarm.
    """

    def __init__(self, max_iterations: int = 25):
        self.max_iterations = max_iterations
        self.goal_history: List[dict] = []
        self.completed_goals: List[str] = []

    async def decompose(self, task: str, understanding: dict, knowledge: str) -> List[dict]:
        """
        Break a task into executable goals.
        Uses understanding + knowledge to create a smart goal tree.
        """
        print(f"[Layer 6] AutoGPT decomposing task...")
        intent = understanding.get("intent", "general")
        constraints = understanding.get("constraints", [])

        goals = self._build_goal_tree(task, intent, constraints, knowledge)
        self.goal_history.extend(goals)

        print(f"[Layer 6] {len(goals)} goal(s) generated.")
        return goals

    def _build_goal_tree(self, task: str, intent: str, constraints: list, knowledge: str) -> List[dict]:
        """Build a goal tree based on intent type."""
        base_goals = []

        if intent == "information_retrieval":
            base_goals = [
                {"type": "search", "task": f"Search for: {task}", "priority": 1},
                {"type": "verify", "task": f"Verify findings for: {task}", "priority": 2},
                {"type": "synthesize", "task": f"Synthesize report on: {task}", "priority": 3},
            ]
        elif intent == "creation":
            base_goals = [
                {"type": "plan", "task": f"Plan structure for: {task}", "priority": 1},
                {"type": "draft", "task": f"Draft content for: {task}", "priority": 2},
                {"type": "refine", "task": f"Refine and polish: {task}", "priority": 3},
                {"type": "validate", "task": f"Validate output for: {task}", "priority": 4},
            ]
        elif intent == "analysis":
            base_goals = [
                {"type": "collect", "task": f"Collect data for: {task}", "priority": 1},
                {"type": "analyze", "task": f"Analyze data for: {task}", "priority": 2},
                {"type": "interpret", "task": f"Interpret results for: {task}", "priority": 3},
                {"type": "report", "task": f"Generate analysis report for: {task}", "priority": 4},
            ]
        elif intent == "problem_solving":
            base_goals = [
                {"type": "diagnose", "task": f"Diagnose problem: {task}", "priority": 1},
                {"type": "generate_solutions", "task": f"Generate solutions for: {task}", "priority": 2},
                {"type": "evaluate", "task": f"Evaluate best solution for: {task}", "priority": 3},
                {"type": "implement", "task": f"Implement solution for: {task}", "priority": 4},
            ]
        elif intent == "automation":
            base_goals = [
                {"type": "map_workflow", "task": f"Map workflow for: {task}", "priority": 1},
                {"type": "build_automation", "task": f"Build automation for: {task}", "priority": 2},
                {"type": "test", "task": f"Test automation for: {task}", "priority": 3},
                {"type": "deploy", "task": f"Deploy automation for: {task}", "priority": 4},
            ]
        else:
            base_goals = [
                {"type": "general", "task": task, "priority": 1},
            ]

        # Apply constraint modifications
        if "speed_priority" in constraints:
            base_goals = base_goals[:2]  # Cut to essentials only

        return base_goals

    async def evaluate(self, task: str, results: List[Any]) -> dict:
        """
        Evaluate if goals were achieved. If not, generate new goals and iterate.
        """
        print(f"[Layer 6] Evaluating results...")
        await asyncio.sleep(0.05)

        success_count = sum(1 for r in results if r and not isinstance(r, Exception))
        total = len(results)
        success_rate = success_count / total if total > 0 else 0

        evaluation = {
            "success_rate": success_rate,
            "total_goals": total,
            "succeeded": success_count,
            "failed": total - success_count,
            "status": "complete" if success_rate >= 0.8 else "partial",
            "timestamp": datetime.utcnow().isoformat()
        }

        print(f"[Layer 6] Evaluation: {success_count}/{total} goals succeeded ({success_rate:.0%})")
        self._log(task, evaluation)
        return evaluation

    def _log(self, task: str, evaluation: dict):
        entry = {"task": task[:100], "evaluation": evaluation}
        existing = []
        if os.path.exists(AUTOGPT_LOG_PATH):
            try:
                with open(AUTOGPT_LOG_PATH) as f:
                    existing = json.load(f)
            except Exception:
                pass
        existing.append(entry)
        with open(AUTOGPT_LOG_PATH, "w") as f:
            json.dump(existing[-100:], f, indent=2)
