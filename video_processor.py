import cv2
import mediapipe as mp
import numpy as np
from pose_utils import calculate_angle

# MediaPipe setup
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

def extract_leg_raise_landmarks(results):
    """
    Extracts LEFT leg landmarks required to calculate the leg raise angle:
    shoulder, hip, knee
    """
    landmarks = results.pose_landmarks.landmark
    return {
        "shoulder": [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y],
        "hip": [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y],
        "knee": [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    }
#-------------------------------------------------------------------------------------------------------
REPS_TARGET = {
    "squat_left": 10,
    "squat_right": 10,
    "elbow_curl_left": 12,
    "elbow_curl_right": 12,
    "arm_raise_left": 15,
    "arm_raise_right": 15,
    "leg_raise_left": 8,
    "leg_raise_right": 8
}
current_reps = {key: 0 for key in REPS_TARGET.keys()}
exercise_stage = {key: None for key in REPS_TARGET.keys()}  # 'up' or 'down'
def update_reps(exercise_key):
    """
    Update reps count and return True if target reached.
    """
    current_reps[exercise_key] += 1
    if current_reps[exercise_key] >= REPS_TARGET[exercise_key]:
        return True
    return False
#--------------------------------------------------------------------------------------
def draw_leg_raise_left(image, results):
    landmarks = results.pose_landmarks.landmark

    # נקודות
    points = [
        mp_pose.PoseLandmark.LEFT_SHOULDER.value,
        mp_pose.PoseLandmark.LEFT_HIP.value,
        mp_pose.PoseLandmark.LEFT_KNEE.value
    ]

    # לצייר נקודות
    for idx in points:
        x = int(landmarks[idx].x * image.shape[1])
        y = int(landmarks[idx].y * image.shape[0])
        cv2.circle(image, (x, y), 5, (0, 0, 255), -1)

    # לצייר קווים בין הנקודות
    connections = [
        (mp_pose.PoseLandmark.LEFT_SHOULDER.value, mp_pose.PoseLandmark.LEFT_HIP.value),
        (mp_pose.PoseLandmark.LEFT_HIP.value, mp_pose.PoseLandmark.LEFT_KNEE.value)
    ]

    for connection in connections:
        x1 = int(landmarks[connection[0]].x * image.shape[1])
        y1 = int(landmarks[connection[0]].y * image.shape[0])
        x2 = int(landmarks[connection[1]].x * image.shape[1])
        y2 = int(landmarks[connection[1]].y * image.shape[0])
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return image
#--------------------------------------------------------------------------------------------
def process_frame(frame):
    global exercise_stage
    exercise_key = "leg_raise_left"
    finished = False

    """
    Process the frame to calculate the leg raise angle (shoulder–hip–knee),
    draw the landmarks, an arc on the hip, and angle text.
    """
    # Convert frame for MediaPipe
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.pose_landmarks:
        # Draw body skeleton
        image = draw_leg_raise_left(image, results)

        # Get relevant landmarks
        lm = extract_leg_raise_landmarks(results)
        shoulder, hip, knee = lm["shoulder"], lm["hip"], lm["knee"]

        # Calculate the leg raise angle
        angle = calculate_angle(shoulder, hip, knee)

        # Convert hip coordinates to pixel values
        hip_px = np.multiply(hip, [640, 480]).astype(int)

        # Draw arc to represent the angle
        cv2.ellipse(
            image,
            tuple(hip_px),
            (40, 40),
            0,
            0,
            int(angle),
            (0, 255, 255),
            3
        )

        cv2.putText(
            image,
            f"{int(angle)}°",
            (hip_px[0] - 20, hip_px[1] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 0),
            3  # outline
        )

        cv2.putText(
            image,
            f"{int(angle)}°",
            (hip_px[0] - 20, hip_px[1] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            1  # main text
        )

        # Leg raise count logic
        if angle > 160:
            exercise_stage[exercise_key] = "down"
        if angle < 80 and exercise_stage[exercise_key] == "down":
            exercise_stage[exercise_key] = "up"
            finished = update_reps(exercise_key)

        # Draw counter
        cv2.putText(
            image,
            f"Reps: {current_reps[exercise_key]}/{REPS_TARGET[exercise_key]}",
            (10, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 0, 0),
            4
        )
        cv2.putText(
            image,
            f"Reps: {current_reps[exercise_key]}/{REPS_TARGET[exercise_key]}",
            (10, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 255, 0),
            2
        )
    return image ,finished


# סקוואט
def process_frame_squat_left(frame):
    pass

def process_frame_squat_right(frame):
    pass

# כפיפת מרפקים
def process_frame_elbow_curl_left(frame):
    pass

def process_frame_elbow_curl_right(frame):
    pass

# הרמת ידיים
def process_frame_arm_raise_left(frame):
    pass

def process_frame_arm_raise_right(frame):
    pass

# הרמת רגליים (הפונקציה שלך)
def process_frame_leg_raise_right(frame):
    pass