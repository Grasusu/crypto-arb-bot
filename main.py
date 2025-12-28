import ccxt
import time
import itertools # <--- NEW: Helps us generate combinations

def fetch_prices():
    exchange = ccxt.binance()
    print("⏳ Fetching live data from Binance...")
    tickers = exchange.fetch_tickers()
    return tickers

def build_graph(tickers):
    # EXPANDED UNIVERSE: Added BNB, SOL, ADA, XRP
    whitelist = ['BTC', 'ETH', 'USDT', 'BNB', 'SOL', 'ADA', 'XRP']
    graph = {coin: {} for coin in whitelist}
    
    for symbol, data in tickers.items():
        try:
            base, quote = symbol.split('/')
        except ValueError:
            continue
            
        if base in whitelist and quote in whitelist:
            price = data['ask'] 
            if price > 0:
                # Forward: Buy Base, Sell Quote
                graph[base][quote] = price # 1 BTC = 50k USDT
                # Backward: Buy Quote, Sell Base
                graph[quote][base] = 1.0 / price # 1 USDT = 0.00002 BTC

    return graph, whitelist

def find_best_triangle(graph, coins):
    best_profit = -999999
    best_path = []
    
    # Binance Standard Fee (0.1%). 
    # If you use BNB to pay fees, it's 0.075%. Let's be conservative with 0.1%
    fee_percentage = 0.001 
    
    possible_paths = list(itertools.permutations(coins, 3))
    
    for path in possible_paths:
        c1, c2, c3 = path
        
        if c2 in graph[c1] and c3 in graph[c2] and c1 in graph[c3]:
            start_money = 100.0
            
            # Step 1: c1 -> c2 (Apply Fee)
            step1_amt = (start_money * graph[c1][c2]) * (1 - fee_percentage)
            
            # Step 2: c2 -> c3 (Apply Fee)
            step2_amt = (step1_amt * graph[c2][c3]) * (1 - fee_percentage)
            
            # Step 3: c3 -> c1 (Apply Fee)
            final_amt = (step2_amt * graph[c3][c1]) * (1 - fee_percentage)
            
            profit = final_amt - start_money
            
            if profit > best_profit:
                best_profit = profit
                best_path = path

    return best_path, best_profit

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    tickers = fetch_prices()
    market_graph, coin_list = build_graph(tickers)
    
    path, profit = find_best_triangle(market_graph, coin_list)
    
    print("\n--- 🏆 WINNER ---")
    if path:
        print(f"Path: {path[0]} -> {path[1]} -> {path[2]} -> {path[0]}")
        print(f"Result: ${100.00} turns into ${100.00 + profit:.6f}")
        if profit > 0:
            print("🚀 PROFITABLE LOOP FOUND!")
        else:
            print("📉 Best loop is still a loss (Market is efficient right now)")