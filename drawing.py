from typing import Dict, Tuple, Union
import numpy as np
from PIL import Image
import time
import sys
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utils_UI import click_button

ColorName = {
    (0, 0, 0): "black",
    (102, 102, 102): "gray_dark",
    (0, 80, 205): "blue_dark",
    (255, 255, 255): "white",
    (170, 170, 170): "gray_light",
    (38, 201, 255): "blue_light",
    (1, 116, 32): "green_dark",
    (153, 0, 0): "red_dark",
    (150, 65, 18): "brown_dark",
    (17, 176, 60): "green_light",
    (255, 0, 19): "red_light",
    (255, 120, 41): "orange",
    (176, 112, 28): "yellow_dark",
    (153, 0, 78): "purple",
    (203, 90, 87): "red_weak_dark",
    (255, 193, 38): "yellow_light",
    (255, 0, 143): "pink",
    (254, 175, 168): "red_weak_light"
}


def closest_color(rgb: Tuple[int, int, int]) -> str:
    global ColorName

    def calculate_distance(color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> float:
        return sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2))

    smallest = ["name", 2 ** 32 - 1]
    for color in ColorName:
        distance = calculate_distance(rgb, color)
        if distance <= smallest[1]:
            smallest[1] = distance
            smallest[0] = ColorName[color]

    return smallest[0]


def image_to_numpy_array(img):
    img_array = np.array(img)
    return img_array


def flip_mirror(img):
    mirrored_img = img.transpose(Image.FLIP_LEFT_RIGHT)
    rotated_img = mirrored_img.transpose(Image.ROTATE_90)
    return rotated_img


def find_key_with_most_values(dic):
    max_len = 0
    max_key = ""
    for key in dic:
        if len(dic[key]) > max_len:
            max_len = len(dic[key])
            max_key = key

    return max_key


def color_to_xpath(color: str):
    match color:
        case "black":
            return "/html/body/div/div[2]/div/div/div[3]/div/div[1]/section[2]/div[1]"
        case "gray_dark":
            return "/html/body/div/div[2]/div/div/div[3]/div/div[1]/section[2]/div[2]"
        case "blue_dark":
            return "/html/body/div/div[2]/div/div/div[3]/div/div[1]/section[2]/div[3]"
        case "white":
            return "/html/body/div/div[2]/div/div/div[3]/div/div[1]/section[2]/div[4]"
        case "gray_light":
            return "/html/body/div/div[2]/div/div/div[3]/div/div[1]/section[2]/div[5]"
        case "blue_light":
            return "/html/body/div/div[2]/div/div/div[3]/div/div[1]/section[2]/div[6]"
        case "green_dark":
            return "/html/body/div/div[2]/div/div/div[3]/div/div[1]/section[2]/div[7]"
        case "red_dark":
            return "/html/body/div/div[2]/div/div/div[3]/div/div[1]/section[2]/div[8]"
        case "brown_dark":
            return "/html/body/div/div[2]/div/div/div[3]/div/div[1]/section[2]/div[9]"
        case "green_light":
            return "/html/body/div/div[2]/div/div/div[3]/div/div[1]/section[2]/div[10]"
        case "red_light":
            return "/html/body/div/div[2]/div/div/div[3]/div/div[1]/section[2]/div[11]"
        case "orange":
            return "/html/body/div/div[2]/div/div/div[3]/div/div[1]/section[2]/div[12]"
        case "yellow_dark":
            return "/html/body/div/div[2]/div/div/div[3]/div/div[1]/section[2]/div[13]"
        case "purple":
            return "/html/body/div/div[2]/div/div/div[3]/div/div[1]/section[2]/div[14]"
        case "red_weak_dark":
            return "/html/body/div/div[2]/div/div/div[3]/div/div[1]/section[2]/div[15]"
        case "yellow_light":
            return "/html/body/div/div[2]/div/div/div[3]/div/div[1]/section[2]/div[16]"
        case "pink":
            return "/html/body/div/div[2]/div/div/div[3]/div/div[1]/section[2]/div[17]"
        case "red_weak_light":
            return "/html/body/div/div[2]/div/div/div[3]/div/div[1]/section[2]/div[18]"


def connect_points_to_lines(points_dict):
    lines_dict = {}
    for color in points_dict:
        original = points_dict[color]
        result = []
        
        lines_dict[color] = result
    return lines_dict


def prepare_instructions(file_path):
    image_array = image_to_numpy_array(flip_mirror(Image.open(file_path)))
    required_pos = defaultdict(list)

    for y in range(image_array.shape[1]):
        for x in range(image_array.shape[0]):
            [r, g, b] = image_array[x][y]
            color = closest_color((r, g, b))
            required_pos[color].append([x, y])

    print(connect_points_to_lines(required_pos))

    return required_pos


def draw_image(file_path, driver, pencil_size):
    required_pos = prepare_instructions(file_path)

    actions = ActionChains(driver)
    color_palett = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/div")
    canvas = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[4]/div[1]/div[2]/div/canvas[3]")

    palett_size = color_palett.size
    canvas_size = canvas.size

    most_common_color = find_key_with_most_values(required_pos)

    click_button(driver, "/html/body/div/div[2]/div/div/div[5]/div/div[8]")  # bucket tool
    click_button(driver, color_to_xpath(most_common_color))
    actions.move_to_element_with_offset(canvas, 0, 0).click().perform()  # fill background with most common color

    click_button(driver, "/html/body/div/div[2]/div/div/div[5]/div/div[1]")  # pen tool

    print(most_common_color)

    required_space = ((3 + 5*pencil_size) // 2) * 0.7

    for color in required_pos:
        print(color)
        amount = len(required_pos[color])

        if color == most_common_color:
            continue

        click_button(driver, color_to_xpath(color))

        i = 1
        for position in required_pos[color]:
            print(f"{i}/{amount}")
            i += 1

            pos_x = (position[0] * required_space) - canvas_size["width"] / 2
            pos_y = (position[1] * required_space) - canvas_size["height"] / 2
            try:
                actions.move_to_element_with_offset(canvas, pos_x, pos_y).click().perform()
            except:
                pass