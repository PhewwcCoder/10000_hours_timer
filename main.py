# Import necessary libraries
import tkinter as tk  # For creating the GUI interface
from tkinter import filedialog  # For file selection dialogs
import time  # For time tracking and calculations
import json  # For saving and loading timer data
import os  # For file path operations
from datetime import timedelta  # For formatting time display
from PIL import Image, ImageTk  # For image handling (background photos)

class CodingTimer:
    def __init__(self, root):
        """Initialize the main application window and components"""
        self.root = root
        self.root.title("10,000 Hours Timer")  # Window title
        
        # Initialize timer variables
        self.remaining = 3600 * 9000  # 10,000 hours converted to seconds, I've written 9000 according to my preference
        self.running = False  # Timer state (running/stopped)
        self.last_update = time.time()  # Last time the timer was updated
        self.bg_image = None  # Will hold the background image
        self.button_states = {}  # Tracks button pressed states for visual feedback
        
        # Load saved timer data from previous session
        self.load_time()
        
        # Configure main window appearance
        self.root.geometry("500x300")  # Set window size (width x height)
        self.root.configure(bg='#333333')  # Default background color (dark gray)
        
        # Create the time display label
        self.time_label = tk.Label(
            root, 
            font=('Helvetica', 24),  # Font style and size
            fg='white',  # Text color (white)
            bg='#333333'  # Background color (matches window)
        )
        self.time_label.pack(pady=40)  # Add vertical padding
        
        # Create a frame to hold control buttons
        self.controls = tk.Frame(root, bg='#333333')  # Same bg as window
        self.controls.pack(pady=20)  # Add vertical padding
        
        # Define style for all buttons
        self.btn_style = {
            'bg': '#555555',  # Normal background color
            'fg': 'white',  # Text color
            'activebackground': '#777777',  # Color when clicked
            'bd': 0,  # Border width (no border)
            'relief': 'raised',  # 3D raised appearance
            'padx': 10, 'pady': 5,  # Horizontal and vertical padding
            'font': ('Helvetica', 10)  # Button font
        }
        
        # Create and configure all buttons
        self.create_buttons()
        
        # Update the time display with current values
        self.update_display()
        
        # Set your personal background photo (MODIFY THIS PATH)
        self.set_default_background("C:\\Users\\Aryan\\Downloads\\image.jpg")  # ← CHANGE THIS PATH
        
        # Start timer if it was running when last closed
        if self.running:
            self.start_timer()
    
    def set_default_background(self, photo_path):
        """Set your personal photo as the default background"""
        try:
            # Open the image file
            img = Image.open(photo_path)
            # Resize to match window dimensions
            img = img.resize((500, 300), Image.Resampling.LANCZOS)
            # Convert to Tkinter-compatible format
            self.bg_image = ImageTk.PhotoImage(img)
            
            # Create a label to hold the background image
            bg_label = tk.Label(self.root, image=self.bg_image)
            # Position the background to fill the window
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            # Bring other elements to the front
            self.time_label.lift()  # Time display
            self.controls.lift()  # Control buttons
        except Exception as e:
            print(f"Error loading background image: {e}")
            # Fallback to solid color if image fails
            self.root.configure(bg='#333333')
    
    def create_buttons(self):
        """Create and configure all control buttons with visual feedback"""
        # Create buttons with their commands
        self.start_btn = tk.Button(
            self.controls, 
            text="Start/Stop", 
            command=self.toggle_timer, 
            **self.btn_style
        )
        self.add_btn = tk.Button(
            self.controls, 
            text="+1h", 
            command=lambda: self.adjust_time(3600), 
            **self.btn_style
        )
        self.sub_btn = tk.Button(
            self.controls, 
            text="-1h", 
            command=lambda: self.adjust_time(-3600), 
            **self.btn_style
        )
        self.bg_btn = tk.Button(
            self.controls, 
            text="Change BG", 
            command=self.change_background, 
            **self.btn_style
        )
        
        # Pack all buttons side by side
        buttons = [self.start_btn, self.add_btn, self.sub_btn, self.bg_btn]
        for btn in buttons:
            btn.pack(side=tk.LEFT, padx=5)  # Add horizontal padding
            
            # Set up hover and click effects
            btn.bind("<Enter>", lambda e, b=btn: self.on_enter(e, b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_leave(e, b))
            btn.bind("<ButtonPress-1>", lambda e, b=btn: self.on_press(e, b))
            btn.bind("<ButtonRelease-1>", lambda e, b=btn: self.on_release(e, b))
            
            # Track button states for visual feedback
            self.button_states[btn] = False
    
    def on_enter(self, event, button):
        """Button hover effect - grows slightly and changes color"""
        button.config(bg='#666666')  # Lighter background
        button.config(font=('Helvetica', 11))  # Slightly larger font
        button.config(padx=12, pady=6)  # Increase padding (makes button bigger)
    
    def on_leave(self, event, button):
        """Reset button when mouse leaves"""
        button.config(bg='#555555')  # Original color
        button.config(font=('Helvetica', 10))  # Original font size
        button.config(padx=10, pady=5)  # Original padding
        # Maintain pressed/unpressed state
        if self.button_states[button]:
            button.config(relief='sunken')
        else:
            button.config(relief='raised')
    
    def on_press(self, event, button):
        """Button press effect - appears depressed"""
        self.button_states[button] = True  # Mark as pressed
        button.config(relief='sunken')  # Sunken 3D effect
        button.config(bg='#444444')  # Darker background
    
    def on_release(self, event, button):
        """Button release effect - bounces back"""
        self.button_states[button] = False  # Mark as released
        button.config(relief='raised')  # Raised 3D effect
        button.config(bg='#666666')  # Hover color
        # Flash effect when fully released
        button.after(100, lambda: button.config(bg='#555555'))
    
    def load_time(self):
        """Load saved timer data from JSON file"""
        try:
            if os.path.exists('coding_timer.json'):
                with open('coding_timer.json', 'r') as f:
                    data = json.load(f)
                    # Get saved values or use defaults
                    self.remaining = data.get('remaining', 3600 * 10000)
                    self.running = data.get('running', False)
                    self.last_update = data.get('last_update', time.time())
                    
                    # If timer was running, calculate elapsed time
                    if self.running:
                        elapsed = time.time() - self.last_update
                        self.remaining = max(0, self.remaining - elapsed)
        except Exception as e:
            print(f"Error loading timer data: {e}")
    
    def save_time(self):
        """Save current timer state to JSON file"""
        data = {
            'remaining': self.remaining,
            'running': self.running,
            'last_update': self.last_update
        }
        try:
            with open('coding_timer.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving timer data: {e}")
    
    def toggle_timer(self):
        """Start or stop the timer"""
        if self.running:
            self.stop_timer()
            self.start_btn.config(text="Start")  # Update button text
        else:
            self.start_timer()
            self.start_btn.config(text="Stop")  # Update button text
        self.save_time()  # Persist the state
    
    def start_timer(self):
        """Start the countdown timer"""
        self.running = True
        self.last_update = time.time()  # Reset last update time
        self.update_timer()  # Begin updates
    
    def stop_timer(self):
        """Stop the countdown timer"""
        self.running = False
    
    def update_timer(self):
        """Update the timer display and calculate remaining time"""
        if self.running:
            now = time.time()
            elapsed = now - self.last_update  # Time since last update
            self.last_update = now
            self.remaining = max(0, self.remaining - elapsed)  # Prevent negative
            self.update_display()  # Refresh the display
            # Schedule next update in 1 second
            self.root.after(1000, self.update_timer)
        self.save_time()  # Save current state
    
    def adjust_time(self, seconds):
        """Adjust the remaining time by specified seconds"""
        self.remaining = max(0, self.remaining + seconds)  # Prevent negative
        self.update_display()
        # Visual confirmation (green flash)
        self.time_label.config(fg='#4CAF50')  # Bright green
        self.root.after(200, lambda: self.time_label.config(fg='white'))
        self.save_time()
    
    def change_background(self):
        """Open file dialog to change background image"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
        )
        if file_path:
            try:
                img = Image.open(file_path)
                img = img.resize((500, 300), Image.Resampling.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(img)
                
                # Create new background label
                bg_label = tk.Label(self.root, image=self.bg_image)
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                
                # Bring other elements to front
                self.time_label.lift()
                self.controls.lift()
                
                # Visual confirmation
                self.bg_btn.config(text="✓ Changed!")
                self.root.after(1000, lambda: self.bg_btn.config(text="Change BG"))
                
            except Exception as e:
                print(f"Error loading image: {e}")
    
    def update_display(self):
        """Update the time display label"""
        hours = self.remaining / 3600  # Convert seconds to hours
        # Format as days, hours:minutes:seconds
        time_str = str(timedelta(seconds=self.remaining)).split('.')[0]
        self.time_label.config(
            text=f"{hours:,.1f} hours remaining\n({time_str})"
        )
    
    def run(self):
        """Start the application main loop"""
        self.root.mainloop()

# Main program execution
if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    app = CodingTimer(root)  # Create the timer application
    app.run()  # Start the application