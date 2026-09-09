"""
Module 1 & 8: Async Ingestion & Self-Healing Daemon (Binance PAXG/Emas Edition)
"""
import asyncio
import json
import random
import logging
import websockets

logger = logging.getLogger(__name__)

class M1_AsyncIngestion:
    """Non-blocking asynchronous data ingestion from Binance Public WebSocket (PAXG = Gold)"""
    
    def __init__(self):
        self.q = asyncio.Queue()
        self.ws = None
        # WebSocket publik Binance untuk Pax Gold (Emas). Tidak butuh API key!
        self.uri = "wss://stream.binance.com:9443/ws/paxgusdt@trade"
        self.symbol = "PAXGUSDT (Gold)"
    
    async def run(self):
        """Main ingestion loop with auto-reconnection"""
        while True:
            try:
                logger.info(f"🔌 Connecting to Binance WebSocket (Gold): {self.uri}")
                self.ws = await websockets.connect(self.uri)
                logger.info(f"✅ Subscribed to {self.symbol} real-time tick stream")
                
                # Reset backoff counter on successful connection
                from modules.ingestion import M8_SelfHealingDaemon # Jika dipisah, atau handle di sini
                
                async for msg in self.ws:
                    data = json.loads(msg)
                    # Format data agar mirip dengan struktur yang diharapkan bot
                    tick_data = {
                        "symbol": self.symbol,
                        "quote": float(data['p']), # 'p' adalah price
                        "epoch": int(data['T']) / 1000 # 'T' adalah timestamp dalam ms
                    }
                    await self.q.put(tick_data)
                    
            except websockets.exceptions.ConnectionClosed:
                logger.warning("⚠️ WebSocket connection closed, reconnecting...")
                await asyncio.sleep(2 ** random.randint(0, 5))
            except Exception as e:
                logger.error(f"❌ Ingestion error: {e}")
                await asyncio.sleep(5)

class M8_SelfHealingDaemon:
    """Exponential backoff reconnection handler"""
    def __init__(self):
        self.attempt = 0
        self.max_delay = 60
    
    def backoff(self):
        delay = min(self.max_delay, 2 ** self.attempt)
        self.attempt += 1
        logger.info(f"🔄 Backoff: waiting {delay}s before retry")
        return delay
    
    def reset(self):
        self.attempt = 0
