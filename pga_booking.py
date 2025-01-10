import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os

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

# Configuration
DESIRED_BAY = "Bay 5"

load_dotenv()

def book_golf_bay():
    # ---------------------------------
    # 1. Set up ChromeDriver and browser
    # ---------------------------------
    chrome_options = Options()
    # Uncomment the line below if you want to run Chrome headlessly (no browser window shown)
    chrome_options.add_argument("--headless")

    # Update the path to where you placed chromedriver.exe
    service = Service("./drivers/chromedriver")  
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # ---------------------------------
        # 2. Log in to the PGA booking portal
        # ---------------------------------
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

        # ---------------------------------
        # 4. Select “Bay 5” from dropdown
        # ---------------------------------
        # Find the dropdown element. You may need to adjust By.ID or By.NAME or By.XPATH.
        # Example (assuming the dropdown has id="ddlFacility"): 
        # Find the bay selection dropdown using its ID
        facility_dropdown = driver.find_element(By.ID, "resource1440")
        select = Select(facility_dropdown)
        select.select_by_value(BAY_MAPPING[DESIRED_BAY])
        time.sleep(2)

        # ---------------------------------
        # 5. Click “Show more results” until 4:30 PM is visible (3 times)
        # ---------------------------------
        # Adjust the element locator for the "Show more results" button.
        # Example XPATH: "//a[@id='showMoreResults']"
        show_more_button = driver.find_element(By.ID, "more_next_avail")

        for _ in range(2):  # click it 3 times
            show_more_button.click()
            time.sleep(2)

        # ---------------------------------
        # 6. Click on the 4:30 PM time slot
        # ---------------------------------
        # You may need to inspect the element to confirm text or ID matches "4:30".
        # Example: if 4:30 is in a <span> or button with text "4:30"
        time_slot_430 = driver.find_element(By.CSS_SELECTOR, "div.next_avail_item[data-time*='1630']")
        time_slot_430.click()
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
        print("Booking process completed successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # ---------------------------------
        # 8. Close the browser
        # ---------------------------------
        time.sleep(5)
        driver.quit()

# For direct script execution
if __name__ == "__main__":
    book_golf_bay()
