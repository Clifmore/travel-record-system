"""
Splash screen with flying plane animation.
"""

import tkinter as tk
from src.utils.theme import PANEL, SECONDARY, SECONDARY_LIGHT, SECONDARY_DARK, ACCENT, TEXT_PRIMARY, TEXT_SECONDARY


class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("")
        self.configure(bg=PANEL)
        self.overrideredirect(True)
        
        # Set size and position
        self.geometry("600x400")
        self.center_window()
        
        # Make it stay on top
        self.lift()
        self.attributes('-topmost', True)
        
        # Create main frame with border
        main_frame = tk.Frame(self, bg=PANEL, highlightbackground=SECONDARY, 
                            highlightthickness=2)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # University info
        uol_frame = tk.Frame(main_frame, bg=PANEL)
        uol_frame.pack(pady=(30, 10))
        
        tk.Label(uol_frame, text="UNIVERSITY OF LIVERPOOL", 
                bg=PANEL, fg=SECONDARY, font=("Segoe UI", 14, "bold")).pack()
        tk.Label(uol_frame, text="Group B - 2026", 
                bg=PANEL, fg=TEXT_SECONDARY, font=("Segoe UI", 11)).pack()
        
        # Title
        tk.Label(main_frame, text="TRAVEL AGENT RECORD MANAGEMENT SYSTEM", 
                bg=PANEL, fg=TEXT_PRIMARY, font=("Segoe UI", 16, "bold")).pack(pady=(10, 20))
        
        # Canvas for flying plane animation
        self.canvas = tk.Canvas(main_frame, width=500, height=150, bg=PANEL, 
                               highlightthickness=0)
        self.canvas.pack(pady=20)
        
        # Draw clouds
        self.clouds = []
        for i in range(3):
            x = 100 + i * 150
            y = 30
            cloud = self.canvas.create_oval(x, y, x+60, y+30, 
                                           fill="#E0E0E0", outline="")
            self.clouds.append(cloud)
        
        # Define plane position
        self.plane_x = -100
        self.plane_target = 600
        
        # Draw plane
        self.create_plane()
        
        # Loading text
        self.loading_text = tk.Label(main_frame, text="Loading System...", 
                                    bg=PANEL, fg=TEXT_SECONDARY, font=("Segoe UI", 10, "bold"))
        self.loading_text.pack(pady=(10, 5))
        
        # Progress bar
        self.progress_frame = tk.Frame(main_frame, bg=SECONDARY_LIGHT, height=4, width=400)
        self.progress_frame.pack(pady=10)
        self.progress_frame.pack_propagate(False)
        
        self.progress = tk.Frame(self.progress_frame, bg=ACCENT, height=4, width=0)
        self.progress.place(x=0, y=0)
        
        self.progress_value = 0
        
        # Start animation
        self.animate_plane()
        self.update_progress()

    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 600) // 2
        y = (self.winfo_screenheight() - 400) // 2
        self.geometry(f"600x400+{x}+{y}")

    def create_plane(self):
        """Draw a simple airplane"""
        # Main body
        self.plane_body = self.canvas.create_polygon(
            0, 50, 40, 40, 80, 50, 40, 60,
            fill=SECONDARY, outline=SECONDARY_DARK, width=2, tags="plane"
        )
        
        # Wings
        self.plane_wing1 = self.canvas.create_polygon(
            30, 30, 50, 20, 70, 30, 50, 35,
            fill=SECONDARY_LIGHT, outline=SECONDARY_DARK, width=1, tags="plane"
        )
        
        self.plane_wing2 = self.canvas.create_polygon(
            30, 70, 50, 80, 70, 70, 50, 65,
            fill=SECONDARY_LIGHT, outline=SECONDARY_DARK, width=1, tags="plane"
        )
        
        # Tail
        self.plane_tail = self.canvas.create_polygon(
            65, 40, 80, 25, 85, 35, 70, 45,
            fill=SECONDARY_DARK, outline=SECONDARY_DARK, width=1, tags="plane"
        )
        
        # Window
        self.plane_window = self.canvas.create_oval(
            45, 45, 55, 55,
            fill="white", outline=SECONDARY_DARK, width=1, tags="plane"
        )
        
        # Move plane to starting position
        self.canvas.move("plane", self.plane_x, 20)

    def animate_plane(self):
        """Animate the plane flying across the screen"""
        self.plane_x += 5
        
        # Move all plane parts
        self.canvas.move("plane", 5, 0)
        
        # Make clouds move slowly
        for cloud in self.clouds:
            self.canvas.move(cloud, 1, 0)
            coords = self.canvas.coords(cloud)
            if coords[0] > 600:
                self.canvas.move(cloud, -700, 0)
        
        # Reset plane position when it goes off screen
        if self.plane_x > self.plane_target:
            self.plane_x = -100
            self.canvas.move("plane", -700, 0)
        
        # Continue animation
        self.after(50, self.animate_plane)

    def update_progress(self):
        """Update progress bar"""
        self.progress_value += 2
        if self.progress_value <= 100:
            # Update progress bar width
            width = int(400 * self.progress_value / 100)
            self.progress.config(width=width)
            
            # Update loading text
            self.loading_text.config(text=f"Loading System... {self.progress_value}%")
            
            # Schedule next update
            self.after(50, self.update_progress)
        else:
            # Close splash and show main app
            self.after(500, self.destroy)
            self.parent.deiconify()