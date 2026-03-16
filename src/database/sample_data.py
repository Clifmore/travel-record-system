"""
Sample data for the application.
Simulates a database.
"""

# Geography data for address selection
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

# Time options for flight selection
TIMES = [f"{h:02d}:{m:02d}" for h in range(0,24) for m in (0,15,30,45)]

# Track recently deleted records
recently_deleted = []