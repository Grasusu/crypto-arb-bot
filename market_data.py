import ccxt
from config import COINS_WHITELIST

def fetch_prices():
    """
    Connects to Binance and fetches raw tickers.
    """
    exchange = ccxt.binance()
    # No print statements here - keep logic pure!
    try:
        return exchange.fetch_tickers()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return {}

def build_graph(tickers):
    """
    Transforms raw tickers into a directional graph.
    """
    graph = {coin: {} for coin in COINS_WHITELIST}
    
    for symbol, data in tickers.items():
        try:
            base, quote = symbol.split('/')
        except ValueError:
            continue
            
        if base in COINS_WHITELIST and quote in COINS_WHITELIST:
            price = data.get('ask')
            if price is not None and price > 0:
                # Forward: Buy Base
                graph[base][quote] = price
                # Backward: Buy Quote (Inverse)
                graph[quote][base] = 1.0 / price 
                
    return graph