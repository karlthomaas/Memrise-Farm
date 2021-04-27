from selenium import webdriver
from WordsHarvest import WordHarvestClass
from config import LoginInformation
import time

# chromedriver.exe destination
PATH = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(PATH)

LOGIN_PANEL = 'https://www.memrise.com/login'
driver.get(LOGIN_PANEL)


def memrise_login():

    """ Logs into memrise account, only need to provide the username and password"""
    username = LoginInformation().username()
    password = LoginInformation().password()
    username_input = driver.find_element_by_name('username')
    password_input = driver.find_element_by_name('password')


    username_input.send_keys(username)
    time.sleep(1)
    password_input.send_keys(password)
    time.sleep(1)
    # login
    driver.find_element_by_xpath('//body/div[@id="__next"]/div[1]/div[2]/div[1]/form[1]/div[3]/button[1]/div[1]').click()


def lesson_pick(lesson):
    try:
        driver.find_element_by_class_name('close').click()
    except Exception as e:
        ...
    time.sleep(5)
    driver.find_element_by_xpath(f"//a[contains(text(),'{lesson}')]").click()


def course_pick(course):
    driver.find_element_by_xpath(f'//body/div[3]/div[4]/div[1]/div[1]/div[1]/div[2]/a[{course}]/div[2]').click()


memrise_login()
time.sleep(5)

lesson_pick('S1 Insight Upper intermediate')
time.sleep(5)
# course number
course_pick('6')

time.sleep(5)
# current url ->
current_url = driver.current_url

# words dictionary ->
words_dictionary = WordHarvestClass(current_url).get_information()
print(words_dictionary)
