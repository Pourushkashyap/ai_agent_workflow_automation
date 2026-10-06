from pathlib import Path

from app.workflow.bootstrap import create_workflow_registry


EXCEL_PATH = Path("data/AI_Agent_Workflow_Assessment (1).xlsx")


def main():
    registry = create_workflow_registry(EXCEL_PATH)

    for workflow in registry.list_all():
        print("=" * 70)
        print(f"ID       : {workflow.workflow_id}")
        print(f"Name     : {workflow.workflow_name}")
        print(f"Tools    : {workflow.tools_required}")
        print()

        for step in workflow.steps:
            print(f"  Step ID : {step.step_id}")
            print(f"  Name    : {step.name}")
            print(f"  Type    : {step.step_type}")
            print(f"  Tool    : {step.tool}")
            print()


if __name__ == "__main__":
    main()