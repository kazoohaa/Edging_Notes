# Predict Number of Fingers

#%% Reference: https://github.com/googlesamples/mediapipe/tree/main/examples/hand_landmarker/raspberry_pi
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

#%% Parameters
numHands = 2  # Max number of hands to detect
model = 'hand_landmarker.task'  # Mediapipe hand model
minHandDetectionConfidence = 0.5  
minHandPresenceConfidence = 0.5
minTrackingConfidence = 0.5
frameWidth = 640
frameHeight = 480

# Visualization parameters
FONT_SIZE = 1
FONT_THICKNESS = 2
TEXT_COLOR = (88, 205, 54)  # Green
LANDMARK_COLOR = (0, 255, 255)  # Yellow
CIRCLE_RADIUS = 5  # Landmark size

#%% Create a HandLandmarker object
base_options = python.BaseOptions(model_asset_path=model)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=numHands,
    min_hand_detection_confidence=minHandDetectionConfidence,
    min_hand_presence_confidence=minHandPresenceConfidence,
    min_tracking_confidence=minTrackingConfidence)
detector = vision.HandLandmarker.create_from_options(options)


def count_fingers(hand_landmarks):
    """
    Count the number of extended fingers.
    - Uses y-coordinates for all fingers except thumb.
    - Uses x-coordinates for thumb (since it moves sideways).
    """
    finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky tips
    finger_bases = [6, 10, 14, 18]  # Base of corresponding fingers
    
    raised_fingers = 0

    # Thumb - Compare x-coordinates (thumb_tip should be right of thumb_base for left hand, and vice versa)
    thumb_tip_x = hand_landmarks[4].x
    thumb_base_x = hand_landmarks[2].x
    if thumb_tip_x > thumb_base_x:  # Thumb extended condition
        raised_fingers += 1

    # Other fingers - Compare y-coordinates (tip should be above base)
    for tip, base in zip(finger_tips, finger_bases):
        if hand_landmarks[tip].y < hand_landmarks[base].y:  # Extended condition
            raised_fingers += 1

    return raised_fingers


#%% Open CV Video Capture and frame analysis
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frameWidth)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frameHeight)

# Check if webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    try:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)  # Flip to match real-world orientation

        # Convert BGR to RGB for Mediapipe processing
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Run hand detection
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
        detection_result = detector.detect(mp_image)

        hand_landmarks_list = detection_result.hand_landmarks
        total_fingers = 0  # Store total raised fingers

        # Loop through detected hands
        for hand_landmarks in hand_landmarks_list:
            fingers = count_fingers(hand_landmarks)
            total_fingers += fingers

            # Draw all 21 hand landmarks
            for landmark in hand_landmarks:
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), CIRCLE_RADIUS, LANDMARK_COLOR, -1)

        # Display total raised fingers
        cv2.putText(frame, str(total_fingers), (50, 100),
                    cv2.FONT_HERSHEY_DUPLEX, FONT_SIZE * 2,
                    TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

        cv2.imshow('Hand Landmark Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except KeyboardInterrupt:
        break

cap.release()
cv2.destroyAllWindows()
