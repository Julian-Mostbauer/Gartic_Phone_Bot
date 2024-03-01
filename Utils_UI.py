from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def click_button(web_driver, xpath: str):
    button = web_driver.find_element(By.XPATH, xpath)
    WebDriverWait(web_driver, 1000000).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()


def click_button_class(web_driver, class_name: str):
    button = web_driver.find_element(By.CLASS_NAME, class_name)
    WebDriverWait(web_driver, 1000000).until(EC.element_to_be_clickable((By.CLASS_NAME, class_name))).click()


def select_in_selection(web_driver, search_text, xpath: str):
    selection = Select(web_driver.find_element(By.XPATH, xpath))
    web_driver.implicitly_wait(1)
    selection.select_by_visible_text(search_text)


def enter_in_textfield(web_driver, xpath, text):
    field = web_driver.find_element(By.XPATH, xpath)
    field.clear()
    field.send_keys(text)
    field.send_keys(Keys.RETURN)
