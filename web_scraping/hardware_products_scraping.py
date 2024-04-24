import re
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (NoSuchElementException, TimeoutException)


def save_data(file_path, headers, data):
    file = open(file_path, 'w')
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)
    file.close()


def hardware_products():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-extensions')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-tools')
    options.add_argument('--disable-notifications')
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)

    try:
        driver.get('https://www.okdam.com/category/hardware-products')
        driver.implicitly_wait(2)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        products = soup.find_all('div', attrs={'class': 'product-box'})
        product_list = []
        for product in products:
            product_name = product.find('div', attrs={'class': 'product_name-cat'}).text
            rating = re.findall(r'\d+', product.find('span', attrs={'class': 'rating-count'}).text)
            price = re.findall(r'\d+', product.find('span', attrs={'class': 'og-price'}).text)
            data = {
                'Product Name': product_name,
                'Rating': ''.join(rating),
                'Price(NPR)': int(''.join(price))
            }
            product_list.append(data)
        save_data('result/product_details.csv', ['Product Name', 'Rating', 'Price(NPR)'], product_list)
    except (NoSuchElementException, TimeoutException) as e:
        print(f'An error occur: {e}')


hardware_products()
