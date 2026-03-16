"""
Server module for the flight‑booking database system.

This module implements a simple server that accepts one client
connection at a time. Each connection carries a single JSON‑encoded
request, which is processed synchronously before the connection is
closed. The server performs CRUD operations on an in‑memory database
and persists all changes to a local JSON file.

Supported record types include 'client', 'airline', and 'flight'.
Requests follow a small action‑based protocol ('create', 'update',
'delete', 'search'), and responses include a status code, message,
timestamp, and optional record data.
"""

import json
import os
import socket
from datetime import datetime
from typing import Any, Optional


# ------------------------------
# TIMESTAMP
# ------------------------------
def current_timestamp() -> str:
    """
    Return the current timestamp in YYYY-MM-DD HH:MM format.

    :returns: The formatted timestamp string.
    :rtype: str
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M")


# ------------------------------
# JSON DATABASE HANDLING
# ------------------------------
DB_FILE = "records.json"


def load_records() -> dict[str, list[Any]]:
    """
    Load records from disk or return an empty structure.

    :returns: A dictionary containing lists for each record type.
    :rtype: dict[str, list[Any]]
    """
    if not os.path.exists(DB_FILE):
        return {"client": [], "airline": [], "flight": []}

    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"client": [], "airline": [], "flight": []}


def save_records(db_records: dict[str, list[Any]]) -> None:
    """
    Write the database records to disk.

    :param db_records: The full in-memory database dictionary.
    """
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db_records, f, indent=4)


# ------------------------------
# ERROR RESPONSE HELPER
# ------------------------------
def error_response(message: str) -> dict[str, str]:
    """
    Create a standardised error response.

    :param message: The error message to include.
    :returns: A dictionary containing status, message, and timestamp.
    :rtype: dict[str, str]
    """
    return {
        "status": "error",
        "message": message,
        "timestamp": current_timestamp(),
    }


# ------------------------------
# CRUD FUNCTIONS
# ------------------------------
def create_record(
    db_records: dict[str, list[Any]],
    record_type: str,
    new_record: dict[str, Any],
) -> tuple[str, str]:
    """
    Create a new record and append it to the database.

    :param db_records: The full in-memory database dictionary.
    :param record_type: The type of record ("client", "airline", "flight").
    :param new_record: The incoming record data.

    :returns: A tuple containing (status, message).
    :rtype: tuple[str, str]
    """
    # Assign ID server-side to guarantee uniqueness and prevent
    # client-supplied IDs
    existing = db_records[record_type]
    next_id = 1 if not existing else max(r["id"] for r in existing) + 1

    new_record["id"] = next_id
    db_records[record_type].append(new_record)

    return "success", f"{record_type.capitalize()} #{next_id:02d} created."


def update_record(
    db_records: dict[str, list[Any]],
    record_type: str,
    record_id: int,
    new_record: dict[str, Any],
) -> tuple[str, str]:
    """
    Update an existing record.

    :param db_records: The full in-memory database dictionary.
    :param record_type: The type of record to update.
    :param record_id: The ID of the record to update.
    :param new_record: The updated field values.

    :returns: A tuple containing (status, message).
    :rtype: tuple[str, str]
    """
    for db_record in db_records[record_type]:
        if db_record["id"] == record_id:
            db_record.update(new_record)
            return "success", f"{record_type.capitalize()} #{record_id:02d} updated."

    return "error", f"{record_type.capitalize()} not found."


def delete_record(
    db_records: dict[str, list[Any]],
    record_type: str,
    record_id: int,
) -> tuple[str, str]:
    """
    Delete a record and cascade-delete related flights.

    :param db_records: The full in-memory database dictionary.
    :param record_type: The type of record to delete.
    :param record_id: The ID of the record to delete.

    :returns: A tuple containing (status, message).
    :rtype: tuple[str, str]
    """
    for db_record in db_records[record_type]:
        if db_record["id"] == record_id:
            db_records[record_type].remove(db_record)

            # Cascade-delete flights because these cannot exist without an airline
            if record_type == "airline":
                removed = [f for f in db_records["flight"] if f["airline_id"] == record_id]
                for f in removed:
                    db_records["flight"].remove(f)
                return (
                    "success",
                    f"Airline #{record_id:02d} deleted. {len(removed)} related flights removed.",
                )

            # Cascade-delete flights because these cannot exist without a client
            if record_type == "client":
                removed = [f for f in db_records["flight"] if f["client_id"] == record_id]
                for f in removed:
                    db_records["flight"].remove(f)
                return (
                    "success",
                    f"Client #{record_id:02d} deleted. {len(removed)} related flights removed.",
                )

            return "success", f"{record_type.capitalize()} #{record_id:02d} deleted."

    return "error", f"{record_type.capitalize()} not found."


def search_record(
    db_records: dict[str, list[Any]],
    record_type: str,
    record_id: int,
) -> tuple[str, str]:
    for db_record in db_records[record_type]:
            if db_record["id"] == record_id:
                #return json.dumps(db_record)
                response = json.dumps(db_record)
                print(response)
                return "success", f"{response}"
                #return "success", f"{record_type.capitalize()} #{record_id:02d} updated."

    return "error", f"{record_type.capitalize()} not found."






# ------------------------------
# VALIDATION HELPERS
# ------------------------------
def find_missing_fields(request: dict[str, Any], required_fields: list[str]) -> list[str]:
    """
    Identify missing required fields in a request.

    :param request: The incoming request dictionary.
    :param required_fields: A list of required field names.

    :returns: A list of missing field names.
    :rtype: list[str]
    """

    return [field for field in required_fields if field not in request]


def format_log_request(request: dict[str, Any]) -> str:
    """
    Format a request into a readable log line.

    :param request: The incoming request dictionary.
    :returns: A formatted string describing the request.
    :rtype: str
    """
    action = request.get("action", "?")
    rtype = request.get("record_type", "?")
    rid = request.get("id")

    rid_str = f"#{rid:02d}" if isinstance(rid, int) else ""
    return f"{action} {rtype} {rid_str}".strip()



REQUIRED_FIELDS = {
    "create": ["record_type", "data"],
    "update": ["record_type", "id", "data"],
    "delete": ["record_type", "id"],
    "search": ["record_type", "id"]
}


# ------------------------------
# DISPATCHER
# ------------------------------
def dispatch_request(
    request: dict[str, Any],
    db_records: dict[str, list[Any]],
) -> dict[str, Any]:
    """
    Dispatch a request to the appropriate CRUD function.

    :param request: The incoming request dictionary.
    :param db_records: The full in-memory database dictionary.

    :returns: A response dictionary containing status, message, and optional record.
    :rtype: dict[str, Any]
    """
    action = request["action"]
    record_type = request["record_type"]

    required = REQUIRED_FIELDS[action]
    missing = find_missing_fields(request, required)
    if missing:
        return error_response(f"Missing required fields: {', '.join(missing)}.")

    if action == "create":
        new_record = request["data"]
        status, msg = create_record(db_records, record_type, new_record)

    elif action == "update":
        record_id = request["id"]
        new_record = request["data"]
        status, msg = update_record(db_records, record_type, record_id, new_record)

    elif action == "delete":
        record_id = request["id"]
        status, msg = delete_record(db_records, record_type, record_id)

    elif action == "search":
        record_id = request["id"]
        status, msg = search_record(db_records, record_type, record_id)

    # ADD CALL TO SEARCH FUNCTION HERE

    response: dict[str, Any] = {
        "status": status,
        "message": msg,
        "timestamp": current_timestamp(),
    }

    if action in ("create", "update", "delete") and status == "success":
        save_records(db_records)

    return response


# ------------------------------
# NETWORKING LAYER
# ------------------------------
HOST = "127.0.0.1"
PORT = 60000


def start_server(db_records: dict[str, list[Any]]) -> None:
    """
    Start the TCP server and handle incoming requests.

    :param db_records: The full in-memory database dictionary.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()

        print(f"Server running on {HOST}:{PORT}")

        while True:
            conn, _ = server.accept()
            with conn:
                data = conn.recv(4096)
                if not data:
                    continue

                try:
                    request = json.loads(data.decode("utf-8"))
                except json.JSONDecodeError:
                    conn.sendall(json.dumps(error_response("Invalid JSON format.")).encode("utf-8"))
                    continue

                response = dispatch_request(request, db_records)
                conn.sendall(json.dumps(response).encode("utf-8"))


# ------------------------------
# MAIN ENTRY POINT
# ------------------------------
if __name__ == "__main__":
    records = load_records()
    start_server(records)