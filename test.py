import asyncio
import websockets
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from threading import Thread, Lock
from PIL import Image, ImageTk
import logging
import re
import time

# Configuration
CONFIG = {
    'ESP32_IP': 'ws://192.168.212.63:81',
    'SENSOR_IP': 'ws://192.168.212.187:81',
    'WINDOW_TITLE': 'ESP32 Video Stream',
    'SENSOR_TITLE': '= SENSOR TELEMETRY =',
    'UI_COLOR': '#00FF00',
    'VIDEO_SIZE': (960, 720)
}

class VideoStreamHandler:
    def _init_(self, video_label):
        self.video_label = video_label
        self.last_valid_frame = None
        self.frame_update_time = time.time()
        self.connection_active = True
        self.frame_count = 0
        self.processing_frame = False
        
    def update_frame_display(self, frame):
        try:
            cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(cv2_image)
            self.frame_image = ImageTk.PhotoImage(image=pil_image)
            self.video_label.configure(image=self.frame_image)
            self.video_label.image = self.frame_image
        except Exception as e:
            logging.error(f"Error updating frame display: {e}")

    def enhance_frame(self, frame):
        try:
            frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=5)
            frame = cv2.fastNlMeansDenoisingColored(frame, None, 10, 10, 7, 21)
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)
            return cv2.filter2D(frame, -1, kernel)
        except Exception as e:
            logging.error(f"Frame enhancement error: {e}")
            return frame

    async def process_frame(self, message):
        if self.processing_frame:
            return
        
        self.processing_frame = True
        try:
            np_arr = np.frombuffer(message, dtype=np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            
            if frame is not None:
                frame = cv2.resize(frame, CONFIG['VIDEO_SIZE'])
                frame = self.enhance_frame(frame)
                self.frame_count += 1
                self.frame_update_time = time.time()
                self.last_valid_frame = frame.copy()
                self.video_label.after(0, self.update_frame_display, frame)
        except Exception as e:
            logging.error(f"Frame processing error: {e}")
        finally:
            self.processing_frame = False

class RetroSensorDisplay:
    def _init_(self, parent):
        self.frame = tk.Frame(parent, bg='black', relief='raised', borderwidth=2)
        self.frame.pack(fill=tk.X, padx=20, pady=10)
        self.create_sensor_grid()
        self.blink_state = True
        self.blink_cursor()
        
    def create_sensor_grid(self):
        # Create header
        header_frame = tk.Frame(self.frame, bg='black')
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        header_label = tk.Label(
            header_frame,
            text=CONFIG['SENSOR_TITLE'],
            font=("OCR A Extended", 16, "bold"),
            fg=CONFIG['UI_COLOR'],
            bg="black"
        )
        header_label.pack()
        
        # Create sensor grid
        self.grid_frame = tk.Frame(self.frame, bg='black')
        self.grid_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.sensor_labels = {}
        sensors = [
            ("TEMPERATURE", "0.0°C"),
            ("HUMIDITY", "0.0%"),
            ("GAS", "0.0"),
            ("HEAT INDEX", "0.0°C"),
            ("STATUS", "ONLINE")
        ]
        
        for i, (name, initial_value) in enumerate(sensors):
            self.create_sensor_display(name, initial_value, i)
            
        self.create_decorative_elements()
        
    def create_sensor_display(self, name, initial_value, row):
        frame = tk.Frame(self.grid_frame, bg='black')
        frame.grid(row=row, column=0, padx=5, pady=2, sticky='ew')
        
        name_frame = tk.Frame(frame, bg=CONFIG['UI_COLOR'], padx=1, pady=1)
        name_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        name_label = tk.Label(
            name_frame,
            text=f"[{name}]",
            font=("OCR A Extended", 12),
            fg=CONFIG['UI_COLOR'],
            bg="black",
            width=15,
            anchor='w'
        )
        name_label.pack()
        
        value_label = tk.Label(
            frame,
            text=initial_value,
            font=("OCR A Extended", 12),
            fg=CONFIG['UI_COLOR'],
            bg="black",
            width=10,
            anchor='e'
        )
        value_label.pack(side=tk.LEFT)
        
        self.sensor_labels[name] = value_label
        
    def create_decorative_elements(self):
        border_frame = tk.Frame(self.frame, bg='black')
        border_frame.pack(fill=tk.X, pady=(5, 0))
        
        border_label = tk.Label(
            border_frame,
            text="═" * 50,
            font=("OCR A Extended", 12),
            fg=CONFIG['UI_COLOR'],
            bg="black"
        )
        border_label.pack()
        
    def update_sensor_data(self, data):
        try:
            pattern = r'gas: ([\d.]+), humidity: ([\d.]+), temp: ([\d.]+), heat_index: ([\d.]+)'
            match = re.match(pattern, data)
            
            if match:
                gas, humidity, temp, heat_index = match.groups()
                updates = {
                    "GAS": f"{float(gas):.1f}",
                    "HUMIDITY": f"{float(humidity):.1f}%",
                    "TEMPERATURE": f"{float(temp):.1f}°C",
                    "HEAT INDEX": f"{float(heat_index):.1f}°C"
                }
                
                for key, value in updates.items():
                    self.sensor_labels[key].config(text=value)
                self.sensor_labels["STATUS"].config(text="ONLINE")
            else:
                raise ValueError("Invalid data format")
                
        except Exception as e:
            logging.error(f"Error updating sensor display: {e}")
            self.sensor_labels["STATUS"].config(text="ERROR")
            
    def blink_cursor(self):
        cursor_char = "█" if self.blink_state else " "
        for label in self.sensor_labels.values():
            current_text = label.cget("text")
            if not current_text.endswith("█") and not current_text.endswith(" "):
                current_text += " "
            label.config(text=current_text[:-1] + cursor_char)
        
        self.blink_state = not self.blink_state
        self.frame.after(500, self.blink_cursor)

async def video_websocket(handler):
    while True:
        try:
            async with websockets.connect(CONFIG['ESP32_IP'], ping_interval=5, ping_timeout=10) as ws:
                logging.info("Connected to video websocket")
                handler.connection_active = True
                
                while handler.connection_active:
                    try:
                        message = await ws.recv()
                        await handler.process_frame(message)
                    except Exception as e:
                        logging.error(f"Error receiving video frame: {e}")
                        await asyncio.sleep(0.1)
                        
        except Exception as e:
            logging.error(f"Video websocket error: {e}")
            await asyncio.sleep(1)

async def sensor_websocket(sensor_display):
    while True:
        try:
            async with websockets.connect(CONFIG['SENSOR_IP'], ping_interval=5, ping_timeout=10) as ws:
                while True:
                    try:
                        message = await ws.recv()
                        sensor_display.update_sensor_data(message)
                    except Exception as e:
                        logging.error(f"Sensor websocket error: {e}")
                        await asyncio.sleep(0.1)
        except Exception as e:
            logging.error(f"Sensor connection error: {e}")
            await asyncio.sleep(1)

async def main(video_label, sensor_display):
    video_handler = VideoStreamHandler(video_label)
    sensor_task = asyncio.create_task(sensor_websocket(sensor_display))
    video_task = asyncio.create_task(video_websocket(video_handler))
    await asyncio.gather(video_task, sensor_task)

def start_application():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Create main window
    root = tk.Tk()
    root.title(CONFIG['WINDOW_TITLE'])
    root.configure(bg="black")
    
    # Create video display
    video_label = ttk.Label(root, anchor="center")
    video_label.pack(padx=20, pady=20)
    
    # Create sensor display
    sensor_display = RetroSensorDisplay(root)
    
    # Start async tasks
    loop = asyncio.new_event_loop()
    thread = Thread(
        target=lambda: asyncio.run(main(video_label, sensor_display)),
        daemon=True
    )
    thread.start()
    
    # Start UI
    try:
        root.mainloop()
    finally:
        cv2.destroyAllWindows()

if __name__ == "_main_":
    start_application()