from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def post_fb(message):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        "/home/quanghuy/Desktop/facebook-group/chromedriver",
        chrome_options=chrome_options,
    )
    # driver = webdriver.Firefox(
    #     executable_path=r"/home/quanghuy/Desktop/facebook-group/geckodriver"
    # )
    driver.implicitly_wait(20)

    driver.get("https://www.facebook.com/")

    email = driver.find_element_by_xpath('.//*[@id="email"]')
    email.send_keys("taolasieunhansylas@gmail.com")
    time.sleep(1)
    password = driver.find_element_by_xpath('.//*[@id="pass"]')
    password.send_keys("kadfiuiwrn298asfdsf@")
    time.sleep(1)
    login = driver.find_element_by_name("login")
    login.click()

    time.sleep(5)
    group = "https://www.facebook.com/groups/964820740753433"

    # Post on each group
    driver.get(group)
    time.sleep(5)
    
    # create_post = driver.find_element_by_xpath(
    #     "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div[1]/div[1]/div/div/div/div[1]/div"
    # ).find_element_by_xpath("..")
    # create_post.click()
    # time.sleep(5)

    # post_box = driver.find_element_by_xpath(
    #     "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div/div/div/div"
    # ).find_element_by_xpath("..")
    # post_box.send_keys(message)
    # time.sleep(5)

    post_image = driver.find_element_by_xpath("//input[@type='file']")
    post_image.send_keys("/home/quanghuy/Desktop/facebook-group/image.jpg")
   
    time.sleep(5)
    post_message = driver.find_element_by_xpath("//*[@class='_1mf _1mj']").find_element_by_xpath("..")
    post_message.send_keys(message)
    

    # if len(message.split(" ")) <= 25:

    #     post_style = driver.find_element_by_xpath(
    #         "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div[2]/div/div/span/img"
    #     ).find_element_by_xpath("..")
    #     post_style.click()
    #     time.sleep(5)

    #     choose_style = driver.find_element_by_xpath(
    #         "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div/div[4]/div/div"
    #     ).find_element_by_xpath("..")
    #     choose_style.click()
    #     time.sleep(3)

    # post_btn = driver.find_element_by_xpath(
    #     "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[3]/div[2]/div/div/div"
    # ).find_element_by_xpath("..")
    # post_btn.click()

    time.sleep(10)
    # Close driver
    driver.close()


post_fb("Đi làm thì ngủ trưa được. Ở nhà mệt cỡ nào cũng không thể ngủ trưa.")
