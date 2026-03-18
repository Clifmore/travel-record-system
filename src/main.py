#!/usr/bin/env python3
"""
Travel Agent Record Management System - Main Entry Point
University of Liverpool - Group B 2026
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

from client import (
    create_record, update_record, delete_record, search_record,
    build_client_dict, build_airline_dict, build_flight_dict
)
import json
# Get the absolute path of the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (travelapp folder)
parent_dir = os.path.dirname(current_dir)

# Add both directories to Python path
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

print(f"Python path: {sys.path}")  # This will help us debug

try:
    from src.gui.app import App
    print("Successfully imported App")
except ImportError as e:
    print(f"Import error: {e}")
    print("\nTrying alternative import...")
    try:
        from gui.app import App
        print("Successfully imported App (alternative)")
    except ImportError as e2:
        print(f"Alternative import also failed: {e2}")
        sys.exit(1)


def main():
    """Main entry point for the application."""
    try:
        app = App()
        app.mainloop()
    except KeyboardInterrupt:
        print("\nApplication terminated by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
