from typing import List

from langchain_groq import ChatGroq
from dotenv import load_dotenv

from app.workflow.models import (
    WorkflowDefinition,
    WorkflowSelection,
)

load_dotenv()


class LLMWorkflowSelector:
    """
    Uses a Groq-hosted LLM to select the most appropriate
    workflow from candidate workflows.
    """

    def __init__(
    self,
    model: str = "openai/gpt-oss-120b",
    temperature: float = 0
):
        self.llm = ChatGroq(
            model=model,
            temperature=temperature,
        )

    def select(
        self,
        user_request: str,
        candidates: List[WorkflowDefinition],
    ) -> WorkflowSelection:

        if not user_request.strip():
            raise ValueError(
                "User request cannot be empty."
            )

        if not candidates:
            raise ValueError(
                "No candidate workflows provided."
            )

        workflow_context = self._build_workflow_context(
            candidates
        )

        prompt = f"""
You are an AI workflow selection agent.

Your task is to select the BEST workflow for the
user's request from the available candidate workflows.

Rules:

1. Select ONLY one workflow from the candidates.
2. Never invent a workflow ID.
3. Extract useful parameters from the user's request.
4. If no parameters are available, return an empty object.
5. Give a short reason for the selection.
6. Confidence must be between 0 and 1.

USER REQUEST:
{user_request}

AVAILABLE WORKFLOWS:
{workflow_context}
"""

        structured_llm = self.llm.with_structured_output(
            WorkflowSelection
        )

        result = structured_llm.invoke(prompt)

        self._validate_selection(
            result,
            candidates,
        )

        return result

    def _build_workflow_context(
        self,
        candidates: List[WorkflowDefinition],
    ) -> str:

        workflow_context = []

        for workflow in candidates:

            workflow_context.append(
                f"""
Workflow ID: {workflow.workflow_id}
Workflow Name: {workflow.workflow_name}
Trigger: {workflow.trigger}
Inputs: {workflow.inputs}
Expected Output: {workflow.expected_output}
Decision Logic: {workflow.decision_logic}
Tools: {workflow.tools_required}
"""
            )

        return "\n".join(workflow_context)

    def _validate_selection(
        self,
        selection: WorkflowSelection,
        candidates: List[WorkflowDefinition],
    ) -> None:

        candidate_ids = {
            workflow.workflow_id
            for workflow in candidates
        }

        if selection.workflow_id not in candidate_ids:
            raise ValueError(
                f"LLM selected invalid workflow: "
                f"{selection.workflow_id}"
            )

        if selection.confidence is None:
            raise ValueError(
                "LLM did not provide confidence."
            )

        if not 0 <= selection.confidence <= 1:
            raise ValueError(
                "Workflow confidence must be between 0 and 1."
            )