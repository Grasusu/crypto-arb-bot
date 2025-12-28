import itertools
import math
from config import TRADING_FEE

def find_best_triangle(graph, coins):
    """
    Scans for profitable triangular arbitrage paths.
    """
    best_profit = -999999
    best_path = []
    
    # Generate all combinations of 3 coins
    possible_paths = list(itertools.permutations(coins, 3))
    
    for path in possible_paths:
        c1, c2, c3 = path
        
        # Check if the path exists in the graph
        if c2 in graph[c1] and c3 in graph[c2] and c1 in graph[c3]:
            
            # Start with 100 units
            # Trade 1
            amt1 = (100.0 * graph[c1][c2]) * (1 - TRADING_FEE)
            # Trade 2
            amt2 = (amt1 * graph[c2][c3]) * (1 - TRADING_FEE)
            # Trade 3
            final = (amt2 * graph[c3][c1]) * (1 - TRADING_FEE)
            
            profit = final - 100.0
            
            if profit > best_profit:
                best_profit = profit
                best_path = path

    return best_path, best_profit