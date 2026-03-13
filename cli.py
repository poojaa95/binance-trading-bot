#!/usr/bin/env python3
"""
Trading Bot CLI for Binance Futures Testnet
"""

import argparse
import sys
from bot.logging_config import setup_logging
from bot.orders import OrderManager
import logging
from colorama import init, Fore, Style
from tabulate import tabulate

# Initialize colorama for colored output
init()

# Setup logging
logger = setup_logging()

# Create order manager instance
order_manager = OrderManager()

def print_success(message):
    """Print success message in green"""
    print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")

def print_error(message):
    """Print error message in red"""
    print(f"{Fore.RED}Error: {message}{Style.RESET_ALL}")

def print_info(message):
    """Print info message in blue"""
    print(f"{Fore.CYAN}{message}{Style.RESET_ALL}")

def print_warning(message):
    """Print warning message in yellow"""
    print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")

def print_table(title, data):
    """Print data as a formatted table"""
    print(f"\n{Fore.CYAN}{title}{Style.RESET_ALL}")
    if isinstance(data, dict):
        table_data = [[k, v] for k, v in data.items()]
        print(tabulate(table_data, headers=["Field", "Value"], tablefmt="grid"))
    else:
        print(data)

def interactive_mode():
    """Run in interactive mode with guided prompts"""
    print_info("=" * 50)
    print_info("Binance Futures Testnet Trading Bot")
    print_info("Interactive Mode")
    print_info("=" * 50)
    
    try:
        # Get order details
        symbol = input(f"{Fore.CYAN}Enter symbol (default: BTCUSDT): {Style.RESET_ALL}").strip()
        if not symbol:
            symbol = "BTCUSDT"
        
        while True:
            side = input(f"{Fore.CYAN}Enter side (BUY/SELL): {Style.RESET_ALL}").strip().upper()
            if side in ["BUY", "SELL"]:
                break
            print_error("Side must be BUY or SELL")
        
        while True:
            order_type = input(f"{Fore.CYAN}Enter order type (MARKET/LIMIT): {Style.RESET_ALL}").strip().upper()
            if order_type in ["MARKET", "LIMIT"]:
                break
            print_error("Order type must be MARKET or LIMIT")
        
        quantity = input(f"{Fore.CYAN}Enter quantity: {Style.RESET_ALL}").strip()
        
        price = None
        if order_type == "LIMIT":
            price = input(f"{Fore.CYAN}Enter price: {Style.RESET_ALL}").strip()
        
        # Place order
        result = order_manager.place_order_simple(symbol, side, order_type, quantity, price)
        
        if result:
            print_success("Order completed successfully!")
        else:
            print_warning("Order failed or was cancelled")
            
    except KeyboardInterrupt:
        print_warning("\nOperation cancelled by user")
    except Exception as e:
        logger.error(f"Error in interactive mode: {e}")
        print_error(str(e))

def main():
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py BTCUSDT BUY MARKET 0.001
  python cli.py BTCUSDT SELL LIMIT 0.001 50000
  python cli.py --interactive
  python cli.py --info
        """
    )
    
    # Add arguments
    parser.add_argument("symbol", nargs="?", help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("side", nargs="?", choices=["BUY", "SELL"], help="BUY or SELL")
    parser.add_argument("type", nargs="?", choices=["MARKET", "LIMIT"], help="MARKET or LIMIT")
    parser.add_argument("quantity", nargs="?", help="Order quantity")
    parser.add_argument("price", nargs="?", help="Price (required for LIMIT orders)")
    
    # Add options
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    parser.add_argument("--info", action="store_true", help="Display account information")
    
    args = parser.parse_args()
    
    try:
        if args.interactive:
            interactive_mode()
        elif args.info:
            # Show account info
            account = order_manager.client.get_account_info()
            print_table("Account Information", {
                "Total Wallet Balance": f"{account.get('totalWalletBalance')} USDT",
                "Available Balance": f"{account.get('availableBalance')} USDT"
            })
        elif args.symbol and args.side and args.type and args.quantity:
            # Place order
            logger.info(f"CLI command: order {args.symbol} {args.side} {args.type} {args.quantity} {args.price if args.price else ''}")
            result = order_manager.place_order_simple(
                args.symbol, args.side, args.type, args.quantity, args.price
            )
            if result:
                logger.info("Order command completed successfully")
            else:
                logger.warning("Order command failed or was cancelled")
        else:
            parser.print_help()
            
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print_error(str(e))

if __name__ == "__main__":
    main()