import math
from config import TRADING_FEE

def find_best_triangle(graph, coins):
    """
    Decides which algorithm to use based on the number of coins.
    """
    if len(coins) < 20:
        # For small lists, Brute Force is actually faster (less overhead)
        return brute_force_search(graph, coins)
    else:
        # For big lists (50+ coins), we NEED Bellman-Ford
        return bellman_ford_search(graph, coins)

def brute_force_search(graph, coins):
    """
    Your original O(N^3) logic.
    """
    import itertools
    best_profit = -999999
    best_path = []
    
    possible_paths = list(itertools.permutations(coins, 3))
    
    for path in possible_paths:
        c1, c2, c3 = path
        if c2 in graph[c1] and c3 in graph[c2] and c1 in graph[c3]:
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

def bellman_ford_search(graph, coins):
    """
    O(V*E) Algorithm to find Negative Cycles (Profit Loops).
    """
    # 1. PREPARE DATA
    # We need a 'distance' table and a 'predecessor' table to rebuild the path
    # We use -log(price) as the weight.
    
    transformed_graph = []
    # Create a list of all edges: (u, v, weight)
    for u in coins:
        if u in graph:
            for v in graph[u]:
                price = graph[u][v]
                # Math Trick: weight = -log(price) + log(fee_multiplier)
                # We include fee in the weight so the algo finds 'Net Profit' not just 'Gross Profit'
                # fee_multiplier = 1 - TRADING_FEE (e.g., 0.999)
                # weight = -math.log(price * 0.999)
                weight = -math.log(price * (1 - TRADING_FEE))
                transformed_graph.append((u, v, weight))

    # Distance to source (arbitrarily pick the first coin) is 0
    distance = {coin: float('inf') for coin in coins}
    predecessor = {coin: None for coin in coins}
    source = coins[0]
    distance[source] = 0

    # 2. RELAXATION (V-1 times)
    for _ in range(len(coins) - 1):
        for u, v, weight in transformed_graph:
            if distance[u] + weight < distance[v]:
                distance[v] = distance[u] + weight
                predecessor[v] = u

    # 3. CHECK FOR NEGATIVE CYCLE (The "Arbitrage" Check)
    # If we can relax one more time, a cycle exists.
    for u, v, weight in transformed_graph:
        if distance[u] + weight < distance[v]:
            # FOUND ONE! Now we must retrace our steps to find the loop.
            # print(f"Cycle detected involving {v}!")
            
            path = []
            curr = v
            
            # Walk backwards through predecessors to find the cycle
            for _ in range(len(coins)):
                curr = predecessor[curr]
                if curr is None: break # Should not happen in a cycle
                
            # Now curr is definitely inside the cycle. Walk forward to build it.
            cycle_start = curr
            path.append(cycle_start)
            while True:
                curr = predecessor[curr]
                if curr not in path:
                    path.append(curr)
                else:
                    path.append(curr) # Close the loop
                    break
            
            # The path is backwards (v -> u), so reverse it
            path.reverse()
            
            # Calculate actual profit for this cycle
            return verify_path_profit(path, graph)

    return [], 0.0

def verify_path_profit(path, graph):
    """
    Takes a raw path from Bellman-Ford (e.g., A->B->C->A)
    and calculates the real dollar profit.
    """
    money = 100.0
    valid = True
    
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i+1]
        
        if start in graph and end in graph[start]:
            rate = graph[start][end]
            money = (money * rate) * (1 - TRADING_FEE)
        else:
            valid = False
            break
            
    if valid:
        return path, money - 100.0
    else:
        return [], 0.0