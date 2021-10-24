import time
from typing import Optional
from imutils.video import VideoStream
import cv2
import numpy as np
import socket

from eye import Eye
from face_tracker import FaceTracker
from running_average import RunningAverage

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


EYE_AR_THRESH = 0.25
FRAME_WINDOW = 100
PORT_NUMBER = 1234

parser = ArgumentParser(
    description="Eye Tracker to detect sleepy drivers",
    formatter_class=ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "-d",
    "--display",
    default=False,
    action="store_true",
    help="display video in real time",
)
parser.add_argument(
    "-a",
    "--address",
    type=str,
    help="IP address to stream data",
)
args = parser.parse_args()

video_source: VideoStream = VideoStream(src=0).start()
face_tracker: FaceTracker = FaceTracker()
output_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def is_open(left_eye: Optional[Eye], right_eye: Optional[Eye]) -> bool:
    if left_eye is None or right_eye is None:
        return False
    return openness_metric(left_eye, right_eye) > EYE_AR_THRESH


def openness_metric(left_eye: Eye, right_eye: Eye) -> float:
    l_ratio = left_eye.aspect_ratio
    r_ratio = right_eye.aspect_ratio

    if l_ratio is None or r_ratio is None:
        return 0
    return max(l_ratio, r_ratio)


r_avg = RunningAverage(FRAME_WINDOW)
while True:
    frame: np.ndarray = video_source.read()
    frame = cv2.resize(frame, (720, 450))
    grayscale_im: np.ndarray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face_tracker.detect_eyes(grayscale_im)
    l_eye = face_tracker.left_eye
    r_eye = face_tracker.right_eye

    metric = openness_metric(l_eye, r_eye)
    open = is_open(l_eye, r_eye)

    r_avg.push(metric)

    if args.address:
        output_socket.sendto(r_avg.value, (args.address, PORT_NUMBER))

    if args.display:
        # Label detected contours
        if l_eye.found:
            l_hull = l_eye.convex_hull
            cv2.putText(
                frame,
                f"L Aspect: {l_eye.aspect_ratio:.4}",
                (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2,
            )
            if l_hull is not None:
                cv2.drawContours(frame, [l_hull], -1, (0, 255, 0), 1)
        if r_eye.found:
            r_hull = r_eye.convex_hull
            cv2.putText(
                frame,
                f"R Aspect: {r_eye.aspect_ratio:.4}",
                (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2,
            )
            if r_hull is not None:
                cv2.drawContours(frame, [r_eye.convex_hull], -1, (0, 255, 0), 1)

        cv2.putText(
            frame,
            f"Eyes: {'Open' if open else 'Closed'}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            2,
        )
        cv2.putText(
            frame,
            f"Running Average Openness: {r_avg.value:.4}",
            (10, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            2,
        )

        cv2.imshow("Stream", frame)
        if cv2.waitKey(1) == ord("q"):
            break

cv2.destroyAllWindows()
video_source.stop()
