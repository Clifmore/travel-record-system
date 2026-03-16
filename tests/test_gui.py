"""
Basic tests for GUI components.
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestGUIImports(unittest.TestCase):
    """Test that GUI can be imported."""
    
    def test_tkinter_available(self):
        """Test that tkinter is installed."""
        try:
            import tkinter
            self.assertTrue(True)
        except ImportError:
            self.fail("tkinter is not available")


if __name__ == "__main__":
    unittest.main()