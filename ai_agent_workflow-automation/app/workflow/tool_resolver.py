from typing import Optional

from app.tools.registry import ToolRegistry
from app.workflow.models import WorkflowStep


class ToolResolver:
    """
    Resolve natural-language workflow steps to executable tools.

    The resolver uses:
    - step wording
    - tool name
    - tool description
    - action synonyms
    """

    ACTION_SYNONYMS = {
        "identify": {"filter", "find", "detect"},
        "filter": {"identify", "find"},
        "find": {"identify", "filter", "search"},
        "load": {"read", "fetch", "retrieve", "get"},
        "read": {"load", "fetch", "retrieve"},
        "retrieve": {"get", "fetch", "read"},
        "get": {"retrieve", "fetch"},
        "calculate": {"compute"},
        "compute": {"calculate"},
        "compare": {"check", "validate"},
        "check": {"compare", "validate"},
        "generate": {"create", "produce", "build"},
        "create": {"generate", "produce"},
    }
    
    PREFERRED_TOOL_FOR_ACTION = {
    "identify": "filter_low_stock_products",
    "filter": "filter_low_stock_products",
    "calculate": "calculate_reorder_quantities",
}

    def __init__(self, tool_registry: ToolRegistry):
        self.tool_registry = tool_registry

    def resolve(self, step: WorkflowStep) -> Optional[str]:
        step_text = step.name.lower().strip()

        # =========================================================
        # Explicit workflow-step mappings
        # =========================================================
        EXACT_STEP_TO_TOOL = {
            # WF001 - Inventory Restock
            "load inventory": "get_inventory",
            "identify low-stock products": "filter_low_stock_products",
            "calculate reorder quantity": "calculate_reorder_quantity",
            "generate restock list": "generate_restock_list",

            # WF002 - Product Price Validation
            "load product prices": "get_product_prices",
            "match products by sku": "match_products_by_sku",
            "compare internal and vendor prices":
                "compare_internal_vendor_prices",
            "calculate percentage difference":
                "calculate_price_percentage_difference",
            "flag exceptions": "flag_price_exceptions",

            # WF003 - Vendor File Processing
            "read file": "read_vendor_file",
            "detect columns": "detect_columns",
            "normalize column names": "normalize_column_names",
            "validate required fields":
                "validate_required_fields",
            "identify invalid rows": "identify_invalid_rows",
            "produce cleaned dataset":
                "produce_cleaned_dataset",

            # WF004 - Product Description
            "validate required attributes":
                "validate_product_attributes",
            "create product description":
                "generate_product_description",
            "generate short description":
                "generate_short_description",
            "generate seo title":
                "generate_seo_title",
            "generate meta description":
                "generate_meta_description",

            # WF005 - Order Status
            "validate identifier":
                "validate_order_identifier",
            "search order data":
                "search_order_data",
            "retrieve order status":
                "retrieve_order_status",
            "retrieve shipment information":
                "retrieve_shipment_information",

            # WF006 - Duplicate Detection
            "load products":
                "load_products",
            "normalize names/skus":
                "normalize_product_identifiers",
            "compare identifiers":
                "compare_product_identifiers",
            "compare product attributes":
                "compare_product_attributes",
            "group likely duplicates":
                "group_likely_duplicates",
            "assign confidence":
                "assign_duplicate_confidence",

            # WF007 - Marketing Campaign
            "validate inputs":
                "validate_campaign_inputs",
            "identify campaign objective":
                "identify_campaign_objective",
            "summarize products":
                "summarize_products",
            "create messaging": None,
            "create channel recommendations":
                "create_channel_recommendations",
            "create campaign checklist":
                "create_campaign_checklist",

            # WF008 - SEO Keywords
            "read keywords":
                "read_keywords",
            "remove duplicates":
                "remove_duplicate_keywords",
            "classify search intent":
                "classify_search_intent",
            "map keywords to categories":
                "map_keywords_to_categories",
            "identify high-priority keywords":
                "identify_high_priority_keywords",
            "export results":
                "export_keyword_results",

            # WF009 - Employee Assignment
            "understand task requirements":
                "understand_task_requirements",
            "compare employee skills":
                "compare_employee_skills",
            "check current workload":
                "check_current_workload",
            "rank candidates":
                "rank_candidates",
            "select employee":
                "select_employee",
            "generate assignment summary": None,

            # WF010 - Performance Report
            "load execution logs":
                "load_execution_logs",
            "calculate success/failure rate":
                "calculate_success_failure_rate",
            "calculate average execution time":
                "calculate_average_execution_time",
            "identify frequent errors":
                "identify_frequent_errors",
            "identify slow steps":
                "identify_slow_steps",
            "generate recommendations":
                "generate_performance_recommendations",
        }

        # Exact normalized match
        if step_text in EXACT_STEP_TO_TOOL:
            tool_name = EXACT_STEP_TO_TOOL[step_text]

            if tool_name is None:
                return None

            if self.tool_registry.exists(tool_name):
                return tool_name

        # =========================================================
        # Existing special cases
        # =========================================================

        step_words = self._tokenize(step_text)

        if (
            "identify" in step_words
            and "low-stock" in step_text
        ):
            if self.tool_registry.exists(
                "filter_low_stock_products"
            ):
                return "filter_low_stock_products"

        if (
            "filter" in step_words
            and "low-stock" in step_text
        ):
            if self.tool_registry.exists(
                "filter_low_stock_products"
            ):
                return "filter_low_stock_products"

        if "calculate reorder quantity" in step_text:
            if self.tool_registry.exists(
                "calculate_reorder_quantity"
            ):
                return "calculate_reorder_quantity"

        if "calculate reorder quantities" in step_text:
            if self.tool_registry.exists(
                "calculate_reorder_quantities"
            ):
                return "calculate_reorder_quantities"

        # =========================================================
        # Generic fallback
        # =========================================================

        best_tool = None
        best_score = 0

        for metadata in (
            self.tool_registry
            .get_tool_metadata()
            .values()
        ):
            tool_name = metadata["name"]
            description = metadata["description"].lower()

            score = self._calculate_match_score(
                step_text=step_text,
                description=description,
                tool_name=tool_name,
            )

            if score > best_score:
                best_score = score
                best_tool = tool_name

        return best_tool
    
    
    
    
    
    def _calculate_match_score(
        self,
        step_text: str,
        description: str,
        tool_name: str = "",
    ) -> int:

        step_words = self._tokenize(step_text)
        description_words = self._tokenize(description)
        tool_words = self._tokenize(
            tool_name.replace("_", " ")
        )

        score = 0

        # ---------------------------------------------------------
        # 1. Exact action match gets highest priority
        # ---------------------------------------------------------

        action_words = {
            "identify",
            "filter",
            "find",
            "load",
            "read",
            "retrieve",
            "get",
            "calculate",
            "compute",
            "compare",
            "check",
            "generate",
            "create",
        }

        step_actions = step_words.intersection(action_words)
        tool_actions = tool_words.intersection(action_words)

        for action in step_actions:

            if action in tool_actions:
                score += 20

            synonyms = self.ACTION_SYNONYMS.get(
                action,
                set(),
            )

            if synonyms.intersection(tool_actions):
                score += 5

        # ---------------------------------------------------------
        # 2. Tool-name overlap
        # ---------------------------------------------------------

        score += (
            len(step_words.intersection(tool_words))
            * 3
        )

        # ---------------------------------------------------------
        # 3. Description overlap
        # ---------------------------------------------------------

        score += len(
            step_words.intersection(description_words)
        )

        # ---------------------------------------------------------
        # 4. Semantic action synonym
        # ---------------------------------------------------------

        for step_word in step_words:

            synonyms = self.ACTION_SYNONYMS.get(
                step_word,
                set(),
            )

            if synonyms.intersection(tool_words):
                score += 3

        return score

    
    
    def _tokenize(self, text: str) -> set[str]:

        stopwords = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "to",
            "of",
            "for",
            "with",
            "data",
            "information",
            "products",
        }

        words = set()

        for word in text.lower().split():

            word = word.strip(
                ".,!?;:()[]{}"
            )

            if len(word) > 2 and word not in stopwords:
                words.add(word)

        return words