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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

BAY_MAPPING = {
    "Any Bay": "-1",
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
BACKUP_BAY_1 = "Bay 7"  # First backup bay
BACKUP_BAY_2 = "Any Bay"  # Second backup bay

# Add at top with other constants

TIME_SLOTS = ['1630', '1700', '1715', '1730', '1745', '1800', '1815']  # 4:30, 5:00, 5:15, 5:30, 5:45, 6:00, 6:15

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
    successful_bookings = []
    
    try:
        # Select 30-minute lesson
        # wait = WebDriverWait(driver, 10)
        # choose_lesson = wait.until(
        #     EC.presence_of_element_located((By.ID, "select_service"))
        # )
        # select = Select(choose_lesson)
        # select.select_by_value("38507")
        # time.sleep(2)

        wait = WebDriverWait(driver, 10)
        facility_dropdown = wait.until(
            EC.presence_of_element_located((By.ID, "resource1440"))
        )
        select = Select(facility_dropdown)
        select.select_by_value(BAY_MAPPING[bay_name])
        time.sleep(2)
        
        # Search for desired time slots
        for _ in range(4):
            for time_slot_value in TIME_SLOTS:
                try:
                    time.sleep(0.5)
                    logger.info(f"Searching for time slot {time_slot_value} in {bay_name}")
                    time_slot = driver.find_element(By.CSS_SELECTOR, f"div.next_avail_item[data-time*='{time_slot_value}']")
                    # time_slot = wait.until(
                    #     EC.element_to_be_clickable((By.CSS_SELECTOR, f"div.next_avail_item[data-time*='{time_slot_value}']"))
                    # )
                    time_slot.click()
                    logger.info(f"Found time slot {time_slot_value} for {bay_name}, attempting confirmation")
                    
                    # Confirm booking
                    try:
                        confirm_button = driver.find_element(By.ID, "book")
                        driver.execute_script("arguments[0].scrollIntoView(true);", confirm_button)
                        time.sleep(1)
                        
                        wait = WebDriverWait(driver, 10)
                        clickable_button = wait.until(EC.element_to_be_clickable((By.ID, "book")))
                        clickable_button.click()
                        
                        # Accept location with verification
                        accept_button = wait.until(EC.presence_of_element_located((By.ID, "accept_location")))
                        driver.execute_script("arguments[0].scrollIntoView(true);", accept_button)
                        time.sleep(1)

                        accept_button = wait.until(EC.element_to_be_clickable((By.ID, "accept_location")))
                        accept_button.click()
                        time.sleep(2)  # Wait for confirmation

                        successful_bookings.append(time_slot_value)
                        logger.info(f"Successfully booked {time_slot_value} for {bay_name}")
                        time.sleep(2)
                        driver.get("https://clients.uschedule.com/pgatsmilwaukee/booking")
                        time.sleep(2)
                        continue  # Continue checking other time slots
                        
                    
                    except Exception as e:
                        logger.error(f"Failed to confirm booking: {str(e)}")
                        continue
                except:
                    continue

            # If no time slots found, try next page
            try:
                time.sleep(1)
                show_more_button = driver.find_element(By.ID, "more_next_avail")
                show_more_button.click()
                time.sleep(1)
            except:
                logger.info(f"No more pages to check for {bay_name}")
                break
        
        if successful_bookings:
            logger.info(f"Successfully booked {len(successful_bookings)} time slots for {bay_name}: {', '.join(successful_bookings)}")
            return True
        else:
            logger.info(f"No available slots found for {bay_name}")
            return False
        
    except Exception as e:
        logger.error(f"Error while trying to book {bay_name}: {str(e)}")
        return False

def book_golf_bay():
    logger.info("Starting golf bay booking process")
    successful_bays = []
    
    #Chrome Driver Settings:
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Basic headless mode
    chrome_options.add_argument('--disable-gpu')  # Required for headless
    chrome_options.add_argument('--no-sandbox')  # Required for headless
    chrome_options.add_argument('--disable-dev-shm-usage')  # Required for headless
    chrome_options.add_argument('--window-size=1920,1080')  # Set window size
    chrome_options.add_argument('--disable-notifications')  # Disable notifications
    chrome_options.add_argument('--disable-extensions')  # Disable extensions
    
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
        # if try_book_bay(driver, PRIMARY_BAY):
        #     logger.info(f"Successfully booked {PRIMARY_BAY}")
        #     return True
        # else:
        #     logger.info(f"No slots available for {PRIMARY_BAY}, trying {BACKUP_BAY_1}")
        #     if try_book_bay(driver, BACKUP_BAY_1):
        #         logger.info(f"Successfully booked {BACKUP_BAY_1}")
        #         return True
        #     else:
        #         logger.info(f"No slots available for {BACKUP_BAY_1}, trying {BACKUP_BAY_2}")
        #         if try_book_bay(driver, BACKUP_BAY_2):
        #             logger.info(f"Successfully booked {BACKUP_BAY_2}")
        #             return True
        #         else:
        #             logger.error("Could not find desired time slot in any bay")
        #             return False
        if try_book_bay(driver, PRIMARY_BAY):
            successful_bays.append(PRIMARY_BAY)
            logger.info(f"Successfully booked {PRIMARY_BAY}")
        else:
            logger.info(f"No slots available for {PRIMARY_BAY}")
            
        # First Backup Bay
        if try_book_bay(driver, BACKUP_BAY_1):
            successful_bays.append(BACKUP_BAY_1)
            logger.info(f"Successfully booked {BACKUP_BAY_1}")
        else:
            logger.info(f"No slots available for {BACKUP_BAY_1}")
            
        # Second Backup Bay
        if try_book_bay(driver, BACKUP_BAY_2):
            successful_bays.append(BACKUP_BAY_2)
            logger.info(f"Successfully booked {BACKUP_BAY_2}")
        else:
            logger.info(f"No slots available for {BACKUP_BAY_2}")
        
        # Return true if any bay was booked
        if successful_bays:
            logger.info(f"Successfully booked bays: {', '.join(successful_bays)}")
            return True
        else:
            logger.error("Could not find desired time slot in any bay")
            return False
            
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return False
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
