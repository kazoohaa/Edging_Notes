# Object Detection Based Video Summarization

import cv2
import mediapipe as mp
import time

from mediapipe.tasks import python  # Import the python wrapper
from mediapipe.tasks.python import vision  # API for calling the recognizer

#%% Parameters
maxResults = 5
scoreThreshold = 0.25
frameWidth = 640
frameHeight = 480
model = 'efficientdet.tflite'

# Target object to filter (change as needed)
TARGET_OBJECT = "cellphone"  # Change this to any object you want to summarize

# Video Output Parameters
output_video_path = "summarized_video.avi"
fps = 10  # Frames per second for the output video
frame_size = (frameWidth, frameHeight)

# Visualization parameters
MARGIN = 10  # pixels
ROW_SIZE = 30  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
TEXT_COLOR = (0, 0, 0)  # Black
BOUNDING_BOX_COLOR = (0, 165, 255)  # Orange for high visibility

#%% Initialize video writer for saving summarized video
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for .avi format
out = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size)

#%% Object Detection Result Callback
detection_result_list = []

def save_result(result: vision.ObjectDetectorResult, unused_output_image: mp.Image, timestamp_ms: int):
    detection_result_list.append(result)

#%% Create an object detection model object.
base_options = python.BaseOptions(model_asset_path=model)
options = vision.ObjectDetectorOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.LIVE_STREAM,
    max_results=maxResults, 
    score_threshold=scoreThreshold,
    result_callback=save_result
)
detector = vision.ObjectDetector.create_from_options(options)

#%% OpenCV Video Capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frameWidth)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frameHeight)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

#%% Processing Loop
while True:
    try:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)  # Flip to match real-world orientation

        # Convert BGR to RGB for Mediapipe processing
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

        # Run object detection asynchronously
        detector.detect_async(mp_image, time.time_ns() // 1_000_000)

        if detection_result_list:
            detected_frame = frame.copy()
            object_detected = False  # Flag to check if target object is in frame

            for detection in detection_result_list[0].detections:
                # Bounding Box
                bbox = detection.bounding_box
                start_point = (bbox.origin_x, bbox.origin_y)
                end_point = (bbox.origin_x + bbox.width, bbox.origin_y + bbox.height)
                cv2.rectangle(detected_frame, start_point, end_point, BOUNDING_BOX_COLOR, 3)

                # Label & Confidence Score
                category = detection.categories[0]
                category_name = category.category_name
                probability = round(category.score, 2)
                result_text = f"{category_name} ({probability})"
                text_location = (MARGIN + bbox.origin_x, MARGIN + ROW_SIZE + bbox.origin_y)
                cv2.putText(detected_frame, result_text, text_location,
                            cv2.FONT_HERSHEY_DUPLEX, FONT_SIZE, TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

                # Check if the detected object is the target object
                if category_name.lower() == TARGET_OBJECT.lower():
                    object_detected = True  # Mark this frame for saving

            # If the target object is detected, save the frame to video
            if object_detected:
                out.write(detected_frame)

            # Display the annotated frame
            cv2.imshow('Object Detection', detected_frame)
            detection_result_list.clear()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except KeyboardInterrupt:
        break

# Cleanup
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Summarized video saved as {output_video_path}")
