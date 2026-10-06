from pathlib import Path
from typing import List

import pandas as pd

from app.workflow.models import WorkflowDefinition, WorkflowStep


class WorkflowLoader:
    """
    Loads workflow definitions from the Excel file.

    The Excel file acts as the source of truth for the workflows.
    """

    REQUIRED_COLUMNS = [
        "Workflow_ID",
        "Workflow_Name",
        "Trigger",
        "Inputs",
        "Steps",
        "Decision_Logic",
        "Tools_Required",
        "Expected_Output",
    ]

    def __init__(self, excel_path: str | Path):
        self.excel_path = Path(excel_path)

    def load(self) -> List[WorkflowDefinition]:
        """
        Load all workflows from the Workflows sheet.
        """

        if not self.excel_path.exists():
            raise FileNotFoundError(
                f"Workflow Excel file not found: {self.excel_path}"
            )

        dataframe = pd.read_excel(
            self.excel_path,
            sheet_name="Workflows"
        )

        self._validate_columns(dataframe)

        workflows = []

        for _, row in dataframe.iterrows():
            workflow = self._parse_workflow(row)
            workflows.append(workflow)

        return workflows

    def _validate_columns(self, dataframe: pd.DataFrame) -> None:
        """
        Make sure the Excel file contains all required columns.
        """

        missing_columns = [
            column
            for column in self.REQUIRED_COLUMNS
            if column not in dataframe.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required Excel columns: {missing_columns}"
            )

    def _parse_workflow(self, row: pd.Series) -> WorkflowDefinition:
        """
        Convert one Excel row into a WorkflowDefinition.
        """

        workflow_id = self._clean_value(row["Workflow_ID"])
        workflow_name = self._clean_value(row["Workflow_Name"])
        trigger = self._clean_value(row["Trigger"])
        inputs_text = self._clean_value(row["Inputs"])
        steps_text = self._clean_value(row["Steps"])
        decision_logic_text = self._clean_value(row["Decision_Logic"])
        tools_text = self._clean_value(row["Tools_Required"])
        expected_output = self._clean_value(row["Expected_Output"])

        steps = self._parse_steps(steps_text)

        return WorkflowDefinition(
            workflow_id=workflow_id,
            workflow_name=workflow_name,
            trigger=trigger,
            inputs=self._split_list(inputs_text, ";"),
            steps=steps,
            decision_logic=self._split_list(decision_logic_text, ";"),
            tools_required=self._split_list(tools_text, ";"),
            expected_output=expected_output,
        )

    def _parse_steps(self, steps_text: str) -> List[WorkflowStep]:
        """
        Convert the Excel step description into structured steps.

        Example:

        Load inventory → compare stock → identify low-stock products

        becomes:

        [
            WorkflowStep(...),
            WorkflowStep(...),
            WorkflowStep(...)
        ]
        """

        if not steps_text:
            return []

        raw_steps = steps_text.split("→")

        steps = []

        for index, raw_step in enumerate(raw_steps, start=1):
            step_name = raw_step.strip()

            if not step_name:
                continue

            step_type = self._infer_step_type(step_name)

            steps.append(
                WorkflowStep(
                    step_id=f"step_{index}",
                    name=step_name,
                    step_type=step_type,
                )
            )

        return steps

    def _infer_step_type(self, step_name: str) -> str:
        """
        Infer the basic type of a workflow step.

        This is intentionally simple for now.
        Later, the workflow engine can use more explicit
        step configuration.
        """

        step = step_name.lower()

        if any(
            keyword in step
            for keyword in [
                "generate",
                "create",
                "write",
                "draft",
            ]
        ):
            return "llm"

        if any(
            keyword in step
            for keyword in [
                "compare",
                "check",
                "validate",
                "calculate",
                "identify",
                "match",
                "filter",
                "classify",
                "rank",
            ]
        ):
            return "processing"

        if any(
            keyword in step
            for keyword in [
                "load",
                "read",
                "fetch",
                "search",
                "lookup",
            ]
        ):
            return "tool"

        return "processing"

    @staticmethod
    def _split_list(value: str, separator: str) -> List[str]:
        """
        Convert a text field into a list.

        Example:

        'CSV reader; calculator'

        becomes:

        ['CSV reader', 'calculator']
        """

        if not value:
            return []

        return [
            item.strip()
            for item in value.split(separator)
            if item.strip()
        ]

    @staticmethod
    def _clean_value(value) -> str:
        """
        Safely convert an Excel cell value into a string.
        """

        if pd.isna(value):
            return ""

        return str(value).strip()


def load_workflows(excel_path: str | Path) -> List[WorkflowDefinition]:
    """
    Convenience function for loading workflows.
    """

    loader = WorkflowLoader(excel_path)

    return loader.load()