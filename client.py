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
        self.root.configure(bg='#000000')
        self.root.geometry("1600x900")  # Increased default size for better layout
        
        # Configure the grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Enhanced retro color scheme
        self.colors = {
            'bg': '#000000',
            'text': '#00ff00',
            'highlight': '#00ff33',
            'dim': '#005500',
            'border': '#008800',
            'header': '#00ff99'
        }
        
        # Custom font styles
        self.custom_font = ("Consolas", 12, "bold")
        self.header_font = ("Consolas", 18, "bold")
        self.title_font = ("Consolas", 24, "bold")
        
        self.setup_styles()
        self.create_main_frame()
        self.create_widgets()
        self.last_valid_frame = None
        self.frame_update_time = datetime.now()
        
        # Start blinking effect for status indicators
        self.blink_status()
        
    def setup_styles(self):
        style = ttk.Style()
        style.configure("Retro.TFrame",
                       background=self.colors['bg'])
        style.configure("Retro.TLabel",
                       background=self.colors['bg'],
                       foreground=self.colors['text'],
                       font=self.custom_font,
                       padding=5)
        style.configure("Header.TLabel",
                       background=self.colors['bg'],
                       foreground=self.colors['header'],
                       font=self.header_font,
                       padding=10)
                       
    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.root, style="Retro.TFrame")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
    def create_widgets(self):
        # Main title
        self.create_title()
        # Create top section with video and sensor data
        self.create_top_section()
        # Create bottom section for additional data
        self.create_bottom_section()
        # Add decorative elements
        self.add_decorative_elements()
    
    def create_title(self):
        title_frame = ttk.Frame(self.main_frame, style="Retro.TFrame")
        title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))  # Reduced the padding
        
        title = tk.Label(title_frame,
                        text="[ ESP32 TACTICAL INTERFACE ]",
                        font=self.title_font,
                        bg=self.colors['bg'],
                        fg=self.colors['header'])
        title.pack(pady=5)  # Reduced the padding here
        
        
    def create_top_section(self):
        # Container for video and sensor data
        top_frame = ttk.Frame(self.main_frame, style="Retro.TFrame")
        top_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        top_frame.grid_columnconfigure(0, weight=2)  # Video takes more space
        top_frame.grid_columnconfigure(1, weight=2)  # Sensor data takes less space
        
        # Video Section (Left)
        self.create_video_section(top_frame)
        # Sensor Section (Right)
        self.create_sensor_section(top_frame)
        
    def create_video_section(self, parent):
        video_frame = ttk.Frame(parent, style="Retro.TFrame")
        video_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        header = tk.Label(video_frame,
                         text="━━━[ TACTICAL FEED ]━━━",
                         font=self.header_font,
                         bg=self.colors['bg'],
                         fg=self.colors['header'])
        header.pack(pady=5)
        
        # Video display with border
        video_container = ttk.Frame(video_frame, style="Retro.TFrame")
        video_container.pack(expand=True, fill="both", padx=10, pady=5)
        
        self.video_label = ttk.Label(video_container, style="Retro.TLabel")
        self.video_label.pack(expand=True, fill="both", padx=2, pady=2)
        
        
        # Status line
        self.video_status = tk.Label(video_frame,
                                   text="⚡ FEED STATUS: ACTIVE ⚡",
                                   font=self.custom_font,
                                   bg=self.colors['bg'],
                                   fg=self.colors['highlight'])
        self.video_status.pack(pady=5)
        
    def create_sensor_section(self, parent):
        sensor_frame = ttk.Frame(parent, style="Retro.TFrame")
        sensor_frame.grid(row=0, column=1, sticky="nsew")
        
        # Sensor Header
        header = tk.Label(sensor_frame,
                         text="━━━[ SENSOR DATA ]━━━",
                         font=self.header_font,
                         bg=self.colors['bg'],
                         fg=self.colors['header'])
        header.pack(pady=5, fill="x")
        
        # Status indicators
        self.status_frame = ttk.Frame(sensor_frame, style="Retro.TFrame")
        self.status_frame.pack(fill="x", padx=10, pady=5)
        
        self.status_indicators = {}
        self.create_status_indicator("LINK STATUS", "NOMINAL")
        self.create_status_indicator("DATA FLOW", "ACTIVE")
        
        # Sensor readings display
        readings_container = ttk.Frame(sensor_frame, style="Retro.TFrame")
        readings_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.sensor_text = tk.Text(readings_container,
                                 height=10,
                                 width=40,
                                 bg=self.colors['bg'],
                                 fg=self.colors['text'],
                                 font=self.custom_font,
                                 wrap=tk.WORD,
                                 padx=10,
                                 pady=10,
                                 insertbackground=self.colors['text'])
        self.sensor_text.pack(fill="both", expand=True, padx=2, pady=2)
        
        scrollbar = tk.Scrollbar(readings_container,
                               orient="vertical",
                               command=self.sensor_text.yview,
                               width=16,
                               bg=self.colors['bg'],
                               troughcolor=self.colors['bg'],
                               activebackground=self.colors['highlight'])
        scrollbar.pack(side="right", fill="y")
        self.sensor_text.configure(yscrollcommand=scrollbar.set)
        
        
    def create_bottom_section(self):
        bottom_frame = ttk.Frame(self.main_frame, style="Retro.TFrame")
        bottom_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        
        # System status display
        status_label = tk.Label(bottom_frame,
                              text="[ SYSTEM STATUS: OPERATIONAL ]",
                              font=self.custom_font,
                              bg=self.colors['bg'],
                              fg=self.colors['highlight'])
        status_label.pack(pady=5)
        
    def create_status_indicator(self, label, initial_value):
        frame = ttk.Frame(self.status_frame, style="Retro.TFrame")
        frame.pack(fill="x", pady=2)
        
        label_widget = tk.Label(frame,
                              text=f"► {label}:",
                              font=self.custom_font,
                              bg=self.colors['bg'],
                              fg=self.colors['text'])
        label_widget.pack(side="left")
        
        value_widget = tk.Label(frame,
                              text=initial_value,
                              font=self.custom_font,
                              bg=self.colors['bg'],
                              fg=self.colors['highlight'])
        value_widget.pack(side="right")
        
        self.status_indicators[label] = value_widget
        
    def draw_box_border(self, widget):
        canvas = tk.Canvas(widget,
                         bg=self.colors['bg'],
                         highlightthickness=2,
                         highlightbackground=self.colors['border'])
        canvas.pack(fill="both", expand=True, padx=1, pady=1)
        
    def add_decorative_elements(self):
        self.add_corners(self.main_frame)
            
    def add_corners(self, frame):
        corner_size = 20
        corners = [
            "╔", "╗",  # Top corners
            "╚", "╝"   # Bottom corners
        ]
        positions = [(0, 0), (1, 0), (0, 1), (1, 1)]
        
        for corner, (col, row) in zip(corners, positions):
            label = tk.Label(frame,
                           text=corner,
                           font=("Consolas", 24),
                           bg=self.colors['bg'],
                           fg=self.colors['border'])
            label.place(x=corner_size * col, y=corner_size * row)
                         
    def blink_status(self):
        for indicator in self.status_indicators.values():
            current_color = indicator.cget("foreground")
            new_color = self.colors['dim'] if current_color == self.colors['highlight'] else self.colors['highlight']
            indicator.configure(foreground=new_color)
        self.root.after(1000, self.blink_status)
        
    def update_sensor_data(self, data):
        self.sensor_text.delete(1.0, tk.END)
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_data = (
            f"TIME: {timestamp}\n"
            f"{'═' * 35}\n"
            f"SENSOR READINGS:\n"
            f"{'═' * 35}\n"
            f"{data}\n"
        )
        self.sensor_text.insert(tk.END, formatted_data)

# [VideoStreamHandler and other supporting classes remain unchanged]
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
