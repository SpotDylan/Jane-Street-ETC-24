import argparse
from collections import deque
from enum import Enum
import time
import socket
import json
from itertools import chain

# ~~~~~============== CONFIGURATION  ==============~~~~~
# Replace "REPLACEME" with your team name!
team_name = "CATERPIE"

# ~~~~~============== MAIN LOOP ==============~~~~~

# You should put your code here! We provide some starter code as an example,
# but feel free to change/remove/edit/update any of it as you'd like. If you
# have any questions about the starter code, or what to do next, please ask us!
tickersList = ['BOND', 'VALE', 'VALBZ', 'XLF', 'GS', 'MS', 'WFC']

posLimitDict = {'BOND': 100,
                'VALE': 10,
                'VALBZ': 10,
                'XLF': 100,
                'GS': 100,
                'MS': 100,
                'WFC': 100
                }

# Using Deque to increase popping and appending efficiency
lastPriceDict = {symbol: deque([0]*5) for symbol in tickersList}

# Initialize EMA dictionary; using an exponential moving average to better react to market flucuation as compared to a simple moving average
emaDict = {symbol: 0 for symbol in ['BOND', 'VALE', 'VALBZ', 'XLF', 'GS', 'MS', 'WFC']}

# N = 5 periods for EMA
smoothing_factor = 2 / (5 + 1)  

# def send_order(self, symbol, dir, price, size):

def on_startup(state_manager):
    """Called immediately after the exchange's HELLO message. This lets you setup your
    initial state and orders"""

    # Immediately short BONDs at 1001 and SELL BONDS at 100
    state_manager.send_order('BOND', 'BUY', 999, 100)
    state_manager.send_order('BOND', 'SELL', 1001, 100)
    # Since the inherent value of BOND is known, we can immediately start trading it. Otherwise, we need market data to make more trades.

    pass

def on_book(state_manager, book_message):
    """Called whenever the book for a symbol updates."""
    # initialize book variables
    symbol = book_message['symbol']

    # Check the book for any undervalued BOND orders
    if symbol == 'BOND' and book_message['sell'][0][0] <= 999:        
        state_manager.send_order(symbol, 'buy', book_message['sell'][0][0], book_message['sell'][0][1])
    elif symbol == 'BOND' and book_message['buy'][0][0] >= 1001:        
        state_manager.send_order(symbol, 'sell', book_message['buy'][0][0], book_message['buy'][0][1])

    # Otherwise, no more real book trades to make. This spread strategy will try to buy and sell at the optimal bid/ask prices rather than the book


def on_fill(state_manager, fill_message):
    """Called when one of your orders is filled."""
    # initialize book variables
    keys = ['symbol', 'dir', 'size', 'price']
    symbol, direction, size, price = (fill_message.get(key) for key in keys)

    if (direction == 'BUY'):
        posLimitDict[symbol] -= size
        state_manager.send_order(symbol, 'SELL', price + price//300, size)
    elif (direction == 'SELL'):
        posLimitDict[symbol] += size
        state_manager.send_order(symbol, 'BUY', price - price//300, size)

    pass

def on_trade(state_manager, trade_message):
    """Called when someone else's order is filled."""
    symbol = trade_message['symbol']
    price = trade_message['price']

    # we only want to trade the spread using EMA for GS, WFC, and MS. XLF, BOND, VALE, VALBZ will be done through arbitrage
    if symbol not in ('BOND'):
        # Calculate new EMA
        if emaDict[symbol] == 0:  # Check if it's the first price input
            emaDict[symbol] = price  # Initialize EMA with the first price
        else:
            emaDict[symbol] = (price * smoothing_factor) + (emaDict[symbol] * (1 - smoothing_factor))

        # Example usage of EMA for trading decision
        fairVal = emaDict[symbol]
        if any(v == 0 for v in lastPriceDict[symbol]) == False:
            state_manager.send_order(symbol, 'BUY', fairVal - fairVal // 300, posLimitDict[symbol])
            state_manager.send_order(symbol, 'SELL', fairVal + fairVal // 300, posLimitDict[symbol])

    # state_manager.send_order(trade_message['symbol'], 'SELL', trade_message['price'] + 1, short)
    pass
