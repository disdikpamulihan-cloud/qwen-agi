"""
Helper functions for the trading bot
"""
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def format_timestamp(ts):
    """Format Unix timestamp to readable string"""
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def calculate_pnl(entry, exit_price, direction):
    """Calculate profit/loss"""
    if direction == "BUY":
        return exit_price - entry
    else:
        return entry - exit_price

def is_trading_hours(utc_hour):
    """Check if within major trading sessions"""
    # London: 08:00-16:00 UTC
    # New York: 13:00-21:00 UTC
    # Tokyo: 00:00-09:00 UTC
    return (0 <= utc_hour <= 21)
