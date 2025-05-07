import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Import the main function from main.py
from src.main import main

# Run the main function
if __name__ == "__main__":
    main()