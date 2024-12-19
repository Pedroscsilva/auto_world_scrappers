import json

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def accept_cookies(driver):
    '''
    Accepts cookies of page to close the initial popup
    '''

    cookie_id = 'didomi-notice-agree-button'

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((
            By.ID, cookie_id
        ))
    )

    cookie_button = driver.find_element(By.ID, cookie_id)
    cookie_button.click()


def search_company(driver, company):
    '''
    Searches the company name given a string and
    redirects scrapper to searched page
    '''

    # types the company name
    input_element_id = 'uqFieldAC'
    input_element = driver.find_element(By.ID, input_element_id)
    input_element.send_keys(company)

    # ensures search list appears
    search_list_id = 'autoComplete_result_0'
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((
            By.ID, search_list_id
        ))
    )

    # finds the company element and goes to page
    company_element_xpath = '//*[@id="autoComplete_result_0"]/p[2]'
    company_element = driver.find_element(By.XPATH, company_element_xpath)
    company_element.click()


def get_text(driver, by, find_string):
    '''
    Returns the inner text of a given element
    '''

    element = driver.find_element(by=by, value=find_string)
    return element.text


def assemble_data(driver):
    '''
    Returns a dictionary with assembled relevant data
    '''

    name_id = 'identite_deno'
    siren_id = 'identite-siren'
    status_class = 'soBadge'
    last_update_xpath = '//ul[@class="CompanyIdentity__message"]\
                         //li[@class="date"]/span[2]'
    address_xpath = '//td[text()="Adresse postale"]/following-sibling::td/a'
    activity_id = 'ape-histo-description'
    employees_id = 'trancheeff-histo-description'

    data = {
        "name": get_text(driver, By.ID, name_id),
        "siren": get_text(driver, By.ID, siren_id),
        "status": get_text(driver, By.CLASS_NAME, status_class),
        "last_update": get_text(driver, By.XPATH, last_update_xpath),
        "address": get_text(driver, By.XPATH, address_xpath),
        "activity": get_text(driver, By.ID, activity_id),
        "employees": get_text(driver, By.ID, employees_id),
    }

    return data


base_url = 'https://www.societe.com/'

options = Options()
options.add_argument('-headless')

with Firefox(options) as driver:
    driver.get(base_url)

    accept_cookies(driver=driver)
    search_company(driver=driver, company='WKDA France')
    data = assemble_data(driver)

with open('extracted_data/societe_data.json', 'w') as fp:
    json.dump(data, fp, ensure_ascii=False)
