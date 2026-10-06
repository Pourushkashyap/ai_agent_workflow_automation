from pathlib import Path

from app.agents.llm_selector import LLMWorkflowSelector
from app.agents.workflow_agent import WorkflowAgent
from app.tools.loader import create_tool_registry
from app.workflow.bootstrap import create_workflow_registry
from app.workflow.engine import WorkflowEngine
from app.workflow.tool_resolver import ToolResolver
from app.tools.business_tools import (
    filter_low_stock_products,
    generate_restock_list,
    get_inventory,
)

EXCEL_PATH = Path("data/AI_Agent_Workflow_Assessment (1).xlsx")


def main():
    print("=" * 70)
    print("        AI AGENT WORKFLOW AUTOMATION")
    print("=" * 70)

    user_request = input(
        "\nEnter your request:\n> "
    ).strip()

    # --------------------------------------------------
    # 1. Load workflows from Excel
    # --------------------------------------------------
    workflow_registry = create_workflow_registry(EXCEL_PATH)

    print(f"\nLoaded workflows: {workflow_registry.count()}")

    # --------------------------------------------------
    # 2. Initialize AI workflow selector
    # --------------------------------------------------
    llm_selector = LLMWorkflowSelector()
    agent = WorkflowAgent(
        workflow_registry=workflow_registry,
        llm_selector=llm_selector,
    )

    # --------------------------------------------------
    # 3. Select workflow
    # --------------------------------------------------
    selection = agent.select_workflow(user_request)

    workflow = agent.get_workflow(selection)

    print("\n" + "-" * 70)
    print("WORKFLOW SELECTED")
    print("-" * 70)

    print(f"Workflow ID   : {selection.workflow_id}")
    print(f"Workflow Name : {selection.workflow_name}")
    print(f"Confidence    : {selection.confidence}")
    print(f"Reason        : {selection.reason}")

    # --------------------------------------------------
    # 4. Resolve tools
    # --------------------------------------------------
    tool_registry = create_tool_registry()
    resolver = ToolResolver(tool_registry)

    print("\n" + "-" * 70)
    print("WORKFLOW STEPS")
    print("-" * 70)

    for step in workflow.steps:

        if step.step_type == "tool":
            tool_name = resolver.resolve(step)
            step.tool = tool_name

            print(
                f"{step.step_id}: "
                f"{step.name} "
                f"→ {tool_name}"
            )

        else:
            print(
                f"{step.step_id}: "
                f"{step.name} "
                f"→ {step.step_type}"
            )

    # --------------------------------------------------
    # 5. Execute workflow
    # --------------------------------------------------
    engine = WorkflowEngine(
        tool_registry=tool_registry
    )

    result = engine.execute(
        workflow=workflow,
        parameters=selection.parameters,
    )
    
    # --------------------------------------------------
    # WF001 business demonstration
    # --------------------------------------------------
    if selection.workflow_id == "WF001":

        inventory = get_inventory()

        low_stock_products = filter_low_stock_products(
            inventory
        )

        restock_list = generate_restock_list(
            low_stock_products
        )

        print("\n" + "-" * 70)
        print("BUSINESS RESULT")
        print("-" * 70)

        if not restock_list:
            print("No products require restocking.")
        else:
            for product in restock_list:
                print(
                    f"  {product['product_name']}: "
                    f"stock={product['current_stock']}, "
                    f"minimum={product['minimum_stock']}, "
                    f"reorder={product['reorder_quantity']}"
                )

    # --------------------------------------------------
    # 6. Display execution result
    # --------------------------------------------------
    print("\n" + "-" * 70)
    print("EXECUTION RESULT")
    print("-" * 70)

    print(f"Execution ID : {result.execution_id}")
    print(f"Status       : {result.status}")

    print("\nExecuted Steps:")

    for step in result.steps_executed:

        print(
            f"  ✓ {step.step_id} | "
            f"{step.step_name} | "
            f"{step.status}"
        )

        if step.result is not None:
            print(f"    Result: {step.result}")

    print("\n" + "-" * 70)
    print("FINAL RESULT")
    print("-" * 70)

    print(result.final_result)

    if result.error:
        print("\nERROR:")
        print(result.error)


if __name__ == "__main__":
    main()