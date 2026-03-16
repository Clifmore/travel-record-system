"""
Unit tests for client module.
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.client import (
    build_client_dict, build_airline_dict, build_flight_dict,
    handle_response
)
from datetime import date


class TestClientBuilders(unittest.TestCase):
    """Test the dictionary builder functions."""
    
    def test_build_client_dict(self):
        """Test that client dictionary is built correctly."""
        client = build_client_dict(
            "John Doe",
            "123 Main St",
            "Apt 4B",
            "",
            "London",
            "Greater London",
            "SW1A 1AA",
            "UK",
            "07123456789"
        )
        
        self.assertEqual(client["Name"], "John Doe")
        self.assertEqual(client["Address Line 1"], "123 Main St")
        self.assertEqual(client["City"], "London")
        self.assertEqual(client["Country"], "UK")
    
    def test_build_airline_dict(self):
        """Test that airline dictionary is built correctly."""
        airline = build_airline_dict("British Airways")
        self.assertEqual(airline["Company Name"], "British Airways")
    
    def test_build_flight_dict(self):
        """Test that flight dictionary is built correctly."""
        flight = build_flight_dict(
            1, 2, "2026-10-12", "London", "Paris"
        )
        self.assertEqual(flight["client_id"], 1)
        self.assertEqual(flight["airline_id"], 2)
        self.assertEqual(flight["Start City"], "London")
        self.assertEqual(flight["End City"], "Paris")


class TestClientResponseHandler(unittest.TestCase):
    """Test the response handling functions."""
    
    def test_handle_response_success(self):
        """Test handling a success response."""
        response = {"status": "success", "message": "Record created"}
        result = handle_response(response)
        self.assertTrue(result)
    
    def test_handle_response_error(self):
        """Test handling an error response."""
        response = {"status": "error", "message": "Record not found"}
        result = handle_response(response)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()