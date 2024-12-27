from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = r"C:\Users\CRS\Downloads\chromedriver\chromedriver-win64\chromedriver.exe"
service = Service(excecutable_path=PATH)
#driver = webdriver.Chrome(service=service)
#driver.get("https://www.google.al/")


# set up options to configure Chrome
options = webdriver.ChromeOptions()

# run in headless mode (no GUI)
options.add_argument("--headless=new")

# set window size
options.add_argument("--window-size=1920x1080")

# initialize the WebDriver with the specified options
driver = webdriver.Chrome(service=service)

# navigate to the target website
driver.get("https://www.scrapingcourse.com/ecommerce/")

print("Taking screenshot...")

# take a screenshot and save it to a file
driver.save_screenshot("WebSiteEcommercePages_screenshot.png")

print("Screenshot taken successfully.")


time.sleep(10)
driver.quit()
exit()
