# Constant for fixed tax per plastic bag
FIXED_TAX_PER_PLASTIC_BAG = 66  

def validate_price(price):
    """
    Validates that the price is a positive number.
    """
    try:
        price = float(price)
        if price < 0:
            raise ValueError(f"The price must be greater than or equal to zero, received {price}.")
    except ValueError:
        raise ValueError(f"The price must be a number, received {price}.")
    return price

def validate_quantity(quantity):
    """
    Validates that the quantity is a positive integer.
    """
    if quantity <= 0:
        raise ValueError(f"The quantity must be greater than zero, received {quantity}.")
    return quantity

def validate_tax_type(tax_type):
    """
    Validates the tax type, which can be 'exempt', 'fixed', or a percentage.
    """
    if isinstance(tax_type, (int, float)) and tax_type < 0:
        raise ValueError("The tax type must be a non-negative number.")
    if not isinstance(tax_type, (int, float, str)):
        raise TypeError("The tax type must be a number, 'fixed', or 'exempt'.")
    return tax_type

def calculate_item_total(price, quantity, tax_type):
    """
    Calculates the total tax and total price of an item given the price, quantity, and tax type.
    
    Args:
        price (float): Unit price of the item.
        quantity (int): Quantity of items.
        tax_type (str or float): Tax type ('VAT', 'INC', 'exempt', 'fixed' or percentage).
    
    Returns:
        tuple: Total tax and total price of the item.
    """
    price = validate_price(price)
    quantity = validate_quantity(quantity)
    tax_type = validate_tax_type(tax_type)

    total_price = price * quantity

    if tax_type == "exempt":
        total_tax = 0
    elif tax_type == "fixed":
        total_tax = FIXED_TAX_PER_PLASTIC_BAG * quantity
    elif isinstance(tax_type, (int, float)):
        total_tax = total_price * (tax_type / 100)
    else:
        raise ValueError("Unrecognized tax type.")

    return total_tax, total_price + total_tax

def calculate_total_purchase(items):
    """
    Calculates the total taxes and total price of a list of items.
    
    Args:
        items (list of tuples): List of tuples (unit_price, quantity, tax_type).
    
    Returns:
        tuple: Total taxes and total purchase price.
    """
    total_tax = 0
    total_price = 0

    for price, quantity, tax_type in items:
        item_tax, item_total = calculate_item_total(price, quantity, tax_type)
        total_tax += item_tax
        total_price += item_total

    return total_tax, total_price
