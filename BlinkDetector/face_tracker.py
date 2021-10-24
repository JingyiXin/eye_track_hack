import dlib
from typing import Optional, Tuple, List
import numpy as np
from eye import Eye
from imutils import face_utils   

(L_START, L_END) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(R_START, R_END) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


class FaceTracker:
    def __init__(self):
        super().__init__()
        print("[INFO] loading facial landmark predictor...")
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        self.left_eye: Optional[Eye] = None
        self.right_eye: Optional[Eye] = None

    def detect_eyes(self, image:np.ndarray) -> None:
        """
        Populate Left and Right Eye information in the Face Tracker
        """
        facial_landmarks: List[Tuple[int, int]] = self.detect_face(image)
        self.left_eye = Eye(facial_landmarks[L_START:L_END])
        self.right_eye = Eye(facial_landmarks[R_START:R_END])
        

    def detect_face(self, image: np.ndarray) -> List[Tuple[int, int]]:
        """
        Return a list of (x, y) coordinates of the main detected face
        """

        # The 0 indicates grayscale, the -1 seems to help dlib detect more faces?
        dets, scores, idx = self.detector.run(image, 0, -1)
        if len(dets) == 0:
            return []

        # Sort by score to find best detection
        main_det = dets[scores.index(max(scores))]

        # zipped_list = zip(dets, scores, idx)
        # sorted(zipped_list, key = lambda x: x[1])
        # main_det = zipped_list[0]

        # Extract landmarks from the main detection
        shape = self.predictor(image, main_det)
        return self.landmark_coordinates(shape)

    @staticmethod
    def landmark_coordinates(shape, dtype='int') -> Tuple[int, int]:
        # initialize the list of (x, y)-coordinates
        coords = np.zeros((shape.num_parts, 2), dtype=dtype)

        # loop over all facial landmarks and convert them
        # to a 2-tuple of (x, y)-coordinates
        for i in range(0, shape.num_parts):
            coords[i] = (shape.part(i).x, shape.part(i).y)

        # return the list of (x, y)-coordinates
        return coords

