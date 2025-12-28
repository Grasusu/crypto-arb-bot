# 🚀 High-Frequency Triangular Arbitrage Engine

A low-latency arbitrage detection system that scans cryptocurrency markets for negative cycles (risk-free profit loops) using Graph Theory.

![Project Status](https://img.shields.io/badge/Status-Production-green)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-purple)

## 📊 Overview
This project simulates a High-Frequency Trading (HFT) strategy. It connects to the Binance API, constructs a directed graph of exchange rates, and uses the **Bellman-Ford Algorithm** to detect inefficiencies in the market.

**Key Features:**
* **O(V·E) Negative Cycle Detection:** Implements Bellman-Ford to find arbitrage loops (e.g., `USDT -> BTC -> ETH -> USDT`).
* **Real-Time TUI Dashboard:** Live terminal interface built with `rich` for monitoring spreads and latency.
* **Latency Optimized:** Execution loop tuned for <300ms cycle time.
* **Audit Logging:** automatically saves profitable opportunities to `trade_log.csv`.

## 🛠️ Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/crypto-arb-bot.git](https://github.com/YOUR_USERNAME/crypto-arb-bot.git)
    cd crypto-arb-bot
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## ⚡ Usage

Run the main engine:
```bash
python main.py