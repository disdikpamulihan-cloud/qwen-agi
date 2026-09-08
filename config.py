"""
SINGULARITY AGI TRADING BOT - Configuration Manager
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Centralized configuration management"""
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    
    # Qwen AI
    DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
    QWEN_MODEL_NAME = os.getenv("QWEN_MODEL_NAME", "qwen-max")
    QWEN_BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
    
    # Deriv API
    DERIV_APP_ID = os.getenv("DERIV_APP_ID", "1089")
    DERIV_API_TOKEN = os.getenv("DERIV_API_TOKEN")
    DERIV_WS_URL = f"wss://ws.derivws.com/websockets/v3?app_id={DERIV_APP_ID}"
    
    # Trading
    TRADING_SYMBOL = os.getenv("TRADING_SYMBOL", "frxXAUUSD")
    MAX_POSITION_SIZE = float(os.getenv("MAX_POSITION_SIZE", "0.05"))
    DEFAULT_RISK_PER_TRADE = float(os.getenv("DEFAULT_RISK_PER_TRADE", "0.02"))
    
    # System
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    TELEMETRY_ENABLED = os.getenv("TELEMETRY_ENABLED", "true").lower() == "true"
    SHADOW_MODE_ENABLED = os.getenv("SHADOW_MODE_ENABLED", "true").lower() == "true"
    
    # Paths
    DATA_DIR = "data"
    LOGS_DIR = "logs"
    MODEL_STATE_PATH = os.path.join(DATA_DIR, "model_state.pkl")
    TELEMETRY_PATH = os.path.join(LOGS_DIR, "telemetry.jsonl")
    
    @classmethod
    def validate(cls):
        """Validate critical configuration"""
        required = [
            cls.TELEGRAM_BOT_TOKEN,
            cls.TELEGRAM_CHAT_ID,
            cls.DASHSCOPE_API_KEY,
        ]
        missing = [k for k, v in zip(
            ["TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID", "DASHSCOPE_API_KEY"],
            required
        ) if not v]
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        # Create directories if not exist
        os.makedirs(cls.DATA_DIR, exist_ok=True)
        os.makedirs(cls.LOGS_DIR, exist_ok=True)
