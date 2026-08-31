# OWNER: P1
#
# PURPOSE:
# Internal representation and generation of trade data.

import random
from typing import Dict

class MarketSimulator:
    def __init__(self, seed: int = None):
        if seed is not None:
            random.seed(seed)
        
        # Symbol -> baseline price
        self.prices: Dict[str, float] = {
            "AAPL": 175.0,
            "MSFT": 420.0,
            "GOOGL": 150.0,
            "AMZN": 178.0
        }

    def generate_next_trade(self, symbol: str) -> tuple:
        """
        Generate next trade price and volume for the symbol.
        Returns (price, volume, side)
        """
        base_price = self.prices.get(symbol, 100.0)
        # Random walk price variation: -1% to +1%
        price_change = base_price * random.uniform(-0.01, 0.01)
        new_price = round(base_price + price_change, 2)
        if new_price <= 0:
            new_price = 0.01
        self.prices[symbol] = new_price
        
        volume = float(random.randint(10, 1000))
        side = "BUY" if random.random() > 0.5 else "SELL"
        
        return new_price, volume, side
