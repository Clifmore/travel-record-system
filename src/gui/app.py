"""
Main Application Window
"""

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

from src.utils.theme import (
    BG_PRIMARY, PANEL, CARD, SECONDARY, SECONDARY_LIGHT, SECONDARY_DARK,
    ACCENT, ACCENT_LIGHT, ACCENT_DARK, GREEN, RED, TEXT_PRIMARY,
    TEXT_SECONDARY, TEXT_MUTED, BORDER, HOME_BTN
)
from src.utils.validators import validate_email
from src.utils.formatters import format_id, get_next_id
from src.utils.exporters import export_to_json, export_to_csv, export_to_sqlite
from src.database.sample_data import SAMPLE_DATA, TIMES, GEOGRAPHY, recently_deleted
from src.gui.splash import SplashScreen
from src.gui.widgets import (
    create_rounded_button, create_small_button, entry, combo, lbl, 
    err_lbl, success_lbl, divider
)


class App(tk.Tk):
    """Main application class."""
    
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
        """Center the window on screen."""
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 1050) // 2
        y = (self.winfo_screenheight() - 720) // 2
        self.geometry(f"1050x720+{x}+{y}")

    def _build_shell(self):
        """Build the main shell with top bar, sidebar, and content area."""
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
                 bg=PANEL, fg=TEXT_MUTED, font=("Segoe UI", 9)).pack(side="left", padx=(10, 0))
        
        # Status indicator
        self.status_lbl = tk.Label(top, text="● ONLINE", bg=PANEL, fg=GREEN,
                                   font=("Segoe UI", 10, "bold"), padx=20)
        self.status_lbl.pack(side="right")

        # Sidebar
        self.side = tk.Frame(self, bg=PANEL, width=200)
        self.side.pack(fill="y", side="left")
        self.side.pack_propagate(False)

        tk.Label(self.side, text="MAIN MENU", bg=PANEL, fg=SECONDARY,
                 font=("Segoe UI", 10, "bold"), padx=16, pady=10).pack(anchor="w")

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
                          font=("Segoe UI", 10, "bold"), anchor="w", padx=8)
            lb.pack(fill="both", expand=True)
            
            # Store reference for highlighting
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
                fr.ref = lb
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
    # SCREEN NAVIGATION METHODS
    # ─────────────────────────────────────────────────────────────────────────
    
    def show_home(self):
        """Show home screen."""
        self._clear()
        self.current_screen = "home"
        self._show_home_content()

    def show_create_menu(self):
        """Show create menu."""
        self._clear()
        self.current_screen = "create_menu"
        self._show_create_menu()

    def show_search(self):
        """Show search screen."""
        self._clear()
        self.current_screen = "search"
        self._show_search()

    def show_update(self):
        """Show update screen."""
        self._clear()
        self.current_screen = "update"
        self._show_update()

    def show_delete(self):
        """Show delete screen."""
        self._clear()
        self.current_screen = "delete"
        self._show_delete()

    def show_deleted_records(self):
        """Show deleted records screen."""
        self._clear()
        self.current_screen = "deleted_records"
        self._show_deleted_records()

    def show_create_client(self):
        """Show create client form."""
        self._clear()
        self.current_screen = "create_client"
        self._show_create_client()

    def show_create_airline(self):
        """Show create airline form."""
        self._clear()
        self.current_screen = "create_airline"
        self._show_create_airline()

    def show_create_flight(self):
        """Show create flight form."""
        self._clear()
        self.current_screen = "create_flight"
        self._show_create_flight()

    # ─────────────────────────────────────────────────────────────────────────
    # HOME SCREEN
    # ─────────────────────────────────────────────────────────────────────────
    
    def _show_home_content(self):
        """Display home screen content."""
        f = tk.Frame(self.content, bg=BG_PRIMARY)
        f.pack(expand=True, fill="both", padx=20, pady=20)

        # Welcome message with date
        today = date.today().strftime("%A, %B %d, %Y")
        tk.Label(f, text="WELCOME BACK", bg=BG_PRIMARY, fg=SECONDARY,
                 font=("Segoe UI", 28, "bold")).pack(pady=(30, 6))
        tk.Label(f, text=today, bg=BG_PRIMARY, fg=TEXT_PRIMARY,
                 font=("Segoe UI", 11)).pack(pady=(0, 6))
        tk.Label(f, text="Manage clients, airlines, and flights from the menu below.",
                 bg=BG_PRIMARY, fg=TEXT_SECONDARY, font=("Segoe UI", 11)).pack(pady=(0, 30))

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
                     font=("Segoe UI", 10, "bold")).pack()
            tk.Label(card, text=str(active), bg=PANEL, fg=TEXT_PRIMARY,
                     font=("Segoe UI", 32, "bold")).pack()
            tk.Label(card, text=f"({deleted} deleted)", bg=PANEL, fg=RED,
                     font=("Segoe UI", 9)).pack()

        # Quick actions
        tk.Label(f, text="QUICK ACTIONS", bg=BG_PRIMARY, fg=SECONDARY,
                 font=("Segoe UI", 10, "bold")).pack(pady=(30, 15))
                 
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
                    bg=PANEL, fg=RED, font=("Segoe UI", 10, "bold")).pack(side="left")
            
            create_small_button(deleted_summary, "VIEW DELETED RECORDS", self.show_deleted_records, RED, 20).pack(side="right")

    # ─────────────────────────────────────────────────────────────────────────
    # CREATE MENU
    # ─────────────────────────────────────────────────────────────────────────
    
    def _show_create_menu(self):
        """Display create menu."""
        f = tk.Frame(self.content, bg=BG_PRIMARY)
        f.pack(expand=True, fill="both", padx=20, pady=20)

        tk.Label(f, text="CREATE A RECORD", bg=BG_PRIMARY, fg=SECONDARY,
                 font=("Segoe UI", 18, "bold")).pack(pady=(20, 8))
        tk.Label(f, text="Choose the record type to create:",
                 bg=BG_PRIMARY, fg=TEXT_PRIMARY, font=("Segoe UI", 11)).pack(pady=(0, 30))

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
                     font=("Segoe UI", 10, "bold")).pack(anchor="w")
            tk.Label(col_, text=desc, bg=PANEL, fg=TEXT_SECONDARY,
                     font=("Segoe UI", 10)).pack(anchor="w")
            
            # Hover effects
            def enter(e, c=card, color=col):
                c.config(bg=SECONDARY_LIGHT if color == SECONDARY else ACCENT_LIGHT)
            def leave(e, c=card, color=col):
                c.config(bg=PANEL)
                
            card.bind("<Enter>", enter)
            card.bind("<Leave>", leave)

        create_rounded_button(f, "↩  RETURN TO HOME", self.show_home, HOME_BTN, 22, 2).pack(pady=30)

    # ─────────────────────────────────────────────────────────────────────────
    # CREATE CLIENT
    # ─────────────────────────────────────────────────────────────────────────
    
    def _show_create_client(self):
        """Display create client form."""
        inner = self._scroll_frame()

        # Header with next ID
        next_id = get_next_id("C", {k:v for k,v in SAMPLE_DATA["clients"].items() if not v.get("deleted", False)})
        
        hdr = tk.Frame(inner, bg=PANEL, padx=20, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="👤  NEW CLIENT RECORD", bg=PANEL, fg=SECONDARY,
                 font=("Segoe UI", 18, "bold")).pack(side="left")
        tk.Label(hdr, text=f"ID: {next_id}", bg=PANEL, fg=TEXT_PRIMARY,
                 font=("Segoe UI", 10, "bold")).pack(side="right")

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
                    bg=PANEL, fg=TEXT_SECONDARY, font=("Segoe UI", 10), width=18, anchor="e").grid(
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
        divider(pnl)

        tk.Label(pnl, text="ADDRESS DETAILS", bg=PANEL, fg=SECONDARY,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 10))

        geo_frame = tk.Frame(pnl, bg=PANEL)
        geo_frame.pack(anchor="w")

        # Country
        tk.Label(geo_frame, text="COUNTRY *", bg=PANEL, fg=TEXT_SECONDARY,
                 font=("Segoe UI", 10), width=18, anchor="e").grid(row=0, column=0, padx=(0, 10), pady=8, sticky="e")
        country_cb = combo(geo_frame, list(GEOGRAPHY.keys()), 32)
        country_cb.grid(row=0, column=1, pady=8, sticky="w")
        country_err = err_lbl(geo_frame)
        country_err.grid(row=0, column=2, sticky="w", padx=(5,0))
        fields["country"] = country_cb
        error_labels["country"] = country_err

        # State
        tk.Label(geo_frame, text="STATE / REGION", bg=PANEL, fg=TEXT_SECONDARY,
                 font=("Segoe UI", 10), width=18, anchor="e").grid(row=1, column=0, padx=(0, 10), pady=8, sticky="e")
        state_cb = combo(geo_frame, [], 32)
        state_cb.grid(row=1, column=1, pady=8, sticky="w")
        fields["state"] = state_cb

        # City
        tk.Label(geo_frame, text="CITY *", bg=PANEL, fg=TEXT_SECONDARY,
                 font=("Segoe UI", 10), width=18, anchor="e").grid(row=2, column=0, padx=(0, 10), pady=8, sticky="e")
        city_cb = combo(geo_frame, [], 32)
        city_cb.grid(row=2, column=1, pady=8, sticky="w")
        city_err = err_lbl(geo_frame)
        city_err.grid(row=2, column=2, sticky="w", padx=(5,0))
        fields["city"] = city_cb
        error_labels["city"] = city_err

        # ZIP
        tk.Label(geo_frame, text="ZIP / POST CODE", bg=PANEL, fg=TEXT_SECONDARY,
                 font=("Segoe UI", 10), width=18, anchor="e").grid(row=3, column=0, padx=(0, 10), pady=8, sticky="e")
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
                          font=("Segoe UI", 10, "bold"), wraplength=500)
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
            
            self._update_status(f"✓ CLIENT {client_id} CREATED SUCCESSFULLY")
            
            # Show success screen
            self._success(
                "CLIENT ADDED SUCCESSFULLY!",
                f"Client {client_id} has been saved.",
                [
                    ("➕ ADD ANOTHER CLIENT", self.show_create_client),
                    ("↩ RETURN TO HOME", self.show_home)
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
    
    def _show_create_airline(self):
        """Display create airline form."""
        inner = self._scroll_frame()

        # Header with next ID
        next_id = get_next_id("A", {k:v for k,v in SAMPLE_DATA["airlines"].items() if not v.get("deleted", False)})
        
        hdr = tk.Frame(inner, bg=PANEL, padx=20, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="✈  NEW AIRLINE RECORD", bg=PANEL, fg=SECONDARY,
                 font=("Segoe UI", 18, "bold")).pack(side="left")
        tk.Label(hdr, text=f"ID: {next_id}", bg=PANEL, fg=TEXT_PRIMARY,
                 font=("Segoe UI", 10, "bold")).pack(side="right")

        pnl = tk.Frame(inner, bg=PANEL, padx=40, pady=30)
        pnl.pack(padx=20, pady=12, fill="x")

        # Airline name field
        tk.Label(pnl, text="COMPANY NAME *", bg=PANEL, fg=TEXT_SECONDARY, font=("Segoe UI", 10)).pack(anchor="w", pady=(0,4))
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
            for airline_id, data in SAMPLE_DATA["airlines"].items():
                if data["name"].lower() == name.lower() and not data.get("deleted", False):
                    exists = True
                    
            if exists:
                name_err.config(text="⚠ AIRLINE ALREADY EXISTS!", fg=RED)
                name_success.config(text="")
            else:
                name_err.config(text="")
                name_success.config(text="✓ AVAILABLE", fg=GREEN)
                
        name_e.bind("<KeyRelease>", check_duplicate)

        banner = tk.Label(pnl, text="", bg=PANEL, fg=RED,
                          font=("Segoe UI", 10, "bold"))
        banner.pack(pady=(10,0), anchor="w")

        def on_submit():
            name = name_e.get().strip()
            if not name:
                name_err.config(text="⚠ COMPANY NAME IS REQUIRED")
                banner.config(text="⚠ PLEASE FIX THE ERRORS ABOVE")
                return
                
            # Check for duplicates again
            exists = False
            for airline_id, data in SAMPLE_DATA["airlines"].items():
                if data["name"].lower() == name.lower() and not data.get("deleted", False):
                    exists = True
                    
            if exists:
                banner.config(text="⚠ AIRLINE ALREADY EXISTS!")
                return
                
            # Get next ID
            airline_id = get_next_id("A", {k:v for k,v in SAMPLE_DATA["airlines"].items() if not v.get("deleted", False)})
            
            # Save to "database"
            SAMPLE_DATA["airlines"][airline_id] = {"name": name, "deleted": False}
            
            self._update_status(f"✓ AIRLINE {airline_id} CREATED SUCCESSFULLY")
            
            self._success(
                "AIRLINE ADDED SUCCESSFULLY!",
                f"Airline '{name}' has been registered.",
                [
                    ("➕ ADD ANOTHER AIRLINE", self.show_create_airline),
                    ("↩ RETURN TO HOME", self.show_home)
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

    # ─────────────────────────────────────────────────────────────────────────
    # CREATE FLIGHT
    # ─────────────────────────────────────────────────────────────────────────
    
    def _show_create_flight(self):
        """Display create flight form."""
        inner = self._scroll_frame()

        # Header with next ID
        next_id = get_next_id("F", {k:v for k,v in SAMPLE_DATA["flights"].items() if not v.get("deleted", False)})
        
        hdr = tk.Frame(inner, bg=PANEL, padx=20, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🛫  NEW FLIGHT RECORD", bg=PANEL, fg=ACCENT,
                 font=("Segoe UI", 18, "bold")).pack(side="left")
        tk.Label(hdr, text=f"ID: {next_id}", bg=PANEL, fg=TEXT_PRIMARY,
                 font=("Segoe UI", 10, "bold")).pack(side="right")

        pnl = tk.Frame(inner, bg=PANEL, padx=32, pady=24)
        pnl.pack(padx=20, pady=12, fill="x")
        
        # Calendar picker will be imported when needed
        from src.gui.calendar_picker import CalendarPicker

        def flbl(text, r):
            tk.Label(form, text=text, bg=PANEL, fg=TEXT_SECONDARY,
                     font=("Segoe UI", 10), width=20, anchor="e").grid(
                row=r, column=0, padx=(0, 10), pady=8, sticky="e")

        form = tk.Frame(pnl, bg=PANEL)
        form.pack(anchor="w")

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
                             font=("Segoe UI", 10, "bold"), relief="solid", cursor="hand2", anchor="w",
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
                          font=("Segoe UI", 10, "bold"), wraplength=500)
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
            
            self._update_status(f"✓ FLIGHT {flight_id} CREATED SUCCESSFULLY")
            
            self._success(
                "FLIGHT ADDED SUCCESSFULLY!",
                f"{origin_e.get().strip()} → {dest_e.get().strip()}",
                [
                    ("➕ ADD ANOTHER FLIGHT", self.show_create_flight),
                    ("↩ RETURN TO HOME", self.show_home)
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
    # SEARCH SCREEN
    # ─────────────────────────────────────────────────────────────────────────
    
    def _show_search(self):
        """Display search screen."""
        f = tk.Frame(self.content, bg=BG_PRIMARY)
        f.pack(fill="both", expand=True, padx=20, pady=16)

        tk.Label(f, text="🔍  SEARCH RECORDS", bg=BG_PRIMARY, fg=SECONDARY,
                 font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0,16))

        # Search controls
        ctrl = tk.Frame(f, bg=PANEL, padx=14, pady=10)
        ctrl.pack(fill="x")
        
        tk.Label(ctrl, text="TYPE:", bg=PANEL, fg=SECONDARY, font=("Segoe UI", 10, "bold")).pack(side="left")
        type_cb = combo(ctrl, ["CLIENTS", "AIRLINES", "FLIGHTS"], 14)
        type_cb.set("CLIENTS")
        type_cb.pack(side="left", padx=8)
        
        tk.Label(ctrl, text="SEARCH:", bg=PANEL, fg=SECONDARY, font=("Segoe UI", 10, "bold")).pack(side="left", padx=(12,0))
        search_e = entry(ctrl, 28)
        search_e.pack(side="left", padx=8)

        # Results count
        result_count = tk.Label(ctrl, text="", bg=PANEL, fg=GREEN, font=("Segoe UI", 10, "bold"))
        result_count.pack(side="left", padx=10)

        # Table frame
        tbl_f = tk.Frame(f, bg=PANEL)
        tbl_f.pack(fill="both", expand=True, pady=10)

        # Treeview style
        style = ttk.Style()
        style.configure("Treeview", background="white", foreground=TEXT_PRIMARY,
                        rowheight=30, fieldbackground="white", font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background=PANEL, foreground=SECONDARY,
                        font=("Segoe UI", 10, "bold"), relief="solid")
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
                    if data.get("deleted", False):
                        continue
                    row = (cid, data["first"], data["last"], data["email"], 
                          data["phone"], data["country"], data["city"], "ACTIVE")
                    if not query or any(query in str(v).lower() for v in row):
                        results.append(row)
                        
            elif rtype == "AIRLINES":
                for aid, data in SAMPLE_DATA["airlines"].items():
                    if data.get("deleted", False):
                        continue
                    row = (aid, data["name"], "ACTIVE")
                    if not query or query in data["name"].lower():
                        results.append(row)
                        
            else:  # FLIGHTS
                for fid, data in SAMPLE_DATA["flights"].items():
                    if data.get("deleted", False):
                        continue
                    airline_name = SAMPLE_DATA["airlines"].get(data["airline"], {}).get("name", "Unknown")
                    row = (fid, airline_name, data["date"], data["time"], 
                          data["origin"], data["destination"], "ACTIVE")
                    if not query or any(query in str(v).lower() for v in row):
                        results.append(row)
                        
            # Insert results
            for row in results:
                tree.insert("", "end", values=row)
                
            # Update count
            count = len(results)
            result_count.config(text=f"{count} RECORD(S) FOUND")

        # Search button and bindings
        create_small_button(ctrl, "🔍 SEARCH", refresh_results, SECONDARY, 12).pack(side="left", padx=4)
        type_cb.bind("<<ComboboxSelected>>", lambda e: refresh_results())
        search_e.bind("<Return>", lambda e: refresh_results())
        
        # Initial search
        refresh_results()

    # ─────────────────────────────────────────────────────────────────────────
    # UPDATE SCREEN
    # ─────────────────────────────────────────────────────────────────────────
    
    def _show_update(self):
        """Display update screen."""
        inner = self._scroll_frame()

        tk.Label(inner, text="✏️  UPDATE RECORD", bg=BG_PRIMARY, fg=SECONDARY,
                 font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=20, pady=(16,10))

        # Search controls
        ctrl = tk.Frame(inner, bg=PANEL, padx=14, pady=10)
        ctrl.pack(fill="x", padx=20)
        
        tk.Label(ctrl, text="TYPE:", bg=PANEL, fg=SECONDARY, font=("Segoe UI", 10, "bold")).pack(side="left")
        type_cb = combo(ctrl, ["CLIENT", "AIRLINE", "FLIGHT"], 12)
        type_cb.set("CLIENT")
        type_cb.pack(side="left", padx=8)
        
        tk.Label(ctrl, text="ID:", bg=PANEL, fg=SECONDARY, font=("Segoe UI", 10, "bold")).pack(side="left", padx=(12,0))
        
        # ID entry
        id_e = entry(ctrl, 12)
        id_e.pack(side="left", padx=8)

        def load_record():
            record_type = type_cb.get()
            record_id = id_e.get().strip()
            
            if not record_id:
                messagebox.showerror("ERROR", "Please enter an ID")
                return
                
            # Format ID with prefix
            prefixes = {"CLIENT": "C-", "AIRLINE": "A-", "FLIGHT": "F-"}
            prefix = prefixes[record_type]
            
            # Pad with zeros to 4 digits
            padded_id = record_id.zfill(4)
            full_id = f"{prefix}{padded_id}"
            
            # Get data
            data_type = {"CLIENT": "clients", "AIRLINE": "airlines", "FLIGHT": "flights"}[record_type]
            data = SAMPLE_DATA[data_type].get(full_id)
            
            if not data:
                messagebox.showerror("ERROR", f"{record_type} {full_id} not found")
                return
                
            if data.get("deleted", False):
                messagebox.showerror("ERROR", f"{record_type} {full_id} has been deleted")
                return
                
            # Show success and return to home (simplified for now)
            self._update_status(f"✓ RECORD FOUND - Edit feature coming soon")
            messagebox.showinfo("INFO", f"{record_type} {full_id} found!\n\nEdit feature will be implemented in the next version.")

        create_small_button(ctrl, "📂 LOAD", load_record, SECONDARY, 12).pack(side="left", padx=4)
        id_e.bind("<Return>", lambda e: load_record())

    # ─────────────────────────────────────────────────────────────────────────
    # DELETE SCREEN
    # ─────────────────────────────────────────────────────────────────────────
    
    def _show_delete(self):
        """Display delete screen."""
        inner = self._scroll_frame()

        tk.Label(inner, text="🗑️  DELETE RECORD", bg=BG_PRIMARY, fg=RED,
                 font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=20, pady=(16,10))

        # Search controls
        ctrl = tk.Frame(inner, bg=PANEL, padx=14, pady=10)
        ctrl.pack(fill="x", padx=20)
        
        tk.Label(ctrl, text="TYPE:", bg=PANEL, fg=RED, font=("Segoe UI", 10, "bold")).pack(side="left")
        type_cb = combo(ctrl, ["CLIENT", "AIRLINE", "FLIGHT"], 12)
        type_cb.set("CLIENT")
        type_cb.pack(side="left", padx=8)
        
        tk.Label(ctrl, text="ID:", bg=PANEL, fg=RED, font=("Segoe UI", 10, "bold")).pack(side="left", padx=(12,0))
        
        # ID entry
        id_e = entry(ctrl, 12)
        id_e.pack(side="left", padx=8)

        def delete_record():
            record_type = type_cb.get()
            record_id = id_e.get().strip()
            
            if not record_id:
                messagebox.showerror("ERROR", "Please enter an ID")
                return
                
            # Format ID with prefix
            prefixes = {"CLIENT": "C-", "AIRLINE": "A-", "FLIGHT": "F-"}
            prefix = prefixes[record_type]
            
            # Pad with zeros to 4 digits
            padded_id = record_id.zfill(4)
            full_id = f"{prefix}{padded_id}"
            
            # Get data
            data_type = {"CLIENT": "clients", "AIRLINE": "airlines", "FLIGHT": "flights"}[record_type]
            data = SAMPLE_DATA[data_type].get(full_id)
            
            if not data:
                messagebox.showerror("ERROR", f"{record_type} {full_id} not found")
                return
                
            if data.get("deleted", False):
                messagebox.showerror("ERROR", f"{record_type} {full_id} is already deleted")
                return
                
            # Confirm deletion
            result = messagebox.askyesno(
                "CONFIRM DELETE",
                f"Are you sure you want to delete {record_type} {full_id}?\n\nThis record can be restored later.",
                icon='warning'
            )
            
            if result:
                data["deleted"] = True
                self.update_deleted_records()
                self._update_status(f"✓ {record_type} {full_id} MOVED TO TRASH")
                messagebox.showinfo("DELETED", f"{record_type} {full_id} has been moved to trash.")

        create_small_button(ctrl, "🗑️ DELETE", delete_record, RED, 12).pack(side="left", padx=4)
        id_e.bind("<Return>", lambda e: delete_record())

    # ─────────────────────────────────────────────────────────────────────────
    # DELETED RECORDS SCREEN
    # ─────────────────────────────────────────────────────────────────────────
    
    def _show_deleted_records(self):
        """Display deleted records screen."""
        f = tk.Frame(self.content, bg=BG_PRIMARY)
        f.pack(fill="both", expand=True, padx=20, pady=16)

        tk.Label(f, text="📋  DELETED RECORDS", bg=BG_PRIMARY, fg=RED,
                 font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 16))

        if not recently_deleted:
            # No deleted records
            no_records = tk.Frame(f, bg=PANEL, padx=40, pady=40)
            no_records.pack(fill="both", expand=True)
            
            tk.Label(no_records, text="🗑️", bg=PANEL, fg=TEXT_MUTED,
                    font=("Segoe UI", 48)).pack(pady=20)
            tk.Label(no_records, text="No Deleted Records Found", bg=PANEL, fg=TEXT_MUTED,
                    font=("Segoe UI", 18, "bold")).pack()
            tk.Label(no_records, text="Records you delete will appear here", bg=PANEL, fg=TEXT_MUTED,
                    font=("Segoe UI", 10)).pack(pady=10)
            return

        # Header with count
        header = tk.Frame(f, bg=PANEL, padx=20, pady=10)
        header.pack(fill="x", pady=(0, 10))
        
        tk.Label(header, text=f"Found {len(recently_deleted)} deleted record(s)", 
                bg=PANEL, fg=SECONDARY, font=("Segoe UI", 10, "bold")).pack(side="left")

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
                    font=("Segoe UI", 10, "bold")).pack(side="left")
            
            # Details based on type
            details = tk.Frame(card, bg=PANEL)
            details.pack(fill="x", pady=10)
            
            if rec_type == "Client":
                tk.Label(details, text=f"Name: {data['first']} {data['last']}", 
                        bg=PANEL, fg=TEXT_PRIMARY, font=("Segoe UI", 10)).pack(anchor="w")
                tk.Label(details, text=f"Email: {data['email']}", 
                        bg=PANEL, fg=TEXT_PRIMARY, font=("Segoe UI", 10)).pack(anchor="w")
                
            elif rec_type == "Airline":
                tk.Label(details, text=f"Name: {data['name']}", 
                        bg=PANEL, fg=TEXT_PRIMARY, font=("Segoe UI", 10)).pack(anchor="w")
                
            else:  # Flight
                airline_name = SAMPLE_DATA["airlines"].get(data["airline"], {}).get("name", "Unknown")
                tk.Label(details, text=f"Airline: {airline_name}", 
                        bg=PANEL, fg=TEXT_PRIMARY, font=("Segoe UI", 10)).pack(anchor="w")
                tk.Label(details, text=f"Route: {data['origin']} → {data['destination']}", 
                        bg=PANEL, fg=TEXT_PRIMARY, font=("Segoe UI", 10)).pack(anchor="w")
            
            # Restore button
            btn_row = tk.Frame(card, bg=PANEL)
            btn_row.pack(fill="x")
            
            def restore(rt=rec_type, rid=rec_id):
                self._restore_record(rt, rid)
                
            create_small_button(btn_row, "🔄 Restore", restore, GREEN, 12).pack(side="left", padx=5)

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
                 font=("Segoe UI", 11)).pack(pady=(0, 30))
                 
        # Action buttons
        for txt, cmd in buttons:
            btn_color = GREEN if "ADD ANOTHER" in txt else SECONDARY
            create_rounded_button(f, txt, cmd, btn_color, 26, 2).pack(pady=8)


# This part is already in main.py, but included for completeness
# if __name__ == "__main__":
#     app = App()
#     app.mainloop()