import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date, datetime
import calendar
import re
import json
import csv
import sqlite3
import os
import math

# ─────────────────────────────── THEME (60-30-10 RULE) ─────────────────────────────

# 60% - Neutral background (brighter, more vibrant)
BG_PRIMARY = "#F8F9FA"        # Brighter off-white - 60% of UI
PANEL = "#FFFFFF"              # Pure white panels
CARD = "#F0F2F5"               # Light gray-blue cards for contrast

# 30% - Secondary color (more vibrant blue)
SECONDARY = "#2C7BE5"          # Brighter, more vibrant blue - 30% of UI
SECONDARY_LIGHT = "#4D94F0"    # Lighter blue for hover
SECONDARY_DARK = "#1A5BBF"     # Darker blue for pressed

# 10% - Accent color for CTAs (warmer orange)
ACCENT = "#F39C12"             # Richer orange - 10% of UI
ACCENT_LIGHT = "#F5B041"       # Lighter orange for hover
ACCENT_DARK = "#D68910"        # Darker orange for pressed

# Supporting colors
GREEN = "#2ECC71"              # Brighter success green
RED = "#E74C3C"                # Error red
TEXT_PRIMARY = "#2C3E50"       # Dark blue-gray for primary text
TEXT_SECONDARY = "#7F8C8D"     # Medium gray for secondary text
TEXT_MUTED = "#95A5A6"         # Light gray for muted text
BORDER = "#D5DBDB"             # Light border
HOME_BTN = "#7F8C8D"           # Gray for home button (instead of brown)

# Fonts
FT = ("Segoe UI", 10)
FB = ("Segoe UI", 10, "bold")
FH = ("Segoe UI", 18, "bold")
FT2 = ("Segoe UI", 11)
FS = ("Segoe UI", 9)

GEOGRAPHY = {
    "United States": {
        "California":  ["Los Angeles", "San Francisco", "San Diego", "Sacramento"],
        "New York":    ["New York City", "Buffalo", "Albany", "Rochester"],
        "Texas":       ["Houston", "Dallas", "Austin", "San Antonio"],
        "Florida":     ["Miami", "Orlando", "Tampa", "Jacksonville"],
    },
    "United Kingdom": {
        "England":     ["London", "Manchester", "Birmingham", "Bristol"],
        "Scotland":    ["Edinburgh", "Glasgow", "Aberdeen"],
        "Wales":       ["Cardiff", "Swansea", "Newport"],
    },
    "Canada": {
        "Ontario":          ["Toronto", "Ottawa", "Hamilton"],
        "British Columbia": ["Vancouver", "Victoria", "Surrey"],
    },
    "Australia": {
        "New South Wales":  ["Sydney", "Newcastle", "Wollongong"],
        "Victoria":         ["Melbourne", "Geelong", "Ballarat"],
    },
}

# Sample data storage (simulates database)
SAMPLE_DATA = {
    "clients": {
        "C-0001": {"first": "Alice", "last": "Johnson", "email": "alice@email.com", 
                  "phone": "07911123456", "address": "12 Baker St", 
                  "country": "United Kingdom", "state": "England", 
                  "city": "London", "zip": "W1A 1AA", "deleted": False},
        "C-0002": {"first": "Bob", "last": "Smith", "email": "bob@email.com", 
                  "phone": "14155552671", "address": "123 Market St", 
                  "country": "United States", "state": "California", 
                  "city": "San Francisco", "zip": "94105", "deleted": False},
        "C-0003": {"first": "Carol", "last": "Davies", "email": "carol@company.co.uk", 
                  "phone": "02079461234", "address": "45 High St", 
                  "country": "United Kingdom", "state": "England", 
                  "city": "Manchester", "zip": "M1 1AB", "deleted": False},
        "C-0004": {"first": "David", "last": "Brown", "email": "david@test.com", 
                  "phone": "0123456789", "address": "78 Park Ave", 
                  "country": "Canada", "state": "Ontario", 
                  "city": "Toronto", "zip": "M5V 2T6", "deleted": True},
    },
    "airlines": {
        "A-0001": {"name": "British Airways", "deleted": False},
        "A-0002": {"name": "Delta Airlines", "deleted": False},
        "A-0003": {"name": "Emirates", "deleted": False},
        "A-0004": {"name": "Lufthansa", "deleted": False},
        "A-0005": {"name": "Ryanair", "deleted": True},
    },
    "flights": {
        "F-0001": {"airline": "A-0001", "date": "2026-04-10", "time": "09:00", 
                  "origin": "London", "destination": "New York City", "deleted": False},
        "F-0002": {"airline": "A-0002", "date": "2026-04-12", "time": "14:30", 
                  "origin": "San Francisco", "destination": "Dallas", "deleted": False},
        "F-0003": {"airline": "A-0003", "date": "2026-04-15", "time": "22:00", 
                  "origin": "Dubai", "destination": "London", "deleted": False},
        "F-0004": {"airline": "A-0004", "date": "2026-04-20", "time": "11:15", 
                  "origin": "Frankfurt", "destination": "New York", "deleted": True},
    }
}

TIMES = [f"{h:02d}:{m:02d}" for h in range(0,24) for m in (0,15,30,45)]

# Track recently deleted records
recently_deleted = []

# ─────────────────────────────── SPLASH SCREEN WITH FLYING PLANE ─────────────────────────────

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
        
        # Define plane position before creating the plane
        self.plane_x = -100
        self.plane_target = 600
        
        # Draw plane
        self.create_plane()
        
        # Loading text
        self.loading_text = tk.Label(main_frame, text="Loading System...", 
                                    bg=PANEL, fg=TEXT_SECONDARY, font=FB)
        self.loading_text.pack(pady=(10, 5))
        
        # Progress bar (modern style)
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

# ─────────────────────────────── EMAIL VALIDATION ───────────────────────────

def validate_email(email):
    """Comprehensive email validation accepting all valid formats"""
    email = email.strip()
    
    # Basic checks
    if not email:
        return False
    
    # Must have exactly one @
    if email.count('@') != 1:
        return False
    
    # Split into local and domain
    local, domain = email.split('@')
    
    # Local part checks
    if not local or len(local) > 64:
        return False
    
    # Domain checks
    if not domain or len(domain) > 255:
        return False
    
    # Domain must have at least one dot
    if '.' not in domain:
        return False
    
    # Check domain parts
    domain_parts = domain.split('.')
    if len(domain_parts) < 2:
        return False
    
    # Each domain part must be non-empty and valid
    for part in domain_parts:
        if not part:
            return False
        # Can't start or end with hyphen
        if part.startswith('-') or part.endswith('-'):
            return False
        # Can only contain letters, numbers, hyphens
        if not re.match(r'^[a-zA-Z0-9-]+$', part):
            return False
    
    # Last part (TLD) must be at least 2 characters
    if len(domain_parts[-1]) < 2:
        return False
    
    return True

# ─────────────────────────────── EXPORT FUNCTIONS ───────────────────────────

def export_to_json(data, filename):
    """Export data to JSON format"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except Exception as e:
        print(f"JSON Export Error: {e}")
        return False

def export_to_csv(data, filename, record_type):
    """Export data to CSV format"""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            if record_type == "clients":
                writer = csv.writer(f)
                writer.writerow(["ID", "First Name", "Last Name", "Email", "Phone", 
                               "Address", "Country", "State", "City", "ZIP", "Status"])
                for cid, info in data.items():
                    status = "DELETED" if info.get("deleted", False) else "ACTIVE"
                    writer.writerow([cid, info["first"], info["last"], info["email"],
                                   info["phone"], info["address"], info["country"],
                                   info.get("state", ""), info["city"], info.get("zip", ""), status])
            
            elif record_type == "airlines":
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Status"])
                for aid, info in data.items():
                    status = "DELETED" if info.get("deleted", False) else "ACTIVE"
                    writer.writerow([aid, info["name"], status])
            
            elif record_type == "flights":
                writer = csv.writer(f)
                writer.writerow(["ID", "Airline ID", "Airline Name", "Date", "Time", "Origin", "Destination", "Status"])
                for fid, info in data.items():
                    airline_name = SAMPLE_DATA["airlines"].get(info["airline"], {}).get("name", "Unknown")
                    status = "DELETED" if info.get("deleted", False) else "ACTIVE"
                    writer.writerow([fid, info["airline"], airline_name, info["date"], info["time"],
                                   info["origin"], info["destination"], status])
        return True
    except Exception as e:
        print(f"CSV Export Error: {e}")
        return False

def export_to_sqlite(data, filename, record_type):
    """Export data to SQLite database"""
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        
        if record_type == "clients":
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clients (
                    id TEXT PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    email TEXT,
                    phone TEXT,
                    address TEXT,
                    country TEXT,
                    state TEXT,
                    city TEXT,
                    zip TEXT,
                    status TEXT
                )
            ''')
            for cid, info in data.items():
                status = "DELETED" if info.get("deleted", False) else "ACTIVE"
                cursor.execute('''
                    INSERT OR REPLACE INTO clients 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (cid, info["first"], info["last"], info["email"], info["phone"],
                      info["address"], info["country"], info.get("state", ""), 
                      info["city"], info.get("zip", ""), status))
        
        elif record_type == "airlines":
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS airlines (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    status TEXT
                )
            ''')
            for aid, info in data.items():
                status = "DELETED" if info.get("deleted", False) else "ACTIVE"
                cursor.execute('INSERT OR REPLACE INTO airlines VALUES (?, ?, ?)',
                             (aid, info["name"], status))
        
        elif record_type == "flights":
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS flights (
                    id TEXT PRIMARY KEY,
                    airline_id TEXT,
                    airline_name TEXT,
                    date TEXT,
                    time TEXT,
                    origin TEXT,
                    destination TEXT,
                    status TEXT
                )
            ''')
            for fid, info in data.items():
                airline_name = SAMPLE_DATA["airlines"].get(info["airline"], {}).get("name", "Unknown")
                status = "DELETED" if info.get("deleted", False) else "ACTIVE"
                cursor.execute('''
                    INSERT OR REPLACE INTO flights 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (fid, info["airline"], airline_name, info["date"], info["time"],
                      info["origin"], info["destination"], status))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"SQLite Export Error: {e}")
        return False

# ─────────────────────────────── HELPERS ─────────────────────────────────────

def create_rounded_button(parent, text, command, color=SECONDARY, width=18, height=2):
    """Create a modern button with rounded corners"""
    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg="white",
        font=FB,
        relief="flat",
        cursor="hand2",
        padx=15,
        pady=8,
        width=width,
        height=height,
        bd=0,
        highlightthickness=0,
        activebackground=_lighten(color),
        activeforeground="white"
    )
    
    # Add rounded corners effect using a frame with border radius
    button.bind("<Enter>", lambda e: button.config(bg=_lighten(color)))
    button.bind("<Leave>", lambda e: button.config(bg=color))
    
    return button

def create_small_button(parent, text, command, color=SECONDARY, width=15):
    """Create a small modern button with adjustable width"""
    return create_rounded_button(parent, text, command, color, width=width, height=1)

def _lighten(hex_color):
    """Lighten color for hover effects"""
    hex_color = hex_color.lstrip("#")
    r,g,b = (int(hex_color[i:i+2],16) for i in (0,2,4))
    return f"#{min(r+30,255):02x}{min(g+30,255):02x}{min(b+30,255):02x}"

def _darken(hex_color):
    """Darken color for hover effects"""
    hex_color = hex_color.lstrip("#")
    r,g,b = (int(hex_color[i:i+2],16) for i in (0,2,4))
    return f"#{max(r-30,0):02x}{max(g-30,0):02x}{max(b-30,0):02x}"

def entry(parent, w=32, show=None):
    """Consistent entry field creation"""
    e = tk.Entry(parent, bg="white", fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY,
                 font=FT, relief="solid", bd=1, width=w, show=show,
                 highlightthickness=1, highlightcolor=SECONDARY,
                 highlightbackground=BORDER)
    return e

def combo(parent, values, w=28, state="readonly"):
    """Consistent combobox creation"""
    s = ttk.Style()
    s.theme_use("clam")
    s.configure("Custom.TCombobox", fieldbackground="white", background="white",
                foreground=TEXT_PRIMARY, arrowcolor=SECONDARY, bordercolor=BORDER,
                selectbackground=SECONDARY_LIGHT, selectforeground="white", 
                borderwidth=1, relief="solid")
    c = ttk.Combobox(parent, values=values, width=w, state=state,
                     font=FT, style="Custom.TCombobox")
    return c

def lbl(parent, text, fg=TEXT_PRIMARY, font=FT, **kw):
    """Consistent label creation"""
    return tk.Label(parent, text=text, bg=BG_PRIMARY, fg=fg, font=font, **kw)

def err_lbl(parent):
    """Consistent error label creation"""
    return tk.Label(parent, text="", bg=BG_PRIMARY, fg=RED,
                    font=FB, anchor="w")

def success_lbl(parent):
    """Success message label"""
    return tk.Label(parent, text="", bg=BG_PRIMARY, fg=GREEN,
                    font=FB, anchor="w")

def divider(parent):
    """Consistent divider"""
    tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=0, pady=8)

def format_id(prefix, num):
    """Format ID consistently"""
    return f"{prefix}-{num:04d}"

def get_next_id(prefix, data_dict):
    """Get next available ID"""
    if not data_dict:
        return format_id(prefix, 1)
    existing = [int(k.split('-')[1]) for k in data_dict.keys()]
    next_num = max(existing) + 1
    return format_id(prefix, next_num)

# ─────────────────────────────── CALENDAR ────────────────────────────────────

class CalendarPicker(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.cur = date.today()
        self.configure(bg=PANEL)
        self.title("Select Date")
        self.resizable(False, False)
        self.grab_set()
        self._draw()
        self.center_window()

    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 300) // 2
        y = (self.winfo_screenheight() - 320) // 2
        self.geometry(f"300x320+{x}+{y}")

    def _draw(self):
        for w in self.winfo_children(): 
            w.destroy()
            
        # Navigation
        nav = tk.Frame(self, bg=PANEL, padx=8, pady=6)
        nav.pack(fill="x")
        
        tk.Button(nav, text="◀", command=self._prev, bg=PANEL, fg=SECONDARY,
                  font=FB, relief="flat", cursor="hand2", bd=0,
                  activebackground=SECONDARY_LIGHT, activeforeground="white").pack(side="left")
                  
        tk.Label(nav, text=self.cur.strftime("%B %Y"), bg=PANEL, fg=TEXT_PRIMARY,
                 font=FB, width=16).pack(side="left", expand=True)
                 
        tk.Button(nav, text="▶", command=self._next, bg=PANEL, fg=SECONDARY,
                  font=FB, relief="flat", cursor="hand2", bd=0,
                  activebackground=SECONDARY_LIGHT, activeforeground="white").pack(side="right")
        
        # Calendar grid
        g = tk.Frame(self, bg=PANEL, padx=8, pady=8)
        g.pack()
        
        # Weekday headers
        for i, d in enumerate(["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]):
            tk.Label(g, text=d, bg=PANEL, fg=SECONDARY, font=FB, width=4).grid(row=0, column=i)
        
        # Calculate month days
        first, days = calendar.monthrange(self.cur.year, self.cur.month)
        col, row = first, 1
        today = date.today()
        
        # Create day buttons
        for day in range(1, days + 1):
            d = date(self.cur.year, self.cur.month, day)
            is_past = d < today
            is_today = d == today
            
            # Visual feedback based on date state
            if is_past:
                fg = TEXT_MUTED
                bg = PANEL
                state = "disabled"
            else:
                fg = ACCENT if is_today else TEXT_PRIMARY
                bg = ACCENT_LIGHT if is_today else PANEL
                state = "normal"
            
            btn = tk.Button(g, text=str(day), width=4, bg=bg, fg=fg, font=FB,
                           relief="flat", cursor="hand2" if not is_past else "arrow", 
                           bd=0, state=state,
                           disabledforeground=TEXT_MUTED, 
                           activebackground=SECONDARY, activeforeground="white",
                           command=lambda dd=d: self._pick(dd))
            btn.grid(row=row, column=col, padx=2, pady=2, ipady=3)
            
            col += 1
            if col == 7:
                col = 0
                row += 1
        
        # Cancel button
        cancel_btn = tk.Button(self, text="Cancel", command=self.destroy,
                              bg=HOME_BTN, fg="white", font=FB, relief="flat",
                              cursor="hand2", bd=0, activebackground=_lighten(HOME_BTN),
                              activeforeground="white")
        cancel_btn.pack(pady=10)

    def _prev(self):
        y, m = self.cur.year, self.cur.month - 1
        if m == 0:
            y -= 1
            m = 12
        self.cur = self.cur.replace(year=y, month=m, day=1)
        self._draw()

    def _next(self):
        y, m = self.cur.year, self.cur.month + 1
        if m == 13:
            y += 1
            m = 1
        self.cur = self.cur.replace(year=y, month=m, day=1)
        self._draw()

    def _pick(self, d):
        self.callback(d)
        self.destroy()

# ─────────────────────────────── LOADING OVERLAY ────────────────────────────

class LoadingOverlay:
    """Simple loading indicator"""
    def __init__(self, parent):
        self.parent = parent
        self.overlay = None
        
    def show(self, message="Loading..."):
        self.overlay = tk.Toplevel(self.parent)
        self.overlay.transient(self.parent)
        self.overlay.grab_set()
        self.overlay.overrideredirect(True)
        
        # Center on parent
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - 150
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - 75
        self.overlay.geometry(f"300x150+{x}+{y}")
        self.overlay.configure(bg=PANEL)
        self.overlay.configure(highlightbackground=SECONDARY, highlightthickness=2)
        
        tk.Label(self.overlay, text="⏳", bg=PANEL, fg=SECONDARY,
                font=("Segoe UI", 36)).pack(pady=(20, 5))
        tk.Label(self.overlay, text=message, bg=PANEL, fg=TEXT_PRIMARY,
                font=FB).pack()
        self.overlay.update()
        
    def hide(self):
        if self.overlay:
            self.overlay.destroy()
            self.overlay = None

# ─────────────────────────────── MAIN APP ──────────────────────────────────────

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Travel Agent Record Management System - UoL Group B 2026")
        self.geometry("1050x720")
        self.minsize(850, 600)
        self.configure(bg=BG_PRIMARY)
        
        # Hide main window initially
        self.withdraw()
        
        # Show splash screen
        self.splash = SplashScreen(self)
        
        # Center main window
        self._center()
        self._build_shell()
        
        # Track current screen for context
        self.current_screen = "home"
        self.loading = LoadingOverlay(self)
        
        # Initialize deleted records list
        self.update_deleted_records()

    def update_deleted_records(self):
        """Update the list of deleted records"""
        global recently_deleted
        recently_deleted = []
        
        # Check clients
        for cid, data in SAMPLE_DATA["clients"].items():
            if data.get("deleted", False):
                recently_deleted.append(("Client", cid, data))
                
        # Check airlines
        for aid, data in SAMPLE_DATA["airlines"].items():
            if data.get("deleted", False):
                recently_deleted.append(("Airline", aid, data))
                
        # Check flights
        for fid, data in SAMPLE_DATA["flights"].items():
            if data.get("deleted", False):
                recently_deleted.append(("Flight", fid, data))

    def _center(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 1050) // 2
        y = (self.winfo_screenheight() - 720) // 2
        self.geometry(f"1050x720+{x}+{y}")

    # ── Shell (top bar + sidebar + content area) ──────────────────────────────
    def _build_shell(self):
        # Top bar
        top = tk.Frame(self, bg=PANEL, height=60)
        top.pack(fill="x")
        top.pack_propagate(False)
        
        # Logo/Title
        title_frame = tk.Frame(top, bg=PANEL)
        title_frame.pack(side="left", padx=20)
        
        tk.Label(title_frame, text="✈", bg=PANEL, fg=SECONDARY,
                font=("Segoe UI", 20, "bold")).pack(side="left", padx=(0, 10))
        
        tk.Label(title_frame, text="TRAVEL AGENT RECORD MANAGEMENT SYSTEM",
                 bg=PANEL, fg=TEXT_PRIMARY, font=("Segoe UI", 14, "bold")).pack(side="left")
        
        tk.Label(title_frame, text="UoL Group B 2026",
                 bg=PANEL, fg=TEXT_MUTED, font=FS).pack(side="left", padx=(10, 0))
        
        # Status indicator
        self.status_lbl = tk.Label(top, text="● ONLINE", bg=PANEL, fg=GREEN,
                                   font=FB, padx=20)
        self.status_lbl.pack(side="right")

        # Sidebar
        self.side = tk.Frame(self, bg=PANEL, width=200)
        self.side.pack(fill="y", side="left")
        self.side.pack_propagate(False)

        tk.Label(self.side, text="MAIN MENU", bg=PANEL, fg=SECONDARY,
                 font=FB, padx=16, pady=10).pack(anchor="w")

        self._nav_btns = []
        self.current_nav = None
        
        for icon, label, cmd in [
            ("🏠", "HOME", self.show_home),
            ("➕", "CREATE RECORD", self.show_create_menu),
            ("🔍", "SEARCH RECORDS", self.show_search),
            ("✏️", "UPDATE RECORD", self.show_update),
            ("🗑️", "DELETE RECORD", self.show_delete),
            ("📋", "DELETED RECORDS", self.show_deleted_records),
        ]:
            f = tk.Frame(self.side, bg=PANEL, cursor="hand2", height=40)
            f.pack(fill="x", pady=1)
            f.pack_propagate(False)
            
            lb = tk.Label(f, text=f"  {icon}  {label}", bg=PANEL, fg=TEXT_PRIMARY,
                          font=FB, anchor="w", padx=8)
            lb.pack(fill="both", expand=True)
            
            # Store reference for highlighting
            f.ref = lb
            lb.parent_frame = f
            
            def _enter(e, fr=f):
                if fr != self.current_nav:
                    fr.config(bg=SECONDARY_LIGHT)
                    e.widget.config(bg=SECONDARY_LIGHT, fg="white")
                    
            def _leave(e, fr=f):
                if fr != self.current_nav:
                    fr.config(bg=PANEL)
                    e.widget.config(bg=PANEL, fg=TEXT_PRIMARY)
                    
            def _click(e, c=cmd, fr=f):
                # Highlight selected nav item
                if self.current_nav:
                    self.current_nav.config(bg=PANEL)
                    self.current_nav.ref.config(bg=PANEL, fg=TEXT_PRIMARY)
                fr.config(bg=SECONDARY)
                lb.config(bg=SECONDARY, fg="white")
                self.current_nav = fr
                c()
                
            lb.bind("<Enter>", _enter)
            lb.bind("<Leave>", _leave)
            lb.bind("<Button-1>", _click)
            f.bind("<Button-1>", _click)

        # Content area
        self.content = tk.Frame(self, bg=BG_PRIMARY)
        self.content.pack(fill="both", expand=True)

    def _clear(self):
        """Clear content area"""
        for w in self.content.winfo_children():
            w.destroy()
            
    def _update_status(self, message, is_error=False):
        """Update status bar with message"""
        self.status_lbl.config(text=f"● {message}", fg=RED if is_error else GREEN)
        # Auto-revert after 5 seconds
        self.after(5000, lambda: self.status_lbl.config(text="● ONLINE", fg=GREEN))

    def _scroll_frame(self):
        """Returns an inner frame inside a scrollable canvas."""
        outer = tk.Frame(self.content, bg=BG_PRIMARY)
        outer.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(outer, bg=BG_PRIMARY, highlightthickness=1, highlightbackground=BORDER)
        sb = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        
        sb.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)
        
        inner = tk.Frame(canvas, bg=BG_PRIMARY)
        win = canvas.create_window((0, 0), window=inner, anchor="nw")
        
        def _configure_inner(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            
        def _configure_canvas(event):
            canvas.itemconfig(win, width=event.width)
            
        inner.bind("<Configure>", _configure_inner)
        canvas.bind("<Configure>", _configure_canvas)
        
        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        return inner

    # ─────────────────────────────────────────────────────────────────────────
    # DELETED RECORDS
    # ─────────────────────────────────────────────────────────────────────────
    def show_deleted_records(self):
        """Show all deleted records with option to restore"""
        self._clear()
        self.current_screen = "deleted_records"
        self.update_deleted_records()
        
        f = tk.Frame(self.content, bg=BG_PRIMARY)
        f.pack(fill="both", expand=True, padx=20, pady=16)

        tk.Label(f, text="📋  DELETED RECORDS", bg=BG_PRIMARY, fg=RED,
                 font=FH).pack(anchor="w", pady=(0, 16))

        if not recently_deleted:
            # No deleted records
            no_records = tk.Frame(f, bg=PANEL, padx=40, pady=40)
            no_records.pack(fill="both", expand=True)
            
            tk.Label(no_records, text="🗑️", bg=PANEL, fg=TEXT_MUTED,
                    font=("Segoe UI", 48)).pack(pady=20)
            tk.Label(no_records, text="No Deleted Records Found", bg=PANEL, fg=TEXT_MUTED,
                    font=FH).pack()
            tk.Label(no_records, text="Records you delete will appear here", bg=PANEL, fg=TEXT_MUTED,
                    font=FT).pack(pady=10)
            return

        # Header with count
        header = tk.Frame(f, bg=PANEL, padx=20, pady=10)
        header.pack(fill="x", pady=(0, 10))
        
        tk.Label(header, text=f"Found {len(recently_deleted)} deleted record(s)", 
                bg=PANEL, fg=SECONDARY, font=FB).pack(side="left")
        
        # Restore all button
        if len(recently_deleted) > 1:
            create_small_button(header, "🔄 Restore All", self._restore_all_deleted, GREEN, 15).pack(side="right")

        # Create scrollable area for deleted records
        canvas = tk.Canvas(f, bg=BG_PRIMARY, highlightthickness=0)
        scrollbar = ttk.Scrollbar(f, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BG_PRIMARY)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Display each deleted record
        for idx, (rec_type, rec_id, data) in enumerate(recently_deleted):
            # Card for each deleted record
            card = tk.Frame(scrollable_frame, bg=PANEL, padx=20, pady=15, 
                          highlightbackground=RED, highlightthickness=1)
            card.pack(fill="x", pady=5, padx=5)
            
            # Header with type and ID
            card_header = tk.Frame(card, bg=PANEL)
            card_header.pack(fill="x")
            
            tk.Label(card_header, text=f"{rec_type}: {rec_id}", bg=PANEL, fg=RED,
                    font=FB).pack(side="left")
            
            # Deleted date (simulated)
            tk.Label(card_header, text="Deleted: Recently", bg=PANEL, fg=TEXT_MUTED,
                    font=FS).pack(side="right")
            
            # Details based on type
            details = tk.Frame(card, bg=PANEL)
            details.pack(fill="x", pady=10)
            
            if rec_type == "Client":
                tk.Label(details, text=f"Name: {data['first']} {data['last']}", 
                        bg=PANEL, fg=TEXT_PRIMARY, font=FT).pack(anchor="w")
                tk.Label(details, text=f"Email: {data['email']}", 
                        bg=PANEL, fg=TEXT_PRIMARY, font=FT).pack(anchor="w")
                tk.Label(details, text=f"Phone: {data['phone']}", 
                        bg=PANEL, fg=TEXT_PRIMARY, font=FT).pack(anchor="w")
                
            elif rec_type == "Airline":
                tk.Label(details, text=f"Name: {data['name']}", 
                        bg=PANEL, fg=TEXT_PRIMARY, font=FT).pack(anchor="w")
                
            else:  # Flight
                airline_name = SAMPLE_DATA["airlines"].get(data["airline"], {}).get("name", "Unknown")
                tk.Label(details, text=f"Airline: {airline_name}", 
                        bg=PANEL, fg=TEXT_PRIMARY, font=FT).pack(anchor="w")
                tk.Label(details, text=f"Route: {data['origin']} → {data['destination']}", 
                        bg=PANEL, fg=TEXT_PRIMARY, font=FT).pack(anchor="w")
            
            # Restore button
            btn_row = tk.Frame(card, bg=PANEL)
            btn_row.pack(fill="x")
            
            def restore(rt=rec_type, rid=rec_id):
                self._restore_record(rt, rid)
                
            create_small_button(btn_row, "🔄 Restore", restore, GREEN, 12).pack(side="left", padx=5)
            
            # Permanent delete button
            def permanent_delete(rt=rec_type, rid=rec_id):
                self._permanent_delete(rt, rid)
                
            create_small_button(btn_row, "🗑️ Delete Permanently", permanent_delete, RED, 18).pack(side="left", padx=5)

    def _restore_record(self, rec_type, rec_id):
        """Restore a deleted record"""
        data_dict = None
        if rec_type == "Client":
            data_dict = SAMPLE_DATA["clients"]
        elif rec_type == "Airline":
            data_dict = SAMPLE_DATA["airlines"]
        else:  # Flight
            data_dict = SAMPLE_DATA["flights"]
            
        if rec_id in data_dict:
            data_dict[rec_id]["deleted"] = False
            self._update_status(f"✓ {rec_type} {rec_id} restored")
            
        self.update_deleted_records()
        self.show_deleted_records()

    def _restore_all_deleted(self):
        """Restore all deleted records"""
        for rec_type, rec_id, _ in recently_deleted:
            if rec_type == "Client":
                SAMPLE_DATA["clients"][rec_id]["deleted"] = False
            elif rec_type == "Airline":
                SAMPLE_DATA["airlines"][rec_id]["deleted"] = False
            else:
                SAMPLE_DATA["flights"][rec_id]["deleted"] = False
                
        self._update_status(f"✓ Restored {len(recently_deleted)} records")
        self.update_deleted_records()
        self.show_deleted_records()

    def _permanent_delete(self, rec_type, rec_id):
        """Permanently delete a record"""
        result = messagebox.askyesno(
            "Confirm Permanent Deletion",
            f"Are you sure you want to permanently delete {rec_type} {rec_id}?\n\nThis action CANNOT be undone!",
            icon='warning'
        )
        
        if result:
            if rec_type == "Client":
                del SAMPLE_DATA["clients"][rec_id]
            elif rec_type == "Airline":
                del SAMPLE_DATA["airlines"][rec_id]
            else:  # Flight
                del SAMPLE_DATA["flights"][rec_id]
                
            self._update_status(f"✓ {rec_type} {rec_id} permanently deleted")
            self.update_deleted_records()
            self.show_deleted_records()

    # ─────────────────────────────────────────────────────────────────────────
    # HOME
    # ─────────────────────────────────────────────────────────────────────────
    def show_home(self):
        self._clear()
        self.current_screen = "home"
        self.update_deleted_records()
        
        f = tk.Frame(self.content, bg=BG_PRIMARY)
        f.pack(expand=True, fill="both", padx=20, pady=20)

        # Welcome message with date
        today = date.today().strftime("%A, %B %d, %Y")
        tk.Label(f, text="WELCOME BACK", bg=BG_PRIMARY, fg=SECONDARY,
                 font=("Segoe UI", 28, "bold")).pack(pady=(30, 6))
        tk.Label(f, text=today, bg=BG_PRIMARY, fg=TEXT_PRIMARY,
                 font=FT2).pack(pady=(0, 6))
        tk.Label(f, text="Manage clients, airlines, and flights from the menu below.",
                 bg=BG_PRIMARY, fg=TEXT_SECONDARY, font=FT2).pack(pady=(0, 30))

        # Stats dashboard
        stats_frame = tk.Frame(f, bg=BG_PRIMARY)
        stats_frame.pack(pady=10)
        
        # Calculate active and deleted counts
        active_clients = sum(1 for c in SAMPLE_DATA["clients"].values() if not c.get("deleted", False))
        deleted_clients = sum(1 for c in SAMPLE_DATA["clients"].values() if c.get("deleted", False))
        active_airlines = sum(1 for a in SAMPLE_DATA["airlines"].values() if not a.get("deleted", False))
        deleted_airlines = sum(1 for a in SAMPLE_DATA["airlines"].values() if a.get("deleted", False))
        active_flights = sum(1 for f in SAMPLE_DATA["flights"].values() if not f.get("deleted", False))
        deleted_flights = sum(1 for f in SAMPLE_DATA["flights"].values() if f.get("deleted", False))
        
        # Stats cards
        stats = [
            ("CLIENTS", active_clients, deleted_clients, SECONDARY),
            ("AIRLINES", active_airlines, deleted_airlines, SECONDARY),
            ("FLIGHTS", active_flights, deleted_flights, SECONDARY),
        ]
        
        for label, active, deleted, color in stats:
            card = tk.Frame(stats_frame, bg=PANEL, padx=30, pady=20,
                          highlightbackground=BORDER, highlightthickness=1)
            card.pack(side="left", padx=10)
            
            tk.Label(card, text=label, bg=PANEL, fg=color,
                     font=FB).pack()
            tk.Label(card, text=str(active), bg=PANEL, fg=TEXT_PRIMARY,
                     font=("Segoe UI", 32, "bold")).pack()
            tk.Label(card, text=f"({deleted} deleted)", bg=PANEL, fg=RED,
                     font=FS).pack()

        # Quick actions
        tk.Label(f, text="QUICK ACTIONS", bg=BG_PRIMARY, fg=SECONDARY,
                 font=FB).pack(pady=(30, 15))
                 
        action_frame = tk.Frame(f, bg=BG_PRIMARY)
        action_frame.pack()
        
        create_rounded_button(action_frame, "➕ ADD CLIENT", self.show_create_client, SECONDARY, 18, 2).pack(side="left", padx=8)
        create_rounded_button(action_frame, "✈ ADD AIRLINE", self.show_create_airline, SECONDARY, 18, 2).pack(side="left", padx=8)
        create_rounded_button(action_frame, "🛫 ADD FLIGHT", self.show_create_flight, ACCENT, 18, 2).pack(side="left", padx=8)
        
        # Deleted records summary
        if recently_deleted:
            deleted_summary = tk.Frame(f, bg=PANEL, padx=20, pady=15,
                                     highlightbackground=RED, highlightthickness=1)
            deleted_summary.pack(fill="x", pady=30)
            
            tk.Label(deleted_summary, text=f"🗑️ {len(recently_deleted)} RECORDS IN TRASH", 
                    bg=PANEL, fg=RED, font=FB).pack(side="left")
            
            # Increased width to prevent truncation
            create_small_button(deleted_summary, "VIEW DELETED RECORDS", self.show_deleted_records, RED, 20).pack(side="right")

    # ─────────────────────────────────────────────────────────────────────────
    # CREATE MENU
    # ─────────────────────────────────────────────────────────────────────────
    def show_create_menu(self):
        self._clear()
        self.current_screen = "create_menu"
        
        f = tk.Frame(self.content, bg=BG_PRIMARY)
        f.pack(expand=True, fill="both", padx=20, pady=20)

        tk.Label(f, text="CREATE A RECORD", bg=BG_PRIMARY, fg=SECONDARY,
                 font=FH).pack(pady=(20, 8))
        tk.Label(f, text="Choose the record type to create:",
                 bg=BG_PRIMARY, fg=TEXT_PRIMARY, font=FT2).pack(pady=(0, 30))

        # Create cards for each type
        cards_frame = tk.Frame(f, bg=BG_PRIMARY)
        cards_frame.pack()

        for icon, label, desc, col, cmd in [
            ("👤", "CLIENT", "Add a new travel client", SECONDARY, self.show_create_client),
            ("✈", "AIRLINE", "Register a new airline company", SECONDARY, self.show_create_airline),
            ("🛫", "FLIGHT", "Create a new flight record", ACCENT, self.show_create_flight),
        ]:
            card = tk.Frame(cards_frame, bg=PANEL, padx=30, pady=20, cursor="hand2",
                          highlightbackground=BORDER, highlightthickness=1)
            card.pack(pady=10, fill="x")
            
            # Make entire card clickable
            for widget in [card]:
                widget.bind("<Button-1>", lambda e, c=cmd: c())
                
            row_ = tk.Frame(card, bg=PANEL)
            row_.pack()
            row_.bind("<Button-1>", lambda e, c=cmd: c())
            
            tk.Label(row_, text=icon, bg=PANEL, fg=col,
                     font=("Segoe UI", 32)).pack(side="left", padx=(0, 20))
            
            col_ = tk.Frame(row_, bg=PANEL)
            col_.pack(side="left", anchor="w")
            col_.bind("<Button-1>", lambda e, c=cmd: c())
            
            tk.Label(col_, text=label, bg=PANEL, fg=col,
                     font=FB).pack(anchor="w")
            tk.Label(col_, text=desc, bg=PANEL, fg=TEXT_SECONDARY,
                     font=FT).pack(anchor="w")
            
            # Hover effects
            def enter(e, c=card, color=col):
                c.config(bg=SECONDARY_LIGHT if color == SECONDARY else ACCENT_LIGHT)
            def leave(e, c=card, color=col):
                c.config(bg=PANEL)
                
            card.bind("<Enter>", enter)
            card.bind("<Leave>", leave)

        # Changed from BORDER to HOME_BTN
        create_rounded_button(f, "↩  RETURN TO HOME", self.show_home, HOME_BTN, 22, 2).pack(pady=30)

    # ─────────────────────────────────────────────────────────────────────────
    # CREATE CLIENT
    # ─────────────────────────────────────────────────────────────────────────
    def show_create_client(self):
        self._clear()
        self.current_screen = "create_client"
        inner = self._scroll_frame()

        # Header with next ID
        next_id = get_next_id("C", {k:v for k,v in SAMPLE_DATA["clients"].items() if not v.get("deleted", False)})
        
        hdr = tk.Frame(inner, bg=PANEL, padx=20, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="👤  NEW CLIENT RECORD", bg=PANEL, fg=SECONDARY,
                 font=FH).pack(side="left")
        tk.Label(hdr, text=f"ID: {next_id}", bg=PANEL, fg=TEXT_PRIMARY,
                 font=FB).pack(side="right")

        pnl = tk.Frame(inner, bg=PANEL, padx=32, pady=24)
        pnl.pack(padx=20, pady=12, fill="x")

        form = tk.Frame(pnl, bg=PANEL)
        form.pack(anchor="w")

        # Form fields with validation
        fields = {}
        error_labels = {}
        success_labels = {}

        def create_row(label_text, row, field_name, required=True, validator=None, maxlen=None):
            # Label
            tk.Label(form, text=label_text + (" *" if required else ""), 
                    bg=PANEL, fg=TEXT_SECONDARY, font=FT, width=18, anchor="e").grid(
                    row=row, column=0, padx=(0, 10), pady=8, sticky="e")
            
            # Entry with white background
            e = entry(form, 34)
            e.grid(row=row, column=1, padx=(0, 8), pady=8, sticky="w")
            
            # Error label
            err = err_lbl(form)
            err.grid(row=row, column=2, sticky="w", padx=(5,0))
            
            # Success label (for valid fields)
            succ = success_lbl(form)
            succ.grid(row=row, column=3, sticky="w", padx=(5,0))
            
            fields[field_name] = e
            error_labels[field_name] = err
            success_labels[field_name] = succ
            
            # Validation on key release
            if validator or maxlen:
                def validate(event=None, fname=field_name, vld=validator, ml=maxlen):
                    val = fields[fname].get()
                    err_lbl = error_labels[fname]
                    succ_lbl = success_labels[fname]
                    
                    # Clear previous messages
                    err_lbl.config(text="")
                    succ_lbl.config(text="")
                    
                    if ml and len(val) > ml:
                        fields[fname].delete(ml, tk.END)
                        err_lbl.config(text=f"⚠ MAX {ml} CHARACTERS")
                    elif vld and val and not vld(val):
                        err_lbl.config(text="⚠ INVALID FORMAT")
                    elif required and not val.strip():
                        err_lbl.config(text="⚠ REQUIRED")
                    else:
                        if val.strip():
                            succ_lbl.config(text="✓ VALID", fg=GREEN)
                            
                e.bind("<KeyRelease>", validate)
                
            return e, err

        # Create rows
        create_row("FIRST NAME", 0, "first", validator=lambda x: len(x.strip()) > 0)
        create_row("LAST NAME", 1, "last", validator=lambda x: len(x.strip()) > 0)
        create_row("EMAIL", 2, "email", validator=validate_email)
        create_row("PHONE", 3, "phone", validator=lambda x: True, maxlen=15)
        create_row("STREET ADDRESS", 4, "address", validator=lambda x: len(x.strip()) > 0)

        # Separator
        tk.Frame(pnl, bg=BORDER, height=1).pack(fill="x", pady=(15, 10))
        tk.Label(pnl, text="ADDRESS DETAILS", bg=PANEL, fg=SECONDARY,
                 font=FB).pack(anchor="w", pady=(0, 10))

        geo_frame = tk.Frame(pnl, bg=PANEL)
        geo_frame.pack(anchor="w")

        # Country
        tk.Label(geo_frame, text="COUNTRY *", bg=PANEL, fg=TEXT_SECONDARY,
                 font=FT, width=18, anchor="e").grid(row=0, column=0, padx=(0, 10), pady=8, sticky="e")
        country_cb = combo(geo_frame, list(GEOGRAPHY.keys()), 32)
        country_cb.grid(row=0, column=1, pady=8, sticky="w")
        country_err = err_lbl(geo_frame)
        country_err.grid(row=0, column=2, sticky="w", padx=(5,0))
        fields["country"] = country_cb
        error_labels["country"] = country_err

        # State
        tk.Label(geo_frame, text="STATE / REGION", bg=PANEL, fg=TEXT_SECONDARY,
                 font=FT, width=18, anchor="e").grid(row=1, column=0, padx=(0, 10), pady=8, sticky="e")
        state_cb = combo(geo_frame, [], 32)
        state_cb.grid(row=1, column=1, pady=8, sticky="w")
        fields["state"] = state_cb

        # City
        tk.Label(geo_frame, text="CITY *", bg=PANEL, fg=TEXT_SECONDARY,
                 font=FT, width=18, anchor="e").grid(row=2, column=0, padx=(0, 10), pady=8, sticky="e")
        city_cb = combo(geo_frame, [], 32)
        city_cb.grid(row=2, column=1, pady=8, sticky="w")
        city_err = err_lbl(geo_frame)
        city_err.grid(row=2, column=2, sticky="w", padx=(5,0))
        fields["city"] = city_cb
        error_labels["city"] = city_err

        # ZIP
        tk.Label(geo_frame, text="ZIP / POST CODE", bg=PANEL, fg=TEXT_SECONDARY,
                 font=FT, width=18, anchor="e").grid(row=3, column=0, padx=(0, 10), pady=8, sticky="e")
        zip_e = entry(geo_frame, 20)
        zip_e.grid(row=3, column=1, pady=8, sticky="w")
        fields["zip"] = zip_e

        # Cascade logic
        def on_country(event=None):
            c = country_cb.get()
            states = list(GEOGRAPHY.get(c, {}).keys())
            if states:
                state_cb.config(values=states, state="readonly")
                state_cb.set("")
                city_cb.config(values=[], state="disabled")
                city_cb.set("")
                country_err.config(text="")
            else:
                country_err.config(text="⚠ SELECT A COUNTRY")
                
        def on_state(event=None):
            cities = GEOGRAPHY.get(country_cb.get(), {}).get(state_cb.get(), [])
            if cities:
                city_cb.config(values=cities, state="readonly")
                city_cb.set("")
            else:
                city_cb.config(values=[], state="disabled")
                city_cb.set("")
                
        country_cb.bind("<<ComboboxSelected>>", on_country)
        state_cb.bind("<<ComboboxSelected>>", on_state)

        # Banner for overall status
        banner = tk.Label(pnl, text="", bg=PANEL, fg=RED,
                          font=FB, wraplength=500)
        banner.pack(pady=(15, 0))

        def validate_all():
            """Validate all fields before submit"""
            errors = []
            
            # Check required text fields
            for field in ["first", "last", "email", "phone", "address"]:
                if not fields[field].get().strip():
                    errors.append(field)
                    error_labels[field].config(text="⚠ REQUIRED")
                    
            # Check email format
            email = fields["email"].get().strip()
            if email and not validate_email(email):
                errors.append("email")
                error_labels["email"].config(text="⚠ INVALID EMAIL")
                
            # Check geography
            if not country_cb.get():
                errors.append("country")
                country_err.config(text="⚠ REQUIRED")
            if not city_cb.get():
                errors.append("city")
                city_err.config(text="⚠ REQUIRED")
                
            return len(errors) == 0

        def on_submit():
            if not validate_all():
                banner.config(text="⚠ PLEASE FIX THE ERRORS ABOVE")
                return
                
            # Show loading
            self.loading.show("SAVING CLIENT...")
            
            # Simulate network delay
            self.after(1000, lambda: save_client())
            
        def save_client():
            # Get next ID
            client_id = get_next_id("C", {k:v for k,v in SAMPLE_DATA["clients"].items() if not v.get("deleted", False)})
            
            # Save to "database"
            SAMPLE_DATA["clients"][client_id] = {
                "first": fields["first"].get().strip(),
                "last": fields["last"].get().strip(),
                "email": fields["email"].get().strip(),
                "phone": fields["phone"].get().strip(),
                "address": fields["address"].get().strip(),
                "country": country_cb.get(),
                "state": state_cb.get(),
                "city": city_cb.get(),
                "zip": zip_e.get().strip(),
                "deleted": False
            }
            
            self.loading.hide()
            self._update_status(f"✓ CLIENT {client_id} CREATED SUCCESSFULLY")
            
            # Show success screen with undo option
            self._success(
                "CLIENT ADDED SUCCESSFULLY!",
                f"Client {client_id} has been saved.",
                [
                    ("➕ ADD ANOTHER CLIENT", self.show_create_client),
                    ("↩ RETURN TO HOME", self.show_home),
                    ("↩ UNDO", lambda: self._undo_create("clients", client_id))
                ]
            )

        # Button row
        btnrow = tk.Frame(pnl, bg=PANEL)
        btnrow.pack(pady=20, anchor="w")
        
        create_rounded_button(btnrow, "✅  SUBMIT", on_submit, GREEN, 16, 2).pack(side="left", padx=(0, 10))
        
        def clear_form():
            for field in fields.values():
                if isinstance(field, tk.Entry):
                    field.delete(0, tk.END)
                elif isinstance(field, ttk.Combobox):
                    field.set("")
            for err in error_labels.values():
                err.config(text="")
            for succ in success_labels.values():
                succ.config(text="")
            banner.config(text="")
            
        create_rounded_button(btnrow, "✖  CLEAR FORM", clear_form, SECONDARY, 14, 2).pack(side="left", padx=(0, 10))
        create_rounded_button(btnrow, "↩  HOME", self.show_home, HOME_BTN, 12, 2).pack(side="left")

    # ─────────────────────────────────────────────────────────────────────────
    # CREATE AIRLINE
    # ─────────────────────────────────────────────────────────────────────────
    def show_create_airline(self):
        self._clear()
        self.current_screen = "create_airline"
        inner = self._scroll_frame()

        # Header with next ID
        next_id = get_next_id("A", {k:v for k,v in SAMPLE_DATA["airlines"].items() if not v.get("deleted", False)})
        
        hdr = tk.Frame(inner, bg=PANEL, padx=20, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="✈  NEW AIRLINE RECORD", bg=PANEL, fg=SECONDARY,
                 font=FH).pack(side="left")
        tk.Label(hdr, text=f"ID: {next_id}", bg=PANEL, fg=TEXT_PRIMARY,
                 font=FB).pack(side="right")

        pnl = tk.Frame(inner, bg=PANEL, padx=40, pady=30)
        pnl.pack(padx=20, pady=12, fill="x")

        # Airline name field
        tk.Label(pnl, text="COMPANY NAME *", bg=PANEL, fg=TEXT_SECONDARY, font=FT).pack(anchor="w", pady=(0,4))
        name_e = entry(pnl, 42)
        name_e.pack(anchor="w")
        name_err = err_lbl(pnl)
        name_err.pack(anchor="w", pady=(2,0))
        name_success = success_lbl(pnl)
        name_success.pack(anchor="w")

        # Check for duplicates in real-time
        def check_duplicate(event=None):
            name = name_e.get().strip()
            if not name:
                name_err.config(text="⚠ REQUIRED")
                name_success.config(text="")
                return
                
            # Check if name already exists (including deleted)
            exists = False
            similar = []
            for airline_id, data in SAMPLE_DATA["airlines"].items():
                if data["name"].lower() == name.lower() and not data.get("deleted", False):
                    exists = True
                elif name.lower() in data["name"].lower() or data["name"].lower() in name.lower():
                    if not data.get("deleted", False):
                        similar.append(data["name"])
                    
            if exists:
                name_err.config(text="⚠ AIRLINE ALREADY EXISTS!", fg=RED)
                name_success.config(text="")
            else:
                name_err.config(text="")
                name_success.config(text="✓ AVAILABLE", fg=GREEN)
                
        name_e.bind("<KeyRelease>", check_duplicate)

        banner = tk.Label(pnl, text="", bg=PANEL, fg=RED,
                          font=FB)
        banner.pack(pady=(10,0), anchor="w")

        def on_submit():
            name = name_e.get().strip()
            if not name:
                name_err.config(text="⚠ COMPANY NAME IS REQUIRED")
                banner.config(text="⚠ PLEASE FIX THE ERRORS ABOVE")
                return
                
            # Check for duplicates again
            exists = False
            similar = []
            for airline_id, data in SAMPLE_DATA["airlines"].items():
                if data["name"].lower() == name.lower() and not data.get("deleted", False):
                    exists = True
                elif name.lower() in data["name"].lower() or data["name"].lower() in name.lower():
                    if not data.get("deleted", False):
                        similar.append(data["name"])
                    
            if exists:
                self._duplicate_airline_dialog(name, similar[:3])
                return
                
            # Show loading
            self.loading.show("SAVING AIRLINE...")
            self.after(1000, lambda: save_airline(name))
            
        def save_airline(name):
            # Get next ID
            airline_id = get_next_id("A", {k:v for k,v in SAMPLE_DATA["airlines"].items() if not v.get("deleted", False)})
            
            # Save to "database"
            SAMPLE_DATA["airlines"][airline_id] = {"name": name, "deleted": False}
            
            self.loading.hide()
            self._update_status(f"✓ AIRLINE {airline_id} CREATED SUCCESSFULLY")
            
            self._success(
                "AIRLINE ADDED SUCCESSFULLY!",
                f"Airline '{name}' has been registered.",
                [
                    ("➕ ADD ANOTHER AIRLINE", self.show_create_airline),
                    ("↩ RETURN TO HOME", self.show_home),
                    ("↩ UNDO", lambda: self._undo_create("airlines", airline_id))
                ]
            )

        btnrow = tk.Frame(pnl, bg=PANEL)
        btnrow.pack(pady=20, anchor="w")
        
        create_rounded_button(btnrow, "✅  SUBMIT", on_submit, GREEN, 16, 2).pack(side="left", padx=(0, 10))
        
        def clear_form():
            name_e.delete(0, tk.END)
            name_err.config(text="")
            name_success.config(text="")
            banner.config(text="")
            
        create_rounded_button(btnrow, "✖  CLEAR FORM", clear_form, SECONDARY, 14, 2).pack(side="left", padx=(0, 10))
        create_rounded_button(btnrow, "↩  HOME", self.show_home, HOME_BTN, 12, 2).pack(side="left")
        
        name_e.focus()
        name_e.bind("<Return>", lambda e: on_submit())

    def _duplicate_airline_dialog(self, name, similar):
        dlg = tk.Toplevel(self)
        dlg.title("DUPLICATE FOUND")
        dlg.configure(bg=BG_PRIMARY)
        dlg.geometry("450x400")
        dlg.grab_set()
        
        # Center the dialog
        dlg.update_idletasks()
        x = (self.winfo_screenwidth() - 450) // 2
        y = (self.winfo_screenheight() - 400) // 2
        dlg.geometry(f"450x400+{x}+{y}")
        
        tk.Label(dlg, text="⚠  DUPLICATE NAME DETECTED", bg=BG_PRIMARY, fg=SECONDARY,
                 font=FH).pack(pady=(22,6))
        tk.Label(dlg, text=f"'{name}' may already exist in the system.",
                 bg=BG_PRIMARY, fg=TEXT_PRIMARY, font=FT).pack(pady=(0,5))
                 
        if similar:
            tk.Label(dlg, text="Did you mean one of these?",
                    bg=BG_PRIMARY, fg=ACCENT, font=FB).pack(pady=(5,5))
            lb = tk.Listbox(dlg, bg="white", fg=TEXT_PRIMARY, font=FT, height=len(similar),
                            relief="solid", highlightthickness=1,
                            highlightbackground=SECONDARY, selectbackground=SECONDARY_LIGHT,
                            selectforeground="white")
            for n in similar:
                lb.insert(tk.END, "  ✈ " + n)
            lb.pack(padx=30, fill="x", pady=5)
            
            # Double-click to select
            def on_select(event):
                if lb.curselection():
                    idx = lb.curselection()[0]
                    selected = similar[idx]
                    dlg.destroy()
                    self.show_update_airline_by_name(selected)
                    
            lb.bind("<Double-Button-1>", on_select)
        else:
            tk.Label(dlg, text="No similar names found.", bg=BG_PRIMARY, fg=TEXT_MUTED,
                    font=FT).pack(pady=10)
        
        # Options
        row_ = tk.Frame(dlg, bg=BG_PRIMARY)
        row_.pack(pady=16)
        
        create_rounded_button(row_, "CONTINUE WITH THIS NAME", 
            lambda: [dlg.destroy(), self._force_create_airline(name)],
            SECONDARY, 20, 2).pack(pady=4)
        create_rounded_button(row_, "TRY AGAIN", 
            lambda: [dlg.destroy(), self.show_create_airline()],
            ACCENT, 20, 2).pack(pady=4)
        create_rounded_button(row_, "CANCEL", 
            lambda: [dlg.destroy(), self.show_home()],
            HOME_BTN, 20, 2).pack(pady=4)
            
    def _force_create_airline(self, name):
        """Force create airline even if duplicate detected"""
        self.loading.show("SAVING AIRLINE...")
        self.after(1000, lambda: self._save_airline_force(name))
        
    def _save_airline_force(self, name):
        airline_id = get_next_id("A", {k:v for k,v in SAMPLE_DATA["airlines"].items() if not v.get("deleted", False)})
        SAMPLE_DATA["airlines"][airline_id] = {"name": name, "deleted": False}
        self.loading.hide()
        self._update_status(f"✓ AIRLINE {airline_id} CREATED (DUPLICATE OVERRIDE)")
        self._success(
            "AIRLINE ADDED!",
            f"Airline '{name}' has been registered (duplicate override).",
            [("➕ ADD ANOTHER AIRLINE", self.show_create_airline),
             ("↩ RETURN TO HOME", self.show_home)]
        )

    def show_update_airline_by_name(self, name):
        """Show update screen for a specific airline name"""
        # Find airline ID by name
        airline_id = None
        for aid, data in SAMPLE_DATA["airlines"].items():
            if data["name"] == name and not data.get("deleted", False):
                airline_id = aid
                break
                
        if airline_id:
            self.show_update_with_id("Airline", airline_id)
        else:
            self.show_update()

    # ─────────────────────────────────────────────────────────────────────────
    # CREATE FLIGHT
    # ─────────────────────────────────────────────────────────────────────────
    def show_create_flight(self):
        self._clear()
        self.current_screen = "create_flight"
        inner = self._scroll_frame()

        # Header with next ID
        next_id = get_next_id("F", {k:v for k,v in SAMPLE_DATA["flights"].items() if not v.get("deleted", False)})
        
        hdr = tk.Frame(inner, bg=PANEL, padx=20, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🛫  NEW FLIGHT RECORD", bg=PANEL, fg=ACCENT,
                 font=FH).pack(side="left")
        tk.Label(hdr, text=f"ID: {next_id}", bg=PANEL, fg=TEXT_PRIMARY,
                 font=FB).pack(side="right")

        pnl = tk.Frame(inner, bg=PANEL, padx=32, pady=24)
        pnl.pack(padx=20, pady=12, fill="x")
        
        form = tk.Frame(pnl, bg=PANEL)
        form.pack(anchor="w")

        def flbl(text, r):
            tk.Label(form, text=text, bg=PANEL, fg=TEXT_SECONDARY,
                     font=FT, width=20, anchor="e").grid(
                row=r, column=0, padx=(0, 10), pady=8, sticky="e")

        # Airline selection (only show active airlines)
        flbl("AIRLINE *", 0)
        airline_list = [f"{aid}  {data['name']}" for aid, data in SAMPLE_DATA["airlines"].items() 
                       if not data.get("deleted", False)]
        airline_cb = combo(form, airline_list, 36)
        airline_cb.grid(row=0, column=1, pady=8, sticky="w")
        a_err = err_lbl(form)
        a_err.grid(row=0, column=2, sticky="w", padx=(5,0))
        a_success = success_lbl(form)
        a_success.grid(row=0, column=3, sticky="w", padx=(5,0))

        # Date picker
        flbl("DEPARTURE DATE *", 1)
        date_var = tk.StringVar(value="CLICK TO SELECT DATE")
        date_btn = tk.Button(form, textvariable=date_var, bg="white", fg=TEXT_PRIMARY,
                             font=FB, relief="solid", cursor="hand2", anchor="w",
                             highlightthickness=1, highlightcolor=SECONDARY,
                             highlightbackground=BORDER, padx=10, pady=8, width=36,
                             activebackground=SECONDARY_LIGHT, activeforeground="white", bd=1)
        date_btn.grid(row=1, column=1, pady=8, sticky="w")
        d_err = err_lbl(form)
        d_err.grid(row=1, column=2, sticky="w", padx=(5,0))
        d_success = success_lbl(form)
        d_success.grid(row=1, column=3, sticky="w", padx=(5,0))
        
        picked_date = [None]
        def open_cal():
            CalendarPicker(self, lambda d: [
                picked_date.__setitem__(0, d),
                date_var.set(d.strftime("%A, %d %B %Y")),
                d_err.config(text=""),
                d_success.config(text="✓ SELECTED", fg=GREEN)
            ])
        date_btn.config(command=open_cal)

        # Time selection
        flbl("DEPARTURE TIME *", 2)
        time_cb = combo(form, TIMES, 16)
        time_cb.grid(row=2, column=1, pady=8, sticky="w")
        t_err = err_lbl(form)
        t_err.grid(row=2, column=2, sticky="w", padx=(5,0))
        t_success = success_lbl(form)
        t_success.grid(row=2, column=3, sticky="w", padx=(5,0))

        # Origin city
        flbl("ORIGIN CITY *", 3)
        origin_e = entry(form, 36)
        origin_e.grid(row=3, column=1, pady=8, sticky="w")
        o_err = err_lbl(form)
        o_err.grid(row=3, column=2, sticky="w", padx=(5,0))
        o_success = success_lbl(form)
        o_success.grid(row=3, column=3, sticky="w", padx=(5,0))

        # Destination city
        flbl("DESTINATION CITY *", 4)
        dest_e = entry(form, 36)
        dest_e.grid(row=4, column=1, pady=8, sticky="w")
        de_err = err_lbl(form)
        de_err.grid(row=4, column=2, sticky="w", padx=(5,0))
        de_success = success_lbl(form)
        de_success.grid(row=4, column=3, sticky="w", padx=(5,0))

        # Real-time validation
        def validate_cities(event=None):
            origin = origin_e.get().strip()
            dest = dest_e.get().strip()
            
            # Origin validation
            if not origin:
                o_err.config(text="⚠ REQUIRED")
                o_success.config(text="")
            else:
                o_err.config(text="")
                o_success.config(text="✓ VALID", fg=GREEN)
                
            # Destination validation
            if not dest:
                de_err.config(text="⚠ REQUIRED")
                de_success.config(text="")
            else:
                de_err.config(text="")
                de_success.config(text="✓ VALID", fg=GREEN)
                
            # Check if same
            if origin and dest and origin.lower() == dest.lower():
                de_err.config(text="⚠ CANNOT MATCH ORIGIN")
                de_success.config(text="")
                
        origin_e.bind("<KeyRelease>", validate_cities)
        dest_e.bind("<KeyRelease>", validate_cities)
        
        # Airline validation
        def validate_airline(event=None):
            if airline_cb.get():
                a_err.config(text="")
                a_success.config(text="✓ SELECTED", fg=GREEN)
            else:
                a_err.config(text="⚠ REQUIRED")
                a_success.config(text="")
        airline_cb.bind("<<ComboboxSelected>>", validate_airline)
        
        # Time validation
        def validate_time(event=None):
            if time_cb.get():
                t_err.config(text="")
                t_success.config(text="✓ SELECTED", fg=GREEN)
            else:
                t_err.config(text="⚠ REQUIRED")
                t_success.config(text="")
        time_cb.bind("<<ComboboxSelected>>", validate_time)

        banner = tk.Label(pnl, text="", bg=PANEL, fg=RED,
                          font=FB, wraplength=500)
        banner.pack(pady=(15,0), anchor="w")

        def validate_all():
            errors = []
            
            # Airline
            if not airline_cb.get():
                a_err.config(text="⚠ REQUIRED")
                errors.append("Airline")
                
            # Date
            if not picked_date[0]:
                d_err.config(text="⚠ REQUIRED")
                errors.append("Date")
                
            # Time
            if not time_cb.get():
                t_err.config(text="⚠ REQUIRED")
                errors.append("Time")
                
            # Origin
            origin = origin_e.get().strip()
            if not origin:
                o_err.config(text="⚠ REQUIRED")
                errors.append("Origin")
                
            # Destination
            dest = dest_e.get().strip()
            if not dest:
                de_err.config(text="⚠ REQUIRED")
                errors.append("Destination")
                
            # Same city check
            if origin and dest and origin.lower() == dest.lower():
                de_err.config(text="⚠ CANNOT MATCH ORIGIN")
                errors.append("Same cities")
                
            return len(errors) == 0

        def on_submit():
            if not validate_all():
                banner.config(text="⚠ PLEASE FIX THE ERRORS ABOVE")
                return
                
            self.loading.show("CREATING FLIGHT...")
            self.after(1000, lambda: save_flight())
            
        def save_flight():
            flight_id = get_next_id("F", {k:v for k,v in SAMPLE_DATA["flights"].items() if not v.get("deleted", False)})
            airline_selected = airline_cb.get().split("  ")[0]  # Get ID part
            
            SAMPLE_DATA["flights"][flight_id] = {
                "airline": airline_selected,
                "date": picked_date[0].isoformat(),
                "time": time_cb.get(),
                "origin": origin_e.get().strip(),
                "destination": dest_e.get().strip(),
                "deleted": False
            }
            
            self.loading.hide()
            self._update_status(f"✓ FLIGHT {flight_id} CREATED SUCCESSFULLY")
            
            self._success(
                "FLIGHT ADDED SUCCESSFULLY!",
                f"{origin_e.get().strip()} → {dest_e.get().strip()}",
                [
                    ("➕ ADD ANOTHER FLIGHT", self.show_create_flight),
                    ("↩ RETURN TO HOME", self.show_home),
                    ("↩ UNDO", lambda: self._undo_create("flights", flight_id))
                ]
            )

        btnrow = tk.Frame(pnl, bg=PANEL)
        btnrow.pack(pady=20, anchor="w")
        
        create_rounded_button(btnrow, "✅  SUBMIT", on_submit, GREEN, 16, 2).pack(side="left", padx=(0, 10))
        
        def clear_form():
            airline_cb.set("")
            time_cb.set("")
            origin_e.delete(0, tk.END)
            dest_e.delete(0, tk.END)
            date_var.set("CLICK TO SELECT DATE")
            picked_date[0] = None
            for err in [a_err, d_err, t_err, o_err, de_err]:
                err.config(text="")
            for succ in [a_success, d_success, t_success, o_success, de_success]:
                succ.config(text="")
            banner.config(text="")
            
        create_rounded_button(btnrow, "✖  CLEAR FORM", clear_form, SECONDARY, 14, 2).pack(side="left", padx=(0, 10))
        create_rounded_button(btnrow, "↩  HOME", self.show_home, HOME_BTN, 12, 2).pack(side="left")

    # ─────────────────────────────────────────────────────────────────────────
    # SEARCH
    # ─────────────────────────────────────────────────────────────────────────
    def show_search(self):
        self._clear()
        self.current_screen = "search"
        
        f = tk.Frame(self.content, bg=BG_PRIMARY)
        f.pack(fill="both", expand=True, padx=20, pady=16)

        tk.Label(f, text="🔍  SEARCH RECORDS", bg=BG_PRIMARY, fg=SECONDARY,
                 font=FH).pack(anchor="w", pady=(0,16))

        # Search controls
        ctrl = tk.Frame(f, bg=PANEL, padx=14, pady=10)
        ctrl.pack(fill="x")
        
        tk.Label(ctrl, text="TYPE:", bg=PANEL, fg=SECONDARY, font=FB).pack(side="left")
        type_cb = combo(ctrl, ["CLIENTS", "AIRLINES", "FLIGHTS"], 14)
        type_cb.set("CLIENTS")
        type_cb.pack(side="left", padx=8)
        
        tk.Label(ctrl, text="SEARCH:", bg=PANEL, fg=SECONDARY, font=FB).pack(side="left", padx=(12,0))
        search_e = entry(ctrl, 28)
        search_e.pack(side="left", padx=8)
        
        # Results count
        result_count = tk.Label(ctrl, text="", bg=PANEL, fg=GREEN, font=FB)
        result_count.pack(side="left", padx=10)

        # Action buttons for selected record
        action_frame = tk.Frame(f, bg=PANEL, padx=14, pady=10)
        action_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(action_frame, text="ACTIONS:", bg=PANEL, fg=SECONDARY, font=FB).pack(side="left", padx=(0, 10))
        
        # These will be enabled when a record is selected
        update_btn = create_small_button(action_frame, "✏️ UPDATE SELECTED", lambda: self._update_selected(), SECONDARY, 15)
        update_btn.pack(side="left", padx=5)
        update_btn.config(state="disabled")
        
        delete_btn = create_small_button(action_frame, "🗑️ DELETE SELECTED", lambda: self._delete_selected(), RED, 15)
        delete_btn.pack(side="left", padx=5)
        delete_btn.config(state="disabled")

        # Export button
        export_btn = create_small_button(action_frame, "📥 EXPORT RESULTS", self._show_export_dialog, ACCENT, 15)
        export_btn.pack(side="left", padx=5)

        # Include deleted checkbox
        show_deleted_var = tk.BooleanVar(value=False)
        show_deleted_cb = tk.Checkbutton(action_frame, text="SHOW DELETED RECORDS", 
                                        variable=show_deleted_var,
                                        bg=PANEL, fg=TEXT_PRIMARY, selectcolor=PANEL,
                                        font=FT, command=lambda: refresh_results())
        show_deleted_cb.pack(side="right", padx=10)

        # Table frame
        tbl_f = tk.Frame(f, bg=PANEL)
        tbl_f.pack(fill="both", expand=True, pady=10)

        # Treeview style
        style = ttk.Style()
        style.configure("Treeview", background="white", foreground=TEXT_PRIMARY,
                        rowheight=30, fieldbackground="white", font=FT)
        style.configure("Treeview.Heading", background=PANEL, foreground=SECONDARY,
                        font=FB, relief="solid")
        style.map("Treeview", background=[("selected", SECONDARY_LIGHT)], 
                  foreground=[("selected", "white")])

        # Treeview with scrollbars
        tree = ttk.Treeview(tbl_f, show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(tbl_f, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(tbl_f, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        tree.pack(fill="both", expand=True)

        # Store current selection
        current_selection = [None]

        def on_select(event):
            """Handle treeview selection"""
            selected = tree.selection()
            if selected:
                current_selection[0] = selected[0]
                update_btn.config(state="normal")
                delete_btn.config(state="normal")
            else:
                current_selection[0] = None
                update_btn.config(state="disabled")
                delete_btn.config(state="disabled")

        tree.bind("<<TreeviewSelect>>", on_select)

        # Define columns for each type
        columns = {
            "CLIENTS": ("ID", "FIRST NAME", "LAST NAME", "EMAIL", "PHONE", "COUNTRY", "CITY", "STATUS"),
            "AIRLINES": ("ID", "COMPANY NAME", "STATUS"),
            "FLIGHTS": ("ID", "AIRLINE", "DATE", "TIME", "FROM", "TO", "STATUS")
        }

        def refresh_results():
            """Refresh search results based on current filters"""
            # Clear existing items
            for row in tree.get_children():
                tree.delete(row)
                
            rtype = type_cb.get()
            query = search_e.get().strip().lower()
            show_deleted = show_deleted_var.get()
            
            # Set columns
            cols = columns.get(rtype, ())
            tree.config(columns=cols)
            for c in cols:
                tree.heading(c, text=c)
                # Adjust column widths
                if c == "ID":
                    width = 80
                elif c == "STATUS":
                    width = 80
                elif c in ["EMAIL", "COMPANY NAME"]:
                    width = 200
                else:
                    width = 120
                tree.column(c, width=width, anchor="w")
                
            # Get data based on type
            results = []
            if rtype == "CLIENTS":
                for cid, data in SAMPLE_DATA["clients"].items():
                    if not show_deleted and data.get("deleted", False):
                        continue
                    status = "DELETED" if data.get("deleted", False) else "ACTIVE"
                    row = (cid, data["first"], data["last"], data["email"], 
                          data["phone"], data["country"], data["city"], status)
                    if not query or any(query in str(v).lower() for v in row):
                        results.append((row, data.get("deleted", False)))
                        
            elif rtype == "AIRLINES":
                for aid, data in SAMPLE_DATA["airlines"].items():
                    if not show_deleted and data.get("deleted", False):
                        continue
                    status = "DELETED" if data.get("deleted", False) else "ACTIVE"
                    row = (aid, data["name"], status)
                    if not query or query in data["name"].lower():
                        results.append((row, data.get("deleted", False)))
                        
            else:  # FLIGHTS
                for fid, data in SAMPLE_DATA["flights"].items():
                    if not show_deleted and data.get("deleted", False):
                        continue
                    airline_name = SAMPLE_DATA["airlines"].get(data["airline"], {}).get("name", "Unknown")
                    status = "DELETED" if data.get("deleted", False) else "ACTIVE"
                    row = (fid, airline_name, data["date"], data["time"], 
                          data["origin"], data["destination"], status)
                    if not query or any(query in str(v).lower() for v in row):
                        results.append((row, data.get("deleted", False)))
                        
            # Insert results with color coding
            for row, is_deleted in results:
                item = tree.insert("", "end", values=row)
                if is_deleted:
                    tree.tag_configure('deleted', foreground=RED)
                    tree.item(item, tags=('deleted',))
                
            # Update count
            count = len(results)
            result_count.config(text=f"{count} RECORD(S) FOUND")

        # Search button and bindings
        create_small_button(ctrl, "🔍 SEARCH", refresh_results, SECONDARY, 12).pack(side="left", padx=4)
        type_cb.bind("<<ComboboxSelected>>", lambda e: refresh_results())
        search_e.bind("<Return>", lambda e: refresh_results())
        
        def _update_selected():
            """Update the selected record"""
            if not current_selection[0]:
                return
                
            item = current_selection[0]
            values = tree.item(item)["values"]
            if not values:
                return
                
            record_id = values[0]
            rtype = type_cb.get()[:-1]  # Remove 'S' from plural
            if rtype == "CLIENT":
                rtype = "Client"
            elif rtype == "AIRLINE":
                rtype = "Airline"
            else:
                rtype = "Flight"
            
            self.show_update_with_id(rtype, record_id)
            
        def _delete_selected():
            """Delete the selected record"""
            if not current_selection[0]:
                return
                
            item = current_selection[0]
            values = tree.item(item)["values"]
            if not values:
                return
                
            record_id = values[0]
            rtype = type_cb.get()[:-1]  # Remove 'S' from plural
            if rtype == "CLIENT":
                rtype = "Client"
            elif rtype == "AIRLINE":
                rtype = "Airline"
            else:
                rtype = "Flight"
            
            # Navigate to delete screen with ID pre-filled
            self.show_delete_with_id(rtype, record_id)
        
        # Double-click to edit
        def on_double_click(event):
            _update_selected()
            
        tree.bind("<Double-1>", on_double_click)
        
        # Initial search
        refresh_results()

    # ─────────────────────────────────────────────────────────────────────────
    # EXPORT DIALOG
    # ─────────────────────────────────────────────────────────────────────────
    def _show_export_dialog(self):
        """Show export options dialog with next actions"""
        dlg = tk.Toplevel(self)
        dlg.title("EXPORT DATA")
        dlg.configure(bg=BG_PRIMARY)
        dlg.geometry("500x500")
        dlg.grab_set()
        
        # Center the dialog
        dlg.update_idletasks()
        x = (self.winfo_screenwidth() - 500) // 2
        y = (self.winfo_screenheight() - 500) // 2
        dlg.geometry(f"500x500+{x}+{y}")
        
        # Header
        tk.Label(dlg, text="📥 EXPORT DATA", bg=BG_PRIMARY, fg=SECONDARY,
                 font=FH).pack(pady=(20, 10))
        
        # Format selection
        format_frame = tk.Frame(dlg, bg=PANEL, padx=20, pady=15)
        format_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(format_frame, text="SELECT EXPORT FORMAT:", bg=PANEL, fg=SECONDARY,
                font=FB).pack(anchor="w")
        
        format_var = tk.StringVar(value="json")
        
        formats = [
            ("JSON - Universal data format", "json"),
            ("CSV - Spreadsheet compatible", "csv"),
            ("SQLite - Database format", "sqlite")
        ]
        
        for text, value in formats:
            rb = tk.Radiobutton(format_frame, text=text, variable=format_var, value=value,
                               bg=PANEL, fg=TEXT_PRIMARY, selectcolor=PANEL, font=FT,
                               activebackground=PANEL, activeforeground=SECONDARY)
            rb.pack(anchor="w", pady=2)
        
        # Data selection
        data_frame = tk.Frame(dlg, bg=PANEL, padx=20, pady=15)
        data_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(data_frame, text="SELECT DATA TO EXPORT:", bg=PANEL, fg=SECONDARY,
                font=FB).pack(anchor="w")
        
        data_var = tk.StringVar(value="all")
        
        data_options = [
            ("ALL DATA (including deleted)", "all"),
            ("ACTIVE RECORDS ONLY", "active"),
            ("DELETED RECORDS ONLY", "deleted"),
            ("CURRENT SEARCH RESULTS", "current")
        ]
        
        for text, value in data_options:
            rb = tk.Radiobutton(data_frame, text=text, variable=data_var, value=value,
                               bg=PANEL, fg=TEXT_PRIMARY, selectcolor=PANEL, font=FT,
                               activebackground=PANEL, activeforeground=SECONDARY)
            rb.pack(anchor="w", pady=2)
        
        # Next actions frame
        next_frame = tk.Frame(dlg, bg=PANEL, padx=20, pady=15)
        next_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(next_frame, text="NEXT ACTIONS:", bg=PANEL, fg=SECONDARY,
                font=FB).pack(anchor="w")
        
        next_action_var = tk.StringVar(value="save")
        
        next_actions = [
            ("💾 SAVE TO FILE", "save"),
            ("📋 COPY TO CLIPBOARD", "clipboard"),
            ("📧 SEND AS EMAIL", "email"),
            ("🖨️ PRINT", "print")
        ]
        
        for text, value in next_actions:
            rb = tk.Radiobutton(next_frame, text=text, variable=next_action_var, value=value,
                               bg=PANEL, fg=TEXT_PRIMARY, selectcolor=PANEL, font=FT,
                               activebackground=PANEL, activeforeground=SECONDARY)
            rb.pack(anchor="w", pady=2)
        
        # Preview frame
        preview_frame = tk.Frame(dlg, bg=PANEL, padx=20, pady=10)
        preview_frame.pack(fill="x", padx=20, pady=5)
        
        preview_text = tk.Text(preview_frame, height=4, width=50, bg="white", fg=TEXT_PRIMARY,
                               font=FS, wrap="word", relief="solid", bd=1)
        preview_text.pack(fill="x")
        preview_text.insert("1.0", "Preview: Ready to export data...")
        preview_text.config(state="disabled")
        
        def update_preview(*args):
            """Update preview based on selections"""
            preview_text.config(state="normal")
            preview_text.delete("1.0", tk.END)
            
            format_type = format_var.get()
            data_option = data_var.get()
            next_action = next_action_var.get()
            
            preview = f"Export Format: {format_type.upper()}\n"
            preview += f"Data: {data_option.replace('_', ' ').upper()}\n"
            preview += f"Next Action: {next_action.upper()}\n"
            
            # Count records
            if data_option == "all":
                client_count = len(SAMPLE_DATA["clients"])
                airline_count = len(SAMPLE_DATA["airlines"])
                flight_count = len(SAMPLE_DATA["flights"])
            elif data_option == "active":
                client_count = sum(1 for c in SAMPLE_DATA["clients"].values() if not c.get("deleted", False))
                airline_count = sum(1 for a in SAMPLE_DATA["airlines"].values() if not a.get("deleted", False))
                flight_count = sum(1 for f in SAMPLE_DATA["flights"].values() if not f.get("deleted", False))
            elif data_option == "deleted":
                client_count = sum(1 for c in SAMPLE_DATA["clients"].values() if c.get("deleted", False))
                airline_count = sum(1 for a in SAMPLE_DATA["airlines"].values() if a.get("deleted", False))
                flight_count = sum(1 for f in SAMPLE_DATA["flights"].values() if f.get("deleted", False))
            else:  # current
                client_count = len(SAMPLE_DATA["clients"])
                airline_count = len(SAMPLE_DATA["airlines"])
                flight_count = len(SAMPLE_DATA["flights"])
            
            preview += f"\nRecords to export:\n"
            preview += f"• Clients: {client_count}\n"
            preview += f"• Airlines: {airline_count}\n"
            preview += f"• Flights: {flight_count}"
            
            preview_text.insert("1.0", preview)
            preview_text.config(state="disabled")
        
        # Bind updates
        format_var.trace('w', update_preview)
        data_var.trace('w', update_preview)
        next_action_var.trace('w', update_preview)
        
        # Initial preview
        update_preview()
        
        def do_export():
            """Execute export based on selections"""
            format_type = format_var.get()
            data_option = data_var.get()
            next_action = next_action_var.get()
            
            # Close dialog
            dlg.destroy()
            
            # Handle next actions
            if next_action == "save":
                # Get filename from user
                if format_type == "json":
                    filetypes = [("JSON files", "*.json")]
                    def_ext = ".json"
                elif format_type == "csv":
                    filetypes = [("CSV files", "*.csv")]
                    def_ext = ".csv"
                else:  # sqlite
                    filetypes = [("SQLite files", "*.db")]
                    def_ext = ".db"
                    
                filename = filedialog.asksaveasfilename(
                    defaultextension=def_ext,
                    filetypes=filetypes,
                    title="Save export as..."
                )
                
                if not filename:
                    return
                    
                self.loading.show("EXPORTING DATA...")
                self.after(500, lambda: self._perform_export(format_type, data_option, filename, next_action))
                
            elif next_action == "clipboard":
                self.loading.show("PREPARING DATA FOR CLIPBOARD...")
                self.after(500, lambda: self._copy_to_clipboard(format_type, data_option))
                
            elif next_action == "email":
                self._show_email_dialog(format_type, data_option)
                
            else:  # print
                self.loading.show("PREPARING PRINT PREVIEW...")
                self.after(500, lambda: self._print_preview(format_type, data_option))
        
        # Buttons
        btn_frame = tk.Frame(dlg, bg=BG_PRIMARY)
        btn_frame.pack(pady=20)
        
        create_rounded_button(btn_frame, "EXPORT NOW", do_export, GREEN, 15, 2).pack(side="left", padx=5)
        create_rounded_button(btn_frame, "CANCEL", dlg.destroy, HOME_BTN, 15, 2).pack(side="left", padx=5)

    def _perform_export(self, format_type, data_option, filename, next_action):
        """Perform the actual export"""
        try:
            # Prepare data based on option
            if data_option == "all":
                export_data = {
                    "clients": SAMPLE_DATA["clients"],
                    "airlines": SAMPLE_DATA["airlines"],
                    "flights": SAMPLE_DATA["flights"]
                }
            elif data_option == "active":
                export_data = {
                    "clients": {k:v for k,v in SAMPLE_DATA["clients"].items() if not v.get("deleted", False)},
                    "airlines": {k:v for k,v in SAMPLE_DATA["airlines"].items() if not v.get("deleted", False)},
                    "flights": {k:v for k,v in SAMPLE_DATA["flights"].items() if not v.get("deleted", False)}
                }
            elif data_option == "deleted":
                export_data = {
                    "clients": {k:v for k,v in SAMPLE_DATA["clients"].items() if v.get("deleted", False)},
                    "airlines": {k:v for k,v in SAMPLE_DATA["airlines"].items() if v.get("deleted", False)},
                    "flights": {k:v for k,v in SAMPLE_DATA["flights"].items() if v.get("deleted", False)}
                }
            else:  # current - export all for simplicity in this demo
                export_data = {
                    "clients": SAMPLE_DATA["clients"],
                    "airlines": SAMPLE_DATA["airlines"],
                    "flights": SAMPLE_DATA["flights"]
                }
            
            success = False
            
            if format_type == "json":
                # Export all data to one JSON file
                success = export_to_json(export_data, filename)
                
            elif format_type == "csv":
                # Export each type to separate CSV files
                base = filename.rsplit('.', 1)[0]
                success1 = export_to_csv(export_data["clients"], f"{base}_clients.csv", "clients")
                success2 = export_to_csv(export_data["airlines"], f"{base}_airlines.csv", "airlines")
                success3 = export_to_csv(export_data["flights"], f"{base}_flights.csv", "flights")
                success = success1 and success2 and success3
                
            else:  # sqlite
                # Export all to one SQLite database
                conn = sqlite3.connect(filename)
                cursor = conn.cursor()
                
                # Export clients
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS clients (
                        id TEXT PRIMARY KEY,
                        first_name TEXT,
                        last_name TEXT,
                        email TEXT,
                        phone TEXT,
                        address TEXT,
                        country TEXT,
                        state TEXT,
                        city TEXT,
                        zip TEXT,
                        status TEXT
                    )
                ''')
                for cid, info in export_data["clients"].items():
                    status = "DELETED" if info.get("deleted", False) else "ACTIVE"
                    cursor.execute('''
                        INSERT OR REPLACE INTO clients 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (cid, info["first"], info["last"], info["email"], info["phone"],
                          info["address"], info["country"], info.get("state", ""), 
                          info["city"], info.get("zip", ""), status))
                
                # Export airlines
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS airlines (
                        id TEXT PRIMARY KEY,
                        name TEXT,
                        status TEXT
                    )
                ''')
                for aid, info in export_data["airlines"].items():
                    status = "DELETED" if info.get("deleted", False) else "ACTIVE"
                    cursor.execute('INSERT OR REPLACE INTO airlines VALUES (?, ?, ?)',
                                 (aid, info["name"], status))
                
                # Export flights
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS flights (
                        id TEXT PRIMARY KEY,
                        airline_id TEXT,
                        airline_name TEXT,
                        date TEXT,
                        time TEXT,
                        origin TEXT,
                        destination TEXT,
                        status TEXT
                    )
                ''')
                for fid, info in export_data["flights"].items():
                    airline_name = SAMPLE_DATA["airlines"].get(info["airline"], {}).get("name", "Unknown")
                    status = "DELETED" if info.get("deleted", False) else "ACTIVE"
                    cursor.execute('''
                        INSERT OR REPLACE INTO flights 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (fid, info["airline"], airline_name, info["date"], info["time"],
                          info["origin"], info["destination"], status))
                
                conn.commit()
                conn.close()
                success = True
            
            self.loading.hide()
            
            if success:
                self._update_status(f"✓ DATA EXPORTED SUCCESSFULLY TO {os.path.basename(filename)}")
                
                # Show success message with option to open folder
                result = messagebox.askyesno(
                    "EXPORT SUCCESSFUL",
                    f"Data has been exported successfully to:\n{filename}\n\nDo you want to open the containing folder?",
                    icon='info'
                )
                
                if result:
                    # Open containing folder
                    folder = os.path.dirname(filename)
                    if os.name == 'nt':  # Windows
                        os.startfile(folder)
                    else:  # Mac/Linux
                        import subprocess
                        subprocess.Popen(['open', folder])
            else:
                self._update_status("✗ EXPORT FAILED", is_error=True)
                messagebox.showerror("EXPORT FAILED", "Failed to export data. Please check permissions and try again.")
                
        except Exception as e:
            self.loading.hide()
            self._update_status(f"✗ EXPORT FAILED: {str(e)}", is_error=True)
            messagebox.showerror("EXPORT FAILED", f"Error exporting data:\n{str(e)}")

    def _copy_to_clipboard(self, format_type, data_option):
        """Copy export data to clipboard"""
        try:
            # Prepare data
            if data_option == "all":
                export_data = SAMPLE_DATA
            elif data_option == "active":
                export_data = {
                    "clients": {k:v for k,v in SAMPLE_DATA["clients"].items() if not v.get("deleted", False)},
                    "airlines": {k:v for k,v in SAMPLE_DATA["airlines"].items() if not v.get("deleted", False)},
                    "flights": {k:v for k,v in SAMPLE_DATA["flights"].items() if not v.get("deleted", False)}
                }
            else:
                export_data = {
                    "clients": {k:v for k,v in SAMPLE_DATA["clients"].items() if v.get("deleted", False)},
                    "airlines": {k:v for k,v in SAMPLE_DATA["airlines"].items() if v.get("deleted", False)},
                    "flights": {k:v for k,v in SAMPLE_DATA["flights"].items() if v.get("deleted", False)}
                }
            
            # Convert to string
            if format_type == "json":
                data_str = json.dumps(export_data, indent=2)
            else:
                # Simple representation for other formats
                data_str = str(export_data)
            
            # Copy to clipboard
            self.clipboard_clear()
            self.clipboard_append(data_str)
            
            self.loading.hide()
            self._update_status("✓ DATA COPIED TO CLIPBOARD")
            
            messagebox.showinfo("COPY SUCCESSFUL", 
                               "Data has been copied to clipboard.\n\nYou can now paste it anywhere (Ctrl+V).")
            
        except Exception as e:
            self.loading.hide()
            self._update_status(f"✗ COPY FAILED: {str(e)}", is_error=True)

    def _show_email_dialog(self, format_type, data_option):
        """Show email dialog"""
        dlg = tk.Toplevel(self)
        dlg.title("SEND AS EMAIL")
        dlg.configure(bg=BG_PRIMARY)
        dlg.geometry("400x300")
        dlg.grab_set()
        
        # Center the dialog
        dlg.update_idletasks()
        x = (self.winfo_screenwidth() - 400) // 2
        y = (self.winfo_screenheight() - 300) // 2
        dlg.geometry(f"400x300+{x}+{y}")
        
        tk.Label(dlg, text="📧 SEND AS EMAIL", bg=BG_PRIMARY, fg=SECONDARY,
                font=FH).pack(pady=(20, 15))
        
        tk.Label(dlg, text="Email Address:", bg=BG_PRIMARY, fg=TEXT_PRIMARY,
                font=FB).pack(anchor="w", padx=20)
        
        email_e = entry(dlg, 30)
        email_e.pack(padx=20, pady=5, fill="x")
        email_e.insert(0, "user@example.com")
        
        tk.Label(dlg, text="Subject:", bg=BG_PRIMARY, fg=TEXT_PRIMARY,
                font=FB).pack(anchor="w", padx=20, pady=(10,0))
        
        subject_e = entry(dlg, 30)
        subject_e.pack(padx=20, pady=5, fill="x")
        subject_e.insert(0, "Exported Data from Travel Agent System")
        
        def send_email():
            email = email_e.get().strip()
            if not validate_email(email):
                messagebox.showerror("INVALID EMAIL", "Please enter a valid email address.")
                return
            
            self.loading.show("SENDING EMAIL...")
            self.after(2000, lambda: self._email_sent(dlg))
        
        btn_frame = tk.Frame(dlg, bg=BG_PRIMARY)
        btn_frame.pack(pady=20)
        
        create_rounded_button(btn_frame, "SEND", send_email, GREEN, 15, 2).pack(side="left", padx=5)
        create_rounded_button(btn_frame, "CANCEL", dlg.destroy, HOME_BTN, 15, 2).pack(side="left", padx=5)

    def _email_sent(self, dlg):
        """Handle email sent"""
        dlg.destroy()
        self.loading.hide()
        self._update_status("✓ EMAIL SENT SUCCESSFULLY")
        messagebox.showinfo("EMAIL SENT", "The data has been sent via email (simulated).")

    def _print_preview(self, format_type, data_option):
        """Show print preview"""
        self.loading.hide()
        
        # Create print preview window
        preview = tk.Toplevel(self)
        preview.title("PRINT PREVIEW")
        preview.configure(bg=BG_PRIMARY)
        preview.geometry("600x400")
        
        # Center the window
        preview.update_idletasks()
        x = (self.winfo_screenwidth() - 600) // 2
        y = (self.winfo_screenheight() - 400) // 2
        preview.geometry(f"600x400+{x}+{y}")
        
        tk.Label(preview, text="🖨️ PRINT PREVIEW", bg=BG_PRIMARY, fg=SECONDARY,
                font=FH).pack(pady=(15, 10))
        
        # Text widget for preview
        text_frame = tk.Frame(preview, bg=PANEL, padx=10, pady=10)
        text_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        text_widget = tk.Text(text_frame, bg="white", fg=TEXT_PRIMARY,
                             font=("Courier New", 10), wrap="word")
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        text_widget.pack(side="left", fill="both", expand=True)
        
        # Add content
        text_widget.insert("1.0", "="*60 + "\n")
        text_widget.insert("end", "TRAVEL AGENT RECORD MANAGEMENT SYSTEM\n")
        text_widget.insert("end", f"Export Date: {date.today().strftime('%B %d, %Y')}\n")
        text_widget.insert("end", f"Data Type: {data_option.upper()}\n")
        text_widget.insert("end", "="*60 + "\n\n")
        
        # Add counts
        if data_option == "all" or data_option == "active" or data_option == "deleted":
            if data_option == "all" or data_option == "active":
                client_count = sum(1 for c in SAMPLE_DATA["clients"].values() if not c.get("deleted", False))
                airline_count = sum(1 for a in SAMPLE_DATA["airlines"].values() if not a.get("deleted", False))
                flight_count = sum(1 for f in SAMPLE_DATA["flights"].values() if not f.get("deleted", False))
            else:
                client_count = sum(1 for c in SAMPLE_DATA["clients"].values() if c.get("deleted", False))
                airline_count = sum(1 for a in SAMPLE_DATA["airlines"].values() if a.get("deleted", False))
                flight_count = sum(1 for f in SAMPLE_DATA["flights"].values() if f.get("deleted", False))
            
            text_widget.insert("end", f"Clients: {client_count}\n")
            text_widget.insert("end", f"Airlines: {airline_count}\n")
            text_widget.insert("end", f"Flights: {flight_count}\n")
        
        text_widget.config(state="disabled")
        
        # Print button
        def do_print():
            self._update_status("✓ SENT TO PRINTER (SIMULATED)")
            preview.destroy()
            messagebox.showinfo("PRINT", "Document sent to printer (simulated).")
        
        btn_frame = tk.Frame(preview, bg=BG_PRIMARY)
        btn_frame.pack(pady=10)
        
        create_rounded_button(btn_frame, "🖨️ PRINT", do_print, GREEN, 15, 2).pack(side="left", padx=5)
        create_rounded_button(btn_frame, "CANCEL", preview.destroy, HOME_BTN, 15, 2).pack(side="left", padx=5)

    # ─────────────────────────────────────────────────────────────────────────
    # UPDATE
    # ─────────────────────────────────────────────────────────────────────────
    def show_update(self):
        self._clear()
        self.current_screen = "update"
        
        inner = self._scroll_frame()

        tk.Label(inner, text="✏️  UPDATE RECORD", bg=BG_PRIMARY, fg=SECONDARY,
                 font=FH).pack(anchor="w", padx=20, pady=(16,10))

        # Search controls
        ctrl = tk.Frame(inner, bg=PANEL, padx=14, pady=10)
        ctrl.pack(fill="x", padx=20)
        
        tk.Label(ctrl, text="TYPE:", bg=PANEL, fg=SECONDARY, font=FB).pack(side="left")
        type_cb = combo(ctrl, ["CLIENT", "AIRLINE", "FLIGHT"], 12)
        type_cb.set("CLIENT")
        type_cb.pack(side="left", padx=8)
        
        tk.Label(ctrl, text="ID:", bg=PANEL, fg=SECONDARY, font=FB).pack(side="left", padx=(12,0))
        
        # ID entry with auto-formatting
        id_frame = tk.Frame(ctrl, bg=PANEL)
        id_frame.pack(side="left", padx=8)
        
        # Prefix label that changes based on type
        prefix_var = tk.StringVar(value="C-")
        prefix_lbl = tk.Label(id_frame, textvariable=prefix_var, bg=PANEL, fg=SECONDARY, font=FB)
        prefix_lbl.pack(side="left")
        
        id_e = entry(id_frame, 8)
        id_e.pack(side="left")
        
        # Update prefix when type changes
        def update_prefix(event=None):
            prefixes = {"CLIENT": "C-", "AIRLINE": "A-", "FLIGHT": "F-"}
            prefix_var.set(prefixes[type_cb.get()])
            id_e.focus()
            
        type_cb.bind("<<ComboboxSelected>>", update_prefix)
        
        # Quick tips
        tips = tk.Label(ctrl, text="(ENTER NUMBER ONLY, e.g., 0001)", 
                       bg=PANEL, fg=TEXT_MUTED, font=FS)
        tips.pack(side="left", padx=10)

        # Detail panel
        detail = tk.Frame(inner, bg=PANEL, padx=28, pady=18)
        detail.pack(fill="x", padx=20, pady=10)
        
        self.current_update_frame = detail
        self.current_update_type = None
        self.current_update_id = None

        def load_record():
            # Clear detail panel
            for w in detail.winfo_children():
                w.destroy()
                
            record_type = type_cb.get()
            id_number = id_e.get().strip()
            
            if not id_number:
                tk.Label(detail, text="⚠ PLEASE ENTER AN ID NUMBER", bg=PANEL, 
                        fg=RED, font=FB).pack(pady=20)
                return
                
            # Format ID with prefix
            prefixes = {"CLIENT": "C-", "AIRLINE": "A-", "FLIGHT": "F-"}
            prefix = prefixes[record_type]
            
            # Pad with zeros to 4 digits
            padded_num = id_number.zfill(4)
            record_id = f"{prefix}{padded_num}"
                
            # Show loading
            loading_lbl = tk.Label(detail, text="⏳ LOADING...", bg=PANEL, 
                                  fg=SECONDARY, font=FB)
            loading_lbl.pack(pady=20)
            detail.update()
            
            # Simulate load delay
            self.after(500, lambda: display_record(record_type, record_id, loading_lbl))
            
        def display_record(record_type, record_id, loading_lbl):
            loading_lbl.destroy()
            
            # Map record type to data type
            data_type = {"CLIENT": "clients", "AIRLINE": "airlines", "FLIGHT": "flights"}[record_type]
            
            # Get data
            data = SAMPLE_DATA[data_type].get(record_id)
            
            if not data:
                tk.Label(detail, text=f"❌ {record_type} {record_id} NOT FOUND", 
                        bg=PANEL, fg=RED, font=FB).pack(pady=20)
                return
            
            # Check if deleted
            if data.get("deleted", False):
                tk.Label(detail, text=f"⚠ {record_type} {record_id} IS DELETED", 
                        bg=PANEL, fg=RED, font=FB).pack(pady=10)
                tk.Label(detail, text="Deleted records cannot be edited. Restore them from the Deleted Records section.",
                        bg=PANEL, fg=TEXT_MUTED, font=FT).pack()
                return
            
            # Display header with record ID
            header = tk.Frame(detail, bg=PANEL)
            header.pack(fill="x", pady=(0, 15))
            
            # Color based on type
            colors = {"CLIENT": SECONDARY, "AIRLINE": SECONDARY, "FLIGHT": ACCENT}
            color = colors[record_type]
            
            tk.Label(header, text=f"✏️ EDITING {record_type}: {record_id}", 
                    bg=PANEL, fg=color, font=FB).pack(side="left")
            
            # Display appropriate form
            if record_type == "CLIENT":
                self._display_client_update(detail, record_id, data)
            elif record_type == "AIRLINE":
                self._display_airline_update(detail, record_id, data)
            else:  # FLIGHT
                self._display_flight_update(detail, record_id, data)

        create_small_button(ctrl, "📂 LOAD", load_record, SECONDARY, 12).pack(side="left", padx=4)
        id_e.bind("<Return>", lambda e: load_record())
        
        # Set initial focus
        id_e.focus()

    def show_update_with_id(self, record_type, record_id):
        """Directly show update screen for a specific record"""
        self.show_update()
        
        # Small delay to let UI initialize
        self.after(100, lambda: self._load_specific_record(record_type, record_id))
        
    def _load_specific_record(self, record_type, record_id):
        """Load a specific record in the update screen"""
        # Find the type combobox and set it
        for widget in self.content.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        for cb in child.winfo_children():
                            if isinstance(cb, ttk.Combobox) and cb.cget("values"):
                                if record_type.upper() in ["CLIENT", "AIRLINE", "FLIGHT"]:
                                    cb.set(record_type.upper())
                                break
                                
        # Extract number from ID (remove prefix)
        id_number = record_id.split('-')[1].lstrip('0') or '0'
        
        # Find ID entry and set it
        for widget in self.content.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        # Look for the ID entry in the nested frames
                        for frame in child.winfo_children():
                            if isinstance(frame, tk.Frame):
                                for entry_widget in frame.winfo_children():
                                    if isinstance(entry_widget, tk.Entry):
                                        entry_widget.delete(0, tk.END)
                                        entry_widget.insert(0, id_number)
                                        # Trigger load
                                        self.after(200, lambda: self._trigger_load())
                                        return

    def show_delete_with_id(self, record_type, record_id):
        """Show delete screen with ID pre-filled"""
        self.show_delete()
        
        # Small delay to let UI initialize
        self.after(100, lambda: self._load_delete_specific(record_type, record_id))
        
    def _load_delete_specific(self, record_type, record_id):
        """Load a specific record in the delete screen"""
        # Find the type combobox and set it
        for widget in self.content.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        for cb in child.winfo_children():
                            if isinstance(cb, ttk.Combobox) and cb.cget("values"):
                                if record_type.upper() in ["CLIENT", "AIRLINE", "FLIGHT"]:
                                    cb.set(record_type.upper())
                                break
                                
        # Extract number from ID (remove prefix)
        id_number = record_id.split('-')[1].lstrip('0') or '0'
        
        # Find ID entry and set it
        for widget in self.content.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        # Look for the ID entry
                        for entry_widget in child.winfo_children():
                            if isinstance(entry_widget, tk.Entry):
                                entry_widget.delete(0, tk.END)
                                entry_widget.insert(0, id_number)
                                # Trigger load
                                self.after(200, lambda: self._trigger_delete_load())
                                return
                                
    def _trigger_load(self):
        """Trigger the load button click in update screen"""
        for widget in self.content.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        for btn_widget in child.winfo_children():
                            if isinstance(btn_widget, tk.Button) and "LOAD" in btn_widget.cget("text"):
                                btn_widget.invoke()
                                return
                                
    def _trigger_delete_load(self):
        """Trigger the load button click in delete screen"""
        for widget in self.content.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        for btn_widget in child.winfo_children():
                            if isinstance(btn_widget, tk.Button) and "LOAD" in btn_widget.cget("text"):
                                btn_widget.invoke()
                                return

    def _display_client_update(self, parent, record_id, data):
        """Display client update form with editable fields"""
        # Create form in a scrollable frame within parent
        form = tk.Frame(parent, bg=PANEL)
        form.pack(fill="both", expand=True)
        
        fields = {}
        row = 0
        
        # Personal Information Section
        tk.Label(form, text="PERSONAL INFORMATION", bg=PANEL, fg=SECONDARY,
                font=FB).grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 10))
        row += 1
        
        for label, key in [("FIRST NAME:", "first"), ("LAST NAME:", "last"),
                          ("EMAIL:", "email"), ("PHONE:", "phone")]:
            tk.Label(form, text=label, bg=PANEL, fg=TEXT_SECONDARY,
                    font=FT, width=15, anchor="e").grid(
                row=row, column=0, padx=(0,10), pady=8, sticky="e")
                
            e = entry(form, 36)
            e.insert(0, data[key])
            e.grid(row=row, column=1, pady=8, sticky="w")
            fields[key] = e
            row += 1
        
        # Address Section
        tk.Label(form, text="ADDRESS INFORMATION", bg=PANEL, fg=SECONDARY,
                font=FB).grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 10))
        row += 1
        
        tk.Label(form, text="STREET:", bg=PANEL, fg=TEXT_SECONDARY,
                font=FT, width=15, anchor="e").grid(
            row=row, column=0, padx=(0,10), pady=8, sticky="e")
        addr_e = entry(form, 36)
        addr_e.insert(0, data["address"])
        addr_e.grid(row=row, column=1, pady=8, sticky="w")
        fields["address"] = addr_e
        row += 1
        
        # Country
        tk.Label(form, text="COUNTRY:", bg=PANEL, fg=TEXT_SECONDARY,
                font=FT, width=15, anchor="e").grid(
            row=row, column=0, padx=(0,10), pady=8, sticky="e")
        country_lbl = tk.Label(form, text=data["country"], bg="white", fg=TEXT_PRIMARY,
                              font=FT, relief="solid", padx=5, pady=3,
                              highlightthickness=1, highlightbackground=BORDER, width=30)
        country_lbl.grid(row=row, column=1, sticky="w")
        row += 1
        
        # State
        tk.Label(form, text="STATE:", bg=PANEL, fg=TEXT_SECONDARY,
                font=FT, width=15, anchor="e").grid(
            row=row, column=0, padx=(0,10), pady=8, sticky="e")
        if data.get("state"):
            state_lbl = tk.Label(form, text=data["state"], bg="white", fg=TEXT_PRIMARY,
                                font=FT, relief="solid", padx=5, pady=3,
                                highlightthickness=1, highlightbackground=BORDER, width=30)
        else:
            state_lbl = tk.Label(form, text="—", bg=PANEL, fg=TEXT_MUTED, font=FT)
        state_lbl.grid(row=row, column=1, sticky="w")
        row += 1
        
        # City
        tk.Label(form, text="CITY:", bg=PANEL, fg=TEXT_SECONDARY,
                font=FT, width=15, anchor="e").grid(
            row=row, column=0, padx=(0,10), pady=8, sticky="e")
        city_lbl = tk.Label(form, text=data["city"], bg="white", fg=TEXT_PRIMARY,
                           font=FT, relief="solid", padx=5, pady=3,
                           highlightthickness=1, highlightbackground=BORDER, width=30)
        city_lbl.grid(row=row, column=1, sticky="w")
        row += 1
        
        # ZIP
        tk.Label(form, text="ZIP CODE:", bg=PANEL, fg=TEXT_SECONDARY,
                font=FT, width=15, anchor="e").grid(
            row=row, column=0, padx=(0,10), pady=8, sticky="e")
        zip_e = entry(form, 20)
        zip_e.insert(0, data.get("zip", ""))
        zip_e.grid(row=row, column=1, pady=8, sticky="w")
        fields["zip"] = zip_e
        row += 1
        
        # Save button
        def save_changes():
            # Update data
            for key, entry_widget in fields.items():
                data[key] = entry_widget.get().strip()
                
            self._update_status(f"✓ CLIENT {record_id} UPDATED SUCCESSFULLY")
            
            # Show success message
            success = tk.Label(form, text="✅ CHANGES SAVED SUCCESSFULLY!", 
                              bg=PANEL, fg=GREEN, font=FB)
            success.grid(row=row, column=0, columnspan=2, pady=15)
            
            # Remove success message after 3 seconds
            self.after(3000, success.destroy)
            
        save_btn = create_rounded_button(form, "💾 SAVE CHANGES", save_changes, GREEN, 20, 2)
        save_btn.grid(row=row, column=0, columnspan=2, pady=15)
        row += 1
        
        # Cancel button
        cancel_btn = create_rounded_button(form, "↩ CANCEL", lambda: self.show_update(), HOME_BTN, 20, 2)
        cancel_btn.grid(row=row, column=0, columnspan=2, pady=(0, 15))

    def _display_airline_update(self, parent, record_id, data):
        """Display airline update form"""
        form = tk.Frame(parent, bg=PANEL)
        form.pack(fill="both", expand=True)
        
        row = 0
        
        tk.Label(form, text="COMPANY INFORMATION", bg=PANEL, fg=SECONDARY,
                font=FB).grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 10))
        row += 1
        
        tk.Label(form, text="COMPANY NAME:", bg=PANEL, fg=TEXT_SECONDARY,
                font=FT, width=15, anchor="e").grid(
            row=row, column=0, padx=(0,10), pady=10, sticky="e")
            
        name_e = entry(form, 36)
        name_e.insert(0, data["name"])
        name_e.grid(row=row, column=1, pady=10, sticky="w")
        row += 1
        
        def save_changes():
            data["name"] = name_e.get().strip()
            self._update_status(f"✓ AIRLINE {record_id} UPDATED SUCCESSFULLY")
            
            success = tk.Label(form, text="✅ CHANGES SAVED SUCCESSFULLY!", 
                              bg=PANEL, fg=GREEN, font=FB)
            success.grid(row=row, column=0, columnspan=2, pady=15)
            self.after(3000, success.destroy)
            
        save_btn = create_rounded_button(form, "💾 SAVE CHANGES", save_changes, GREEN, 20, 2)
        save_btn.grid(row=row, column=0, columnspan=2, pady=15)
        row += 1
        
        cancel_btn = create_rounded_button(form, "↩ CANCEL", lambda: self.show_update(), HOME_BTN, 20, 2)
        cancel_btn.grid(row=row, column=0, columnspan=2, pady=(0, 15))

    def _display_flight_update(self, parent, record_id, data):
        """Display flight update form"""
        form = tk.Frame(parent, bg=PANEL)
        form.pack(fill="both", expand=True)
        
        row = 0
        
        tk.Label(form, text="FLIGHT INFORMATION", bg=PANEL, fg=ACCENT,
                font=FB).grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 10))
        row += 1
        
        # Get airline name
        airline_name = SAMPLE_DATA["airlines"].get(data["airline"], {}).get("name", "Unknown")
        
        # Read-only info
        tk.Label(form, text="AIRLINE:", bg=PANEL, fg=TEXT_SECONDARY,
                font=FT, width=15, anchor="e").grid(
            row=row, column=0, padx=(0,10), pady=8, sticky="e")
        airline_lbl = tk.Label(form, text=f"{data['airline']} - {airline_name}", 
                              bg="white", fg=TEXT_PRIMARY, font=FT,
                              relief="solid", padx=5, pady=3,
                              highlightthickness=1, highlightbackground=BORDER, width=30)
        airline_lbl.grid(row=row, column=1, sticky="w")
        row += 1
        
        tk.Label(form, text="DATE:", bg=PANEL, fg=TEXT_SECONDARY,
                font=FT, width=15, anchor="e").grid(
            row=row, column=0, padx=(0,10), pady=8, sticky="e")
        date_lbl = tk.Label(form, text=data["date"], bg="white", fg=TEXT_PRIMARY,
                           font=FT, relief="solid", padx=5, pady=3,
                           highlightthickness=1, highlightbackground=BORDER, width=30)
        date_lbl.grid(row=row, column=1, sticky="w")
        row += 1
        
        tk.Label(form, text="TIME:", bg=PANEL, fg=TEXT_SECONDARY,
                font=FT, width=15, anchor="e").grid(
            row=row, column=0, padx=(0,10), pady=8, sticky="e")
        time_lbl = tk.Label(form, text=data["time"], bg="white", fg=TEXT_PRIMARY,
                           font=FT, relief="solid", padx=5, pady=3,
                           highlightthickness=1, highlightbackground=BORDER, width=30)
        time_lbl.grid(row=row, column=1, sticky="w")
        row += 1
        
        # Editable fields
        tk.Label(form, text="ORIGIN:", bg=PANEL, fg=TEXT_SECONDARY,
                font=FT, width=15, anchor="e").grid(
            row=row, column=0, padx=(0,10), pady=8, sticky="e")
        origin_e = entry(form, 36)
        origin_e.insert(0, data["origin"])
        origin_e.grid(row=row, column=1, pady=8, sticky="w")
        row += 1
        
        tk.Label(form, text="DESTINATION:", bg=PANEL, fg=TEXT_SECONDARY,
                font=FT, width=15, anchor="e").grid(
            row=row, column=0, padx=(0,10), pady=8, sticky="e")
        dest_e = entry(form, 36)
        dest_e.insert(0, data["destination"])
        dest_e.grid(row=row, column=1, pady=8, sticky="w")
        row += 1
        
        def save_changes():
            data["origin"] = origin_e.get().strip()
            data["destination"] = dest_e.get().strip()
            self._update_status(f"✓ FLIGHT {record_id} UPDATED SUCCESSFULLY")
            
            success = tk.Label(form, text="✅ CHANGES SAVED SUCCESSFULLY!", 
                              bg=PANEL, fg=GREEN, font=FB)
            success.grid(row=row, column=0, columnspan=2, pady=15)
            self.after(3000, success.destroy)
            
        save_btn = create_rounded_button(form, "💾 SAVE CHANGES", save_changes, GREEN, 20, 2)
        save_btn.grid(row=row, column=0, columnspan=2, pady=15)
        row += 1
        
        cancel_btn = create_rounded_button(form, "↩ CANCEL", lambda: self.show_update(), HOME_BTN, 20, 2)
        cancel_btn.grid(row=row, column=0, columnspan=2, pady=(0, 15))

    # ─────────────────────────────────────────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────────────────────────────────────────
    def show_delete(self):
        self._clear()
        self.current_screen = "delete"
        
        f = tk.Frame(self.content, bg=BG_PRIMARY)
        f.pack(fill="both", expand=True, padx=20, pady=16)

        tk.Label(f, text="🗑️  DELETE RECORD", bg=BG_PRIMARY, fg=RED,
                 font=FH).pack(anchor="w", pady=(0,12))

        # Search controls
        ctrl = tk.Frame(f, bg=PANEL, padx=14, pady=10)
        ctrl.pack(fill="x")
        
        tk.Label(ctrl, text="TYPE:", bg=PANEL, fg=RED, font=FB).pack(side="left")
        type_cb = combo(ctrl, ["CLIENT", "AIRLINE", "FLIGHT"], 12)
        type_cb.set("CLIENT")
        type_cb.pack(side="left", padx=8)
        
        tk.Label(ctrl, text="ID:", bg=PANEL, fg=RED, font=FB).pack(side="left", padx=(12,0))
        
        # ID entry with auto-formatting
        id_frame = tk.Frame(ctrl, bg=PANEL)
        id_frame.pack(side="left", padx=8)
        
        # Prefix label that changes based on type
        prefix_var = tk.StringVar(value="C-")
        prefix_lbl = tk.Label(id_frame, textvariable=prefix_var, bg=PANEL, fg=RED, font=FB)
        prefix_lbl.pack(side="left")
        
        id_e = entry(id_frame, 8)
        id_e.pack(side="left")
        
        # Update prefix when type changes
        def update_prefix(event=None):
            prefixes = {"CLIENT": "C-", "AIRLINE": "A-", "FLIGHT": "F-"}
            prefix_var.set(prefixes[type_cb.get()])
            id_e.focus()
            
        type_cb.bind("<<ComboboxSelected>>", update_prefix)
        
        create_small_button(ctrl, "📂 LOAD", self._load_for_delete, RED, 12).pack(side="left", padx=4)
        id_e.bind("<Return>", lambda e: self._load_for_delete())
        
        # Store references for delete screen
        self.delete_type_cb = type_cb
        self.delete_id_e = id_e
        self.delete_content = f
        
        # Preview area (will be populated when Load is clicked)
        self.delete_preview = tk.Frame(f, bg=PANEL, padx=20, pady=15)
        self.delete_preview.pack(fill="x", pady=10)
        
        # Show initial message
        tk.Label(self.delete_preview, text="ENTER AN ID TO LOAD RECORD DETAILS",
                bg=PANEL, fg=TEXT_MUTED, font=FT).pack()

    def _load_for_delete(self):
        """Load record for deletion"""
        # Clear preview
        for w in self.delete_preview.winfo_children():
            w.destroy()
            
        record_type = self.delete_type_cb.get()
        id_number = self.delete_id_e.get().strip()
        
        if not id_number:
            tk.Label(self.delete_preview, text="⚠ PLEASE ENTER AN ID NUMBER", 
                    bg=PANEL, fg=RED, font=FB).pack(pady=20)
            return
            
        # Format ID with prefix
        prefixes = {"CLIENT": "C-", "AIRLINE": "A-", "FLIGHT": "F-"}
        prefix = prefixes[record_type]
        
        # Pad with zeros to 4 digits
        padded_num = id_number.zfill(4)
        record_id = f"{prefix}{padded_num}"
        
        # Show loading
        loading_lbl = tk.Label(self.delete_preview, text="⏳ LOADING...", 
                              bg=PANEL, fg=RED, font=FB)
        loading_lbl.pack(pady=20)
        self.delete_preview.update()
        
        # Simulate load delay
        self.after(500, lambda: self._show_delete_preview(record_type, record_id, loading_lbl))
        
    def _show_delete_preview(self, record_type, record_id, loading_lbl):
        """Show record preview with delete confirmation"""
        loading_lbl.destroy()
        
        # Map record type to data type
        data_type = {"CLIENT": "clients", "AIRLINE": "airlines", "FLIGHT": "flights"}[record_type]
        
        # Get data
        data = SAMPLE_DATA[data_type].get(record_id)
            
        if not data:
            tk.Label(self.delete_preview, 
                    text=f"❌ {record_type} {record_id} NOT FOUND", 
                    bg=PANEL, fg=RED, font=FB).pack(pady=20)
            return
        
        # Clear preview again
        for w in self.delete_preview.winfo_children():
            w.destroy()
        
        # Header with warning
        warn_frame = tk.Frame(self.delete_preview, bg=PANEL)
        warn_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(warn_frame, text="⚠  RECORD FOUND", bg=PANEL, fg=SECONDARY,
                font=FB).pack()
                
        # Check if already deleted
        if data.get("deleted", False):
            tk.Label(warn_frame, text="(THIS RECORD IS ALREADY DELETED)", 
                    bg=PANEL, fg=RED, font=FS).pack()
        
        # Record details
        details = tk.Frame(self.delete_preview, bg=PANEL)
        details.pack(fill="x", pady=5)
        
        # Color based on type
        colors = {"CLIENT": SECONDARY, "AIRLINE": SECONDARY, "FLIGHT": ACCENT}
        color = colors[record_type]
        
        tk.Label(details, text=f"ID: {record_id}", bg=PANEL, fg=color,
                font=FB).pack(anchor="w")
        
        if record_type == "CLIENT":
            tk.Label(details, 
                    text=f"NAME: {data['first']} {data['last']}",
                    bg=PANEL, fg=TEXT_PRIMARY, font=FT).pack(anchor="w")
            tk.Label(details, text=f"EMAIL: {data['email']}",
                    bg=PANEL, fg=TEXT_PRIMARY, font=FT).pack(anchor="w")
            tk.Label(details, text=f"PHONE: {data['phone']}",
                    bg=PANEL, fg=TEXT_PRIMARY, font=FT).pack(anchor="w")
            tk.Label(details, text=f"LOCATION: {data['city']}, {data['country']}",
                    bg=PANEL, fg=TEXT_PRIMARY, font=FT).pack(anchor="w")
                    
        elif record_type == "AIRLINE":
            tk.Label(details, text=f"NAME: {data['name']}",
                    bg=PANEL, fg=TEXT_PRIMARY, font=FT).pack(anchor="w")
                    
        else:  # FLIGHT
            airline_name = SAMPLE_DATA["airlines"].get(data["airline"], {}).get("name", "Unknown")
            tk.Label(details, text=f"AIRLINE: {airline_name}",
                    bg=PANEL, fg=TEXT_PRIMARY, font=FT).pack(anchor="w")
            tk.Label(details, text=f"DATE: {data['date']} {data['time']}",
                    bg=PANEL, fg=TEXT_PRIMARY, font=FT).pack(anchor="w")
            tk.Label(details, text=f"ROUTE: {data['origin']} → {data['destination']}",
                    bg=PANEL, fg=TEXT_PRIMARY, font=FT).pack(anchor="w")
                    
        # Warning message
        tk.Label(self.delete_preview, text="⚠  THIS ACTION CANNOT BE UNDONE!",
                bg=PANEL, fg=RED, font=FB).pack(pady=(15, 10))
                
        # Confirmation field
        confirm_frame = tk.Frame(self.delete_preview, bg=PANEL)
        confirm_frame.pack(fill="x", pady=5)
        
        tk.Label(confirm_frame, text=f"TYPE '{record_id}' TO CONFIRM:",
                bg=PANEL, fg=TEXT_SECONDARY, font=FB).pack(anchor="w")
                
        confirm_e = entry(confirm_frame, 20)
        confirm_e.pack(anchor="w", pady=5)
        confirm_e.focus()
        
        def do_delete():
            if confirm_e.get().strip() != record_id:
                # Show error
                error_lbl = tk.Label(confirm_frame, text="❌ ID DOES NOT MATCH",
                                    bg=PANEL, fg=RED, font=FB)
                error_lbl.pack(anchor="w")
                self.after(2000, error_lbl.destroy)
                return
                
            # Perform deletion (soft delete by marking as deleted)
            data["deleted"] = True
            self.update_deleted_records()
                
            self._update_status(f"✓ {record_type} {record_id} MOVED TO TRASH")
            
            # Clear preview and show success
            for w in self.delete_preview.winfo_children():
                w.destroy()
                
            success_frame = tk.Frame(self.delete_preview, bg=PANEL)
            success_frame.pack(fill="x")
            
            tk.Label(success_frame, text="✅", bg=PANEL, fg=GREEN,
                    font=("Segoe UI", 32)).pack(pady=10)
            tk.Label(success_frame, text=f"{record_type} {record_id} MOVED TO TRASH",
                    bg=PANEL, fg=GREEN, font=FB).pack()
            tk.Label(success_frame, text="(Record can be restored from Deleted Records)",
                    bg=PANEL, fg=TEXT_MUTED, font=FS).pack()
                    
            # Undo option (restore)
            def undo_delete():
                data["deleted"] = False
                self.update_deleted_records()
                self._update_status(f"↩ UNDO SUCCESSFUL - {record_id} RESTORED")
                self.show_delete()
                
            create_small_button(success_frame, "↩ UNDO", undo_delete, SECONDARY, 12).pack(pady=10)
            create_small_button(success_frame, "🗑️ DELETE ANOTHER", self.show_delete, ACCENT, 15).pack()
            
        # Buttons
        btn_frame = tk.Frame(self.delete_preview, bg=PANEL)
        btn_frame.pack(fill="x", pady=10)
        
        create_rounded_button(btn_frame, "🗑️ CONFIRM DELETE", do_delete, RED, 18, 2).pack(side="left", padx=5)
        
        def cancel_delete():
            self.show_delete()
            
        create_rounded_button(btn_frame, "↩ CANCEL", cancel_delete, HOME_BTN, 12, 2).pack(side="left", padx=5)

    # ─────────────────────────────────────────────────────────────────────────
    # UNDO FUNCTIONALITY
    # ─────────────────────────────────────────────────────────────────────────
    def _undo_create(self, data_type, record_id):
        """Undo a create operation"""
        if record_id in SAMPLE_DATA[data_type]:
            del SAMPLE_DATA[data_type][record_id]
            self._update_status(f"↩ UNDO SUCCESSFUL - {record_id} REMOVED")
        self.update_deleted_records()
        self.show_home()

    # ─────────────────────────────────────────────────────────────────────────
    # SUCCESS SCREEN
    # ─────────────────────────────────────────────────────────────────────────
    def _success(self, title, subtitle, buttons):
        """Show success screen with options"""
        self._clear()
        self.current_screen = "success"
        
        f = tk.Frame(self.content, bg=BG_PRIMARY)
        f.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Success icon
        tk.Label(f, text="✅", bg=BG_PRIMARY, fg=GREEN,
                 font=("Segoe UI", 72)).pack(pady=(40, 8))
                 
        # Title and subtitle
        tk.Label(f, text=title, bg=BG_PRIMARY, fg=GREEN,
                 font=("Segoe UI", 20, "bold")).pack(pady=(0, 6))
        tk.Label(f, text=subtitle, bg=BG_PRIMARY, fg=TEXT_PRIMARY,
                 font=FT2).pack(pady=(0, 30))
                 
        # Action buttons
        for txt, cmd in buttons:
            btn_color = GREEN if "ADD ANOTHER" in txt else (SECONDARY if "UNDO" in txt else ACCENT)
            create_rounded_button(f, txt, cmd, btn_color, 26, 2).pack(pady=8)

# ─────────────────────────────── RUN THE APPLICATION ─────────────────────────

if __name__ == "__main__":
    # Create and run the application
    app = App()
    app.mainloop()
