import numpy as np
from typing import List

class RunningAverage:
    def __init__(self, n_frames: int) -> None:
        self._history_queue: List[float] = []
        self._n_frames = n_frames

    def push(self, new_value: float):
        self._history_queue.append(new_value)
        self._history_queue = self._history_queue[-self._n_frames:]

    @property
    def value(self) -> float:
        return np.mean(self._history_queue)