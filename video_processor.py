import cv2
import mediapipe as mp
import numpy as np
import time
from pose_utils import calculate_angle  # Custom function to calculate angle between three points

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Constants and state variables
REPS_TARGET = 5
current_reps = 0
exercise_stage = None  # Tracks whether user is in "up" or "down" position

# Feedback counters
feedback = {
    "low_range": 0,
    "short_hold": 0,
    "fast_movement": 0,
    "inconsistent_tempo": 0,
    "fast_down": 0,
    "body_tilt": 0,
    "low_lift": 0
}

# Track time and angles for feedback
hold_counter = 0
tempo_times = []
prev_angle = None
prev_time = None

# Flags to prevent duplicate feedback in the same rep
feedback_flags = {k: False for k in feedback}

# Angle thresholds to detect movement
DOWN_THRESHOLD = 140
UP_THRESHOLD = 110


def extract_leg_raise_landmarks(results):
    """Extract coordinates for left shoulder, hip, and knee."""
    landmarks = results.pose_landmarks.landmark
    return {
        "shoulder": [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y],
        "hip": [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y],
        "knee": [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    }


def draw_leg_raise_left(image, results):
    """Draw shoulder, hip, and knee points and lines connecting them on the image."""
    landmarks = results.pose_landmarks.landmark
    points = [
        mp_pose.PoseLandmark.LEFT_SHOULDER.value,
        mp_pose.PoseLandmark.LEFT_HIP.value,
        mp_pose.PoseLandmark.LEFT_KNEE.value
    ]

    for idx in points:
        x = int(landmarks[idx].x * image.shape[1])
        y = int(landmarks[idx].y * image.shape[0])
        cv2.circle(image, (x, y), 15, (0, 0, 255), -1)

    connections = [
        (mp_pose.PoseLandmark.LEFT_SHOULDER.value, mp_pose.PoseLandmark.LEFT_HIP.value),
        (mp_pose.PoseLandmark.LEFT_HIP.value, mp_pose.PoseLandmark.LEFT_KNEE.value)
    ]
    for connection in connections:
        x1 = int(landmarks[connection[0]].x * image.shape[1])
        y1 = int(landmarks[connection[0]].y * image.shape[0])
        x2 = int(landmarks[connection[1]].x * image.shape[1])
        y2 = int(landmarks[connection[1]].y * image.shape[0])
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)

    return image


def feedback_text(key, count):
    """Return user-readable feedback messages based on issue type and count."""
    messages = {
        "low_range": f"You didn't raise your leg high enough ({count} times).",
        "short_hold": f"You didn't hold your leg up long enough ({count} times).",
        "fast_movement": f"Your movement was too fast ({count} times).",
        "inconsistent_tempo": f"Your tempo was inconsistent ({count} times).",
        "fast_down": f"You lowered your leg too quickly ({count} times).",
        "body_tilt": f"You tilted your body to the side ({count} times).",
        "low_lift": f"Your leg lift was too low ({count} times)."
    }
    return messages.get(key, "")


def calculate_stars():
    """Give star rating (1-3) based on total issues during exercise."""
    total_issues = sum(min(v, 10) for v in feedback.values())
    if total_issues <= 2:
        return 3
    elif total_issues <= 5:
        return 2
    else:
        return 1


def draw_star(image, center, size, color, thickness=2, filled=False):
    """Draw a 5-point star at center. Use filled=True for solid star."""
    points = []
    for i in range(5):
        angle_deg = 72 * i - 90  # Start from top
        outer_angle_rad = np.radians(angle_deg)
        inner_angle_rad = np.radians(angle_deg + 36)

        outer_x = int(center[0] + size * np.cos(outer_angle_rad))
        outer_y = int(center[1] + size * np.sin(outer_angle_rad))
        inner_x = int(center[0] + size * 0.5 * np.cos(inner_angle_rad))
        inner_y = int(center[1] + size * 0.5 * np.sin(inner_angle_rad))

        points.append((outer_x, outer_y))
        points.append((inner_x, inner_y))

    contour = np.array(points, dtype=np.int32).reshape((-1, 1, 2))

    if filled:
        cv2.fillPoly(image, [contour], color)
        cv2.polylines(image, [contour], isClosed=True, color=(0, 0, 0), thickness=2)  # black border
    else:
        cv2.polylines(image, [contour], isClosed=True, color=color, thickness=thickness)


def draw_feedback_screen(height, width, stars, tips):
    image = np.full((height, width, 3), (30, 30, 30), dtype=np.uint8)
    cv2.putText(image, "Workout Complete", (80, 120), cv2.FONT_HERSHEY_DUPLEX, 2.2, (255, 255, 255), 4)
    cv2.putText(image, "Your Score:", (80, 210), cv2.FONT_HERSHEY_DUPLEX, 1.8, (240, 240, 240), 3)

    start_x = 500
    for i in range(3):  # Always draw 3 stars
        center = (start_x + i * 70, 195)
        if i < stars:
            draw_star(image, center, 25, (0, 255, 255), filled=True)  # Filled star
        else:
            draw_star(image, center, 25, (100, 100, 100), thickness=2)  # Empty star

    y_offset = 320
    if tips:
        cv2.putText(image, "Focus for next time:", (80, y_offset), cv2.FONT_HERSHEY_DUPLEX, 1.4, (200, 200, 255), 2)
        for i, tip in enumerate(tips):
            text = feedback_text(tip, feedback[tip])
            cv2.putText(image, f"- {text}", (100, y_offset + 50 + i * 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255),
                        2)
    return image


def reset_feedback_flags():
    """Reset feedback flags so they can be triggered again in the next rep."""
    for key in feedback_flags:
        feedback_flags[key] = False


def process_frame(frame):
    """Main function to process each frame, detect pose, evaluate reps, and track feedback."""
    global exercise_stage, current_reps, feedback
    global hold_counter, tempo_times, prev_angle, prev_time

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    height, width, _ = image.shape

    # Show feedback screen when reps are complete
    if current_reps >= REPS_TARGET:
        stars = calculate_stars()
        sorted_feedback = sorted(feedback.items(), key=lambda x: x[1], reverse=True)
        tips = [k for k, v in sorted_feedback if v > 0][:2]
        return draw_feedback_screen(height, width, stars, tips)

    if results.pose_landmarks:
        image = draw_leg_raise_left(image, results)
        lm = extract_leg_raise_landmarks(results)
        shoulder, hip, knee = lm["shoulder"], lm["hip"], lm["knee"]

        angle = calculate_angle(shoulder, hip, knee)
        hip_px = np.multiply(hip, [width, height]).astype(int)

        # Draw angle arc between vectors
        v1 = np.array(shoulder) - np.array(hip)
        v2 = np.array(knee) - np.array(hip)
        v1 /= np.linalg.norm(v1)
        v2 /= np.linalg.norm(v2)
        angle1 = np.degrees(np.arctan2(v1[1], v1[0]))
        angle2 = np.degrees(np.arctan2(v2[1], v2[0]))
        if angle1 < 0: angle1 += 360
        if angle2 < 0: angle2 += 360
        start_angle = min(angle1, angle2)
        end_angle = max(angle1, angle2)
        cv2.ellipse(image, tuple(hip_px), (60, 60), 0, start_angle, end_angle, (0, 255, 255), 5)

        # Display angle text
        cv2.putText(image, f"{int(angle)}", (hip_px[0] - 20, hip_px[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 3,
                    (0, 0, 0), 10)
        cv2.putText(image, f"{int(angle)}", (hip_px[0] - 20, hip_px[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 3,
                    (0, 255, 255), 4)

        # ==== Repetition logic ====
        # If leg is in down position
        if angle > DOWN_THRESHOLD:
            if exercise_stage == "up":  # Transitioning from up to down
                # Check if the hold was too short - REDUCED from 15 to just 5 frames
                if hold_counter < 3 and not feedback_flags["short_hold"]:
                    feedback["short_hold"] += 1
                    feedback_flags["short_hold"] = True

                # Check for fast downward movement
                if prev_angle and (prev_angle - angle) > 20 and not feedback_flags["fast_down"]:
                    feedback["fast_down"] += 1
                    feedback_flags["fast_down"] = True

            exercise_stage = "down"

        # If leg is in up position
        elif angle < UP_THRESHOLD:
            if exercise_stage == "down":  # Transitioning from down to up
                exercise_stage = "up"
                current_reps += 1

                # Reset flags at the start of a new rep
                reset_feedback_flags()

                # Check for low range of motion - FURTHER INCREASED threshold from 95 to 105
                if angle > 105 and not feedback_flags["low_range"]:
                    feedback["low_range"] += 1
                    feedback_flags["low_range"] = True

                # Check for body tilt - made more lenient
                if abs(shoulder[0] - hip[0]) > 0.08 and not feedback_flags["body_tilt"]:
                    feedback["body_tilt"] += 1
                    feedback_flags["body_tilt"] = True

                # Check for low leg lift - FURTHER INCREASED threshold from 115 to 120
                if angle > 120 and not feedback_flags["low_lift"]:
                    feedback["low_lift"] += 1
                    feedback_flags["low_lift"] = True

                # Check for fast upward movement - made more lenient
                if prev_angle is not None and abs(angle - prev_angle) > 45 and not feedback_flags["fast_movement"]:
                    feedback["fast_movement"] += 1
                    feedback_flags["fast_movement"] = True

                # Check for inconsistent tempo - made more lenient
                if len(tempo_times) >= 2:
                    diff = abs(tempo_times[-1] - tempo_times[-2])
                    if diff > 0.8 and not feedback_flags["inconsistent_tempo"]:
                        feedback["inconsistent_tempo"] += 1
                        feedback_flags["inconsistent_tempo"] = True

            # Increment hold counter when in up position
            hold_counter += 1
        else:
            # In between up and down positions
            hold_counter = 0

        # Update time and angle for tempo analysis
        current_time = time.time()
        if exercise_stage == "up" and prev_time is not None:
            tempo_times.append(current_time - prev_time)

        prev_angle = angle
        prev_time = current_time

        # UI: Exercise label
        cv2.putText(image, "Leg raise", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2.2, (0, 0, 0), 18)
        cv2.putText(image, "Leg raise", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2.2, (255, 255, 255), 6)

        # UI: Reps counter
        counter_text = f"Reps: {current_reps}/{REPS_TARGET}"
        cv2.putText(image, counter_text, (20, 1020), cv2.FONT_HERSHEY_SIMPLEX, 2.2, (0, 0, 0), 18)
        cv2.putText(image, counter_text, (20, 1020), cv2.FONT_HERSHEY_SIMPLEX, 2.2, (5, 187, 242), 6)

    return image