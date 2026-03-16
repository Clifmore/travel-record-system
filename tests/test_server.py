"""
Unit tests for server module.
"""

import unittest
import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.server import (
    create_record, update_record, delete_record, search_record,
    error_response, find_missing_fields
)


class TestServerCRUD(unittest.TestCase):
    """Test the CRUD operations."""
    
    def setUp(self):
        """Set up test database before each test."""
        self.db = {
            "client": [],
            "airline": [],
            "flight": []
        }
        
        # Add a test client
        self.test_client = {
            "Name": "Test Client",
            "City": "London",
            "Country": "UK"
        }
        status, msg = create_record(self.db, "client", self.test_client)
        
        # Add a test airline
        self.test_airline = {
            "Company Name": "Test Airlines"
        }
        status, msg = create_record(self.db, "airline", self.test_airline)
        
        # Add a test flight
        self.test_flight = {
            "client_id": 1,
            "airline_id": 1,
            "Date": "2026-10-12",
            "Start City": "London",
            "End City": "Paris"
        }
        status, msg = create_record(self.db, "flight", self.test_flight)
    
    def test_create_record(self):
        """Test creating a new record."""
        new_client = {"Name": "New Client", "City": "Manchester"}
        status, msg = create_record(self.db, "client", new_client)
        
        self.assertEqual(status, "success")
        self.assertEqual(len(self.db["client"]), 2)
    
    def test_update_record(self):
        """Test updating an existing record."""
        updated_data = {"Name": "Updated Client Name"}
        status, msg = update_record(self.db, "client", 1, updated_data)
        
        self.assertEqual(status, "success")
        self.assertEqual(self.db["client"][0]["Name"], "Updated Client Name")
    
    def test_update_nonexistent_record(self):
        """Test updating a record that doesn't exist."""
        updated_data = {"Name": "Should Fail"}
        status, msg = update_record(self.db, "client", 999, updated_data)
        
        self.assertEqual(status, "error")
    
    def test_delete_record(self):
        """Test deleting a record."""
        status, msg = delete_record(self.db, "client", 1)
        self.assertEqual(status, "success")
        self.assertEqual(len(self.db["client"]), 0)
    
    def test_search_record(self):
        """Test searching for a record."""
        status, result = search_record(self.db, "client", 1)
        self.assertEqual(status, "success")
    
    def test_search_nonexistent(self):
        """Test searching for a nonexistent record."""
        status, msg = search_record(self.db, "client", 999)
        self.assertEqual(status, "error")


class TestServerHelpers(unittest.TestCase):
    """Test helper functions."""
    
    def test_error_response(self):
        """Test error response format."""
        error = error_response("Test error message")
        self.assertEqual(error["status"], "error")
        self.assertEqual(error["message"], "Test error message")
    
    def test_find_missing_fields(self):
        """Test finding missing required fields."""
        request = {"action": "create", "record_type": "client"}
        required = ["action", "record_type", "data"]
        
        missing = find_missing_fields(request, required)
        self.assertEqual(missing, ["data"])


if __name__ == "__main__":
    unittest.main()