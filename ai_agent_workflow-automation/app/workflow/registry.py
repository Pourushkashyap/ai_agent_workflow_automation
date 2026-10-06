from typing import Dict, List, Optional

from app.workflow.models import WorkflowDefinition


class WorkflowRegistry:
    """
    Central registry for all available workflows.

    The registry provides a single place to:
    - Register workflows
    - Retrieve workflows by ID
    - Search workflows by name
    - List all workflows
    """

    def __init__(self, workflows: Optional[List[WorkflowDefinition]] = None):
        self._workflows: Dict[str, WorkflowDefinition] = {}

        if workflows:
            self.register_many(workflows)

    def register(self, workflow: WorkflowDefinition) -> None:
        """
        Register a single workflow.
        """

        if workflow.workflow_id in self._workflows:
            raise ValueError(
                f"Workflow already registered: {workflow.workflow_id}"
            )

        self._workflows[workflow.workflow_id] = workflow

    def register_many(
        self,
        workflows: List[WorkflowDefinition]
    ) -> None:
        """
        Register multiple workflows.
        """

        for workflow in workflows:
            self.register(workflow)

    def get(self, workflow_id: str) -> WorkflowDefinition:
        """
        Retrieve a workflow by its ID.
        """

        workflow = self._workflows.get(workflow_id)

        if workflow is None:
            raise KeyError(
                f"Workflow not found: {workflow_id}"
            )

        return workflow

    def get_optional(
        self,
        workflow_id: str
    ) -> Optional[WorkflowDefinition]:
        """
        Retrieve a workflow without raising an exception
        when it does not exist.
        """

        return self._workflows.get(workflow_id)

    def list_all(self) -> List[WorkflowDefinition]:
        """
        Return all registered workflows.
        """

        return list(self._workflows.values())

    def count(self) -> int:
        """
        Return the number of registered workflows.
        """

        return len(self._workflows)

    def search(self, query: str) -> List[WorkflowDefinition]:
        """
        Search workflows using their name, description/trigger,
        inputs and expected output.

        This is a simple keyword-based search.
        Later, the AI workflow selector can use this registry
        to retrieve candidate workflows.
        """

        query = query.lower().strip()

        if not query:
            return []

        results = []

        for workflow in self._workflows.values():

            searchable_text = " ".join(
                [
                    workflow.workflow_name,
                    workflow.trigger,
                    workflow.expected_output,
                    " ".join(workflow.inputs),
                    " ".join(workflow.decision_logic),
                    " ".join(workflow.tools_required),
                ]
            ).lower()

            if query in searchable_text:
                results.append(workflow)

        return results

    def exists(self, workflow_id: str) -> bool:
        """
        Check whether a workflow exists.
        """

        return workflow_id in self._workflows

    def remove(self, workflow_id: str) -> None:
        """
        Remove a workflow from the registry.
        """

        if workflow_id not in self._workflows:
            raise KeyError(
                f"Workflow not found: {workflow_id}"
            )

        del self._workflows[workflow_id]

    def clear(self) -> None:
        """
        Remove all workflows from the registry.
        """

        self._workflows.clear()

    def __len__(self) -> int:
        """
        Allow len(registry).
        """

        return len(self._workflows)

    def __contains__(self, workflow_id: str) -> bool:
        """
        Allow:
            'WF001' in registry
        """

        return workflow_id in self._workflows