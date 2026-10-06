from app.tools.business_tools import (
    get_inventory,
    get_product_inventory,
    find_low_stock_products,
    compare_stock_with_threshold,
    calculate_reorder_quantities,
    calculate_reorder_quantity,
    filter_low_stock_products,
    generate_restock_list,
    get_product_price,
    calculate_price_difference,
    get_order_status,
    calculate_percentage,
)

from app.tools.workflow_tools import (
    # WF002
    get_product_prices,
    match_products_by_sku,
    compare_internal_vendor_prices,
    calculate_price_percentage_difference,
    flag_price_exceptions,

    # WF003
    read_vendor_file,
    detect_columns,
    normalize_column_names,
    validate_required_fields,
    identify_invalid_rows,
    produce_cleaned_dataset,

    # WF004
    validate_product_attributes,
    generate_product_description,
    generate_short_description,
    generate_seo_title,
    generate_meta_description,

    # WF005
    validate_order_identifier,
    search_order_data,
    retrieve_order_status,
    retrieve_shipment_information,

    # WF006
    load_products,
    normalize_product_identifiers,
    compare_product_identifiers,
    compare_product_attributes,
    group_likely_duplicates,
    assign_duplicate_confidence,

    # WF007
    validate_campaign_inputs,
    identify_campaign_objective,
    summarize_products,
    create_channel_recommendations,
    create_campaign_checklist,

    # WF008
    read_keywords,
    remove_duplicate_keywords,
    classify_search_intent,
    map_keywords_to_categories,
    identify_high_priority_keywords,
    export_keyword_results,

    # WF009
    get_employees,
    understand_task_requirements,
    compare_employee_skills,
    check_current_workload,
    rank_candidates,
    select_employee,

    # WF010
    load_execution_logs,
    calculate_success_failure_rate,
    calculate_average_execution_time,
    identify_frequent_errors,
    identify_slow_steps,
    generate_performance_recommendations,
)

from app.tools.registry import ToolRegistry


def create_tool_registry() -> ToolRegistry:
    """
    Create and configure the application's tool registry.

    All workflow tools are registered here.

    The WorkflowEngine remains generic and does not
    contain workflow-specific tool logic.
    """

    registry = ToolRegistry()

    # ========================================================
    # WF001 - INVENTORY RESTOCK CHECK
    # ========================================================

    registry.register(
        "get_inventory",
        get_inventory,
        description=(
            "Load inventory data and retrieve current stock "
            "and minimum stock for products."
        ),
    )

    registry.register(
        "get_product_inventory",
        get_product_inventory,
        description=(
            "Retrieve inventory information for a specific "
            "product using its product ID."
        ),
    )

    registry.register(
        "find_low_stock_products",
        find_low_stock_products,
        description=(
            "Identify products whose current stock is below "
            "their minimum stock threshold."
        ),
    )

    registry.register(
        "compare_stock_with_threshold",
        compare_stock_with_threshold,
        description=(
            "Compare current stock with minimum stock "
            "threshold for every product."
        ),
    )

    registry.register(
        "calculate_reorder_quantities",
        calculate_reorder_quantities,
        description=(
            "Calculate reorder quantities for products "
            "based on current and minimum stock."
        ),
    )

    registry.register(
        "calculate_reorder_quantity",
        calculate_reorder_quantity,
        description=(
            "Calculate the quantity of products that need "
            "to be reordered to reach the minimum stock level."
        ),
    )

    registry.register(
        "filter_low_stock_products",
        filter_low_stock_products,
        description=(
            "Filter inventory products whose current stock "
            "is below their minimum stock threshold."
        ),
    )

    registry.register(
        "generate_restock_list",
        generate_restock_list,
        description=(
            "Generate a restock list containing low-stock "
            "products and their suggested reorder quantities."
        ),
    )

    registry.register(
        "get_product_price",
        get_product_price,
        description=(
            "Retrieve the current internal price of a product."
        ),
    )

    registry.register(
        "calculate_price_difference",
        calculate_price_difference,
        description=(
            "Calculate the difference between internal and "
            "competitor or vendor product prices."
        ),
    )

    registry.register(
        "get_order_status",
        get_order_status,
        description=(
            "Search order data and retrieve the current "
            "customer order status."
        ),
    )

    registry.register(
        "calculate_percentage",
        calculate_percentage,
        description=(
            "Calculate a percentage from a value and total."
        ),
    )

    # ========================================================
    # WF002 - PRODUCT PRICE VALIDATION
    # ========================================================

    registry.register(
        "get_product_prices",
        get_product_prices,
        description=(
            "Load product prices for price validation."
        ),
    )

    registry.register(
        "match_products_by_sku",
        match_products_by_sku,
        description=(
            "Match products using SKU."
        ),
    )

    registry.register(
        "compare_internal_vendor_prices",
        compare_internal_vendor_prices,
        description=(
            "Compare internal and vendor prices."
        ),
    )

    registry.register(
        "calculate_price_percentage_difference",
        calculate_price_percentage_difference,
        description=(
            "Calculate percentage difference between "
            "internal and vendor prices."
        ),
    )

    registry.register(
        "flag_price_exceptions",
        flag_price_exceptions,
        description=(
            "Flag products exceeding the configured "
            "price difference threshold."
        ),
    )

    # ========================================================
    # WF003 - VENDOR FILE PROCESSING
    # ========================================================

    registry.register(
        "read_vendor_file",
        read_vendor_file,
        description=(
            "Read vendor Excel or CSV data."
        ),
    )

    registry.register(
        "detect_columns",
        detect_columns,
        description=(
            "Detect columns in uploaded vendor data."
        ),
    )

    registry.register(
        "normalize_column_names",
        normalize_column_names,
        description=(
            "Normalize dataset column names."
        ),
    )

    registry.register(
        "validate_required_fields",
        validate_required_fields,
        description=(
            "Validate required fields in vendor data."
        ),
    )

    registry.register(
        "identify_invalid_rows",
        identify_invalid_rows,
        description=(
            "Identify invalid rows in vendor data."
        ),
    )

    registry.register(
        "produce_cleaned_dataset",
        produce_cleaned_dataset,
        description=(
            "Produce a cleaned dataset containing valid rows."
        ),
    )

    # ========================================================
    # WF004 - PRODUCT DESCRIPTION GENERATOR
    # ========================================================

    registry.register(
        "validate_product_attributes",
        validate_product_attributes,
        description=(
            "Validate required product attributes."
        ),
    )

    registry.register(
        "generate_product_description",
        generate_product_description,
        description=(
            "Generate a detailed product description."
        ),
    )

    registry.register(
        "generate_short_description",
        generate_short_description,
        description=(
            "Generate a short product description."
        ),
    )

    registry.register(
        "generate_seo_title",
        generate_seo_title,
        description=(
            "Generate an SEO title for a product."
        ),
    )

    registry.register(
        "generate_meta_description",
        generate_meta_description,
        description=(
            "Generate a product meta description."
        ),
    )

    # ========================================================
    # WF005 - CUSTOMER ORDER STATUS
    # ========================================================

    registry.register(
        "validate_order_identifier",
        validate_order_identifier,
        description=(
            "Validate a customer order identifier."
        ),
    )

    registry.register(
        "search_order_data",
        search_order_data,
        description=(
            "Search order database data using order ID."
        ),
    )

    registry.register(
        "retrieve_order_status",
        retrieve_order_status,
        description=(
            "Retrieve the current order status."
        ),
    )

    registry.register(
        "retrieve_shipment_information",
        retrieve_shipment_information,
        description=(
            "Retrieve shipment and tracking information."
        ),
    )

    # ========================================================
    # WF006 - DUPLICATE PRODUCT DETECTION
    # ========================================================

    registry.register(
        "load_products",
        load_products,
        description=(
            "Load product data for duplicate detection."
        ),
    )

    registry.register(
        "normalize_product_identifiers",
        normalize_product_identifiers,
        description=(
            "Normalize product names and SKUs."
        ),
    )

    registry.register(
        "compare_product_identifiers",
        compare_product_identifiers,
        description=(
            "Compare product identifiers and calculate "
            "name similarity."
        ),
    )

    registry.register(
        "compare_product_attributes",
        compare_product_attributes,
        description=(
            "Compare attributes of duplicate candidates."
        ),
    )

    registry.register(
        "group_likely_duplicates",
        group_likely_duplicates,
        description=(
            "Group products that are likely duplicates."
        ),
    )

    registry.register(
        "assign_duplicate_confidence",
        assign_duplicate_confidence,
        description=(
            "Assign confidence scores to duplicate candidates."
        ),
    )

    # ========================================================
    # WF007 - MARKETING CAMPAIGN BRIEF
    # ========================================================

    registry.register(
        "validate_campaign_inputs",
        validate_campaign_inputs,
        description=(
            "Validate marketing campaign inputs."
        ),
    )

    registry.register(
        "identify_campaign_objective",
        identify_campaign_objective,
        description=(
            "Identify the marketing campaign objective."
        ),
    )

    registry.register(
        "summarize_products",
        summarize_products,
        description=(
            "Summarize products for a marketing campaign."
        ),
    )

    registry.register(
        "create_channel_recommendations",
        create_channel_recommendations,
        description=(
            "Recommend marketing channels for a campaign."
        ),
    )

    registry.register(
        "create_campaign_checklist",
        create_campaign_checklist,
        description=(
            "Create a marketing campaign execution checklist."
        ),
    )

    # ========================================================
    # WF008 - SEO KEYWORD CLASSIFICATION
    # ========================================================

    registry.register(
        "read_keywords",
        read_keywords,
        description=(
            "Read SEO keywords."
        ),
    )

    registry.register(
        "remove_duplicate_keywords",
        remove_duplicate_keywords,
        description=(
            "Remove duplicate SEO keywords."
        ),
    )

    registry.register(
        "classify_search_intent",
        classify_search_intent,
        description=(
            "Classify keywords by search intent."
        ),
    )

    registry.register(
        "map_keywords_to_categories",
        map_keywords_to_categories,
        description=(
            "Map keywords to product or business categories."
        ),
    )

    registry.register(
        "identify_high_priority_keywords",
        identify_high_priority_keywords,
        description=(
            "Identify high-priority SEO keywords."
        ),
    )

    registry.register(
        "export_keyword_results",
        export_keyword_results,
        description=(
            "Export keyword classification results."
        ),
    )

    # ========================================================
    # WF009 - EMPLOYEE TASK ASSIGNMENT
    # ========================================================

    registry.register(
        "get_employees",
        get_employees,
        description=(
            "Load employee data."
        ),
    )

    registry.register(
        "understand_task_requirements",
        understand_task_requirements,
        description=(
            "Understand task requirements and required skills."
        ),
    )

    registry.register(
        "compare_employee_skills",
        compare_employee_skills,
        description=(
            "Compare employee skills with task requirements."
        ),
    )

    registry.register(
        "check_current_workload",
        check_current_workload,
        description=(
            "Check current employee workload and availability."
        ),
    )

    registry.register(
        "rank_candidates",
        rank_candidates,
        description=(
            "Rank employee candidates for task assignment."
        ),
    )

    registry.register(
        "select_employee",
        select_employee,
        description=(
            "Select the best available employee candidate."
        ),
    )

    # ========================================================
    # WF010 - WORKFLOW PERFORMANCE REPORT
    # ========================================================

    registry.register(
        "load_execution_logs",
        load_execution_logs,
        description=(
            "Load workflow execution logs."
        ),
    )

    registry.register(
        "calculate_success_failure_rate",
        calculate_success_failure_rate,
        description=(
            "Calculate workflow success and failure rates."
        ),
    )

    registry.register(
        "calculate_average_execution_time",
        calculate_average_execution_time,
        description=(
            "Calculate average workflow execution time."
        ),
    )

    registry.register(
        "identify_frequent_errors",
        identify_frequent_errors,
        description=(
            "Identify frequent workflow errors."
        ),
    )

    registry.register(
        "identify_slow_steps",
        identify_slow_steps,
        description=(
            "Identify slow workflow steps."
        ),
    )

    registry.register(
        "generate_performance_recommendations",
        generate_performance_recommendations,
        description=(
            "Generate recommendations for improving "
            "workflow performance."
        ),
    )

    return registry