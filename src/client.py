"""
Client module for the record management database system.

This module constructs JSON requests and sends them to the server. It 
provides helper functions for building record dictionaries, formatting 
CRUD requests, and handling server responses.
"""

import socket
import json
from typing import Any
from datetime import date

HOST = "127.0.0.1"
PORT = 60000

def send_request_to_server(request: dict[str, Any]) -> Any:
    """
    Send a JSON request to the server and return the JSON response.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(json.dumps(request).encode("utf-8"))
        response = s.recv(4096)
        decoded_response = json.loads(response.decode())
        return decoded_response


def handle_response(response: dict[str, Any]) -> bool:
    """
    Handle a server response.

    Returns True if the operation succeeded.
    Returns False if an error occurred (and prints the message).
    """
    if response["status"] == "error":
        print(f"ERROR: {response['message']}")
        return False
    return True


def send_action(action: str, record_type: str, **kwargs) -> dict[str, Any] | None:
    """
    Build and send a request for any CRUD action.

    :param action: The action to perform (create, update, delete).
    :param record_type: The type of record (client, flight, booking, airline).
    :param kwargs: Additional fields such as id=..., data=...
    """
    request = {
        "action": action,
        "record_type": record_type,
    }
    request.update(kwargs)

    response = send_request_to_server(request)

    if not handle_response(response):
        return None

    return response


# ------------------------------------------------------------
#  CRUD wrappers
# ------------------------------------------------------------

def create_record(record_type: str, data: dict[str, Any]):
    """Send a CREATE request to the server."""
    return send_action("create", record_type, data=data)


def update_record(record_type: str, record_id: int, data: dict[str, Any]):
    """Send an UPDATE request to the server."""
    return send_action("update", record_type, id=record_id, data=data)


def delete_record(record_type: str, record_id: int):
    """Send a DELETE request to the server."""
    return send_action("delete", record_type, id=record_id)


def search_record(record_type: str, record_id: int):
    """Send a SEARCH request to the server."""
    return send_action("search", record_type, id=record_id)


# ------------------------------
# DICTIONARY BUILDERS
# ------------------------------

def build_client_dict(
        name: str,
        address1: str,
        address2: str,
        address3: str,
        city: str,
        state: str,
        zip_code: str,
        country: str,
        phone_number: str
    ) -> dict[str, Any]:
    """
    Create a dictionary representing a client record.
    """
    return {
        "Name": name,
        "Address Line 1": address1,
        "Address Line 2": address2,
        "Address Line 3": address3,
        "City": city,
        "State": state,
        "Zip Code": zip_code,
        "Country": country,
        "Phone Number": phone_number
    }


def build_airline_dict(company_name: str) -> dict[str, str]:
    """
    Create a dictionary representing an airline record.
    """
    return {
        "Company Name": company_name
    }


def build_flight_dict(
        client_id: int,
        airline_id: int,
        flight_date: str,
        start_city: str,
        end_city: str
    ) -> dict[str, Any]:
    """
    Create a dictionary representing a flight record.
    """
    return {
        "client_id": client_id,
        "airline_id": airline_id,
        "Date": flight_date,
        "Start City": start_city,
        "End City": end_city
    }