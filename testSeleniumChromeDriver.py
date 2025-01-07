import driver as driver
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = r"C:\Users\CRS\Downloads\chromedriver\chromedriver-win64\chromedriver.exe"
service = Service(excecutable_path=PATH)

# set up options to configure Chrome
options = webdriver.ChromeOptions()

# run in headless mode (no GUI)
options.add_argument("--headless=new")

# set window size
options.add_argument("--window-size=1920x1080")

# initialize the WebDriver with the specified options
driver = webdriver.Chrome(service=service)

# navigate to the target website
driver.get('https://www.scrapingcourse.com/ecommerce/?orderby=popularity')

# print("Taking screenshot...")
# take a screenshot and save it to a file
# driver.save_screenshot("WebSiteEcommercePages_screenshot.png")
# print("Screenshot taken successfully.")

#total_links = driver.find_elements(by=By.TAG_NAME, value='a')

links = driver.find_elements(By.XPATH, "//div[contains(@class, 'content-area')]/main/ul/li/a")

#for el in elem:
#    links = el.find_elements(by=By.TAG_NAME, value='a')

for link in links:
    print(link.get_attribute('href'))


time.sleep(1)
driver.quit()

