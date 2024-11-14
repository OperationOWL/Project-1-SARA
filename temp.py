import asyncio
import websockets
import cv2
import numpy as np

# WebSocket IPs
ESP32_IP = "ws://192.168.212.63:81"
SENSOR_IP = "ws://192.168.212.195:81"

# Global variable to store sensor data
sensor_data = ""
sensor_data_lock = asyncio.Lock()

# Function to handle incoming sensor data
async def on_sensor_message(ws, message):
    global sensor_data
    async with sensor_data_lock:
        sensor_data = message

# Function to enhance video quality
def enhance_frame(frame):

    # Sharpening
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    frame = cv2.filter2D(frame, -1, kernel)

    # Contrast and Saturation Adjustment
    frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=15)  # Adjust alpha for contrast, beta for brightness
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_frame[:, :, 1] = cv2.add(hsv_frame[:, :, 1], 30)  # Increase saturation
    frame = cv2.cvtColor(hsv_frame, cv2.COLOR_HSV2BGR)

    return frame


# Function to overlay sensor data with a background on the left side
def overlay_sensor_data(frame, data):
    font = cv2.FONT_HERSHEY_PLAIN  # Retro-style font
    font_scale = 2.5  # Increased font scale for better readability
    thickness = 3
    color = (0, 255, 0)  # Bright green for a retro feel
    background_color = (0, 0, 0)  # Black for the semi-transparent background
    alpha = 0.5  # Opacity for the background

    # Split sensor data into individual lines
    sensor_values = data.split(", ")

    # Draw background for text on the left side
    left_x, left_y = 20, 50
    max_text_width = max([cv2.getTextSize(text, font, font_scale, thickness)[0][0] for text in sensor_values]) + 20
    text_height = cv2.getTextSize(sensor_values[0], font, font_scale, thickness)[0][1] + 10

    overlay = frame.copy()
    for i, value in enumerate(sensor_values):
        y0 = left_y + i * (text_height + 10)
        cv2.rectangle(overlay, (left_x - 10, y0 - text_height), (left_x + max_text_width, y0 + 10), background_color, -1)
        cv2.putText(overlay, value, (left_x, y0), font, font_scale, color, thickness)

    # Blend the overlay with the original frame
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

# Function to handle video stream from the WebSocket
async def on_video_message(ws, message):
    # Convert message to numpy array, assuming the message is a raw JPEG frame
    np_arr = np.frombuffer(message, dtype=np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if frame is not None:
        # Resize the frame to 1280x720 (720p)
        frame = cv2.resize(frame, (960, 720))

        # Enhance frame clarity
        frame = enhance_frame(frame)

        # Read sensor data with lock
        async with sensor_data_lock:
            overlay_text = sensor_data

        # Overlay sensor data on the frame
        overlay_sensor_data(frame, overlay_text)

        # Display the frame
        cv2.imshow("ESP32 Video Stream with Sensor Data", frame)

        # Exit condition (press 'q' to quit)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            await ws.close()

# Function to handle WebSocket connection for video stream
async def video_websocket():
    async with websockets.connect(ESP32_IP) as ws:
        print("Connected to video WebSocket")
        while True:
            message = await ws.recv()
            await on_video_message(ws, message)

# Function to handle WebSocket connection for sensor data
async def sensor_websocket():
    async with websockets.connect(SENSOR_IP) as ws:
        print("Connected to sensor WebSocket")
        while True:
            message = await ws.recv()
            await on_sensor_message(ws, message)

# Main function to run both WebSocket connections concurrently
async def main():
    sensor_task = asyncio.create_task(sensor_websocket())
    video_task = asyncio.create_task(video_websocket())
    await asyncio.gather(sensor_task, video_task)

# Run the main function
asyncio.run(main())
cv2.destroyAllWindows()