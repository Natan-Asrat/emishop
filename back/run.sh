#!/bin/bash

# Load environment variables from /etc/environment
source /etc/environment

# Activate the virtual environment (optional)
source venv/bin/activate

# Start Daphne (replace with your ASGI app)
exec daphne back.asgi:application --bind 0.0.0.0 --port 8000
