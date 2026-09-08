"""
Module 7, 9, 11, 19, 27: Risk Management
"""
import logging
import numpy as np
import scipy.stats as st

logger = logging.getLogger(__name__)

class M7_DynamicRROptimizer:
    """Dynamic risk-to-reward optimizer"""
    
    def kelly_atr(self, win_rate, reward, atr):
        """Calculate position size using Kelly Criterion"""
        q = 1 - win_rate
        kelly = (win_rate * reward - q) / reward if reward > 0 else 0
        return max(0, min(kelly * (atr / 100), 0.05))

class M9_AnomalyGuard:
    """Anomaly and outlier detection"""
    
    def check(self, x):
        """Check for anomalies using IQR and MAD"""
        q1, q3 = np.percentile(x, [25, 75])
        iqr = q3 - q1
        mad = np.median(np.abs(x - np.median(x)))
        
        return not (np.any(x > q3 + 1.5 * iqr) or mad > np.std(x) * 2)

class M11_MacroAwareness:
    """Macro-awareness and news regime filter"""
    
    def regime_filter(self, vol_history):
        """Detect extreme volatility regimes"""
        if len(vol_history) < 500:
            return True
        
        current_vol = np.std(np.diff(np.log(vol_history[-50:])))
        hist_vol = np.std(np.diff(np.log(vol_history[-500:-50])))
        
        return current_vol < hist_vol * 2.5

class M19_TimeOfDayVolatility:
    """Time-of-day volatility profiling"""
    
    def __init__(self):
        self.matrix = np.ones(24)
    
    def profile(self, utc_hour, vol):
        """Update and return volatility profile for hour"""
        self.matrix[utc_hour] = 0.9 * self.matrix[utc_hour] + 0.1 * vol
        return self.matrix[utc_hour]

class M27_EVTailRisk:
    """Extreme Value Theory tail-risk modeling"""
    
    def model_tail(self, returns):
        """Fit Generalized Pareto Distribution to tail"""
        tail = returns[returns < np.percentile(returns, 5)]
        
        if len(tail) < 10:
            return 0.0
        
        try:
            c, loc, scale = st.genpareto.fit(-tail)
            return c
        except:
            return 0.0
