from typing import Any, Dict, List



INVENTORY_DATA = [
    {
        "product_id": "P001",
        "product_name": "Laptop",
        "current_stock": 5,
        "minimum_stock": 10,
    },
    {
        "product_id": "P002",
        "product_name": "Keyboard",
        "current_stock": 25,
        "minimum_stock": 10,
    },
    {
        "product_id": "P003",
        "product_name": "Mouse",
        "current_stock": 3,
        "minimum_stock": 8,
    },
]


PRODUCT_PRICES = {
    "Laptop": 75000,
    "Keyboard": 1500,
    "Mouse": 800,
}


ORDER_DATA = {
    "ORD001": {
        "order_id": "ORD001",
        "customer": "Rahul",
        "status": "Shipped",
    },
    "ORD002": {
        "order_id": "ORD002",
        "customer": "Aman",
        "status": "Processing",
    },
}



def get_inventory() -> List[Dict[str, Any]]:
    """
    Return all inventory records.
    """

    return INVENTORY_DATA


def get_product_inventory(
    product_id: str,
) -> Dict[str, Any]:

    for product in INVENTORY_DATA:

        if product["product_id"] == product_id:
            return product

    raise ValueError(
        f"Product not found: {product_id}"
    )


def find_low_stock_products() -> List[Dict[str, Any]]:
    """
    Find products whose stock is below minimum level.
    """

    return [
        product
        for product in INVENTORY_DATA
        if product["current_stock"] < product["minimum_stock"]
    ]



def get_product_price(
    product_name: str,
) -> float:
    """
    Return the current price of a product.
    """

    if product_name not in PRODUCT_PRICES:
        raise ValueError(
            f"Product price not found: {product_name}"
        )

    return PRODUCT_PRICES[product_name]


def calculate_price_difference(
    internal_price: float,
    competitor_price: float,
) -> float:
    """
    Calculate the difference between two prices.
    """

    return internal_price - competitor_price



def get_order_status(
    order_id: str,
) -> Dict[str, Any]:
    """
    Return order information.
    """

    if order_id not in ORDER_DATA:
        raise ValueError(
            f"Order not found: {order_id}"
        )

    return ORDER_DATA[order_id]



def calculate_percentage(
    value: float,
    total: float,
) -> float:
    """
    Calculate percentage.
    """

    if total == 0:
        raise ValueError(
            "Total cannot be zero."
        )

    return (value / total) * 100

def calculate_reorder_quantity(
    current_stock: int,
    minimum_stock: int,
) -> int:
    """
    Calculate how many units need to be reordered
    to reach the minimum stock level.
    """

    return max(minimum_stock - current_stock, 0)

def filter_low_stock_products(inventory):
    """
    Return products whose current stock is below
    their minimum stock threshold.
    """

    return [
        product
        for product in inventory
        if product["current_stock"] < product["minimum_stock"]
    ]
def generate_restock_list(products):
    """
    Generate a restock list with suggested reorder quantities.
    """

    restock_list = []

    for product in products:
        reorder_quantity = calculate_reorder_quantity(
            current_stock=product["current_stock"],
            minimum_stock=product["minimum_stock"],
        )

        if reorder_quantity > 0:
            restock_list.append(
                {
                    "product_id": product["product_id"],
                    "product_name": product["product_name"],
                    "current_stock": product["current_stock"],
                    "minimum_stock": product["minimum_stock"],
                    "reorder_quantity": reorder_quantity,
                }
            )

    return restock_list    

def compare_stock_with_threshold(
    inventory: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Compare current stock with minimum stock threshold
    for every product.
    """

    return [
        {
            **product,
            "below_threshold": (
                product["current_stock"]
                < product["minimum_stock"]
            ),
        }
        for product in inventory
    ]


def calculate_reorder_quantities(
    products: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Calculate reorder quantity for each product.
    """

    return [
        {
            **product,
            "reorder_quantity": calculate_reorder_quantity(
                current_stock=product["current_stock"],
                minimum_stock=product["minimum_stock"],
            ),
        }
        for product in products
    ]
    