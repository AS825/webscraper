from selenium import webdriver  # type: ignore
from selenium.webdriver.chrome.service import Service  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.chrome.options import Options  # type: ignore
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore
from selenium.webdriver.support import expected_conditions as EC  # type: ignore
from selenium.common.exceptions import ElementClickInterceptedException  # type: ignore
from datetime import datetime
import urllib.parse


def initialize_driver():
    path_to_chromedriver = r'C:\Users\VA63BL8\OneDrive - Porsche Holding Salzburg\Desktop\SACIPI\chromedriver-win64\chromedriver.exe'
    service = Service(executable_path=path_to_chromedriver)
    options = Options()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def set_cookies(driver, cookies):
    for cookie in cookies:
        driver.add_cookie(cookie)

def set_cookie_consent(driver):
    cookie_value = "{stamp:%27mLfy49YPYoIPpeOuD8V0H5pBOXaktuVW9pQtgdjVg3H9+6xF18KQHQ==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1716365377864%2Cregion:%27at%27}"
    decoded_cookie_value = urllib.parse.unquote(cookie_value)
    
    cookie_dict = {
        'name': 'CookieConsent',
        'value': decoded_cookie_value,
        'domain': 'www.viennaairport.com',
        'path': '/'
    }
    driver.add_cookie(cookie_dict)

def accept_cookies(driver, wait):
    try:
        overlay = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "CybotCookiebotDialogBodyUnderlay")))
        if overlay:
            driver.execute_script("document.getElementById('CybotCookiebotDialogBodyUnderlay').style.display = 'none';")
        cookie_button = wait.until(EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")))
        cookie_button.click()
    except TimeoutException:
        print("Cookie consent dialog did not disappear.")

def set_airline_filter(driver, wait):
    form_group = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//label[@for='airline' and contains(text(), 'Fluglinie')]/following-sibling::div")))
    dropdown = form_group.find_element(By.CSS_SELECTOR, "a.chosen-single")
    
    try:
        dropdown.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
        dropdown.click()

    option = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Austrian')]")))
    option.click()
