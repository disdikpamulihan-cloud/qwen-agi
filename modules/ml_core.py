"""
Module 2, 3, 14, 36: Machine Learning Core
"""
import os
import pickle
import logging
import numpy as np
from config import Config

logger = logging.getLogger(__name__)

class M2_OnlineMLCore:
    """Incremental learning with dynamic weights"""
    
    def __init__(self, n_features=10):
        self.w = np.random.randn(n_features) * 0.01
        self.b = 0.0
        self.lr = 0.01
    
    def update(self, x, y):
        """Online gradient descent update"""
        pred = np.dot(x, self.w) + self.b
        err = pred - y
        self.w -= self.lr * err * x
        self.b -= self.lr * err
        return pred

class M3_StatePersistence:
    """Auto-save model state serialization"""
    
    def __init__(self, path=None):
        self.path = path or Config.MODEL_STATE_PATH
    
    def save(self, state):
        """Serialize and save state to disk"""
        try:
            with open(self.path, 'wb') as f:
                pickle.dump(state, f)
            logger.debug(f"💾 State saved to {self.path}")
        except Exception as e:
            logger.error(f"❌ Failed to save state: {e}")
    
    def load(self):
        """Load state from disk"""
        if os.path.exists(self.path):
            try:
                with open(self.path, 'rb') as f:
                    state = pickle.load(f)
                logger.info(f"📂 State loaded from {self.path}")
                return state
            except Exception as e:
                logger.error(f"❌ Failed to load state: {e}")
        return None

class M14_RLHF:
    """Reinforcement Learning from Human Feedback"""
    
    def __init__(self):
        self.alpha = 0.5
    
    def update_reward(self, pnl, sharpe):
        """Update reward function based on performance"""
        reward = self.alpha * pnl + (1 - self.alpha) * sharpe
        self.alpha = max(0.1, min(0.9, self.alpha + 0.01 * np.sign(reward)))
        return reward

class M36_MAML:
    """Model-Agnostic Meta-Learning"""
    
    def meta_step(self, tasks, inner_lr=0.01, outer_lr=0.001):
        """Meta-learning update across tasks"""
        theta = np.random.randn(10)
        meta_grad = np.zeros_like(theta)
        
        for x, y in tasks:
            theta_prime = theta - inner_lr * np.dot(x.T, np.dot(x, theta) - y)
            meta_grad += np.dot(x.T, np.dot(x, theta_prime) - y)
        
        theta -= outer_lr * meta_grad / len(tasks)
        return theta
