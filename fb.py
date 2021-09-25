import time
import os

from hepler import remove_emojis, download_image

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def set_chrome_options():
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    if use docker: uncomment chrome_options.add_argument('--headless')
    """
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    return chrome_options


def init_chrome():
    """
    if use docker: set executable_path=/usr/local/bin/chromedriver
    """
    chrome_options = set_chrome_options()
    driver = webdriver.Chrome(
        chrome_options=chrome_options,
        executable_path="/home/quanghuy/Desktop/facebook-group/chromedriver",
    )
    driver.implicitly_wait(20)

    driver.get("https://www.facebook.com/")

    return driver


def login_fb(account):
    driver = init_chrome()

    email = driver.find_element_by_xpath('.//*[@id="email"]')
    email.send_keys(account["gmail"])
    time.sleep(5)
    password = driver.find_element_by_xpath('.//*[@id="pass"]')
    password.send_keys(account["password"])
    time.sleep(5)

    login = driver.find_element_by_name("login")
    login.click()

    return driver


def post_fb(driver, contents):
    time.sleep(15)
    group = "https://www.facebook.com/groups/964820740753433"

    # Post on each group
    driver.get(group)
    time.sleep(5)

    for content in contents:

        if "full_picture" not in content:

            create_post = driver.find_element_by_xpath(
                "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div[1]/div[1]/div/div/div/div[1]/div"
            ).find_element_by_xpath("..")
            create_post.click()
            time.sleep(15)

            post_box = driver.find_element_by_xpath(
                "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div/div/div/div"
            ).find_element_by_xpath("..")
            post_box.send_keys(remove_emojis(content["message"]))
            time.sleep(15)

            if len(content["message"].split(" ")) <= 25:
                post_style = driver.find_element_by_xpath(
                    "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div[2]/div/div/span/img"
                ).find_element_by_xpath("..")
                post_style.click()
                time.sleep(15)

                choose_style = driver.find_element_by_xpath(
                    "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div/div[4]/div/div"
                ).find_element_by_xpath("..")
                choose_style.click()
                time.sleep(15)

        else:
            name = "sample.png"
            download_image(name, content["full_picture"])
            time.sleep(15)

            post_image = driver.find_element_by_xpath("//input[@type='file']")
            post_image.send_keys(os.path.abspath("image") + "/" + name)

            time.sleep(15)
            post_message = driver.find_element_by_xpath(
                "//*[@class='_1mf _1mj']"
            ).find_element_by_xpath("..")
            post_message.send_keys(remove_emojis(content["message"]))

        post_btn = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[3]/div[2]/div/div/div"
        ).find_element_by_xpath("..")
        post_btn.click()

        time.sleep(180)
