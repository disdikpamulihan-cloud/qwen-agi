"""
Module 46: Qwen Cognitive Engine
"""
import json
import logging
from openai import AsyncOpenAI
from config import Config

logger = logging.getLogger(__name__)

class M46_QwenCognitiveEngine:
    """Qwen LLM cognitive validation engine"""
    
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=Config.DASHSCOPE_API_KEY,
            base_url=Config.QWEN_BASE_URL,
        )
        self.model_name = Config.QWEN_MODEL_NAME
    
    async def analyze_market_state(self, market_context: dict) -> dict:
        """Analyze market state with Qwen AI"""
        
        system_prompt = """
        Anda adalah SINGULARITY TRADING ARCHITECT, seorang trader kuantitatif institusional.
        Tugas Anda adalah memvalidasi sinyal trading berdasarkan data kuantitatif yang diberikan.
        Anda HANYA BOLEH membalas dalam format JSON yang valid tanpa markdown atau teks tambahan.
        Format JSON yang diminta:
        {
            "action": "BUY" | "SELL" | "HOLD",
            "confidence_score": 0.0 hingga 1.0,
            "reasoning": "Penjelasan singkat 1-2 kalimat mengapa keputusan ini diambil berdasarkan data.",
            "risk_warning": "Peringatan risiko spesifik"
        }
        """
        
        user_prompt = f"""
        Analisis keadaan pasar XAUUSD saat ini:
        - Harga Terakhir: {market_context.get('price')}
        - Tren Kalman Filter: {market_context.get('kalman_trend')}
        - Regime Pasar (HMM State): {market_context.get('hmm_state')}
        - Eksponen Lyapunov (Chaos): {market_context.get('lyapunov')}
        - RSI / Momentum: {market_context.get('momentum')}
        - ATR (Volatilitas): {market_context.get('atr')}
        - Korelasi DXY Proxy: {market_context.get('dxy_corr')}
        
        Apakah kuantitatif setup ini valid untuk dieksekusi? Berikan keputusan JSON Anda.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            
            result_text = response.choices[0].message.content
            parsed_result = json.loads(result_text)
            
            logger.info(f"🧠 Qwen AI decision: {parsed_result.get('action')}")
            return parsed_result
            
        except Exception as e:
            logger.error(f"❌ Qwen Engine error: {e}")
            return {
                "action": "HOLD",
                "confidence_score": 0.0,
                "reasoning": "API Error",
                "risk_warning": "Fallback"
            }
