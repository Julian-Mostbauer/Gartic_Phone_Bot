from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from drawing import draw_image
from Utils_UI import click_button, select_in_selection


def init_webdriver(profile_path):
    firefox_options = webdriver.FirefoxOptions()
    firefox_profile = webdriver.FirefoxProfile(profile_path)
    firefox_options.profile = firefox_profile
    web_driver = webdriver.Firefox(options=firefox_options)
    return web_driver


driver = init_webdriver(r"C:\Users\julia\AppData\Roaming\Mozilla\Firefox\Profiles\5iuiq8bh.Marionette")

driver.get("https://garticphone.com/de")
action = webdriver.ActionChains(driver)

assert "Gartic Phone – Stille Post" in driver.title

# cookies
driver.implicitly_wait(3)
try:
    click_button(driver, "/html/body/div[1]/div[1]/div[2]/span[1]/a")
except:
    pass

name_field = driver.find_element(By.CLASS_NAME,
                                 "jsx-1347952224 ")
name_field.clear()
name_field.send_keys("test")
name_field.send_keys(Keys.RETURN)

click_button(driver, "/html/body/div/div[2]/div/div/div[4]/div[1]/div[2]/button")  # okay button
driver.implicitly_wait(2)
click_button(driver, "/html/body/div/div[2]/div/div/div[2]/div[2]/div/div[1]/span[2]")  # custom game button

select_in_selection(driver, "UNENDLICH",
                    "/html/body/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div[1]/section/label/select")  # time options

select_in_selection(driver, "NUR ZEICHNEN",
                    "/html/body/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div[2]/section/label/select")  # game order
click_button(driver, "/html/body/div/div[2]/div/div/div[2]/div[2]/span/button")  # start button

click_button(driver, "/html/body/div/div[3]/div/span/button[1]")

driver.implicitly_wait(4)
pencil_size = 5
click_button(driver, f"/html/body/div/div[2]/div/div/div[4]/div[2]/div/div[1]/div[{pencil_size}]")

draw_image("Assets/Triforce.png", driver)

input()
driver.close()
