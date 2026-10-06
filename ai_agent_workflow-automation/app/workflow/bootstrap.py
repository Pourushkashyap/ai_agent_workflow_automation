from pathlib import Path

from app.workflow.loader import load_workflows
from app.workflow.registry import WorkflowRegistry


def create_workflow_registry(
    excel_path: str | Path,
) -> WorkflowRegistry:
    """
    Load workflows from Excel and create the
    application's workflow registry.
    """

    workflows = load_workflows(excel_path)

    registry = WorkflowRegistry(workflows)

    return registry