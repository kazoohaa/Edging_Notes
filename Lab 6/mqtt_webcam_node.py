# Import the necessary libraries
import paho.mqtt.client as mqtt  # Paho MQTT library for MQTT communication
import cv2  # OpenCV library for image capture from webcam
import time  # Time module for measuring execution time
import io  # IO library for handling image data in memory
import base64  # Base64 module for encoding and decoding binary data to string

# MQTT settings
BROKER_IP = "192.168.10.149"  # IP address of the MQTT broker
TOPIC_CAPTURE = "capture/image"  # Topic to listen for capture requests
TOPIC_IMAGE = "image/data"  # Topic to publish captured image data

# Initialize MQTT client
client = mqtt.Client(client_id="WebcamNode", callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
# Creating a new MQTT client instance for the webcam node with a unique client ID and version for the callback API

# Callback when a message is received
def on_message(client, userdata, message):
    # This function is called when a message is received on a topic the client is subscribed to
    print("Received capture request...")  # Print message when a capture request is received

    # Capture image using OpenCV
    cap = cv2.VideoCapture(0)  # Initialize webcam capture (default webcam)
    ret, frame = cap.read()  # Capture a frame from the webcam
    cap.release()  # Release the webcam after capturing the frame

    if ret:
        # If the capture was successful, proceed with encoding the image
        _, buffer = cv2.imencode(".jpg", frame)  # Encode the frame as a JPEG image
        image_bytes = buffer.tobytes()  # Convert the image buffer to bytes

        # Convert the image to base64 for transmission over MQTT
        encoded_image = base64.b64encode(image_bytes).decode()  # Encode the image bytes into a base64 string

        # Publish image data to the MQTT broker on the image topic
        client.publish(TOPIC_IMAGE, encoded_image)  # Send the base64-encoded image data to the 'image/data' topic
        print("Image captured and sent!")  # Confirm that the image has been captured and sent

client.on_message = on_message  # Assign the 'on_message' function to handle incoming messages

# Connect to MQTT Broker
client.connect(BROKER_IP, 1883)  # Connect to the MQTT broker using the provided IP and default port 1883
client.subscribe(TOPIC_CAPTURE)  # Subscribe to the 'capture/image' topic to receive capture requests

print("Waiting for image capture request...")  # Indicate that the webcam node is waiting for requests
client.loop_forever()  # Start the MQTT client loop, which will keep it running indefinitely, waiting for messages


# Code Explanation:

### Libraries:
# paho.mqtt.client: Used to handle MQTT communication (both publishing and subscribing).
# cv2: OpenCV library to capture images from the webcam.
# time, io, base64: Used for time measurement, handling image data, and encoding/decoding the image to base64 for transmission.

### MQTT Configuration:
# Set the broker IP and topics (capture requests and image data).
# Image Capture and Transmission:
    # When a message is received on the capture/image topic, the callback function on_message is triggered.
    # The webcam is accessed using OpenCV, and an image is captured. This image is then encoded to JPEG, converted to base64, and sent to the image/data topic.

# MQTT Client Loop:
# The client subscribes to the capture/image topic, listens for capture requests, and enters an infinite loop to handle incoming messages.

