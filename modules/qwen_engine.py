"""
Module 46: Qwen Cognitive Engine (Optimized for High Precision & Strict Confidence)
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
        
        # DI-OME: Prompt diperketat parah, AI dibikin pelit mere sinyal
        system_prompt = """
        Anda adalah SINGULARITY TRADING ARCHITECT, seorang trader kuantitatif institusional dengan manajemen risiko sangat ketat.
        Tugas Utama: Memvalidasi sinyal trading XAUUSD secara SANGAT KONSERVATIF. Lebih baik tidak mengeksekusi posisi daripada mengambil posisi yang berisiko/meragukan.

        Aturan Ketat Eksekusi:
        1. DEFAULT UTAMA adalah "HOLD". Anda HANYA BOLEH memberikan sinyal "BUY" atau "SELL" jika kondisi setup BENAR-BENAR sempurna dan terkonfirmasi oleh minimal 3 indikator kuantitatif yang searah.
        2. Jika pasar terindikasi Sideways/Ragu-ragu (misal: HMM State tidak mendukung atau RSI di area netral 40-60), Anda WAJIB menjawab "HOLD" dengan confidence_score < 0.60.
        3. Ambang batas (confidence_score) minimal untuk "BUY" atau "SELL" adalah 0.85 (85%). Jika di bawah itu, ubah action menjadi "HOLD".

        Output Format HANYA JSON tanpa markdown:
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
        
        Analisis secara ketat. Berikan keputusan JSON Anda.
        """
        
        try:
            # DI-OME: temperature diturunkeun tina 0.2 jadi 0.0 sangkan AI teu konsisten/ngaraco
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            
            result_text = response.choices[0].message.content
            parsed_result = json.loads(result_text)
            
            # DI-OME: Post-filtering paksa dina kodingan!
            # Lamun AI ngeyel milih BUY/SELL tapi confidence di bawah 0.85, paksa jadi HOLD!
            conf = float(parsed_result.get("confidence_score", 0.0))
            if parsed_result.get("action") in ["BUY", "SELL"] and conf < 0.85:
                logger.info(f"⚠️ Sinyal {parsed_result.get('action')} di-reject ku bot sabab confidence cuma {conf} (butuh >= 0.85)")
                parsed_result["action"] = "HOLD"
                parsed_result["reasoning"] += " (Di-overridden ke HOLD karena confidence di bawah 85%)"
            
            logger.info(f"🧠 Qwen AI decision: {parsed_result.get('action')} (Conf: {conf})")
            return parsed_result
            
        except Exception as e:
            logger.error(f"❌ Qwen Engine error: {e}")
            return {
                "action": "HOLD",
                "confidence_score": 0.0,
                "reasoning": "API Error",
                "risk_warning": "Fallback"
            }
