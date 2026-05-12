"""
Layer 5 — Infinite Swarm
Spawns as many specialized agent instances as the task demands.
One problem → infinite parallel solvers.
"""

import asyncio
from typing import Any, Callable, Dict, List, Optional


class SwarmAgent:
    """A single specialized agent in the swarm."""

    def __init__(self, agent_id: str, specialization: str, task: str):
        self.agent_id = agent_id
        self.specialization = specialization
        self.task = task
        self.result = None
        self.status = "idle"

    async def execute(self) -> Any:
        self.status = "running"
        print(f"  [Swarm Agent {self.agent_id}] Executing: {self.task[:60]}...")
        await asyncio.sleep(0.2)  # Simulated execution
        self.result = f"[Agent {self.agent_id} | {self.specialization}] Result: {self.task[:80]} — completed."
        self.status = "done"
        return self.result


class InfiniteSwarm:
    """
    Spawns unlimited parallel agents. No task too large, no scope too wide.
    Agents are spawned based on goals, run in parallel, results collected.
    """

    def __init__(self, max_concurrent: int = 50):
        self.max_concurrent = max_concurrent
        self.agent_registry: Dict[str, SwarmAgent] = {}
        self._agent_counter = 0

    async def execute(self, goals: List[dict]) -> List[Any]:
        """
        Spawn one agent per goal. Execute all in parallel.
        Returns list of results.
        """
        if not goals:
            return []

        print(f"[Layer 5] Spawning swarm — {len(goals)} agent(s)...")
        agents = [self._spawn_agent(goal) for goal in goals]

        # Execute in batches to respect max_concurrent
        results = []
        for i in range(0, len(agents), self.max_concurrent):
            batch = agents[i:i + self.max_concurrent]
            batch_results = await asyncio.gather(
                *[a.execute() for a in batch],
                return_exceptions=True
            )
            results.extend(batch_results)
            print(f"[Layer 5] Batch {i // self.max_concurrent + 1} complete — {len(batch)} agents.")

        successes = [r for r in results if not isinstance(r, Exception)]
        failures = [r for r in results if isinstance(r, Exception)]

        if failures:
            print(f"[Layer 5] {len(failures)} agent(s) failed — passing to Layer 1 for recovery.")

        print(f"[Layer 5] Swarm complete — {len(successes)}/{len(results)} succeeded.")
        return results

    def _spawn_agent(self, goal: dict) -> SwarmAgent:
        self._agent_counter += 1
        agent_id = f"A{self._agent_counter:04d}"
        agent = SwarmAgent(
            agent_id=agent_id,
            specialization=goal.get("type", "general"),
            task=goal.get("task", "")
        )
        self.agent_registry[agent_id] = agent
        return agent

    async def spawn_specialist(self, specialization: str, task: str) -> Any:
        """Spawn a single specialist agent on demand."""
        goal = {"type": specialization, "task": task}
        agent = self._spawn_agent(goal)
        return await agent.execute()

    def status(self) -> dict:
        total = len(self.agent_registry)
        done = sum(1 for a in self.agent_registry.values() if a.status == "done")
        running = sum(1 for a in self.agent_registry.values() if a.status == "running")
        return {
            "total_spawned": total,
            "completed": done,
            "running": running,
            "idle": total - done - running
        }
