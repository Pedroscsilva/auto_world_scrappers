from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

base_url = 'https://www.societe.com/'

options = Options()
# options.add_argument('-headless')

def accept_cookies(driver):
    # accept cookies to close the popup
    cookie_id = 'didomi-notice-agree-button'

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((
            By.ID, cookie_id
        ))
    )

    cookie_button = driver.find_element(By.ID, cookie_id)
    cookie_button.click()

def search_company(driver, company):
    # type the company name
    input_element_id = 'uqFieldAC'
    input_element = driver.find_element(By.ID, input_element_id)
    input_element.send_keys(company)

    # assures search list appears
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((
            By.ID, 'autoComplete_result_0'
        ))
    )

    # click the company element and goes to page
    company_element = driver.find_element(By.XPATH, '//*[@id="autoComplete_result_0"]/p[2]')
    company_element.click()

with Firefox(options) as driver:
    driver.get(base_url)

    accept_cookies(driver=driver)
    search_company(driver=driver, company='WKDA France')
    time.sleep(65)