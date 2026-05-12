"""
∞ InfinityPrime — The Unlimited Engine
Orchestrator — ties all 8 layers together.
"""

import asyncio
from layers.layer1_execution import InfiniteExecution
from layers.layer2_absorb import AbsorbPrime
from layers.layer3_knowledge import InfiniteKnowledge
from layers.layer4_alice import InfiniteAlice
from layers.layer5_swarm import InfiniteSwarm
from layers.layer6_autogpt import AutoGPTLoop
from layers.layer7_deeprwkv import DeepRWKV
from layers.layer8_deepthink import DeepThink


class InfinityPrime:
    """
    The Unlimited Engine.
    No ceiling. No limits. No walls.
    """

    def __init__(self, config: dict = None):
        self.config = config or {}
        self.execution = InfiniteExecution()
        self.absorb = AbsorbPrime()
        self.knowledge = InfiniteKnowledge()
        self.alice = InfiniteAlice()
        self.swarm = InfiniteSwarm()
        self.autogpt = AutoGPTLoop()
        self.deeprwkv = DeepRWKV()
        self.deepthink = DeepThink()

    async def run(self, task: str, deep: bool = False) -> str:
        """
        Main entry point. Feed it a task, it executes without limits.
        deep=True activates Deep Think (Layer 8) before execution.
        """
        print(f"\n∞ InfinityPrime activated — Task: {task}\n")

        # Layer 8 — Deep Think (activate first if deep mode)
        if deep:
            task = await self.deepthink.think(task)

        # Layer 4 — Alice understands the task
        understanding = await self.alice.understand(task)

        # Layer 3 — Pull knowledge needed
        knowledge = await self.knowledge.research(task)

        # Layer 6 — AutoGPT breaks it into goals
        goals = await self.autogpt.decompose(task, understanding, knowledge)

        # Layer 5 — Swarm executes goals in parallel
        results = await self.swarm.execute(goals)

        # Layer 1 — Route around any walls hit
        final = await self.execution.resolve(results)

        # Layer 7 — DeepRWKV synthesizes with full context
        output = await self.deeprwkv.synthesize(task, final)

        print(f"\n∞ InfinityPrime complete.\n")
        return output

    async def absorb_tool(self, tool_name: str, config: dict):
        """Layer 2 — AbsorbPrime: grab any external tool on demand."""
        return await self.absorb.grab(tool_name, config)


if __name__ == "__main__":
    import sys

    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Analyze the Pantheon and report on all active Primes."
    deep = "--deep" in sys.argv

    prime = InfinityPrime()
    result = asyncio.run(prime.run(task, deep=deep))
    print(result)
