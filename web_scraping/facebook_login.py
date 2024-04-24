from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchElementException, TimeoutException)


def facebook_login():

    options = Options()
    options.add_argument('--disable-extensions')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-dev-tools')
    options.add_argument('--disable-notifications')
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)

    try:
        driver.get('https://www.facebook.com/')
        driver.implicitly_wait(2)
        driver.find_element(By.ID, 'email').send_keys('*********')
        driver.find_element(By.ID, 'pass').send_keys('*********')
        driver.find_element(By.NAME, 'login').click()
        wait = WebDriverWait(driver, timeout=5)
        wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div['
                                                      '1]/div/div[1]/div/div/div[1]/div/div/div[1]/ul/li/div/a/div['
                                                      '1]/div['
                                                      '2]/div/div/div/div/span/span')))
        driver.save_screenshot('screenshot/facebook.png')
        driver.close()
    except (NoSuchElementException, TimeoutException) as e:
        print(f'An error occur: {e}')


facebook_login()
