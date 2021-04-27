from bs4 import BeautifulSoup
import requests
""" Uses bs4 to harvest all words and it's meanings and then returns the dictionary"""
class WordHarvestClass:
    def __init__(self, url):
        self.url = url
        self.word_dicionary = {}

        link = self.url
        result = requests.get(link)

        rc = result.content
        self.soup = BeautifulSoup(rc, features='html.parser')

    def get_information(self):
        words_cell = self.soup.find(class_='things clearfix')
        for words in words_cell.find_all(class_='thing text-text'):
            word_A = words.find(class_='col_a col text').get_text()
            word_B = words.find(class_='col_b col text').get_text()
            self.word_dicionary[word_A] = word_B
        return self.word_dicionary

