import time
import os
import csv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live

# IMPORT YOUR MODULES
import config
import market_data
import strategy

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def log_opportunity(path, profit):
    """
    Appends profitable trades to the CSV file defined in config.py.
    """
    file_exists = os.path.isfile(config.LOG_FILE)
    with open(config.LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Timestamp', 'Path', 'Profit_USD'])
            
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        path_str = " -> ".join(path)
        writer.writerow([timestamp, path_str, f"{profit:.6f}"])

def run():
    print("🚀 Starting Arbitrage Bot...")
    
    # Initialize the Rich Console
    console = Console()
    
    try:
        while True:
            # --- 1. DATA COLLECTION & STRATEGY ---
            tickers = market_data.fetch_prices()
            graph = market_data.build_graph(tickers)
            path, profit = strategy.find_best_triangle(graph, config.COINS_WHITELIST)
            
            # --- 2. VISUALIZATION ---
            clear_screen()
            
            # A. The Header Panel
            console.print(Panel.fit(
                "[bold cyan]Jane Street Internship Project v5.0[/bold cyan]\n"
                f"[dim]Scanning {len(config.COINS_WHITELIST)} assets via Binance API[/dim]",
                border_style="cyan"
            ))
            console.print(f"Last Update: [yellow]{time.strftime('%H:%M:%S')}[/yellow]")

            # B. The Data Table
            table = Table(show_header=True, header_style="bold magenta", expand=True)
            table.add_column("Status", justify="center", style="bold")
            table.add_column("Arbitrage Path", min_width=40)
            table.add_column("Net Profit ($)", justify="right")

            if path:
                # Format the path for display (e.g., BTC -> ETH -> USDT)
                path_str = " -> ".join(path) + f" -> {path[0]}"
                
                if profit > 0:
                    # --- CRITICAL: LOGGING HAPPENS HERE ---
                    log_opportunity(path, profit)
                    
                    status = "[green]✅ FOUND[/green]"
                    profit_display = f"[bold green]+${profit:.4f}[/bold green]"
                    path_display = f"[bold white]{path_str}[/bold white]"
                else:
                    status = "[red]❌ LOW[/red]"
                    profit_display = f"[red]${profit:.4f}[/red]"
                    path_display = f"[dim]{path_str}[/dim]"
                
                table.add_row(status, path_display, profit_display)
            else:
                table.add_row("[yellow]SCANNING[/yellow]", "No valid cycles detected", "--")

            console.print(table)
            
            # C. Performance Footer
            if path and profit > 0:
                console.print(Panel("[bold green]💰 PROFITABLE OPPORTUNITY LOGGED TO CSV[/bold green]", border_style="green"))
            
            # --- 3. RATE LIMITING ---
            time.sleep(config.REFRESH_RATE)
            
    except KeyboardInterrupt:
        console.print("\n[bold red]🛑 Bot stopped by user.[/bold red]")

if __name__ == "__main__":
    run()