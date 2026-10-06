from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class WorkflowStep(BaseModel):
    """
    Represents one executable step inside a workflow.
    """

    step_id: str
    name: str

   
    step_type: str = "tool"

    # Name of the tool/function to execute
    tool: Optional[str] = None

    # Optional input parameters for the step
    parameters: Dict[str, Any] = Field(default_factory=dict)

    # Optional condition associated with the step
    condition: Optional[str] = None


class WorkflowDefinition(BaseModel):
    """
    Standard representation of a business workflow.

    This model is independent of any particular workflow.
    Therefore, the same model can represent WF001, WF002 ... WF010
    and future workflows such as WF011.
    """

    workflow_id: str
    workflow_name: str

    # Natural-language description of when this workflow should run
    trigger: str

    # Required inputs
    inputs: List[str] = Field(default_factory=list)

    # Human-readable workflow steps
    steps: List[WorkflowStep] = Field(default_factory=list)

    # Business rules / decision logic
    decision_logic: List[str] = Field(default_factory=list)

    # Tools required by the workflow
    tools_required: List[str] = Field(default_factory=list)

    # Description of the expected result
    expected_output: str

    # Optional metadata for future extensibility
    metadata: Dict[str, Any] = Field(default_factory=dict)


class WorkflowSelection(BaseModel):
    """
    Structured output produced by the AI workflow selector.
    """

    workflow_id: str

    workflow_name: str

    reason: str

    parameters: Dict[str, Any] = Field(default_factory=dict)

    confidence: Optional[float] = None


class StepExecution(BaseModel):
    """
    Stores the result of executing one workflow step.
    """

    step_id: str
    step_name: str

    status: str

    result: Any = None

    error: Optional[str] = None


class WorkflowExecutionResult(BaseModel):
    """
    Final execution record returned by the workflow engine.
    """

    execution_id: str

    workflow_id: str
    workflow_name: str

    status: str

    steps_executed: List[StepExecution] = Field(default_factory=list)

    final_result: Any = None

    error: Optional[str] = None