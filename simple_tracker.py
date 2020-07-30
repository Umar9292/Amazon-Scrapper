from selenium.webdriver.common.keys import Keys
import time
from amazon_config import (
    get_chrome_web_driver,
    get_web_driver_options,
    set_ignore_certificate_error,
    set_browser_as_incognito,
    NAME,
    CURRENCY,
    FILTERS,
    BASE_URL,
    DIRECTORY
)


class GenerateReport:
    def __init__(self):
        pass


class AmazonAPI:
    def __init__(self, search_term, filters, base_url, currency):
        self.base_url = base_url
        self.search_term = search_term
        options = get_web_driver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.driver = get_chrome_web_driver(options)
        self.currency = currency
        self.price_filter = f"&rh=p_36%3A{filters['min']}00-{filters['max']}00"

    def run(self):
        print('Starting Script....')
        print(f"Looking for {self.search_term}")
        link = self.get_product_links()
        time.sleep(3)
        if not links:
            print('Stopped Script..')
            return
        print(f"Got {len(links)} for our product...")
        print("Getting info about products...")
        products = self.get_product_info(links)
        self.driver.quit()

    def get_products_info(self, links):
        asins = self.get_asins(links)
        products = []
        for asin in asins:
            products = self.get_single_product_info(asin)

    def get_single_product_info(self, asin):
        print(f"Product ID: {asin} - getting data...")
        product_shorten_url = self.shorten_url(asin)
        self.driver.get(f'{product_short_url}?language=en_GB')
        time.sleep(2)
        title = self.get_title()
        seller = ''
        price = ''

    def get_title(self):
        try:
            return self.driver.find_element_by_id('productTitle')
        except Exception as e:
            print(e)
            print(
                f"Cannot get the title of a product = {self.driver.current_url}")
            return None

    def shorten_url(self, asin):
        return self.base_url + 'dp/' + asin

    def get_asins(self, links):
        return [self.get_asin(link) for link in links]

    def get_asin(self, asin):
        return product_link[product_link.find('/dp/') + 4:product_link.find('/ref')]

    def get_product_links(self):
        self.driver.get(self.base_url)
        element = self.driver.find_element_by_id("twotabsearchtextbox")
        element.send_keys(self.search_term)
        element.send_keys(Keys.ENTER)
        time.sleep(2)
        self.driver.get(f"{self.driver.current_url}{self.price_filter}")
        time.sleep(2)
        result_list = self.driver.find_element_by_class_name('s-result-list')

        links = []
        try:
            results = result_list[0].find_elements_by_xpath(
                "//div/span/div/div/dic[2]/div[2]/div/div[1]/div/div/div[1]/div/div/div[1]/h2/a"
            )
            links = [link.get_attribute('href') for link in results]
            return links
        except Exception as e:
            print('Did not found ant products...')
            print(e)
            return links


if __name__ == '__main__':
    amazon = AmazonAPI(NAME, FILTERS, BASE_URL, CURRENCY)
    amazon.run()
