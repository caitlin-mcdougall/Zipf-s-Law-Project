import wikipedia
import urllib3
import requests
import ctypes
import matplotlib.pyplot as plt


class WordFrequencyDistribution:
    def __init__(self, text_dict=dict()):
        self.__text_dict = text_dict

    def merge(self, current_wfd):
        if not self.__text_dict:
            self.__text_dict = current_wfd.__text_dict
        else:
            for key in current_wfd.__text_dict:
                for item in self.__text_dict:
                    is_found = False
                    if key == item:
                        is_found = True
                        break
                if is_found:
                    self.__text_dict[key] += current_wfd.__text_dict[key]
                else:
                    self.__text_dict[key] = current_wfd.__text_dict[key]

    def sort_dictionary(self):
        self.__text_dict = sorted(self.__text_dict.items(), key=lambda x: x[1], reverse=True)

    def plot_graph(self):
        if len(self.__text_dict) > 100:
            for a in range(0, 101):
                plt.plot(a + 1, self.__text_dict[a][1], 'ro', markersize=1)
                plt.axis = (0, 100, 0, self.get_word_count())

        else:
            for a in range(0, len(self.__text_dict)):
                plt.plot(a + 1, self.__text_dict[a][1], 'ro', markersize=2)
                plt.axis = (0, len(dict(self.__text_dict)), 0, self.get_word_count())
        plt.title("Zipf's Law")
        plt.xlabel("Frequency Rank")
        plt.ylabel("Number of Occurrences")
        plt.show()

    def get_word_count(self):
        word_count = 0
        for key in dict(self.__text_dict):
            word_count += dict(self.__text_dict)[key]

    def get_text_dict(self):
        return self.__text_dict


class Page:
    def __init__(self):
        self.__page = list()
        self.__reference = ctypes.Union
        self.__content = ''
        self.__url = ''
        self.__word_list = list()
        self.__page_wfd = dict()

    def get_reference(self):
        reference = ''
        while reference == '':
            self.__page = wikipedia.random()
            try:
                reference = wikipedia.page(self.__page)
            except wikipedia.exceptions.DisambiguationError as e:
                reference = ''
            except ConnectionError as a:
                reference = ''
            except TimeoutError as t:
                reference = ''
            except urllib3.exceptions.NewConnectionError as n:
                reference = ''
            except urllib3.exceptions.MaxRetryError as m:
                reference = ''
            except requests.exceptions.ConnectionError as q:
                reference = ''
            except wikipedia.exceptions.PageError as w:
                reference = ''
            except Exception as h:
                reference = ''
        self.__reference = reference

    def get_content(self):
        error = ''
        while error == '':
            try:
                self.__content = self.__reference.content
                error = 'no'
            except UnicodeEncodeError as e:
                error = ''

    def get_url(self):
        self.__url = self.__reference.url
        return self.__url

    def form_list(self):
        text_list = []
        original_list = []
        spli_cont = self.__content.split()
        for b in spli_cont:
            original_list.append(b)
        for a in range(0, len(original_list)):
            if original_list[a].isalnum():
                text_list.append(original_list[a])
        self.__word_list = text_list
        for key in self.__word_list:
            key.lower()

    def get_wfd(self):
        text_dict = dict()
        for counter in range(0, len(self.__word_list)):
            current_word = self.__word_list[counter].lower()
            is_found = False
            for key in text_dict:
                if key == current_word:
                    is_found = True
                    break
            if is_found:
                text_dict[current_word] += 1
            else:
                text_dict[current_word] = 1
        self.__page_wfd = WordFrequencyDistribution(text_dict)
        return self.__page_wfd


def user_input():
    n = int(input("Enter how many wiki pages to add: "))
    while n <= 0 or type(n) is not int:
        n = int(input("Please enter an integer bigger than 0: "))
    return n


def processing():
    main_wfd = WordFrequencyDistribution()
    number_of_pages_to_process = user_input()
    for counter in range(0, number_of_pages_to_process):
        page = Page()
        page.get_reference()
        page.get_content()
        print(counter + 1, "/", number_of_pages_to_process, "-", page.get_url())
        page.form_list()
        current_wfd = page.get_wfd()
        main_wfd.merge(current_wfd)
    main_wfd.sort_dictionary()
    print(main_wfd.get_text_dict())
    maximum = main_wfd.get_text_dict()[0]
    print("The most frequently occurring word was \"", maximum[0], "\" which was used ", maximum[1], "times")
    main_wfd.plot_graph()


if __name__ == "__main__":

    processing()