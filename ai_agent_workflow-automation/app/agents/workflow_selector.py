from typing import Any, Dict, List

from app.workflow.models import (
    WorkflowDefinition,
    WorkflowSelection,
)
from app.workflow.registry import WorkflowRegistry


class WorkflowSelector:
    """
    Selects the most relevant workflow for a user request.

    Current version:
    - Uses simple keyword matching.
    - Provides a clean interface for future LLM integration.

    Later:
        User Request
            ↓
        Candidate Retrieval
            ↓
        LLM
            ↓
        WorkflowSelection
    """

    def __init__(self, registry: WorkflowRegistry):
        self.registry = registry

    def select(
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

        candidates = self.find_candidates(
            user_request
        )

        if not candidates:
            raise ValueError(
                f"No workflow found for request: "
                f"{user_request}"
            )

        workflow = candidates[0]

        return WorkflowSelection(
            workflow_id=workflow.workflow_id,
            workflow_name=workflow.workflow_name,
            reason=(
                "Workflow selected using keyword-based "
                "candidate matching."
            ),
            parameters={},
            confidence=self._calculate_confidence(
                user_request,
                workflow,
            ),
        )

    def find_candidates(
    self,
    user_request: str,
) -> List[WorkflowDefinition]:
        """
        Find workflows that may be relevant to the request.
        """

        request_words = self._tokenize(
            user_request
        )

        scored_workflows = []

        for workflow in self.registry.list_all():

            searchable_text = self._build_search_text(
                workflow
            )

            score = 0

            for word in request_words:
                if word in searchable_text:
                    score += 1

            if score > 0:
                scored_workflows.append(
                    (score, workflow)
                )

        scored_workflows.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            workflow
            for _, workflow in scored_workflows
        ]

    def _build_search_text(
        self,
        workflow: WorkflowDefinition,
    ) -> str:
        """
        Build searchable text from workflow metadata.
        """

        return " ".join(
            [
                workflow.workflow_name,
                workflow.trigger,
                workflow.expected_output,
                " ".join(workflow.inputs),
                " ".join(workflow.decision_logic),
                " ".join(workflow.tools_required),
            ]
        ).lower()

    def _tokenize(
        self,
        text: str,
    ) -> List[str]:
        """
        Convert text into simple searchable words.
        """

        return [
            word.strip(".,!?;:")
            for word in text.lower().split()
            if len(word.strip(".,!?;:")) > 2
        ]

    def _calculate_confidence(
        self,
        user_request: str,
        workflow: WorkflowDefinition,
    ) -> float:
        """
        Calculate a simple confidence score.

        This is only a temporary deterministic score.
        The future LLM selector will provide the actual
        confidence/selection reasoning.
        """

        request_words = set(
            self._tokenize(user_request)
        )

        searchable_words = set(
            self._tokenize(
                self._build_search_text(workflow)
            )
        )

        if not request_words:
            return 0.0

        matched_words = (
            request_words & searchable_words
        )

        confidence = (
            len(matched_words)
            / len(request_words)
        )

        return round(
            min(confidence, 1.0),
            2,
        )