from binance.client import Client
from binance.exceptions import BinanceAPIException
import logging
import os
import random
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Set this to False if you get real API keys
USE_MOCK = True  # Changed to True since you can't get real keys

class MockBinanceClient:
    """Mock client for testing without real API keys"""
    
    def __init__(self):
        logger.info("🚀 Running in MOCK MODE - No real API keys needed")
        print("\n⚠️  RUNNING IN MOCK MODE - No real orders will be placed")
        print("   This simulates Binance Futures for testing purposes\n")
    
    def place_order(self, symbol: str, side: str, order_type: str, 
                   quantity: float, price: float = None):
        """
        Mock placing an order - simulates Binance response
        """
        logger.info(f"MOCK: Placing {side} {order_type} order for {quantity} {symbol}")
        
        # Simulate different order statuses
        order_id = random.randint(1000000, 9999999)
        
        # Simulate market order (usually fills immediately)
        if order_type.upper() == 'MARKET':
            status = 'FILLED'
            executed_qty = quantity
            avg_price = round(random.uniform(50000, 51000), 2)
            price = 0
        else:  # LIMIT order
            # Simulate limit order (might be new, might be filled)
            if random.random() > 0.3:  # 70% chance of being filled
                status = 'FILLED'
                executed_qty = quantity
                avg_price = price
            else:
                status = 'NEW'
                executed_qty = 0
                avg_price = None
        
        mock_response = {
            'orderId': order_id,
            'symbol': symbol,
            'status': status,
            'side': side,
            'type': order_type,
            'price': str(price) if price else '0',
            'avgPrice': str(avg_price) if avg_price else '0',
            'executedQty': str(executed_qty),
            'origQty': str(quantity),
            'time': int(datetime.now().timestamp() * 1000)
        }
        
        logger.info(f"MOCK: Order response: {mock_response}")
        return mock_response
    
    def get_account_info(self):
        """Mock account information"""
        return {
            'totalWalletBalance': '10000.00',
            'availableBalance': '9999.99',
            'positions': []
        }
    
    def get_symbol_info(self, symbol: str):
        """Mock symbol information"""
        return {
            'symbol': symbol,
            'status': 'TRADING',
            'filters': [
                {'filterType': 'LOT_SIZE', 'stepSize': '0.001'},
                {'filterType': 'PRICE_FILTER', 'tickSize': '0.01'}
            ]
        }

class BinanceFuturesClient:
    """Real Binance Futures Testnet client"""
    
    def __init__(self):
        if USE_MOCK:
            # Use mock client
            self.mock = MockBinanceClient()
            return
            
        # Real client code (only used if USE_MOCK = False)
        self.api_key = os.getenv('BINANCE_TESTNET_API_KEY')
        self.api_secret = os.getenv('BINANCE_TESTNET_API_SECRET')
        
        if not self.api_key or not self.api_secret:
            raise ValueError("API credentials not found. Set USE_MOCK = True to run without keys")
        
        self.client = Client(
            api_key=self.api_key,
            api_secret=self.api_secret,
            testnet=True
        )
        
        self.client.FUTURES_URL = 'https://testnet.binancefuture.com'
        self.client.futures_url = self.client.FUTURES_URL
        
        logger.info("Binance Futures Testnet client initialized")
    
    def place_order(self, symbol: str, side: str, order_type: str, 
                   quantity: float, price: float = None):
        """Place order - uses mock if USE_MOCK is True"""
        if USE_MOCK:
            return self.mock.place_order(symbol, side, order_type, quantity, price)
        
        # Real order placement code (only runs if USE_MOCK = False)
        try:
            order_params = {
                'symbol': symbol,
                'side': side,
                'type': order_type,
                'quantity': quantity
            }
            
            if order_type.upper() == 'LIMIT':
                if not price:
                    raise ValueError("Price is required for LIMIT orders")
                order_params['price'] = price
                order_params['timeInForce'] = 'GTC'
            
            logger.info(f"Placing order: {order_params}")
            order = self.client.futures_create_order(**order_params)
            logger.info(f"Order placed successfully: {order}")
            return order
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error placing order: {e}")
            raise
    
    def get_account_info(self):
        """Get account info - uses mock if USE_MOCK is True"""
        if USE_MOCK:
            return self.mock.get_account_info()
        
        try:
            account = self.client.futures_account()
            logger.info("Account info retrieved successfully")
            return account
        except BinanceAPIException as e:
            logger.error(f"Error getting account info: {e}")
            raise
    
    def get_symbol_info(self, symbol: str):
        """Get symbol info - uses mock if USE_MOCK is True"""
        if USE_MOCK:
            return self.mock.get_symbol_info(symbol)
        
        try:
            info = self.client.futures_exchange_info()
            for s in info['symbols']:
                if s['symbol'] == symbol:
                    return s
            return None
        except BinanceAPIException as e:
            logger.error(f"Error getting symbol info: {e}")
            raise