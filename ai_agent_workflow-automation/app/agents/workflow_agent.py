from typing import Any, Dict

from app.agents.llm_selector import LLMWorkflowSelector
from app.agents.workflow_selector import WorkflowSelector
from app.workflow.models import (
    WorkflowDefinition,
    WorkflowSelection,
)
from app.workflow.registry import WorkflowRegistry


class WorkflowAgent:
    """
    Orchestrates workflow discovery and LLM-based
    workflow selection.

    Flow:

        User Request
            ↓
        Candidate Retrieval
            ↓
        Groq LLM
            ↓
        WorkflowSelection
            ↓
        Selected Workflow
    """

    def __init__(
        self,
        workflow_registry: WorkflowRegistry,
        llm_selector: LLMWorkflowSelector,
    ):
        self.workflow_registry = workflow_registry

        self.candidate_selector = WorkflowSelector(
            workflow_registry
        )

        self.llm_selector = llm_selector

    def select_workflow(
        self,
        user_request: str,
    ) -> WorkflowSelection:
        """
        Select the best workflow for a user request.
        """

        if not user_request or not user_request.strip():
            raise ValueError(
                "User request cannot be empty."
            )

       

        candidates = self.candidate_selector.find_candidates(
            user_request
        )

        if not candidates:
            raise ValueError(
                f"No workflow candidates found for: "
                f"{user_request}"
            )

        

        selection = self.llm_selector.select(
            user_request=user_request,
            candidates=candidates,
        )

       

        workflow = self.workflow_registry.get(
            selection.workflow_id
        )

        
        selection.workflow_name = (
            workflow.workflow_name
        )

        return selection

    def get_workflow(
        self,
        selection: WorkflowSelection,
    ) -> WorkflowDefinition:
        """
        Retrieve the complete WorkflowDefinition
        selected by the agent.
        """

        return self.workflow_registry.get(
            selection.workflow_id
        )