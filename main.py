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
from Utils_UI import click_button, select_in_selection, enter_in_textfield, click_button_class
from Hidden import profile_path_firefox

def init_webdriver(profile_path):
    firefox_options = webdriver.FirefoxOptions()
    firefox_profile = webdriver.FirefoxProfile(profile_path)
    firefox_options.profile = firefox_profile
    web_driver = webdriver.Firefox(options=firefox_options)
    return web_driver


def navigate_game_creation(web_driver):
    web_driver.get("https://garticphone.com/de")
    action = webdriver.ActionChains(web_driver)

    assert "Gartic Phone – Stille Post" in web_driver.title

    # cookies
    web_driver.implicitly_wait(3)
    try:
        click_button(web_driver, "/html/body/div[1]/div[1]/div[2]/span[1]/a")
    except:
        pass

    enter_in_textfield(web_driver, "/html/body/div/div[2]/div/div/div[4]/div[1]/div[1]/div[2]/section/span/input",
                       "test")
    driver.implicitly_wait(1)

    click_button(web_driver, "/html/body/div/div[2]/div/div/div[4]/div[1]/div[2]/button")  # okay button
    web_driver.implicitly_wait(2)
    click_button(web_driver, "/html/body/div/div[2]/div/div/div[2]/div[2]/div/div[1]/span[2]")  # custom game button

    select_in_selection(web_driver, "UNENDLICH",
                        "/html/body/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div[1]/section/label/select")  # time options

    select_in_selection(web_driver, "NUR ZEICHNEN",
                        "/html/body/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div[2]/section/label/select")  # game order
    click_button(web_driver, "/html/body/div/div[2]/div/div/div[2]/div[2]/span/button")  # start button

    click_button(web_driver, "/html/body/div/div[3]/div/span/button[1]")


driver = init_webdriver(profile_path_firefox)
navigate_game_creation(driver)

driver.implicitly_wait(4)

pencil_size = 4
click_button(driver, f"/html/body/div/div[2]/div/div/div[4]/div[2]/div/div[1]/div[{pencil_size}]")
draw_image("Assets/kirby.png", driver, pencil_size)

input()
driver.close()
