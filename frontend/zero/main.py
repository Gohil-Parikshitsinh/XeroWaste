import tkinter as tk
from tkinter import ttk
import cv2
from datetime import datetime, timedelta
import json
import base64
from PIL import Image, ImageTk
import io
import threading
import time

class InventoryItem:
    def __init__(self, id, name, quantity, expiry_date, status):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.expiry_date = expiry_date
        self.status = status

class SmartInventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Inventory Management")
        self.root.geometry("1200x800")
        
        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Style
        self.style = ttk.Style()
        self.style.configure("Header.TLabel", font=("Helvetica", 24, "bold"))
        self.style.configure("Item.TFrame", padding=10)
        
        # Header
        header = ttk.Frame(root)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=20)
        ttk.Label(header, text="Smart Inventory Management", style="Header.TLabel").pack()
        
        # Camera Frame
        self.camera_frame = ttk.Frame(root)
        self.camera_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        # Video display
        self.video_label = ttk.Label(self.camera_frame)
        self.video_label.pack(pady=10)
        
        # Capture button
        self.capture_btn = ttk.Button(self.camera_frame, text="Capture Inventory", command=self.capture_image)
        self.capture_btn.pack(pady=10)
        
        # Inventory List Frame
        self.inventory_frame = ttk.Frame(root)
        self.inventory_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
        
        ttk.Label(self.inventory_frame, text="Detected Items", font=("Helvetica", 18, "bold")).pack(anchor="w", pady=10)
        
        self.items_frame = ttk.Frame(self.inventory_frame)
        self.items_frame.pack(fill="both", expand=True)
        
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        self.is_capturing = True
        
        # Start video stream
        self.update_video()
        
        # Sample inventory items (simulating detection)
        self.inventory_items = []
        
    def update_video(self):
        if self.is_capturing:
            ret, frame = self.cap.read()
            if ret:
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Convert to PhotoImage
                image = Image.fromarray(frame_rgb)
                image = image.resize((640, 480))
                photo = ImageTk.PhotoImage(image=image)
                
                self.video_label.configure(image=photo)
                self.video_label.image = photo
            
            self.root.after(10, self.update_video)
    
    def capture_image(self):
        self.capture_btn.configure(state="disabled", text="Processing...")
        
        # Simulate processing delay
        self.root.after(2000, self.process_image)
    
    def process_image(self):
        # Simulate detection results
        current_date = datetime.now()
        
        self.inventory_items = [
            InventoryItem("1", "Apples", 5, 
                         (current_date + timedelta(days=5)).strftime("%Y-%m-%d"), 
                         "fresh"),
            InventoryItem("2", "Milk", 1, 
                         (current_date + timedelta(days=2)).strftime("%Y-%m-%d"), 
                         "expiring-soon"),
            InventoryItem("3", "Bread", 1, 
                         (current_date - timedelta(days=1)).strftime("%Y-%m-%d"), 
                         "expired")
        ]
        
        self.update_inventory_list()
        self.capture_btn.configure(state="normal", text="Capture Inventory")
    
    def update_inventory_list(self):
        # Clear existing items
        for widget in self.items_frame.winfo_children():
            widget.destroy()
        
        # Status colors
        status_colors = {
            "fresh": "#dcfce7",
            "expiring-soon": "#fef9c3",
            "expired": "#fee2e2"
        }
        
        # Add items
        for item in self.inventory_items:
            item_frame = ttk.Frame(self.items_frame, style="Item.TFrame")
            item_frame.pack(fill="x", pady=5)
            item_frame.configure(style="Item.TFrame")
            
            # Create a colored background frame
            bg_color = status_colors.get(item.status, "#ffffff")
            canvas = tk.Canvas(item_frame, bg=bg_color, height=80, highlightthickness=0)
            canvas.pack(fill="x", padx=5, pady=5)
            
            # Add item details
            details_frame = ttk.Frame(canvas)
            details_frame.pack(padx=10, pady=10)
            
            ttk.Label(details_frame, text=item.name, font=("Helvetica", 12, "bold")).pack(anchor="w")
            ttk.Label(details_frame, 
                     text=f"Quantity: {item.quantity} • Expires: {item.expiry_date}",
                     font=("Helvetica", 10)).pack(anchor="w")
    
    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartInventoryApp(root)
    root.mainloop()