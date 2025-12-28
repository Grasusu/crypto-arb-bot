import ccxt
import time
import itertools
import os
import math 
from colorama import Fore, Style, init

# Initialize colors
init(autoreset=True)

def clear_screen():
    # Windows uses 'cls', Mac/Linux uses 'clear'
    os.system('cls' if os.name == 'nt' else 'clear')

def fetch_prices():
    exchange = ccxt.binance()
    # We remove the print statement here so it doesn't clutter the dashboard
    tickers = exchange.fetch_tickers()
    return tickers

def build_graph(tickers):
    whitelist = ['BTC', 'ETH', 'USDT', 'BNB', 'SOL', 'ADA', 'XRP', 'DOGE'] # Added DOGE for fun
    graph = {coin: {} for coin in whitelist}
    
    for symbol, data in tickers.items():
        try:
            base, quote = symbol.split('/')
        except ValueError:
            continue
            
        if base in whitelist and quote in whitelist:
            # SAFETY CHECK: Get 'ask', but if it's missing/None, return 0
            price = data.get('ask')
            
            # CHANGED LINE: We check "is not None" specifically
            if price is not None and price > 0:
                graph[base][quote] = price
                graph[quote][base] = 1.0 / price 
    return graph, whitelist

def transform_graph_to_log(graph):
    """
    Turns Price Graph (Multiplication) into Weight Graph (Addition).
    Weight = -log(price).
    """
    log_graph = {}
    
    for base in graph:
        log_graph[base] = {}
        for quote in graph[base]:
            price = graph[base][quote]
            
            
            weight = -math.log(price)
            
            log_graph[base][quote] = weight
            
    return log_graph

def find_best_triangle(graph, coins):
    best_profit = -999999
    best_path = []
    
    # Binance Fee: 0.1% per trade = 0.001
    fee = 0.001
    
    possible_paths = list(itertools.permutations(coins, 3))
    
    for path in possible_paths:
        c1, c2, c3 = path
        if c2 in graph[c1] and c3 in graph[c2] and c1 in graph[c3]:
            
            # Start with 100 units
            # Trade 1 (Fee applied)
            amt1 = (100.0 * graph[c1][c2]) * (1 - fee)
            # Trade 2 (Fee applied)
            amt2 = (amt1 * graph[c2][c3]) * (1 - fee)
            # Trade 3 (Fee applied)
            final = (amt2 * graph[c3][c1]) * (1 - fee)
            
            profit = final - 100.0
            
            if profit > best_profit:
                best_profit = profit
                best_path = path

    return best_path, best_profit

def check_profit_math(path, graph):
    """
    Verifies if a path is profitable using raw math.
    """
    money = 100.0
    fee = 0.001
    
    for i in range(len(path) - 1):
        start_coin = path[i]
        end_coin = path[i+1]
        rate = graph[start_coin][end_coin]
        money = (money * rate) * (1 - fee)
        
    # Close the loop (back to start)
    start_node = path[0]
    last_node = path[-1]
    if start_node in graph[last_node]:
        rate = graph[last_node][start_node]
        money = (money * rate) * (1 - fee)
        
    return money - 100.0

# --- MAIN LOOP ---
if __name__ == "__main__":
    print("🚀 Starting Arbitrage Bot... (Press Ctrl+C to stop)")
    
    try:
        while True:
            # 1. Get Data
            tickers = fetch_prices()
            graph, coins = build_graph(tickers)
            
            # 2. Analyze
            path, profit = find_best_triangle(graph, coins)
            
            # 3. Visualize (The Dashboard)
            clear_screen()
            print(Fore.CYAN + "=================================================")
            print(Fore.CYAN + "       JANE STREET INTERNSHIP PROJECT v3.0       ")
            print(Fore.CYAN + "=================================================")
            print(f"Scanning {len(coins)} coins across Binance...")
            print(f"Last Update: {time.strftime('%H:%M:%S')}\n")
            
            if path:
                # ... (Previous print code) ...
                
                # NEW: Double check using the validation function
                real_profit = check_profit_math(list(path), graph)
                
                print(f"Math Verification: ${100.0 + real_profit:.4f}")
                
                if real_profit > 0:
                     print(Fore.GREEN + Style.BRIGHT + "💰 CONFIRMED PROFIT! 💰")
                     # TODO: This is where you would save to a file
            
            print(Fore.CYAN + "\n=================================================")
            
            # 4. Wait
            # Don't spam the API or you get banned. 3 seconds is safe.
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user.")