"""
Module 4, 6, 24, 26: Signal Processing & Filtering (Optimized for High Accuracy & Low Noise)
"""
import logging
import numpy as np
import pandas as pd
import scipy.signal as sig

logger = logging.getLogger(__name__)

class M4_NoiseFilterZScore:
    """Noise filtering with Z-Score normalization"""
    
    # DI-OME: Window dinaékkeun ka 35 sangkan grafik leuwih mulus (ngabuang noise leutik)
    def filter(self, x, window=35):
        """Apply Savitzky-Golay filter and normalize"""
        window_length = min(len(x), window)
        if window_length % 2 == 0:
            window_length -= 1
        if window_length < 3:
            window_length = 3
        
        # Polyorder dijadikeun 1 pikeun smoothing leuwih kuat
        smoothed = sig.savgol_filter(x, window_length=window_length, polyorder=1)
        mean, std = np.mean(smoothed), np.std(smoothed)
        return (smoothed - mean) / (std + 1e-8)

class M6_MTFConfluence:
    """Multi-timeframe confluence engine"""
    
    def resample(self, ticks):
        """
        DI-OME: Timeframe dinaékkeun tina 1m/5m jadi 15m jeung 1h!
        Pasar XAUUSD (Emas) 1 menit éta liar pisan (loba sinyal palsu).
        """
        df = pd.DataFrame(ticks, columns=['time', 'price'])
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)
        
        m15 = df.resample('15min').ohlc()['price']
        h1 = df.resample('1h').ohlc()['price']
        
        return m15, h1

class M24_FractionalCalculus:
    """Fractional order calculus feature transformation"""
    
    # DI-OME: Alpha di-adjust ka 0.75 sangkan langkung sensitif ka tren gedé, sanés fluktuasi leutik
    def gl_derivative(self, x, alpha=0.75):
        """Grünwald-Letnikov fractional derivative"""
        n = len(x)
        w = np.zeros(n)
        w[0] = 1.0
        
        for j in range(1, n):
            w[j] = w[j-1] * (1 - (alpha + 1) / j)
        
        return np.convolve(x, w)[:n]

class M26_KalmanFilter:
    """Kalman filter state estimation (Optimized for Heavy Filtering)"""
    
    def __init__(self):
        self.x = np.zeros(2)
        self.P = np.eye(2)
        self.F = np.eye(2)
        self.H = np.array([[1, 0]])
        
        # DI-OME PARAH DI DIEU:
        # Q (Process Noise) diturunkeun jadi 0.0001 (bot teu gampang ngaréspon kejutan harga/fakeout)
        # R (Measurement Noise) dinaékkeun jadi 1.0 (bot nganggap kejutan leutik salaku noise)
        self.Q = np.eye(2) * 0.0001
        self.R = np.eye(1) * 1.0
    
    def update(self, z):
        """Kalman filter update step"""
        # Predict
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
        
        # Update
        y = z - self.H @ self.x
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        self.x = self.x + K @ y
        self.P = (np.eye(2) - K @ self.H) @ self.P
        
        return self.x[0]
