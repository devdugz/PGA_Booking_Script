# PGA_Booking_Script

# PGA Golf Bay Booking Automation

Automated booking system for PGA golf practice bays using Python and Selenium WebDriver.

## Features

- Automated booking for multiple golf bays
- Configurable time slot preferences
- Multi-bay fallback system
- 24/7 scheduling with configurable intervals
- Detailed logging and monitoring

## Tech Stack

- Python 3.x
- Selenium WebDriver
- ChromeDriver
- APScheduler
- python-dotenv

## Installation

1. Clone repository

```bash
git clone <repository-url>
cd PGA_Booking_Script_2
```

## Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install dependencies

```bash
pip install selenium python-dotenv apscheduler
```

## Configure ChromeDriver

```bash
brew install chromedriver
```

# Configuration

- Create .env file:

```
PGA_USERNAME=your_username
PGA_PASSWORD=your_password
```

- Configure bay preferences in pga_booking.py

```
PRIMARY_BAY = "Bay 5"
BACKUP_BAY_1 = "Bay 7"
BACKUP_BAY_2 = "Any Bay"
```

## Usage

- Run the scheduler (Make sure your in your virutal environment):

```
python3 scheduler.py
```

### The script will:

- Check available time slots every 5 minutes
- Attempt bookings in preferred bays
- Log all activities and booking attempts
- Continue running after successful bookings

## Logging

### Log Locations

- Console output: Real-time scheduling and booking updates
- `/logs/booking.log`: Detailed booking attempts and results
  - Bay selection attempts
  - Time slot searches
  - Booking confirmations
  - Error messages

## Troubleshooting

- Common log messages:

  - Successfully booked {bay}: Confirmed booking
  - No slots available for {bay}: Bay unavailable
  - No more pages to check for {bay}: All slots checked
  - Error while trying to book {bay}: Booking attempt failed

- For debugging:
  - Check ChromeDriver status
  - Verify network connectivity
  - Confirm login credentials
  - Review bay availability

## License

This project is licensed under the MIT License - see the LICENSE file for details.
