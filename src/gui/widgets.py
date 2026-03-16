"""
Reusable GUI widgets with consistent styling.
"""

import tkinter as tk
from tkinter import ttk
from src.utils.theme import (
    BG_PRIMARY, PANEL, SECONDARY, SECONDARY_LIGHT, SECONDARY_DARK,
    ACCENT, ACCENT_LIGHT, TEXT_PRIMARY, TEXT_SECONDARY, BORDER
)


def _lighten(hex_color):
    """Lighten color for hover effects"""
    hex_color = hex_color.lstrip("#")
    r,g,b = (int(hex_color[i:i+2],16) for i in (0,2,4))
    return f"#{min(r+30,255):02x}{min(g+30,255):02x}{min(b+30,255):02x}"


def create_rounded_button(parent, text, command, color=SECONDARY, width=18, height=2):
    """Create a modern button with rounded corners"""
    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg="white",
        font=("Segoe UI", 10, "bold"),
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
    
    button.bind("<Enter>", lambda e: button.config(bg=_lighten(color)))
    button.bind("<Leave>", lambda e: button.config(bg=color))
    
    return button


def create_small_button(parent, text, command, color=SECONDARY, width=15):
    """Create a small modern button with adjustable width"""
    return create_rounded_button(parent, text, command, color, width=width, height=1)


def entry(parent, w=32, show=None):
    """Consistent entry field creation"""
    e = tk.Entry(parent, bg="white", fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY,
                 font=("Segoe UI", 10), relief="solid", bd=1, width=w, show=show,
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
                     font=("Segoe UI", 10), style="Custom.TCombobox")
    return c


def lbl(parent, text, fg=TEXT_PRIMARY, font=("Segoe UI", 10), **kw):
    """Consistent label creation"""
    return tk.Label(parent, text=text, bg=BG_PRIMARY, fg=fg, font=font, **kw)


def err_lbl(parent):
    """Consistent error label creation"""
    return tk.Label(parent, text="", bg=BG_PRIMARY, fg="#E74C3C",
                    font=("Segoe UI", 10, "bold"), anchor="w")


def success_lbl(parent):
    """Success message label"""
    return tk.Label(parent, text="", bg=BG_PRIMARY, fg="#2ECC71",
                    font=("Segoe UI", 10, "bold"), anchor="w")


def divider(parent):
    """Consistent divider"""
    tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=0, pady=8)