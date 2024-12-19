from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
import pandas as pd

companies_df = pd.DataFrame(
    columns=['name', 'street', 'zip', 'city', 'siren', 'status',
             'description', 'working_hours', 'no_cars']
)


def get_text(driver, by, find_string):
    '''
    Returns the inner text of a given element
    '''
    try:
        element = driver.find_element(by=by, value=find_string)
        return element.text
    except NoSuchElementException:
        return None


def click_btn_if_exists(driver):
    '''
    Checks for the existance of the "Voir plus" button and clicks it if exists.
    Useful for getting the whole description
    '''
    try:
        voir_plus_button = driver.find_element(
            By.XPATH,
            '//button[text()="Voir plus"]'
        )
        voir_plus_button.click()
    except (NoSuchElementException, ElementClickInterceptedException):
        pass


def extract_data(driver, url):
    '''
    Extracts the data of a page from a given URL of leboncoin announcers
    '''
    # Connects to the website and ensures it will not be detected
    driver.uc_open_with_reconnect(url, reconnect_time=3)
    click_btn_if_exists(driver)

    # Paths and classes. Might change.
    name_class = 'text-headline-1'
    street_xpath = '//h2[text()="Adresse"]/ancestor::div[1]\
                    /following-sibling::p'
    zip_xpath = '//h2[text()="Adresse"]/ancestor::div[1]/following-sibling::\
                 div[@class="flex gap-sm"]/p[1]'
    city_xpath = '//h2[text()="Adresse"]/ancestor::div[1]/following-sibling::\
                  div[@class="flex gap-sm"]/p[2]'
    siren_xpath = '//span[@data-qa-id="siren_number"]'
    status_css_selector = '.ml-sm.text-body-2'
    description_xpath = '//div[@data-qa-id="company_description"]/p'
    working_xpath = '//div[@data-qa-id="company_timesheet"]'
    no_cars_xpath = '//a[@data-qa-id="sticky_online_ads"]'

    data = {
        'name': get_text(driver, By.CLASS_NAME, name_class),
        'street': get_text(driver, By.XPATH, street_xpath),
        'zip': get_text(driver, By.XPATH, zip_xpath),
        'city': get_text(driver, By.XPATH, city_xpath),
        'siren': get_text(driver, By.XPATH, siren_xpath),
        'status': get_text(driver, By.CSS_SELECTOR, status_css_selector),
        'description': get_text(driver, By.XPATH, description_xpath),
        'working_hours': get_text(driver, By.XPATH, working_xpath),
        'no_cars': get_text(driver, By.XPATH, no_cars_xpath)
    }

    return data


with open('extracted_data/leboncoin_urls.txt', 'r') as file:
    urls = list(file)
    url_list = [url.rstrip('\n') for url in urls]


with Driver(uc=True, headless=False, size='1366,768') as driver:
    for url in url_list:
        data = extract_data(driver, url)
        print(data['name'])
        companies_df = pd.concat(
            [companies_df, pd.DataFrame(data, index=[0])],
            ignore_index=True
        )

companies_df.to_csv('extracted_data/companies.csv')
