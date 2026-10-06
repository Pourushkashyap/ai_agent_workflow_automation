from pathlib import Path


from fastapi import FastAPI, HTTPException

from app.agents.workflow_agent import WorkflowAgent
from app.agents.llm_selector import LLMWorkflowSelector
from app.api.schemas import WorkflowRequest, WorkflowResponse
from app.tools.loader import create_tool_registry
from app.workflow.bootstrap import create_workflow_registry
from app.workflow.engine import WorkflowEngine


BASE_DIR = Path(__file__).resolve().parents[2]

EXCEL_PATH = (
    BASE_DIR
    / "data"
    / "AI_Agent_Workflow_Assessment (1).xlsx"
)


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Agent Workflow Automation",
        description="AI-driven workflow execution system",
        version="1.0.0",
    )

    workflow_registry = create_workflow_registry(EXCEL_PATH)
    tool_registry = create_tool_registry()

    llm_selector = LLMWorkflowSelector()

    workflow_agent = WorkflowAgent(
        workflow_registry=workflow_registry,
        llm_selector=llm_selector,
    )

    workflow_engine = WorkflowEngine(
        tool_registry=tool_registry
    )

    @app.get("/health")
    def health_check():
        return {
            "status": "healthy",
            "workflows": workflow_registry.count(),
            "tools": tool_registry.count(),
        }

    @app.post(
        "/api/workflows/execute",
        response_model=WorkflowResponse,
    )
    def execute_workflow(request: WorkflowRequest):

        try:
            selection = workflow_agent.select_workflow(
                request.query
            )

            workflow = workflow_agent.get_workflow(
                selection
            )

           

            result = workflow_engine.execute(
                workflow=workflow,
                parameters=selection.parameters,
            )

            return WorkflowResponse(
                execution_id=result.execution_id,
                workflow_id=result.workflow_id,
                workflow_name=result.workflow_name,
                status=result.status,
                steps_executed=[
                    {
                        "step_id": step.step_id,
                        "step_name": step.step_name,
                        "status": step.status,
                        "result": step.result,
                        "error": step.error,
                    }
                    for step in result.steps_executed
                ],
                final_result=result.final_result,
                error=result.error,
            )

        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=str(exc),
            ) from exc
    
    app.state.workflow_registry = workflow_registry
    app.state.tool_registry = tool_registry
    app.state.workflow_agent = workflow_agent
    app.state.workflow_engine = workflow_engine

    return app        

    return app


app = create_app()