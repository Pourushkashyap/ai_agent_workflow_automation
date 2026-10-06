from typing import Any, Callable, Dict, List, Optional


class ToolNotFoundError(Exception):
    """Raised when a requested tool is not registered."""
    pass


class ToolRegistry:
    """
    Central registry for tools that can be used by workflows.

    Each tool has:
    - name
    - callable
    - optional description

    The description helps the generic tool resolver
    understand which tool matches a workflow step.
    """

    def __init__(self):
        self._tools: Dict[str, Callable[..., Any]] = {}
        self._descriptions: Dict[str, str] = {}

    def register(
        self,
        name: str,
        tool: Callable[..., Any],
        description: Optional[str] = None,
    ) -> None:
        """Register a tool."""

        if not name or not name.strip():
            raise ValueError("Tool name cannot be empty.")

        if not callable(tool):
            raise TypeError(
                f"Tool '{name}' must be callable."
            )

        name = name.strip()

        if name in self._tools:
            raise ValueError(
                f"Tool already registered: {name}"
            )

        self._tools[name] = tool
        self._descriptions[name] = (
            description.strip()
            if description
            else ""
        )

    def get(self, name: str) -> Callable[..., Any]:
        """Get a registered tool."""

        tool = self._tools.get(name)

        if tool is None:
            raise ToolNotFoundError(
                f"Tool not registered: {name}"
            )

        return tool

    def execute(
        self,
        name: str,
        **kwargs,
    ) -> Any:
        """Execute a registered tool."""

        tool = self.get(name)

        return tool(**kwargs)

    def exists(self, name: str) -> bool:
        """Check whether a tool exists."""

        return name in self._tools

    def get_description(self, name: str) -> str:
        """Get the description of a registered tool."""

        if name not in self._tools:
            raise ToolNotFoundError(
                f"Tool not registered: {name}"
            )

        return self._descriptions.get(name, "")

    def get_tool_metadata(self) -> Dict[str, Dict[str, str]]:
        """
        Return metadata for all registered tools.
        """

        return {
            name: {
                "name": name,
                "description": self._descriptions.get(name, ""),
            }
            for name in self._tools
        }

    def list_tools(self) -> List[str]:
        """Return names of all registered tools."""

        return list(self._tools.keys())

    def count(self) -> int:
        """Return number of registered tools."""

        return len(self._tools)

    def remove(self, name: str) -> None:
        """Remove a registered tool."""

        if name not in self._tools:
            raise ToolNotFoundError(
                f"Tool not registered: {name}"
            )

        del self._tools[name]
        self._descriptions.pop(name, None)

    def clear(self) -> None:
        """Remove all registered tools."""

        self._tools.clear()
        self._descriptions.clear()

    def __len__(self) -> int:
        return len(self._tools)

    def __contains__(self, name: str) -> bool:
        return name in self._tools