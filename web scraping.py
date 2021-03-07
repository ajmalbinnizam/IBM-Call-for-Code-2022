#selenium is an automation framework that allows you to interact with websites
# using something called a webdrive

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://techwithtim.net")

# driver.close()#close the webpage
# print(driver.title)

search = driver.find_element_by_name("s")
search.send_keys("test")
search.send_keys(Keys.RETURN)

print(driver.page_source)


time.sleep(10)
driver.quit()#browser quit