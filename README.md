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

## Project Structure
trading_bot/
├── bot/
│ ├── init.py
│ ├── client.py # Binance API wrapper (includes mock mode)
│ ├── orders.py # Order placement logic
│ ├── validators.py # Input validation functions
│ └── logging_config.py # Logging configuration
├── cli.py # Main CLI entry point
├── logs/ # Log files directory
├── requirements.txt # Python dependencies
├── README.md # This file
└── .env # API keys (optional)

text

## Installation

1. **Clone or download** this repository
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
Run the bot (no API keys needed - runs in mock mode)

## Quick Commands
#MARKET BUY order
python cli.py BTCUSDT BUY MARKET 0.001

#LIMIT SELL order
python cli.py BTCUSDT SELL LIMIT 0.001 50000

#Check account info
python cli.py --info

#View help
python cli.py --help

## Logging
Each log file records:
Order placement attempts
API requests and responses
Success/failure status
Error messages (if any)

## Mock Mode
The bot runs in mock mode by default, simulating all Binance API responses. This allows:
Testing without real API keys
Safe experimentation
Demonstration of all features
To use real Binance Testnet, set USE_MOCK = False in client.py and add your API keys to .env.

## Requirements
Python 3.7+
Dependencies listed in requirements.txt
