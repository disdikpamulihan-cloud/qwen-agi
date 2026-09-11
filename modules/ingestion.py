"""
Module 1 & 8: Async Ingestion & Self-Healing Daemon (Binance PAXG/Emas Edition)
Optimized with Multi-Exchange Geo-block Auto-Fallback for GitHub Actions Runner
"""
import asyncio
import json
import random
import logging
import websockets

logger = logging.getLogger(__name__)

class M1_AsyncIngestion:
    """Non-blocking asynchronous data ingestion with Auto-Fallback Endpoints"""
    
    def __init__(self):
        self.q = asyncio.Queue()
        self.ws = None
        
        # Daftar endpoint WebSocket untuk data PAXG/Gold yang kompatibel dengan server AS
        self.endpoints = [
            {
                "name": "Binance US",
                "uri": "wss://stream.binance.us:9443/ws/paxgusdt@trade",
                "parser": self._parse_binance
            },
            {
                "name": "Binance Global",
                "uri": "wss://stream.binance.com:9443/ws/paxgusdt@trade",
                "parser": self._parse_binance
            }
        ]
        self.current_ep_idx = 0
        self.symbol = "PAXGUSDT (Gold)"
        self.daemon = M8_SelfHealingDaemon()

    def _parse_binance(self, data):
        """Parser standar untuk stream trade Binance"""
        return {
            "symbol": self.symbol,
            "quote": float(data['p']),       # Price
            "epoch": int(data['T']) / 1000  # Timestamp in seconds
        }

    async def run(self):
        """Main ingestion loop with multi-endpoint fallback & self-healing"""
        while True:
            active_ep = self.endpoints[self.current_ep_idx]
            uri = active_ep["uri"]
            ep_name = active_ep["name"]
            
            try:
                logger.info(f"🔌 Connecting to {ep_name} WebSocket: {uri}")
                
                # Menghubungkan WebSocket tanpa extra_headers yang memicu TypeError
                async with websockets.connect(uri) as ws:
                    self.ws = ws
                    logger.info(f"✅ Connected to {ep_name} ({self.symbol} stream)")
                    
                    # Connection success, reset backoff daemon
                    self.daemon.reset()
                    
                    async for msg in self.ws:
                        data = json.loads(msg)
                        tick_data = active_ep["parser"](data)
                        await self.q.put(tick_data)
                        
            except websockets.exceptions.ConnectionClosed:
                logger.warning(f"⚠️ {ep_name} WebSocket connection closed. Reconnecting...")
                delay = self.daemon.backoff()
                await asyncio.sleep(delay)
                
            except Exception as e:
                logger.error(f"❌ Ingestion error on {ep_name}: {e}")
                
                # Berganti ke endpoint berikutnya jika ada kegagalan jaringan
                self.current_ep_idx = (self.current_ep_idx + 1) % len(self.endpoints)
                next_ep_name = self.endpoints[self.current_ep_idx]["name"]
                logger.info(f"🔄 Switching ingestion endpoint to: {next_ep_name}")
                
                await asyncio.sleep(3)

class M8_SelfHealingDaemon:
    """Exponential backoff reconnection handler"""
    def __init__(self):
        self.attempt = 0
        self.max_delay = 60
    
    def backoff(self):
        delay = min(self.max_delay, (2 ** self.attempt) + random.uniform(0, 1))
        self.attempt += 1
        logger.info(f"🔄 Backoff: waiting {delay:.2f}s before retry")
        return delay
    
    def reset(self):
        self.attempt = 0
