import numpy as np
from typing import Optional


class ZScoreAnomalyDetector:
    def __init__(self, threshold: float = 3.0):
        self.threshold = threshold
        self.mean_: Optional[float] = None
        self.std_: Optional[float] = None

    def fit(self, X: np.ndarray) -> "ZScoreAnomalyDetector":
        self.mean_ = np.mean(X)
        self.std_ = np.std(X)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.mean_ is None or self.std_ is None:
            raise RuntimeError("call fit before predict")
        z_scores = np.abs((X - self.mean_) / self.std_)
        return np.where(z_scores > self.threshold, 1, 0)

    def fit_predict(self, X: np.ndarray) -> np.ndarray:
        return self.fit(X).predict(X)
