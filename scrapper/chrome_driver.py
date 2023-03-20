from selenium import webdriver
import os

def get_page(url):
    chrome_options = webdriver.ChromeOptions()
    # Line below was used on Heroku
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    driver.get(url)
    page = driver.page_source
    driver.close()
    return page