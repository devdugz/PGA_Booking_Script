#!/bin/bash

# Set working directory
cd /Users/cdugz/Documents/PGA_Booking_Script_2

# Activate virtual environment
source .venv/bin/activate

# Set timestamp for logging
timestamp=$(date "+%Y-%m-%d %H:%M:%S")

# Run script with logging
echo "[$timestamp] Starting booking script" >> booking.log
python pga_booking.py >> booking.log 2>&1

# Check if script succeeded
if [ $? -eq 0 ]; then
    echo "[$timestamp] Script completed successfully" >> booking.log
else
    echo "[$timestamp] Script failed with error code $?" >> booking.log
fi

# Deactivate virtual environment
deactivate