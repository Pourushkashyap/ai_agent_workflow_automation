from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict


class AgentState(TypedDict, total=False):
    """
    Shared state maintained during a workflow execution.
    """

    
    user_request: str

    
    workflow_id: str

    
    workflow_name: str

    
    parameters: Dict[str, Any]

    
    current_step: int

   
    step_results: Dict[str, Any]

    
    tool_results: Dict[str, Any]

    
    condition_results: Dict[str, bool]

    
    execution_log: List[str]

    
    errors: List[str]

    
    final_result: Any

   
    status: str

    
    execution_id: str