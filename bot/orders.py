from bot.client import BinanceFuturesClient
from bot.validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price
import logging
from colorama import Fore, Style

logger = logging.getLogger(__name__)

class OrderManager:
    """Manages order placement and display"""
    
    def __init__(self):
        self.client = BinanceFuturesClient()
    
    def place_order_simple(self, symbol: str, side: str, order_type: str, 
                          quantity: str, price: str = None):
        """
        Simplified order placement with basic console output
        """
        try:
            # Validate inputs
            validated_symbol = validate_symbol(symbol)
            validated_side = validate_side(side)
            validated_order_type = validate_order_type(order_type)
            validated_quantity = validate_quantity(quantity)
            validated_price = validate_price(price, order_type)
            
            # Display order summary
            print(f"\n{Fore.CYAN}Order Summary:{Style.RESET_ALL}")
            print(f"  Symbol: {validated_symbol}")
            print(f"  Side: {validated_side}")
            print(f"  Type: {validated_order_type}")
            print(f"  Quantity: {validated_quantity}")
            if validated_price:
                print(f"  Price: {validated_price}")
            
            # Confirm with user
            confirm = input(f"\n{Fore.YELLOW}Confirm order? (y/n): {Style.RESET_ALL}").lower()
            if confirm != 'y':
                logger.info("Order cancelled by user")
                print(f"{Fore.YELLOW}Order cancelled{Style.RESET_ALL}")
                return None
            
            # Place the order
            logger.info(f"Placing order: {validated_symbol} {validated_side} {validated_order_type}")
            order = self.client.place_order(
                symbol=validated_symbol,
                side=validated_side,
                order_type=validated_order_type,
                quantity=validated_quantity,
                price=validated_price
            )
            
            # Display order response
            print(f"\n{Fore.GREEN}Order Response:{Style.RESET_ALL}")
            print(f"  Order ID: {order.get('orderId', 'N/A')}")
            print(f"  Status: {order.get('status', 'N/A')}")
            print(f"  Executed Quantity: {order.get('executedQty', '0')}")
            print(f"  Price: {order.get('price', 'N/A')}")
            
            if order.get('status') in ['NEW', 'FILLED', 'PARTIALLY_FILLED']:
                print(f"{Fore.GREEN}✓ Order placed successfully!{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}⚠ Order placed with status: {order.get('status')}{Style.RESET_ALL}")
            
            return order
            
        except Exception as e:
            logger.error(f"Failed to place order: {e}")
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            return None