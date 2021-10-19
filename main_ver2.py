from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import LoginInformation
import time

class MemriseScript:
    def __init__(self, username, password, course_lesson, course_unit):
        self.site = 'https://www.memrise.com/login'
        self.PATH = r'C:\Program Files (x86)\chromedriver.exe'
        self.driver = webdriver.Chrome(self.PATH)

        self.username = username
        self.password = password

        self.course_lesson = course_lesson
        self.course_unit = course_unit

        self.wait_timer = 15
        self.ans_cooldown = 2
        self.state1 = False
        self.state2 = False


        self.current_url = ''
        self.words_dictionary = {}

    """ Logs into memrise account, using username and password from config.py file"""

    # def EC_xpath(self, xpath):
    #     elem = WebDriverWait(self.driver, self.wait_timer).until(
    #             EC.presence_of_element_located((By.XPATH, xpath)))
    #
    # def EC_name(self, name):
    #     elem = WebDriverWait(self.driver, self.wait_timer).until(
    #         EC.presence_of_element_located((By.NAME, name)))

    def memrise_login(self):
        # username = LoginInformation().username()
        # password = LoginInformation().password()

        try:

            print('> Inserting username')
            username_input = WebDriverWait(self.driver, self.wait_timer).until(
                EC.presence_of_element_located((By.NAME, 'username')))
            username_input.send_keys(self.username)

            print('> Inserting password')
            password_input = WebDriverWait(self.driver, self.wait_timer).until(
                EC.presence_of_element_located((By.NAME, 'password')))
            password_input.send_keys(self.password)

            print('> Locating login button')
            login_xpath = '//body/div[@id="__next"]/div[1]/div[2]/div[1]/form[1]/div[3]/button[1]/div[1]'
            login_button = WebDriverWait(self.driver, self.wait_timer).until(
                EC.presence_of_element_located((By.XPATH, login_xpath)))
            print('> Clicking login button')
            login_button.click()

        except Exception as e:
            print(f'Memrise_login error!\nError: {e}')


    def ad_close(self):
        try:
            element = WebDriverWait(self.driver, self.wait_timer).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'close')))
            element.click()
            print('> Closed ad!')

        except Exception as e:
            print('> No ad was detected!')

    def lesson_pick(self):
        try:
            print(f'Clicking lesson: {self.course_lesson}!')
            element = WebDriverWait(self.driver, self.wait_timer).until(
                EC.presence_of_element_located((By.XPATH, f"//a[contains(text(),'{self.course_lesson}')]")))
            element.click()
        except Exception as e:
            print(f'> Lesson pick failed:\nError:{e}')

    def course_pick(self):
        try:
            print(f'Clicking course: {self.course_unit}!')
            xpath = f'//body/div[3]/div[4]/div[1]/div[1]/div[1]/div[2]/a[{self.course_unit}]'
            element = WebDriverWait(self.driver, self.wait_timer).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            element.click()
        except Exception as e:
            print(f'> Lesson pick failed:\nError:{e}')

    def console_log(self, sentence):
        sentence_length = len(sentence)
        print('-' * sentence_length)
        print(sentence)

    def word_counter(self, dictionary):
        words_count = len(dictionary)
        print(f'{words_count} Words is in this lessson. ')

    def word_dictionary(self):
        try:

            # checks if the page is loaded ->
            element = WebDriverWait(self.driver, self.wait_timer).until(
                EC.presence_of_element_located((By.XPATH, f"//h1[contains(text(),'{self.course_lesson}')]")))

            # 1. Salvestab kõik inglise keelsed sõnad
            # 2. Salvestab kõik eesti keelsed sõnad
            a_sona_list_xpath = self.driver.find_elements_by_xpath('//div[@class="col_a col text"]')  # 1
            b_sona_list_xpath = self.driver.find_elements_by_xpath('//div[@class="col_b col text"]')  # 2

            # Teisendab inglise & eesti keelsed sõnad loetaval kujul listi ->
            a_sona_list = [sona.text for sona in a_sona_list_xpath]
            b_sona_list = [sona.text for sona in b_sona_list_xpath]

            # Teeb dictionary kahe listi põhjal
            self.words_dictionary = dict(zip(a_sona_list, b_sona_list))
            self.word_counter(self.words_dictionary)

        except Exception as e:
            print(f'word_dictionary error! \nError: {e}')

    def different_scenariums(self):

        try:
            # clicks "Learn these words" ->
            self.driver.find_element_by_xpath("//a[contains(text(),'Learn these words')]").click()  # 1
            return '1'
        except:
            try:
                # clicks "Continue learning" ->
                self.driver.find_element_by_xpath('//a[contains(text(),\'Continue learning\')]').click()  # 2
                return '1'
            except:
                try:
                    # clicks "Continue learning" ->
                    self.driver.find_element_by_xpath('//a[contains(text(),\'Learn\')]').click()  # 2
                    return '1'
                except:
                    try:
                        # clicks Review words (2 step clicking) ->
                        # opens menu and clicks Review words
                        self.driver.find_element_by_xpath(
                            "//body/div[3]/div[4]/div[1]/div[1]/div[1]/div[1]/div[3]/a[3]").click()
                        return '2'
                    except:
                        ...

    def word_check(self, word):
        """ Returns the value of key and key of value"""
        if word in self.words_dictionary.keys():
            return self.words_dictionary[word]

        elif word in self.words_dictionary.values():
            for key, value in self.words_dictionary.items():
                if value == word:
                    return key

    def state_one(self):
        state_boolean = True
        print("State loop 1 activated")
        time.sleep(2)
        while state_boolean:
            try:
                category_xpath = "//body/div[@id='__next']/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[1]/div[1]"
                category = self.driver.find_element_by_xpath(category_xpath).text

                # töötab
                if category == 'Type the correct translation':
                    """Selenium only need to type the correct translation into input box and click enter"""
                    aWord_xpath = "//body/div[@id='__next']/div[2]/div[1]/div[1]/div[1" \
                                  "]/div[1]/div[1]/div[4]/div[1]/div[2]/div[1]/div[1]"
                    aWord = self.driver.find_element_by_xpath(aWord_xpath).text
                    # takes the word translation
                    bWord = self.word_check(aWord)

                    # selects the input box
                    #
                    input_box_xpath = "//body/div[@id='__next']/div[2]/div[1]/div[1]/div[1]/div[1" \
                                      "]/div[1]/div[4]/div[1]/div[2]/div[1]/div[2]/div[1]/input[1]"

                    input_box = self.driver.find_element_by_xpath(input_box_xpath)
                    # sends the answer into input box
                    self.console_log(F'SEARCHED WORD: {aWord}\nANSWER: {bWord}')

                    input_box.send_keys(bWord)

                elif category == 'Pick the correct answer':
                    # otsitav sõna ->
                    searched_word_xpath = "//body/div[@id='__next']/div[2]/div[1]/div[1]/div" \
                                          "[1]/div[1]/div[1]/div[4]/div[1]/div[2]/div[1]/div[1]"

                    searched_word = self.driver.find_element_by_xpath(searched_word_xpath).text

                    # Prints out the valikvastused ->
                    ctct1_xpath = "//body/div[@id='__next']/div[2]/div[1]/div[1]/div" \
                                  "[1]/div[1]/div[1]/div[4]/div[1]/div[2]/div[1]/div[2]"

                    ctct1 = self.driver.find_element_by_xpath(ctct1_xpath).text

                    if ctct1[0] == '1':
                        nimekiri = ctct1.split('\n')
                        nimekiri.insert(0, '')
                        answer = self.word_check(searched_word)
                        self.console_log(f'SEARCHED WORD: {searched_word}\nANSWER: {answer}')
                        choice_answer = nimekiri.index(answer) - 1

                        site = self.driver.find_element_by_xpath('//html')
                        site.send_keys(nimekiri[choice_answer])
                    else:
                        # todo sometimes bugs out and stays in picking loop

                        site = self.driver.find_element_by_xpath('//html')
                        # valiksõnad input boxi all
                        nimekiri = ctct1.split('\n')
                        nimekiri.insert(0, '')

                        answer = self.word_check(searched_word)
                        # vastus tehtud eraldi juppideks
                        answer_splitted = answer.split(' ')

                        # activates the number answering
                        site.send_keys('1')
                        # nii mitu korda käib, kuniks sõna on täiesti läbi
                        for i in range(len(answer_splitted)):
                            number = nimekiri.index(answer_splitted[i])
                            site.send_keys(str(number))
                            time.sleep(1)
                        self.console_log(f'SEARCHED WORD: {searched_word}\nANSWER: {answer}')
                        self.driver.find_element_by_xpath("/html[1]/body[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[5]/button[1]").click()
                else:

                    """ There's nothing to do with Lesson card, script will skip it"""
                    self.console_log('Lesson card.. Skipping.')
                    # Clicks the Next button ->
                    next_button_xpath = "//body/div[@id='__next']/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[5]/button[1]"
                    self.driver.find_element_by_xpath(next_button_xpath).click()

                time.sleep(self.ans_cooldown)
            except Exception as e:
                print('Ran out of words. Restarting!')
                self.driver.get(self.current_url)
                state_boolean = False

    def state_two(self):
        state_boolean = True
        while state_boolean:
            try:
                time.sleep(2)
                print('> state 2 ')
                kategooria = self.driver.find_element_by_xpath(
                    "/html[1]/body[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[1]/div[1]/h2[1]").text


                searched_word = self.driver.find_element_by_xpath(
                    "/html[1]/body[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[1]/div[2]/div[1]/div[1]/h2[1]").text
                answer = self.word_check(searched_word)

                if kategooria == 'Pick the correct answer':
                    # Prints out the valikvastused ->
                    ctct1_xpath = "//body/div[@id='__next']/div[2]/div[1]/div[1]/div" \
                                  "[1]/div[1]/div[1]/div[4]/div[1]/div[2]/div[1]/div[2]"

                    ctct1 = self.driver.find_element_by_xpath(ctct1_xpath).text

                    if ctct1[0] == '1':
                        nimekiri = ctct1.split('\n')
                        nimekiri.insert(0, '')
                        answer = self.word_check(searched_word)
                        self.console_log(f'SEARCHED WORD: {searched_word}\nANSWER: {answer}')
                        choice_answer = nimekiri.index(answer) - 1

                        site = self.driver.find_element_by_xpath('//html')
                        site.send_keys(nimekiri[choice_answer])
                    else:
                        # todo sometimes bugs out and stays in picking loop

                        site = self.driver.find_element_by_xpath('//html')
                        # valiksõnad input boxi all
                        nimekiri = ctct1.split('\n')
                        nimekiri.insert(0, '')

                        answer = self.word_check(searched_word)
                        # vastus tehtud eraldi juppideks
                        answer_splitted = answer.split(' ')

                        # activates the number answering
                        site.send_keys('1')
                        # nii mitu korda käib, kuniks sõna on täiesti läbi
                        for i in range(len(answer_splitted)):
                            number = nimekiri.index(answer_splitted[i])
                            site.send_keys(str(number))
                            time.sleep(1)
                        self.console_log(f'SEARCHED WORD: {searched_word}\nANSWER: {answer}')
                        self.driver.find_element_by_xpath(
                            "/html[1]/body[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[5]/button[1]").click()

                elif kategooria == 'Type the correct translation':
                    input_box = self.driver.find_element_by_xpath(
                        "/html[1]/body[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[1]/div[2]/div[1]/div[2]/div[1]/input[1]")
                    input_box.send_keys(answer)
                    time.sleep(self.ans_cooldown)

                else:
                    skip_button = "//body/div[@id='gardening-area']/div[@id='central-area']/div[@id='boxes']/div[1]/div[1]/button[1]"
                    self.driver.find_element_by_xpath(skip_button).click()
                    time.sleep(self.ans_cooldown)

            except Exception as e:
                print('Ran out of words. Restarting!')

                self.driver.get(self.current_url)
                state_boolean = False

    def run(self):
        self.driver.get(self.site)
        self.memrise_login()
        self.ad_close()
        self.lesson_pick()
        self.course_pick()
        self.current_url = self.driver.current_url
        self.word_dictionary()
        while True:
            time.sleep(3)
            state = self.different_scenariums()
            if state == '1':
                self.state_one()
            elif state == '2':
                self.state_two()


USERNAME = 'karl-thomas@zink.ee'
PASSWORD = 'MemriseBot6969'

UNIT_NAME = '2021 P1 Insight'
UNIT_COURSE = '2'

MemriseScript(USERNAME, PASSWORD, UNIT_NAME, UNIT_COURSE).run()
