from selenium import webdriver
from WordsHarvest import WordHarvestClass
from config import LoginInformation
import time

# chromedriver.exe destination
PATH = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(PATH)

LOGIN_PANEL = 'https://www.memrise.com/login'
driver.get(LOGIN_PANEL)

course_lesson = 'B2 elective course Secunda'
course_unit = '1'

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
    # login button
    driver.find_element_by_xpath('//body/div[@id="__next"]/div[1]/div[2]/div[1]/form[1]/div[3]/button[1]/div[1]').click()


def lesson_pick(lesson):
    try:
        # closes the ad
        driver.find_element_by_class_name('close').click()
    except Exception as e:
        ...
    time.sleep(5)
    # clicks on lesson
    driver.find_element_by_xpath(f"//a[contains(text(),'{lesson}')]").click()


# picks the course
def course_pick(course):
    driver.find_element_by_xpath(f'//body/div[3]/div[4]/div[1]/div[1]/div[1]/div[2]/a[{course}]/div[2]').click()


# prints text into terminal
def console_log(sentence):
    sentence_length = len(sentence)
    print('-' * sentence_length)
    print(sentence)


def word_counter(dict):
    words_count = len(dict)
    print(f'{words_count  } Words is in this lessson. ')
        

memrise_login()
time.sleep(5)

lesson_pick(course_lesson)

time.sleep(5)
# course number
course_pick(course_unit)

time.sleep(5)
# takes the current url, so it can go back after doing all tasks
current_url = driver.current_url

# words dictionary ->
try:
    # copies all words into dictionary, using another class in other file
    words_dictionary = WordHarvestClass(current_url).get_information()
    console_log('Words copied to dictionary successfully')
    # count's the words
    word_counter(words_dictionary)
except Exception as e:
    print('Error:')
    print(e)

def word_check(word):
    """ Returns the value of key and key of value"""
    if word in words_dictionary.keys():
        return words_dictionary[word]

    elif word in words_dictionary.values():
        for key, value in words_dictionary.items():
            if value == word:
                return key

time.sleep(5)

""" 
If you haven't started learning memrise words yet, then #1 activates.
If you want to continue learning memrise words, then #2 activates.
 """
try:
    driver.find_element_by_xpath("//a[contains(text(),'Learn these words')]").click()  # 1
except Exception as e:
    driver.find_element_by_xpath('//a[contains(text(),\'Continue learning\')]').click()  # 2

time.sleep(5)
state = True

answering_cooldown = 2
while state:
    try:

        category = driver.find_element_by_xpath("//body/div[@id='__next']/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[1]/div[1]").text
        if category == 'Type the correct translation':
            """Selenium only need to type the correct translation into input box and click enter"""


            aWord = driver.find_element_by_xpath("//body/div[@id='__next']/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[1]/div[2]/div[1]/div[1]").text
            # takes the word translation
            bWord = words_dictionary[aWord]
            # selects the input box
            input_box = driver.find_element_by_xpath("//body/div[@id='__next']/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[1]/div[2]/div[1]/div[2]/div[1]/input[1]")
            # sends the answer into input box
            console_log(F'SEARCHED WORD: {aWord}\nANSWER: {bWord}')
            input_box.send_keys(bWord)

        elif category == 'Choose the correct translation':

            # otsitav sõna ->
            searched_word = driver.find_element_by_xpath("//body/div[@id='__next']/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[1]/div[2]/div[1]/div[1]").text

            # Prints out the valikvastused ->
            ctct1 = driver.find_element_by_xpath("//body/div[@id='__next']/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[1]/div[2]/div[1]/div[2]").text

            if ctct1[0] == '1':
                list = ctct1.split('\n')
                list.insert(0, '')
                answer = word_check(searched_word)
                console_log(f'SEARCHED WORD: {searched_word}\nANSWER: {answer}')
                choice_answer = list.index(answer) - 1

                site = driver.find_element_by_xpath('//html')
                site.send_keys(list[choice_answer])
            else:
                site = driver.find_element_by_xpath('//html')
                # valiksõnad input boxi all
                list = ctct1.split('\n')
                list.insert(0, '')

                answer = word_check(searched_word)
                # vastus tehtud eraldi juppideks
                answer_splitted = answer.split(' ')

                # activates the number answering
                site.send_keys('1')
                # nii mitu korda käib, kuniks sõna on täiesti läbi
                for i in range(len(answer_splitted)):

                    number = list.index(answer_splitted[i])
                    site.send_keys(str(number))
                    time.sleep(1)
                console_log(f'SEARCHED WORD: {searched_word}\nANSWER: {answer}')

        else:

            """ There's nothing to do with Lesson card, script will skip it"""
            console_log('Lesson card.. Skipping.')
            # Clicks the Next button ->
            driver.find_element_by_xpath("//body/div[@id='__next']/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[5]/button[1]").click()

        time.sleep(answering_cooldown)
    except Exception as e:
        print(e)
        print('Ran out of words. Restarting!')
        driver.get(current_url)
        time.sleep(2)
        """
        
        """
        try:
            driver.find_element_by_xpath("//a[contains(text(),'Learn these words')]").click()  # 1

        except Exception as e:
            driver.find_element_by_xpath('//a[contains(text(),\'Continue learning\')]').click()  # 2

        time.sleep(2)