import cv2
import mediapipe as mp
import numpy as np
from pose_utils import calculate_angle

# Initialize MediaPipe pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

def extract_landmarks(results):
    """
    Extract key body landmarks (shoulder, elbow, wrist).
    """
    landmarks = results.pose_landmarks.landmark
    return {
        "shoulder": [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y],
        "elbow": [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y],
        "wrist": [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    }
def process_frame(frame):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        lm = extract_landmarks(results)

        shoulder = lm["shoulder"]
        elbow = lm["elbow"]
        wrist = lm["wrist"]

        # calculate angle
        angle = calculate_angle(shoulder, elbow, wrist)

        # convert to pixel coordinates
        elbow_px = tuple(np.multiply(elbow, [640, 480]).astype(int))
        radius = 50  # radius of arc
        start_angle = int(min(0, angle - 45))
        end_angle = int(max(180, angle + 45))

        # draw arc near elbow
        cv2.ellipse(
            image,
            elbow_px,        # center
            (radius, radius),
            0,               # rotation
            0, angle,        # start/end angle
            (0, 255, 0),     # color
            3                # thickness
        )

        # draw text inside arc
        cv2.putText(
            image,
            f"{int(angle)}°",
            (elbow_px[0] - 25, elbow_px[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    return image