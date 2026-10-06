from typing import Any, Dict, List
from collections import Counter
import re
from difflib import SequenceMatcher


# ============================================================
# WF002 - PRODUCT PRICE VALIDATION
# ============================================================

PRODUCT_PRICE_DATA = [
    {
        "sku": "SKU001",
        "product_name": "Laptop",
        "internal_price": 75000,
        "vendor_price": 78000,
    },
    {
        "sku": "SKU002",
        "product_name": "Keyboard",
        "internal_price": 1500,
        "vendor_price": 1500,
    },
    {
        "sku": "SKU003",
        "product_name": "Mouse",
        "internal_price": 800,
        "vendor_price": 950,
    },
]


def get_product_prices() -> List[Dict[str, Any]]:
    return PRODUCT_PRICE_DATA.copy()


def match_products_by_sku(
    products: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    return [
        product
        for product in products
        if product.get("sku")
    ]


def compare_internal_vendor_prices(
    products: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    results = []

    for product in products:
        internal = product.get("internal_price", 0)
        vendor = product.get("vendor_price", 0)

        difference = vendor - internal

        item = dict(product)
        item["price_difference"] = difference

        results.append(item)

    return results


def calculate_price_percentage_difference(
    products: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    results = []

    for product in products:
        internal = product.get("internal_price", 0)
        vendor = product.get("vendor_price", 0)

        if internal == 0:
            percentage = 0
        else:
            percentage = (
                abs(vendor - internal)
                / internal
            ) * 100

        item = dict(product)
        item["percentage_difference"] = round(
            percentage,
            2,
        )

        results.append(item)

    return results


def flag_price_exceptions(
    products: List[Dict[str, Any]],
    threshold: float = 10,
) -> List[Dict[str, Any]]:

    results = []

    for product in products:
        item = dict(product)

        percentage = item.get(
            "percentage_difference",
            0,
        )

        item["exception"] = (
            percentage > threshold
        )

        results.append(item)

    return results


# ============================================================
# WF003 - VENDOR FILE PROCESSING
# ============================================================

REQUIRED_VENDOR_FIELDS = {
    "sku",
    "product_name",
    "price",
}


def read_vendor_file(
    rows: List[Dict[str, Any]] | None = None,
) -> List[Dict[str, Any]]:

    if rows is not None:
        return rows

    return [
        {
            "SKU": "SKU001",
            "Product Name": "Laptop",
            "Price": 75000,
        },
        {
            "SKU": "SKU002",
            "Product Name": "Keyboard",
            "Price": 1500,
        },
    ]


def detect_columns(rows):
    if not rows:
        return {
            "columns": [],
            "rows": [],
        }

    columns = list(rows[0].keys())

    return {
        "columns": columns,
        "rows": rows,
    }


def normalize_column_names(rows):
    if isinstance(rows, dict):
        rows = rows.get("rows", [])

    normalized_rows = []

    for row in rows:
        normalized_row = {}

        for key, value in row.items():
            normalized_key = (
                str(key)
                .strip()
                .lower()
                .replace(" ", "_")
            )

            normalized_row[normalized_key] = value

        normalized_rows.append(normalized_row)

    return normalized_rows


def validate_required_fields(
    rows: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:

    results = []

    for index, row in enumerate(rows):

        missing = [
            field
            for field in REQUIRED_VENDOR_FIELDS
            if not row.get(field)
        ]

        results.append(
            {
                "row_number": index + 1,
                "valid": not missing,
                "missing_fields": missing,
                "data": row,
            }
        )

    return results


def identify_invalid_rows(
    rows: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:

    return [
        row
        for row in rows
        if not row.get("valid", False)
    ]


def produce_cleaned_dataset(
    rows: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:

    return [
        row["data"]
        for row in rows
        if row.get("valid", False)
    ]



def validate_product_attributes(
    product: Dict[str, Any],
) -> Dict[str, Any]:

    required = [
        "name",
        "category",
        "features",
    ]

    missing = [
        field
        for field in required
        if not product.get(field)
    ]

    return {
        "valid": not missing,
        "missing_fields": missing,
        "product": product,
    }


def generate_product_description(
    product: Dict[str, Any],
) -> str:

    return (
        f"{product.get('name', 'Product')} is a "
        f"{product.get('category', 'high-quality product')} "
        f"designed with "
        f"{product.get('features', 'useful features')}."
    )


def generate_short_description(
    product: Dict[str, Any],
) -> str:

    return (
        f"{product.get('name', 'Product')} - "
        f"{product.get('category', 'quality product')}."
    )


def generate_seo_title(
    product: Dict[str, Any],
) -> str:

    return (
        f"Buy {product.get('name', 'Product')} | "
        f"{product.get('category', 'Products')}"
    )


def generate_meta_description(
    product: Dict[str, Any],
) -> str:

    return (
        f"Explore {product.get('name', 'this product')}, "
        f"featuring {product.get('features', 'quality features')}."
    )



SHIPMENT_DATA = {
    "ORD001": {
        "carrier": "Delhivery",
        "tracking_id": "TRK001",
        "estimated_delivery": "2026-10-10",
    },
    "ORD002": {
        "carrier": "BlueDart",
        "tracking_id": "TRK002",
        "estimated_delivery": "2026-10-12",
    },
}


def validate_order_identifier(
    order_id: str,
) -> Dict[str, Any]:

    return {
        "valid": bool(
            order_id
            and order_id.strip()
        ),
        "order_id": order_id,
    }


def search_order_data(
    order_id: str,
) -> Dict[str, Any]:

    from app.tools.business_tools import ORDER_DATA

    order = ORDER_DATA.get(order_id)

    if not order:
        raise ValueError(
            f"Order not found: {order_id}"
        )

    return order


def retrieve_order_status(order_id):
    from app.tools.business_tools import ORDER_DATA

    if isinstance(order_id, dict):
        order_id = order_id.get("order_id")

    order = ORDER_DATA.get(order_id)

    if not order:
        raise ValueError(
            f"Order not found: {order_id}"
        )

    return {
        "order_id": order["order_id"],
        "status": order["status"],
    }


def retrieve_shipment_information(order_id):
    shipment = SHIPMENT_DATA.get(order_id)

    if not shipment:
        return {
            "order_id": order_id,
            "shipment_status": "No shipment information available",
        }

    return shipment


# ============================================================
# WF006 - DUPLICATE PRODUCT DETECTION
# ============================================================

def load_products(
    products: List[Dict[str, Any]] | None = None,
) -> List[Dict[str, Any]]:

    if products is not None:
        return products

    return [
        {
            "sku": "SKU001",
            "name": "Apple Laptop",
            "category": "Laptop",
            "price": 75000,
        },
        {
            "sku": "SKU002",
            "name": "Apple Laptop 15 inch",
            "category": "Laptop",
            "price": 75000,
        },
        {
            "sku": "SKU003",
            "name": "Wireless Mouse",
            "category": "Mouse",
            "price": 800,
        },
    ]


def normalize_product_identifiers(
    products: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:

    results = []

    for product in products:
        item = dict(product)

        item["normalized_name"] = re.sub(
            r"[^a-z0-9]",
            "",
            product.get("name", "").lower(),
        )

        item["normalized_sku"] = (
            product.get("sku", "")
            .strip()
            .lower()
        )

        results.append(item)

    return results


def compare_product_identifiers(
    products: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:

    results = []

    for i, first in enumerate(products):
        for second in products[i + 1:]:

            same_sku = (
                first.get("normalized_sku")
                == second.get("normalized_sku")
            )

            similarity = SequenceMatcher(
                None,
                first.get("normalized_name", ""),
                second.get("normalized_name", ""),
            ).ratio()

            if same_sku or similarity >= 0.8:
                results.append(
                    {
                        "product_1": first,
                        "product_2": second,
                        "name_similarity": round(
                            similarity,
                            3,
                        ),
                    }
                )

    return results


def compare_product_attributes(
    duplicate_candidates: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:

    results = []

    for candidate in duplicate_candidates:

        first = candidate["product_1"]
        second = candidate["product_2"]

        same_category = (
            first.get("category")
            == second.get("category")
        )

        same_price = (
            first.get("price")
            == second.get("price")
        )

        item = dict(candidate)

        item["same_category"] = same_category
        item["same_price"] = same_price

        results.append(item)

    return results


def group_likely_duplicates(
    candidates: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:

    return [
        candidate
        for candidate in candidates
        if (
            candidate.get("name_similarity", 0) >= 0.8
            or (
                candidate.get("same_category")
                and candidate.get("same_price")
            )
        )
    ]


def assign_duplicate_confidence(
    groups: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:

    results = []

    for group in groups:

        confidence = group.get(
            "name_similarity",
            0,
        )

        if (
            group.get("same_category")
            and group.get("same_price")
        ):
            confidence = min(
                1.0,
                confidence + 0.1,
            )

        item = dict(group)

        item["confidence"] = round(
            confidence,
            3,
        )

        results.append(item)

    return results


def validate_campaign_inputs(
    campaign: Dict[str, Any],
) -> Dict[str, Any]:

    required = [
        "objective",
        "products",
    ]

    missing = [
        field
        for field in required
        if not campaign.get(field)
    ]

    return {
        "valid": not missing,
        "missing_fields": missing,
        "campaign": campaign,
    }


def identify_campaign_objective(
    campaign: Dict[str, Any],
) -> str:

    return campaign.get(
        "objective",
        "increase product awareness",
    )


def summarize_products(
    products: List[Dict[str, Any]],
) -> str:

    if not products:
        return "No products available."

    names = [
        product.get("name", "Product")
        for product in products
    ]

    return ", ".join(names)


def create_channel_recommendations(
    objective: str,
) -> List[str]:

    objective = objective.lower()

    if "sales" in objective:
        return [
            "Email",
            "Google Ads",
            "Social Media",
        ]

    if "awareness" in objective:
        return [
            "Instagram",
            "YouTube",
            "Social Media",
        ]

    return [
        "Email",
        "Social Media",
    ]


def create_campaign_checklist(
    objective: str,
) -> List[str]:

    return [
        "Define campaign objective",
        "Prepare target audience",
        "Prepare campaign messaging",
        "Create visual assets",
        "Configure channels",
        "Launch campaign",
        "Monitor performance",
    ]


# ============================================================
# WF008 - SEO KEYWORD CLASSIFICATION
# ============================================================

def read_keywords(
    keywords: List[str] | None = None,
) -> List[str]:

    if keywords is not None:
        return keywords

    return [
        "buy laptop",
        "laptop price",
        "best laptop",
        "laptop review",
        "buy laptop",
    ]


def remove_duplicate_keywords(
    keywords: List[str],
) -> List[str]:

    seen = set()
    result = []

    for keyword in keywords:

        normalized = keyword.strip().lower()

        if normalized not in seen:
            seen.add(normalized)
            result.append(normalized)

    return result


def classify_search_intent(
    keywords: List[str],
) -> List[Dict[str, str]]:

    results = []

    for keyword in keywords:

        text = keyword.lower()

        if any(
            word in text
            for word in ["buy", "price", "deal", "discount"]
        ):
            intent = "transactional"

        elif any(
            word in text
            for word in ["best", "review", "compare"]
        ):
            intent = "commercial"

        elif any(
            word in text
            for word in ["how", "what", "guide"]
        ):
            intent = "informational"

        else:
            intent = "navigational"

        results.append(
            {
                "keyword": keyword,
                "intent": intent,
            }
        )

    return results


def map_keywords_to_categories(
    keywords: List[Dict[str, str]],
) -> List[Dict[str, str]]:

    results = []

    for item in keywords:

        keyword = item["keyword"].lower()

        if "laptop" in keyword:
            category = "laptop"

        elif "phone" in keyword:
            category = "mobile"

        elif "mouse" in keyword:
            category = "mouse"

        else:
            category = "general"

        result = dict(item)
        result["category"] = category

        results.append(result)

    return results


def identify_high_priority_keywords(
    keywords: List[Dict[str, str]],
) -> List[Dict[str, str]]:

    high_priority_intents = {
        "transactional",
        "commercial",
    }

    return [
        keyword
        for keyword in keywords
        if keyword.get("intent")
        in high_priority_intents
    ]


def export_keyword_results(
    keywords: List[Dict[str, str]],
) -> Dict[str, Any]:

    return {
        "total_keywords": len(keywords),
        "keywords": keywords,
    }


# ============================================================
# WF009 - EMPLOYEE TASK ASSIGNMENT
# ============================================================

EMPLOYEE_DATA = [
    {
        "employee_id": "E001",
        "name": "Rahul",
        "skills": ["python", "ai", "ml"],
        "workload": 30,
    },
    {
        "employee_id": "E002",
        "name": "Aman",
        "skills": ["react", "javascript", "frontend"],
        "workload": 60,
    },
    {
        "employee_id": "E003",
        "name": "Priya",
        "skills": ["python", "backend", "api"],
        "workload": 20,
    },
]


def get_employees() -> List[Dict[str, Any]]:
    return EMPLOYEE_DATA.copy()


def understand_task_requirements(
    task: Dict[str, Any],
) -> Dict[str, Any]:

    return {
        "task": task.get("task", ""),
        "required_skills": [
            skill.lower()
            for skill in task.get(
                "required_skills",
                [],
            )
        ],
    }


def compare_employee_skills(
    employees: List[Dict[str, Any]],
    required_skills: List[str],
) -> List[Dict[str, Any]]:

    results = []

    for employee in employees:

        employee_skills = {
            skill.lower()
            for skill in employee.get(
                "skills",
                [],
            )
        }

        matched = (
            employee_skills
            & set(required_skills)
        )

        item = dict(employee)

        item["matched_skills"] = list(
            matched
        )

        item["skill_score"] = len(
            matched
        )

        results.append(item)

    return results


def check_current_workload(
    employees: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:

    return [
        {
            **employee,
            "available": employee.get(
                "workload",
                100,
            ) < 80,
        }
        for employee in employees
    ]


def rank_candidates(
    employees: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:

    return sorted(
        employees,
        key=lambda employee: (
            employee.get("skill_score", 0),
            -employee.get("workload", 100),
        ),
        reverse=True,
    )


def select_employee(
    employees: List[Dict[str, Any]],
) -> Dict[str, Any]:

    available = [
        employee
        for employee in employees
        if employee.get("available", True)
    ]

    if not available:
        raise ValueError(
            "No available employee found."
        )

    return available[0]


# ============================================================
# WF010 - WORKFLOW PERFORMANCE REPORT
# ============================================================

EXECUTION_LOGS = [
    {
        "workflow_id": "WF001",
        "status": "success",
        "execution_time": 1.2,
        "error": None,
        "slow_step": None,
    },
    {
        "workflow_id": "WF002",
        "status": "success",
        "execution_time": 2.1,
        "error": None,
        "slow_step": "price comparison",
    },
    {
        "workflow_id": "WF003",
        "status": "failed",
        "execution_time": 3.5,
        "error": "Invalid vendor file",
        "slow_step": "file validation",
    },
]


def load_execution_logs() -> List[Dict[str, Any]]:
    return EXECUTION_LOGS.copy()


def calculate_success_failure_rate(
    logs: List[Dict[str, Any]],
) -> Dict[str, float]:

    total = len(logs)

    if total == 0:
        return {
            "success_rate": 0,
            "failure_rate": 0,
        }

    success = sum(
        log.get("status") == "success"
        for log in logs
    )

    return {
        "success_rate": round(
            success / total * 100,
            2,
        ),
        "failure_rate": round(
            (total - success)
            / total
            * 100,
            2,
        ),
    }


def calculate_average_execution_time(
    logs: List[Dict[str, Any]],
) -> float:

    if not logs:
        return 0

    return round(
        sum(
            log.get(
                "execution_time",
                0,
            )
            for log in logs
        )
        / len(logs),
        2,
    )


def identify_frequent_errors(
    logs: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:

    errors = Counter(
        log.get("error")
        for log in logs
        if log.get("error")
    )

    return [
        {
            "error": error,
            "count": count,
        }
        for error, count in errors.items()
    ]


def identify_slow_steps(
    logs: List[Dict[str, Any]],
) -> List[str]:

    return list(
        {
            log["slow_step"]
            for log in logs
            if log.get("slow_step")
        }
    )


def generate_performance_recommendations(
    metrics: Dict[str, Any],
) -> List[str]:

    recommendations = []

    if metrics.get(
        "failure_rate",
        0,
    ) > 10:

        recommendations.append(
            "Investigate frequent workflow failures."
        )

    if metrics.get(
        "average_execution_time",
        0,
    ) > 3:

        recommendations.append(
            "Optimize slow workflow steps."
        )

    if not recommendations:
        recommendations.append(
            "Workflow performance is within acceptable limits."
        )

    return recommendations