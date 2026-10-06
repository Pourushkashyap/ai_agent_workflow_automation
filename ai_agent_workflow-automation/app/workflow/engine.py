from typing import Any, Dict, Optional
from uuid import uuid4
import inspect
from app.workflow.conditions import ConditionEngine
from app.tools.registry import ToolRegistry
from app.workflow.models import (
    StepExecution,
    WorkflowDefinition,
    WorkflowExecutionResult,
)
from app.workflow.tool_resolver import ToolResolver
from app.services.llm_service import LLMService

class WorkflowExecutionError(Exception):
    """Raised when workflow execution fails."""

    pass


class WorkflowEngine:
    """
    Generic workflow execution engine.

    Responsibilities:
    - Execute workflow steps in order
    - Resolve natural-language steps to tools
    - Execute registered tools
    - Pass workflow context between steps
    - Support single-item and collection processing
    - Track execution results
    - Handle execution errors
    - Build final workflow result

    No workflow ID is hard-coded here.
    """

    def __init__(
        self,
        tool_registry: Optional[ToolRegistry] = None,
        tool_resolver: Optional[ToolResolver] = None,
        llm_service: Optional[LLMService] = None,
        condition_engine: Optional[ConditionEngine] = None,
    ):
        self.tool_registry = tool_registry or ToolRegistry()

        self.tool_resolver = (
            tool_resolver
            or ToolResolver(self.tool_registry)
        )

        self.llm_service = llm_service 

        self.condition_engine = (
            condition_engine
            or ConditionEngine()
        )
    # =========================================================
    # Main workflow execution
    # =========================================================

    def execute(
        self,
        workflow: WorkflowDefinition,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> WorkflowExecutionResult:

        parameters = parameters or {}

        execution_id = str(uuid4())

        steps_executed = []

        
        step_results: Dict[str, Any] = {}

        try:

            for step in workflow.steps:

                try:

                    step_result = self._execute_step(
                        step=step,
                        parameters=parameters,
                        step_results=step_results,
                    )

                    step_results[
                        step.step_id
                    ] = step_result

                    steps_executed.append(
                        StepExecution(
                            step_id=step.step_id,
                            step_name=step.name,
                            status="completed",
                            result=step_result,
                        )
                    )

                except Exception as exc:

                    steps_executed.append(
                        StepExecution(
                            step_id=step.step_id,
                            step_name=step.name,
                            status="failed",
                            result=None,
                            error=str(exc),
                        )
                    )

                    raise

            final_result = self._build_final_result(
                workflow=workflow,
                steps_executed=steps_executed,
            )

            return WorkflowExecutionResult(
                execution_id=execution_id,
                workflow_id=workflow.workflow_id,
                workflow_name=workflow.workflow_name,
                status="completed",
                steps_executed=steps_executed,
                final_result=final_result,
            )

        except Exception as exc:

            return WorkflowExecutionResult(
                execution_id=execution_id,
                workflow_id=workflow.workflow_id,
                workflow_name=workflow.workflow_name,
                status="failed",
                steps_executed=steps_executed,
                error=str(exc),
            )

    

    def _execute_step(self, step, parameters, step_results):
       
        if step.condition:
            context = dict(parameters)

            latest_result = self._latest_result(step_results)

            if isinstance(latest_result, dict):
                context.update(latest_result)

            condition_result = self.condition_engine.evaluate(
                condition=step.condition,
                context=context,
            )

            if not condition_result:
                return {
                    "status": "skipped",
                    "reason": f"Condition not satisfied: {step.condition}",
                }

        
        tool_name = step.tool

        
        if not tool_name:
            tool_name = self.tool_resolver.resolve(step)

        
            tool = self.tool_registry.get(tool_name)

            tool_parameters = dict(parameters)

            tool_parameters = self._map_context_to_tool(
                tool,
                parameters=tool_parameters,
                step_results=step_results,
            )

            return self._execute_tool(
                tool=tool,
                tool_parameters=tool_parameters,
            )


        if step.step_type == "llm":
            if self.llm_service is None:
                self.llm_service = LLMService()

            context = self._latest_result(step_results)

            return self.llm_service.generate(
                instruction=step.name,
                context=context,
            )

        
        raise WorkflowExecutionError(
            f"Unable to resolve executable tool for step: {step.name}"
        )
        
    
    
    
    
    
    
    def _execute_tool(
        self,
        tool,
        tool_parameters: Dict[str, Any],
    ) -> Any:
        """
        Execute a tool.

        Supports:

        1. Normal execution

            tool(value)

        2. Collection execution

            [
                {"a": 1, "b": 2},
                {"a": 3, "b": 4},
            ]

        for a tool such as:

            calculate(a, b)

        The original dictionaries are preserved and enriched
        with the calculated result.
        """

        collection = tool_parameters.pop(
            "__collection_context__",
            None,
        )

        

        if collection is None:

            return tool(
                **tool_parameters
            )

        
        if not isinstance(collection, list):

            raise WorkflowExecutionError(
                "Collection context must be a list."
            )

        if not collection:

            return []

        if not all(
            isinstance(item, dict)
            for item in collection
        ):

            raise WorkflowExecutionError(
                "Collection context must contain dictionaries."
            )

        

        signature = inspect.signature(tool)

        required_parameters = [
            parameter
            for parameter in signature.parameters.values()
            if (
                parameter.kind
                in (
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.KEYWORD_ONLY,
                )
                and parameter.default
                is inspect.Parameter.empty
            )
        ]

        results = []

        

        for item in collection:

            item_parameters = {}

            
            for key, value in tool_parameters.items():
                item_parameters[key] = value

            
            for parameter in required_parameters:

                parameter_name = parameter.name

                if parameter_name in item:

                    item_parameters[
                        parameter_name
                    ] = item[parameter_name]

            # Check missing parameters.
            missing_parameters = [
                parameter.name
                for parameter in required_parameters
                if parameter.name not in item_parameters
            ]

            if missing_parameters:

                raise WorkflowExecutionError(
                    f"Missing parameters "
                    f"{missing_parameters} for tool "
                    f"'{tool.__name__}'."
                )

            # Execute actual tool.
            result = tool(
                **item_parameters
            )

           

            enriched_item = dict(item)

            if isinstance(result, dict):

                enriched_item.update(result)

            else:

                output_field = self._infer_output_field(
                    tool
                )

                enriched_item[
                    output_field
                ] = result

            results.append(
                enriched_item
            )

        return results

    

    def _map_context_to_tool(
        self,
        tool,
        parameters: Dict[str, Any],
        step_results: Dict[str, Any],
    ) -> Dict[str, Any]:

        mapped_parameters = dict(parameters)

        latest_result = self._latest_result(
            step_results
        )

        signature = inspect.signature(tool)

        required_parameters = [
            parameter
            for parameter in signature.parameters.values()
            if (
                parameter.kind
                in (
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.KEYWORD_ONLY,
                )
                and parameter.name
                not in mapped_parameters
                and parameter.default
                is inspect.Parameter.empty
            )
        ]

        

        if not required_parameters:

            return mapped_parameters

        

        if (
            latest_result is not None
            and len(required_parameters) == 1
        ):

            parameter_name = (
                required_parameters[0].name
            )

            mapped_parameters[
                parameter_name
            ] = latest_result

            return mapped_parameters

        

        if (
            isinstance(latest_result, list)
            and all(
                isinstance(item, dict)
                for item in latest_result
            )
        ):

            mapped_parameters[
                "__collection_context__"
            ] = latest_result

            return mapped_parameters

        
        return mapped_parameters

    

    def _latest_result(
        self,
        step_results: Dict[str, Any],
    ) -> Any:

        if not step_results:
            return None

        latest_step_id = list(
            step_results.keys()
        )[-1]

        return step_results[
            latest_step_id
        ]

    

    def _infer_output_field(
        self,
        tool,
    ) -> str:
        """
        Infer a useful output field for scalar tool results.

        Example:

            calculate_reorder_quantity
                ↓
            reorder_quantity
        """

        tool_name = tool.__name__

        prefixes = [
            "calculate_",
            "get_",
            "find_",
            "filter_",
        ]

        for prefix in prefixes:

            if tool_name.startswith(prefix):

                field_name = tool_name[
                    len(prefix):
                ]

                return field_name

        return "result"

   

    def _build_final_result(
        self,
        workflow: WorkflowDefinition,
        steps_executed,
    ) -> Dict[str, Any]:

        return {
            "workflow_id": workflow.workflow_id,
            "workflow_name": workflow.workflow_name,
            "expected_output": workflow.expected_output,
            "steps": [
                {
                    "step_id": step.step_id,
                    "step_name": step.step_name,
                    "status": step.status,
                    "result": step.result,
                    "error": step.error,
                }
                for step in steps_executed
            ],
        }