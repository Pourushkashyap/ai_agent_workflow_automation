from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class WorkflowRequest(BaseModel):
    query: str = Field(..., min_length=1)


class StepResponse(BaseModel):
    step_id: str
    step_name: str
    status: str
    result: Any = None
    error: Optional[str] = None


class WorkflowResponse(BaseModel):
    execution_id: str
    workflow_id: str
    workflow_name: str
    status: str
    steps_executed: List[StepResponse]
    final_result: Any = None
    error: Optional[str] = None