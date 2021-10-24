from scipy.spatial import distance as dist
from typing import List, Tuple, Optional
import cv2

class Eye:
    def __init__(self, landmarks_coor: Optional[List[Tuple[int, int]]]):
        super().__init__()
        self._landmarks = landmarks_coor

    @property
    def convex_hull(self):
        if not self.found:
            return None
        return cv2.convexHull(self._landmarks)

    @property
    def found(self) -> bool:
        return len(self._landmarks) >= 5

    @property
    def aspect_ratio(self) -> Optional[float]:
        if not self.found:
            return None
        # compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(self._landmarks[1], self._landmarks[5])
        B = dist.euclidean(self._landmarks[2], self._landmarks[4])

        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(self._landmarks[0], self._landmarks[3])

        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)

        # return the eye aspect ratio
        return ear