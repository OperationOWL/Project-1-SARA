import asyncio
import websockets
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from threading import Thread, Lock
from PIL import Image, ImageTk
import logging
from datetime import datetime

# WebSocket configurations
ESP32_IP = "ws://192.168.212.63:81"
SENSOR_IP = "ws://192.168.212.187:81"

# Global variables
sensor_data = ""
sensor_data_lock = asyncio.Lock()
frame_lock = Lock()

class RetroDisplay:
    def __init__(self, root):
        self.root = root
        self.root.title("ESP32 TACTICAL DISPLAY")
        self.root.configure(bg='black')
        self.root.geometry("1200x800")
        
        # Configure the grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Custom font styles
        self.custom_font = ("Courier", 12, "bold")
        self.header_font = ("Courier", 16, "bold")
        
        self.setup_styles()
        self.create_main_frame()
        self.create_widgets()
        self.last_valid_frame = None
        self.frame_update_time = datetime.now()
        
        # Start blinking effect for status indicators
        self.blink_status()
        
    def setup_styles(self):
        style = ttk.Style()
        style.configure("Retro.TFrame", background="black")
        style.configure("Retro.TLabel",
                       background="black",
                       foreground="#00ff00",
                       font=self.custom_font)
        style.configure("Header.TLabel",
                       background="black",
                       foreground="#00ff00",
                       font=self.header_font)
                       
    def create_main_frame(self):
        # Main container frame to center video display
        self.main_frame = ttk.Frame(self.root, style="Retro.TFrame")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
    def create_widgets(self):
        # Video section
        self.create_video_section()
        # Data section
        self.create_data_section()
        # Add decorative elements
        self.add_decorative_elements()
        
    def create_video_section(self):
        # Header with retro design
        header_frame = ttk.Frame(self.main_frame, style="Retro.TFrame")
        header_frame.pack(fill="x", pady=5)
        
        self.video_header = ttk.Label(header_frame,
                                    text="[ TACTICAL FEED ]",
                                    style="Header.TLabel")
        self.video_header.pack(pady=5)
        
        # Video display
        self.video_label = ttk.Label(self.main_frame, style="Retro.TLabel")
        self.video_label.pack(padx=10, pady=10)
        
        # Status line
        self.video_status = ttk.Label(self.main_frame,
                                    text="FEED STATUS: ACTIVE",
                                    style="Retro.TLabel")
        self.video_status.pack(pady=5)
        
    def create_data_section(self):
        # Header
        self.data_header = ttk.Label(self.main_frame,
                                   text="[ SENSOR TELEMETRY ]",
                                   style="Header.TLabel")
        self.data_header.pack(pady=10)
        
        # Status indicators
        self.status_frame = ttk.Frame(self.main_frame, style="Retro.TFrame")
        self.status_frame.pack(fill="x", padx=10, pady=5)
        
        self.status_indicators = {}
        self.create_status_indicator("LINK STATUS", "NOMINAL")
        self.create_status_indicator("DATA FLOW", "ACTIVE")
        
        # Sensor data display
        self.sensor_frame = ttk.Frame(self.main_frame, style="Retro.TFrame")
        self.sensor_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create a text widget with retro styling
        self.sensor_text = tk.Text(self.sensor_frame,
                                 height=10,
                                 width=50,
                                 bg="black",
                                 fg="#00ff00",
                                 font=self.custom_font,
                                 wrap=tk.WORD)
        self.sensor_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add a scrollbar with retro styling
        scrollbar = ttk.Scrollbar(self.sensor_frame, orient="vertical",
                                command=self.sensor_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.sensor_text.configure(yscrollcommand=scrollbar.set)
        
    def create_status_indicator(self, label, initial_value):
        frame = ttk.Frame(self.status_frame, style="Retro.TFrame")
        frame.pack(fill="x", pady=2)
        
        label_widget = ttk.Label(frame,
                               text=f"{label}:",
                               style="Retro.TLabel")
        label_widget.pack(side="left")
        
        value_widget = ttk.Label(frame,
                               text=initial_value,
                               style="Retro.TLabel")
        value_widget.pack(side="right")
        
        self.status_indicators[label] = value_widget
        
    def add_decorative_elements(self):
        # Add retro-style borders
        self.add_border(self.main_frame)
            
    def add_border(self, frame):
        canvas = tk.Canvas(frame,
                         height=2,
                         bg="black",
                         highlightthickness=0)
        canvas.pack(fill="x", pady=5)
        canvas.create_line(0, 1, 1200, 1,
                         fill="#00ff00",
                         width=1,
                         dash=(4, 4))
                         
    def blink_status(self):
        # Alternate colors for status indicators
        for indicator in self.status_indicators.values():
            current_color = indicator.cget("foreground")
            new_color = "#005500" if current_color == "#00ff00" else "#00ff00"
            indicator.configure(foreground=new_color)
        self.root.after(1000, self.blink_status)
        
    def update_sensor_data(self, data):
        self.sensor_text.delete(1.0, tk.END)
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_data = (
            f"TIME: {timestamp}\n"
            f"{'-' * 35}\n"
            f"SENSOR READINGS:\n"
            f"{'-' * 35}\n"
            f"{data}\n"
        )
        self.sensor_text.insert(tk.END, formatted_data)

class VideoStreamHandler:
    def __init__(self, display):
        self.display = display
        self.connection_active = True
        self.frame_count = 0
        
    def enhance_frame(self, frame):
        # Keep the original frame for color output
        return frame

    def process_frame(self, frame):
        enhanced_frame = self.enhance_frame(frame)
        with frame_lock:
            self.display.last_valid_frame = enhanced_frame
            self.display.frame_update_time = datetime.now()
        
        # Convert OpenCV image (BGR) to PIL format (RGB) for Tkinter
        image = cv2.cvtColor(enhanced_frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image_tk = ImageTk.PhotoImage(image=image)
        
        # Update the video display in the Tkinter window
        self.display.video_label.configure(image=image_tk)
        self.display.video_label.image = image_tk

    async def receive_frames(self):
        async with websockets.connect(ESP32_IP) as websocket:
            while self.connection_active:
                try:
                    # Receive frame data from WebSocket
                    frame_data = await websocket.recv()
                    np_data = np.frombuffer(frame_data, dtype=np.uint8)
                    frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

                    if frame is not None:
                        self.process_frame(frame)
                except Exception as e:
                    logging.error(f"Error receiving or processing frame: {e}")
                    break

    def start_stream(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.receive_frames())

def start_video_thread(display):
    video_handler = VideoStreamHandler(display)
    video_thread = Thread(target=video_handler.start_stream, daemon=True)
    video_thread.start()

async def receive_sensor_data(display):
    async with websockets.connect(SENSOR_IP) as websocket:
        while True:
            try:
                data = await websocket.recv()
                async with sensor_data_lock:
                    display.update_sensor_data(data)
            except Exception as e:
                logging.error(f"Error receiving sensor data: {e}")
                break

def start_sensor_thread(display):
    sensor_thread = Thread(target=lambda: asyncio.run(receive_sensor_data(display)), daemon=True)
    sensor_thread.start()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    root = tk.Tk()
    display = RetroDisplay(root)
    
    # Start video and sensor data threads
    start_video_thread(display)
    start_sensor_thread(display)

    # Run the main Tkinter event loop
    root.mainloop()
