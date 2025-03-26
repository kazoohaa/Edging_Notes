# Import the necessary libraries
import paho.mqtt.client as mqtt  # Paho MQTT library for MQTT communication
import base64  # Base64 library for decoding the image data
import time  # Time module for measuring execution time
import threading  # Threading library to run capture requests in parallel

# MQTT settings
BROKER_IP = "192.168.10.149"  # IP address of the MQTT broker
TOPIC_IMAGE = "image/data"  # Topic to receive image data
TOPIC_CAPTURE = "capture/image"  # Topic to send image capture requests

# Callback when an image message is received
def on_message(client, userdata, message):
    # This function is called when a message is received on a topic the client is subscribed to
    print("Receiving image data...")  # Print message when image data is received

    # Decode base64 image
    image_bytes = base64.b64decode(message.payload)  # Decode the base64-encoded image data back to bytes

    # Save the image to a file
    with open("received_image.jpg", "wb") as img_file:  # Open a file in write-binary mode
        img_file.write(image_bytes)  # Write the decoded image bytes to the file

    print("Image received and saved as 'received_image.jpg'")  # Confirm that the image has been saved

# Function to send a capture signal every 10 seconds
def send_capture_signal():
    # This function sends a capture signal to request an image capture every 10 seconds
    while True:
        print("Requesting image capture...")  # Print message when a capture request is sent
        client.publish(TOPIC_CAPTURE, "snap")  # Publish the capture request to the 'capture/image' topic
        time.sleep(10)  # Wait for 10 seconds before sending the next request

# Initialize MQTT client
client = mqtt.Client(client_id="LaptopNode", callback_api_version=mqtt.CallbackAPIVersion.VERSION1)  # Create a new MQTT client with a unique client ID for the laptop node
client.on_message = on_message  # Assign the 'on_message' function to handle incoming messages

# Connect to MQTT Broker
client.connect(BROKER_IP, 1883)  # Connect to the MQTT broker using the provided IP and default port 1883
client.subscribe(TOPIC_IMAGE)  # Subscribe to the 'image/data' topic to receive image data

# Start the capture request loop in a separate thread
threading.Thread(target=send_capture_signal, daemon=True).start()  # Start the capture request loop in a separate thread so it doesn't block the main thread

print("Listening for images and requesting capture every 10 seconds...")  # Indicate that the laptop node is listening for images and requesting captures
client.loop_forever()  # Start the MQTT client loop, which will keep it running indefinitely, waiting for messages

# Code Explanation:#

### Libraries:
# paho.mqtt.client: Handles MQTT communication for subscribing and publishing.
# base64: Decodes the base64-encoded image data.
# time, threading: Handles periodic tasks (sending capture requests) in a separate thread.

### MQTT Configuration:
# Set the broker IP and topics (image data and capture requests).
# Image Reception and Saving:
# When the laptop node receives a message on the image/data topic, it decodes the base64-encoded image and saves it as a .jpg file.

### Capture Request:
# The send_capture_signal function sends a capture request every 10 seconds by publishing a message to the capture/image topic.
# This function runs in a separate thread to allow continuous capture requests while the main loop listens for incoming images.

### MQTT Client Loop:
# The client subscribes to the image/data topic, listens for images, and continuously sends capture requests every 10 seconds.