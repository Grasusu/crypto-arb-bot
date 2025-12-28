import time
import os
import csv
from colorama import Fore, Style, init

# IMPORT OUR NEW MODULES
import config
import market_data
import strategy

# Initialize colors
init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def log_opportunity(path, profit):
    file_exists = os.path.isfile(config.LOG_FILE)
    with open(config.LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Timestamp', 'Path', 'Profit_USD'])
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        path_str = " -> ".join(path)
        writer.writerow([timestamp, path_str, f"{profit:.6f}"])

def run():
    print("🚀 Starting Arbitrage Bot (Modular Version)...")
    
    try:
        while True:
            # 1. FETCH
            tickers = market_data.fetch_prices()
            graph = market_data.build_graph(tickers)
            
            # 2. ANALYZE
            # We pass the whitelist from config
            path, profit = strategy.find_best_triangle(graph, config.COINS_WHITELIST)
            
            # 3. VISUALIZE
            clear_screen()
            print(Fore.CYAN + "=== JANE STREET INTERNSHIP PROJECT v4.0 ===")
            print(f"Scanning {len(config.COINS_WHITELIST)} coins...")
            
            if path:
                # FIX: Handle variable path lengths (Bellman-Ford can find 4+ coin loops)
                # Instead of "c1, c2, c3", we join the whole list into a string
                path_str = " -> ".join(path)
                
                color = Fore.GREEN if profit > 0 else Fore.RED
                
                print("\nTop Opportunity:")
                print(f"{Style.BRIGHT}{path_str} -> {path[0]}") # Close the loop visually
                print(f"{color}Net Result: ${100.00 + profit:.4f}")
                
                if profit > 0:
                    print(Fore.GREEN + "💰 PROFIT CONFIRMED 💰")
                    log_opportunity(path, profit)
            
            # 4. SLEEP
            time.sleep(config.REFRESH_RATE)
            
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped.")

if __name__ == "__main__":
    run()