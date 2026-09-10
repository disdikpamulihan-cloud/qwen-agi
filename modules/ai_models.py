"""
Module 23, 30, 31, 39: AI Models (Optimized)
"""
import logging
import numpy as np
import torch
import torch.nn as nn
from hmmlearn import hmm

logger = logging.getLogger(__name__)

class M23_HMMRegime:
    """Hidden Markov Model regime classification"""
    
    def __init__(self):
        # DI-OME: covariance_type diganti ka "diag" tur n_iter dinaekkeun sangkan modél HMM leuwih stabil ngecek regime pasar
        self.model = hmm.GaussianHMM(
            n_components=3,
            covariance_type="diag",
            n_iter=200,
            random_state=42
        )
    
    def classify(self, X):
        """Classify market regime"""
        # DI-OME: Syarat data dinaekkeun tina 10 jadi 30 baris sangkan analisa regime teu acak-acakan
        if len(X) < 30:
            return 0
        
        try:
            self.model.fit(X)
            return int(self.model.predict(X)[-1])
        except Exception as e:
            logger.warning(f"HMM Fit Warning: {e}")
            return 0

class M30_TDA:
    """Topological Data Analysis"""
    
    def persistent_homology(self, points):
        """Compute persistent homology score"""
        if len(points) < 2:
            return 0.0
            
        dists = np.linalg.norm(points[:, None] - points, axis=-1)
        nonzero_dists = dists[dists > 0]
        if len(nonzero_dists) == 0:
            return 0.0
            
        thresh = np.percentile(nonzero_dists, 15)
        adj = (dists < thresh).astype(int)
        
        return float(np.sum(adj) / (len(points) * (len(points) - 1)))

class M31_GNNTopology:
    """Graph Neural Network market topology"""
    
    def message_pass(self, A, H, W):
        """Graph message passing"""
        return torch.relu(torch.tensor(A, dtype=torch.float32) @ torch.tensor(H, dtype=torch.float32) @ torch.tensor(W, dtype=torch.float32))

class M39_MaskedTransformer:
    """Self-supervised masked time-series transformer"""
    
    def __init__(self):
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=32,
            nhead=4,
            batch_first=True
        )
        self.model = nn.TransformerEncoder(encoder_layer, num_layers=2)
    
    def predict(self, x):
        """Predict with masked attention"""
        mask = torch.triu(
            torch.ones(x.shape[1], x.shape[1]),
            diagonal=1
        ).bool()
        
        return self.model(x, mask=mask)
