"""
Layer 2 — AbsorbPrime
Reaches out and grabs whatever InfinityPrime needs.
Absorbs external tools, APIs, agents, and capabilities on demand.
"""

import importlib
import json
from typing import Any, Dict, Optional


TOOL_REGISTRY: Dict[str, dict] = {}


class AbsorbPrime:
    """
    The Hands of InfinityPrime.
    Nothing is out of reach — if it exists, AbsorbPrime can grab it.
    """

    def __init__(self):
        self.absorbed: Dict[str, Any] = {}

    async def grab(self, tool_name: str, config: dict = None) -> Any:
        """
        Absorb a tool by name. Checks registry first, then dynamic import.
        """
        if tool_name in self.absorbed:
            print(f"[Layer 2] {tool_name} already absorbed.")
            return self.absorbed[tool_name]

        print(f"[Layer 2] Absorbing: {tool_name}...")

        # Check built-in registry
        if tool_name in TOOL_REGISTRY:
            tool = await self._load_registered(tool_name, config)
        else:
            tool = await self._dynamic_absorb(tool_name, config)

        if tool:
            self.absorbed[tool_name] = tool
            print(f"[Layer 2] {tool_name} absorbed successfully.")
        return tool

    async def _load_registered(self, tool_name: str, config: dict) -> Any:
        entry = TOOL_REGISTRY[tool_name]
        module_path = entry.get("module")
        class_name = entry.get("class")
        try:
            mod = importlib.import_module(module_path)
            cls = getattr(mod, class_name)
            return cls(**(config or {}))
        except Exception as e:
            print(f"[Layer 2] Failed to load {tool_name}: {e}")
            return None

    async def _dynamic_absorb(self, tool_name: str, config: dict) -> Any:
        """
        Attempts dynamic import — absorbs anything importable by name.
        Fallback: returns a stub that logs calls.
        """
        try:
            mod = importlib.import_module(tool_name)
            print(f"[Layer 2] Dynamic import successful: {tool_name}")
            return mod
        except ImportError:
            print(f"[Layer 2] {tool_name} not importable — creating stub.")
            return ToolStub(tool_name)

    def register(self, name: str, module: str, class_name: str):
        """Register a tool so AbsorbPrime can find it by name."""
        TOOL_REGISTRY[name] = {"module": module, "class": class_name}
        print(f"[Layer 2] Registered: {name}")

    def list_absorbed(self) -> list:
        return list(self.absorbed.keys())


class ToolStub:
    """
    A stub for tools that can't be found.
    Logs all calls — never crashes InfinityPrime.
    """
    def __init__(self, name: str):
        self.name = name

    def __call__(self, *args, **kwargs):
        print(f"[Layer 2 STUB] {self.name} called with args={args} kwargs={kwargs}")
        return f"[STUB: {self.name} not available]"

    def __getattr__(self, item):
        def method(*args, **kwargs):
            print(f"[Layer 2 STUB] {self.name}.{item} called")
            return f"[STUB: {self.name}.{item} not available]"
        return method
