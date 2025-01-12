import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
import logging
import sys

BAY_MAPPING = {
    "Bay 1": "4008",
    "Bay 2": "4009",
    "Bay 3": "4010",
    "Bay 4": "4011",
    "Bay 5": "4012",
    "Bay 6": "4013",
    "Bay 7": "4014",
    "Bay 8": "4015"
}

# Configuration - primary and backup bays
PRIMARY_BAY = "Bay 5"
BACKUP_BAY = "Bay 7"  # Add your preferred backup bay

# Create logs directory if it doesn't exist
os.makedirs('/Users/cdugz/Documents/PGA_Booking_Script_2/logs', exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('/Users/cdugz/Documents/PGA_Booking_Script_2/logs/booking.log'),
        logging.StreamHandler(sys.stdout)
    ],
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

load_dotenv()

def try_book_bay(driver, bay_name):
    """Attempt to book a specific bay"""
    logger.info(f"Attempting to book {bay_name}")
    
    facility_dropdown = driver.find_element(By.ID, "resource1440")
    select = Select(facility_dropdown)
    select.select_by_value(BAY_MAPPING[bay_name])
    time.sleep(2)
    
    # Search for desired time slot
    for _ in range(4):
        try:
            time_slot = driver.find_element(By.CSS_SELECTOR, "div.next_avail_item[data-time*='1630']")
            time_slot.click()
            logger.info(f"Successfully found time slot for {bay_name}")
            return True
        except:
            show_more_button = driver.find_element(By.ID, "more_next_avail")
            show_more_button.click()
            time.sleep(2)
    return False

def book_golf_bay():
    logger.info("Starting golf bay booking process")
    
    chrome_options = Options()
    # chrome_options.add_argument("--headless=new")
    
    try:
        logger.info("Initializing Chrome driver")
        service = Service("./drivers/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        logger.info("Attempting login")
        driver.get("https://clients.uschedule.com/pgatsmilwaukee/account/login")
        time.sleep(2)

        # Enter your login credentials
        # (Update the IDs or XPaths as needed if they differ)
        driver.find_element(By.ID, "UserName").send_keys(os.getenv('PGA_USERNAME'))
        driver.find_element(By.ID, "Password").send_keys(os.getenv('PGA_PASSWORD'))
        driver.find_element(By.ID, "loginBtn").click()  # Might differ (e.g., "login-button")

        time.sleep(3)  # Give time for login to complete

        # ---------------------------------
        # 3. Navigate to the booking page
        # ---------------------------------
        driver.get("https://clients.uschedule.com/pgatsmilwaukee/booking")
        time.sleep(3)

        # Try primary bay first
        if not try_book_bay(driver, PRIMARY_BAY):
            logger.info(f"No slots available for {PRIMARY_BAY}, trying {BACKUP_BAY}")
            if not try_book_bay(driver, BACKUP_BAY):
                logger.error("Could not find desired time slot in any bay")
                raise Exception("Desired time slot not found")

        time.sleep(2)


        # ---------------------------------
        # 7. Click "Confirm Facility"
        # ---------------------------------
        # Adjust the element locator if needed.
        confirm_button = driver.find_element(By.ID, "book")
        confirm_button.click()
        time.sleep(3)

        #Confirm Booking in Modal
        accept_location = driver.find_element(By.ID, "accept_location")
        accept_location.click()
        time.sleep(3)

        # You can add any final steps or checks here
        logger.info("Booking process completed successfully!")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        logger.info("Closing browser")
        time.sleep(5)
        driver.quit()

# For direct script execution
if __name__ == "__main__":
    try:
        book_golf_bay()
    except Exception as e:
        logger.error(f"Script failed: {str(e)}")
        sys.exit(1)
