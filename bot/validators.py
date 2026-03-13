from typing import Tuple
import logging

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom validation exception"""
    pass

def validate_symbol(symbol: str) -> str:
    """Validate and format symbol"""
    if not symbol or not isinstance(symbol, str):
        raise ValidationError("Symbol must be a non-empty string")
    
    # Convert to uppercase and ensure USDT suffix
    symbol = symbol.upper()
    if not symbol.endswith('USDT'):
        symbol = symbol + 'USDT'
    
    return symbol

def validate_side(side: str) -> str:
    """Validate order side"""
    side = side.upper()
    if side not in ['BUY', 'SELL']:
        raise ValidationError("Side must be either 'BUY' or 'SELL'")
    return side

def validate_order_type(order_type: str) -> str:
    """Validate order type"""
    order_type = order_type.upper()
    if order_type not in ['MARKET', 'LIMIT']:
        raise ValidationError("Order type must be either 'MARKET' or 'LIMIT'")
    return order_type

def validate_quantity(quantity: str) -> float:
    """Validate and convert quantity"""
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValidationError("Quantity must be greater than 0")
        return qty
    except ValueError:
        raise ValidationError("Quantity must be a valid number")

def validate_price(price: str, order_type: str) -> float:
    """Validate price (required for LIMIT orders)"""
    if order_type.upper() == 'LIMIT':
        try:
            p = float(price)
            if p <= 0:
                raise ValidationError("Price must be greater than 0")
            return p
        except ValueError:
            raise ValidationError("Price must be a valid number for LIMIT orders")
    return None