# 1. First, see what we're working with
dir
dir src

# 2. If my_script.py is your GUI, rename it to main.py (if not already in src)
#    First check if my_script.py exists
if (Test-Path my_script.py) {
    move my_script.py src\main.py
}

# 3. Create tests folder if it doesn't exist
mkdir tests -Force

# 4. Create test files (copy from my previous messages)
notepad tests\test_client.py
# (paste the test code and save)

notepad tests\test_server.py
# (paste the test code and save)

notepad tests\test_gui.py
# (paste the simple test code and save)

notepad tests\__init__.py
# (just save an empty file)