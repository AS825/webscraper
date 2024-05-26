from selenium import webdriver  # type: ignore
from selenium.webdriver.chrome.service import Service  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.chrome.options import Options  # type: ignore
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore
from selenium.webdriver.support import expected_conditions as EC  # type: ignore
from selenium.common.exceptions import ElementClickInterceptedException  # type: ignore
from datetime import datetime
import json
import common  

home = '/home/va63bl8/webscraper/webscraped_data/'

def process_flights(driver, wait):
    rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.row-cont')))
    flight_details = []
    previous_hour = [None]  

    for row in rows:
        details_button = row.find_element(By.CSS_SELECTOR, 'a.toggle-details')
        try:
            details_button.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", details_button)
        
        if not extract_and_print_flight_details(row, previous_hour, flight_details):
            break

    return flight_details

def extract_and_print_flight_details(row, previous_hour, flight_details):
    time_str = row.find_element(By.CSS_SELECTOR, '.col-3.col-md-2.col-lg-1.text-center').text
    current_hour = datetime.strptime(time_str, '%H:%M').time().hour

    if previous_hour[0] is not None and previous_hour[0] == 23 and current_hour < 6:
        return False  

    previous_hour[0] = current_hour  

    flight = row.find_element(By.CSS_SELECTOR, '.col-3.col-lg-3.col-xl-2').text[:6]
    destination = row.find_element(By.CSS_SELECTOR, '.d-lg-none').text
    airplane_type = row.find_element(By.XPATH, ".//dt[contains(text(), 'Flugzeugtyp:')]/following-sibling::dd").text
    status_text = row.find_element(By.CSS_SELECTOR, '.d-none.d-md-block.col-md-3.col-lg-3').text
    formatted_status = extract_status_time(status_text)

    flight_info = {
        "Time": time_str,
        "Flight": flight,
        "From": destination,
        "Status": formatted_status,
        "Plane": airplane_type
    }
    flight_details.append(flight_info)
    print(flight_info)
    return True

def extract_status_time(status_text):
    try:
        time_str = status_text[-5:]
        return datetime.strptime(time_str, '%H:%M').time().strftime('%H:%M')
    except ValueError:
        return status_text
        

def scrape_arrivals():
    website = 'https://www.viennaairport.com/passagiere/ankunft__abflug/ankuenfte'
    driver = common.initialize_driver()
    driver.get(website)
    wait = WebDriverWait(driver, 30)
 
    common.set_cookie_consent(driver)
    driver.get(website)

    try:
        wait = WebDriverWait(driver, 10)
        common.set_airline_filter(driver, wait)
        print("Processing flights...")
        flights = process_flights(driver, wait)
        with open(home + 'flight_data_Arrival.json', 'w') as file:
            json.dump(flights, file, indent=4) 
        print("Flight data saved to 'flight_data_Arrival.json'")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_arrivals()
