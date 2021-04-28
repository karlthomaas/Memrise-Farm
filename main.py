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
try:
    words_dictionary = WordHarvestClass(current_url).get_information()
    print('Words copied successfully')
except Exception as e:
    print('Error:')
    print(e)
time.sleep(5)
driver.find_element_by_xpath('//a[contains(text(),\'Continue learning\')]').click()
time.sleep(5)

"""
Next line types the category header -> 
PS! Need to split the header and take in the first sentence (header)
"""
state = True
while state:
    category = driver.find_element_by_xpath("//body/div[@id='__next']/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[1]/div[1]").text
    if category == 'Type the correct translation':
        """Selenium only need to type the correct translation into input box and click enter"""

        print('DETECTED: Type the correct translation')

        # takes the word
        aWord = driver.find_element_by_xpath("//body/div[@id='__next']/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[1]/div[2]/div[1]/div[1]").text
        # takes the word translation
        bWord = words_dictionary[aWord]
        # selects the input box
        input_box = driver.find_element_by_xpath("//body/div[@id='__next']/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[1]/div[2]/div[1]/div[2]/div[1]/input[1]")
        # sends the answer into input box
        input_box.send_keys(bWord)

    elif category == 'Choose the correct translation':
        print('DETECTED: Choose the correct translation')

    else:
        """ There's nothing to do with Lesson card, script will skip it"""

        print('DETECTED: Lesson card')
        print('Skipping.')
        # Clicks the Next button ->
        driver.find_element_by_xpath("//body/div[@id='__next']/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[5]/button[1]").click()

    time.sleep(5)
