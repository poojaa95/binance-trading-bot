# Binance Futures Testnet Trading Bot

A Python-based trading bot for placing orders on Binance Futures Testnet (USDT-M) with proper logging, error handling, and a clean CLI interface.

## Features

- Place MARKET and LIMIT orders on Binance Futures Testnet
- Support both BUY and SELL sides
- Interactive CLI mode with guided prompts
- Command-line arguments for scripting
- Comprehensive logging of all API requests and responses
- Input validation with clear error messages
- Rich console output with formatted tables
- Exception handling for API errors and network issues

## Important Note About API Access

Due to recent Binance Testnet changes requiring KYC verification, this bot includes a **Mock Mode** that simulates all Binance Futures API responses. This allows you to:

- ✅ Test all functionality without real API keys
- ✅ See how orders would be placed
- ✅ Generate realistic log files
- ✅ Demonstrate the complete code structure

### To Switch to Real Testnet:
1. Complete KYC on Binance Testnet (if possible)
2. Set `USE_MOCK = False` in `client.py`
3. Add your API keys to `.env` file

## Prerequisites

- Python 3.7+
- Binance Futures Testnet account
- API credentials from [Binance Futures Testnet](https://testnet.binancefuture.com/)

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd trading_bot