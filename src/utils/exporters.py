"""
Export functions for JSON, CSV, and SQLite formats.
"""

import json
import csv
import sqlite3


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
                writer.writerow(["ID", "Airline ID", "Date", "Time", "Origin", "Destination", "Status"])
                for fid, info in data.items():
                    status = "DELETED" if info.get("deleted", False) else "ACTIVE"
                    writer.writerow([fid, info["airline"], info["date"], info["time"],
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
                    date TEXT,
                    time TEXT,
                    origin TEXT,
                    destination TEXT,
                    status TEXT
                )
            ''')
            for fid, info in data.items():
                status = "DELETED" if info.get("deleted", False) else "ACTIVE"
                cursor.execute('''
                    INSERT OR REPLACE INTO flights 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (fid, info["airline"], info["date"], info["time"],
                      info["origin"], info["destination"], status))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"SQLite Export Error: {e}")
        return False