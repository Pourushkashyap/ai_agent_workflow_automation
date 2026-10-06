from typing import Any, Dict


class ConditionEvaluationError(Exception):
    """Raised when a condition cannot be evaluated."""
    pass


class ConditionEngine:
    """
    Evaluates business conditions used by workflows.

    Example:

        current_stock < minimum_stock

    Context:

        {
            "current_stock": 5,
            "minimum_stock": 10
        }

    Result:

        True
    """

    OPERATORS = {
        "<": lambda left, right: left < right,
        ">": lambda left, right: left > right,
        "<=": lambda left, right: left <= right,
        ">=": lambda left, right: left >= right,
        "==": lambda left, right: left == right,
        "!=": lambda left, right: left != right,
    }

    def evaluate(
        self,
        condition: str,
        context: Dict[str, Any],
    ) -> bool:
        """
        Evaluate a condition using the provided context.
        """

        if not condition or not condition.strip():
            raise ConditionEvaluationError(
                "Condition cannot be empty."
            )

        condition = condition.strip()

        operator = self._find_operator(condition)

        if operator is None:
            raise ConditionEvaluationError(
                f"Unsupported condition: {condition}"
            )

        left_expression, right_expression = condition.split(
            operator,
            1,
        )

        left_expression = left_expression.strip()
        right_expression = right_expression.strip()

        left_value = self._resolve_value(
            left_expression,
            context,
        )

        right_value = self._resolve_value(
            right_expression,
            context,
        )

        try:
            return self.OPERATORS[operator](
                left_value,
                right_value,
            )
        except TypeError as exc:
            raise ConditionEvaluationError(
                f"Cannot compare {left_value!r} "
                f"and {right_value!r}"
            ) from exc

    def _find_operator(
        self,
        condition: str,
    ) -> str | None:
        """
        Find a supported comparison operator.
        """

        operators = [
            "<=",
            ">=",
            "==",
            "!=",
            "<",
            ">",
        ]

        for operator in operators:
            if operator in condition:
                return operator

        return None

    def _resolve_value(
        self,
        expression: str,
        context: Dict[str, Any],
    ) -> Any:
        """
        Resolve an expression from the execution context.

        Example:

            expression = "current_stock"

            context = {
                "current_stock": 5
            }

            returns 5
        """

        expression = expression.strip()

        
        if expression in context:
            return context[expression]

        
        try:
            return int(expression)
        except ValueError:
            pass

        try:
            return float(expression)
        except ValueError:
            pass

       
        if expression.lower() == "true":
            return True

        if expression.lower() == "false":
            return False

        
        if (
            len(expression) >= 2
            and expression[0] == expression[-1]
            and expression[0] in {"'", '"'}
        ):
            return expression[1:-1]

        raise ConditionEvaluationError(
            f"Unable to resolve value: {expression}"
        )