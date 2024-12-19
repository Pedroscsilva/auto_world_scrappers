import time
from selenium.webdriver.common.by import By
from seleniumbase import Driver


def extract_urls(driver, amount):
    '''
    Extract an indicated amount of URLs from leboncoin vehicules pages
    '''

    base_url = 'https://www.leboncoin.fr/boutiques/vehicules/ \
                toutes_categories/p-'
    urls = []
    current_page = 1

    while len(urls) < amount:
        driver.uc_open_with_reconnect(f'{base_url}{current_page}',
                                      reconnect_time=6)
        time.sleep(6)

        article_links = driver.find_elements(By.XPATH, "//article//a[@href]")
        for link in article_links:
            urls.append(link.get_attribute('href'))
        current_page += 1

    if len(urls) > amount:
        urls = urls[:amount]

    return urls


with Driver(uc=True, headless=False) as driver:
    urls = extract_urls(driver, 2000)

with open('extracted_data/leboncoin/leboncoin_urls.txt', 'w') as fp:
    fp.write('\n'.join(str(urls) for urls in urls))
