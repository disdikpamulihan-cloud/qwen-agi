"""
Module 1 & 8: Async Ingestion & Self-Healing Daemon
"""
import asyncio
import json
import random
import logging
import websockets
from config import Config

logger = logging.getLogger(__name__)

class M1_AsyncIngestion:
    """Non-blocking asynchronous data ingestion from Deriv API"""
    
    def __init__(self):
        self.q = asyncio.Queue()
        self.ws = None
        self.uri = Config.DERIV_WS_URL
        self.symbol = Config.TRADING_SYMBOL
    
    async def run(self):
        """Main ingestion loop with auto-reconnection"""
        while True:
            try:
                logger.info(f"🔌 Connecting to Deriv WebSocket: {self.uri}")
                self.ws = await websockets.connect(self.uri)
                
                # Subscribe to ticks
                subscribe_msg = {
                    "ticks_history": self.symbol,
                    "end": "latest",
                    "count": 500,
                    "style": "ticks",
                    "subscribe": 1
                }
                await self.ws.send(json.dumps(subscribe_msg))
                logger.info("✅ Subscribed to tick stream")
                
                # Listen for messages
                async for msg in self.ws:
                    data = json.loads(msg)
                    if "tick" in data:
                        await self.q.put(data["tick"])
                    elif "error" in data:
                        logger.error(f"❌ API Error: {data['error']}")
                        
            except websockets.exceptions.ConnectionClosed:
                logger.warning("⚠️ WebSocket connection closed, reconnecting...")
                await asyncio.sleep(2 ** random.randint(0, 5))
            except Exception as e:
                logger.error(f"❌ Ingestion error: {e}")
                await asyncio.sleep(2 ** random.randint(0, 5))

class M8_SelfHealingDaemon:
    """Exponential backoff reconnection handler"""
    
    def __init__(self):
        self.attempt = 0
        self.max_delay = 60
    
    def backoff(self):
        """Calculate backoff delay"""
        delay = min(self.max_delay, 2 ** self.attempt)
        self.attempt += 1
        logger.info(f"🔄 Backoff: waiting {delay}s before retry")
        return delay
    
    def reset(self):
        """Reset attempt counter on successful connection"""
        self.attempt = 0
