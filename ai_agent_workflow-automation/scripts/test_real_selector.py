from pathlib import Path

from app.workflow.bootstrap import create_workflow_registry
from app.agents.llm_selector import LLMWorkflowSelector
from app.agents.workflow_agent import WorkflowAgent


EXCEL_PATH = Path("data/AI_Agent_Workflow_Assessment (1).xlsx")


def main():
    print("Loading workflows...")

    registry = create_workflow_registry(EXCEL_PATH)

    print(f"Loaded workflows: {registry.count()}")
    print()

    llm_selector = LLMWorkflowSelector()

    agent = WorkflowAgent(
        workflow_registry=registry,
        llm_selector=llm_selector,
    )

    request = "Check which products are low in stock and need restocking."

    print(f"User Request: {request}")
    print()
    print("Selecting workflow using Groq...")
    print()

    selection = agent.select_workflow(request)

    print("========== WORKFLOW SELECTION ==========")
    print(f"Workflow ID   : {selection.workflow_id}")
    print(f"Workflow Name : {selection.workflow_name}")
    print(f"Confidence    : {selection.confidence}")
    print(f"Reason        : {selection.reason}")
    print(f"Parameters    : {selection.parameters}")


if __name__ == "__main__":
    main()