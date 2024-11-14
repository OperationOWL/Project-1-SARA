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
    def _init_(self, root):
        self.root = root
        self.root.title("ESP32 TACTICAL DISPLAY")
        self.root.configure(bg='black')
        self.root.geometry("1200x800")
        
        # Configure the grid
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Custom font styles
        self.custom_font = ("Courier", 12, "bold")
        self.header_font = ("Courier", 16, "bold")
        
        self.setup_styles()
        self.create_frames()
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
                       
    def create_frames(self):
        # Main container frames
        self.video_frame = ttk.Frame(self.root, style="Retro.TFrame")
        self.video_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.data_frame = ttk.Frame(self.root, style="Retro.TFrame")
        self.data_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
    def create_widgets(self):
        # Video section
        self.create_video_section()
        # Data section
        self.create_data_section()
        # Add decorative elements
        self.add_decorative_elements()
        
    def create_video_section(self):
        # Header with retro design
        header_frame = ttk.Frame(self.video_frame, style="Retro.TFrame")
        header_frame.pack(fill="x", pady=5)
        
        self.video_header = ttk.Label(header_frame,
                                    text="[ TACTICAL FEED ]",
                                    style="Header.TLabel")
        self.video_header.pack(pady=5)
        
        # Video display
        self.video_label = ttk.Label(self.video_frame, style="Retro.TLabel")
        self.video_label.pack(padx=10, pady=10)
        
        # Status line
        self.video_status = ttk.Label(self.video_frame,
                                    text="FEED STATUS: ACTIVE",
                                    style="Retro.TLabel")
        self.video_status.pack(pady=5)
        
    def create_data_section(self):
        # Header
        self.data_header = ttk.Label(self.data_frame,
                                   text="[ SENSOR TELEMETRY ]",
                                   style="Header.TLabel")
        self.data_header.pack(pady=10)
        
        # Status indicators
        self.status_frame = ttk.Frame(self.data_frame, style="Retro.TFrame")
        self.status_frame.pack(fill="x", padx=10, pady=5)
        
        self.status_indicators = {}
        self.create_status_indicator("LINK STATUS", "NOMINAL")
        self.create_status_indicator("SIGNAL", "87%")
        self.create_status_indicator("DATA FLOW", "ACTIVE")
        
        # Sensor data display
        self.sensor_frame = ttk.Frame(self.data_frame, style="Retro.TFrame")
        self.sensor_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create a text widget with retro styling
        self.sensor_text = tk.Text(self.sensor_frame,
                                 height=20,
                                 width=35,
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
        for frame in [self.video_frame, self.data_frame]:
            self.add_border(frame)
            
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
    def _init_(self, display):
        self.display = display
        self.connection_active = True
        self.frame_count = 0
        
    def enhance_frame(self, frame):
        try:
            # Apply retro green tint
            b, g, r = cv2.split(frame)
            g = cv2.addWeighted(g, 1.2, g, 0, 0)
            frame = cv2.merge([b, g, r])
            
            # Add scan lines effect
            height, width = frame.shape[:2]
            scan_lines = np.zeros((height, width), dtype=np.uint8)
            scan_lines[::3, :] = 32
            frame = cv2.subtract(frame, cv2.merge([scan_lines]*3))
            
            # Add slight noise
            noise = np.random.normal(0, 2, frame.shape).astype(np.uint8)
            frame = cv2.add(frame, noise)
            
            return frame
        except Exception as e:
            logging.error(f"Frame enhancement error: {e}")
            return frame
            
    async def process_frame(self, message):
        try:
            np_arr = np.frombuffer(message, dtype=np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            
            if frame is not None:
                frame = cv2.resize(frame, (640, 480))
                frame = self.enhance_frame(frame)
                
                self.display.last_valid_frame = frame.copy()
                self.frame_count += 1
                
                cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(cv2_image)
                photo = ImageTk.PhotoImage(image=pil_image)
                
                self.display.video_label.configure(image=photo)
                self.display.video_label.image = photo
                
        except Exception as e:
            logging.error(f"Frame processing error: {e}")

async def video_websocket(handler):
    while True:
        try:
            async with websockets.connect(ESP32_IP) as ws:
                while handler.connection_active:
                    message = await ws.recv()
                    await handler.process_frame(message)
        except Exception as e:
            logging.error(f"Video websocket error: {e}")
            await asyncio.sleep(1)

async def sensor_websocket(display):
    while True:
        try:
            async with websockets.connect(SENSOR_IP) as ws:
                while True:
                    message = await ws.recv()
                    async with sensor_data_lock:
                        display.update_sensor_data(message)
        except Exception as e:
            logging.error(f"Sensor websocket error: {e}")
            await asyncio.sleep(1)

def run_async_loop(loop, display):
    asyncio.set_event_loop(loop)
    handler = VideoStreamHandler(display)
    
    async def main():
        sensor_task = asyncio.create_task(sensor_websocket(display))
        video_task = asyncio.create_task(video_websocket(handler))
        await asyncio.gather(video_task, sensor_task)
        
    loop.run_until_complete(main())

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO,
                       format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Create main window
    root = tk.Tk()
    
    # Initialize display
    display = RetroDisplay(root)
    
    # Start async tasks
    loop = asyncio.new_event_loop()
    thread = Thread(target=run_async_loop, args=(loop, display))
    thread.daemon = True
    thread.start()
    
    # Start GUI
    root.mainloop()
    
if __name__ == "__main__":
    main()