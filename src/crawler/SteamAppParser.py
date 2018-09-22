from selenium import webdriver
from bs4 import BeautifulSoup
from src.utills.dateFormatter import get_full_date
import time


class HeadlessChrome:

    def __init__(self, driver_path='C:/chromedriver_win32/chromedriver'):
        self.driverPath = driver_path
        self.driver = self.__load_webdriver()
        self.soup = None

    def __load_webdriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('disable-gpu')
        driver = webdriver.Chrome(self.driverPath, chrome_options=options)
        driver.implicitly_wait(3)
        return driver

    def __request_url(self, url):
        self.driver.get(url)

    def __age_check(self):
        if 'agecheck' in self.driver.current_url:
            el = self.driver.find_element_by_name('ageYear')
            for option in el.find_elements_by_tag_name('option'):
                if option.text == '1980':
                    option.click()
                    break
            self.driver.find_element_by_xpath('//*[@id="app_agegate"]/div[1]/div[4]/a[1]').click()

    def __get_soup(self):
        time.sleep(3)
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup)
        return soup

    def parse_url(self, url):
        self.__request_url(url)
        self.__age_check()
        self.soup = self.__get_soup()
        return self.soup

    def __del__(self):
        self.driver.quit()
        print("quit")


class GetAppInfo:

    def __init__(self, soup, info):
        self.soup = soup
        self.title = info['title']
        self.appid = info['appid']
        self.recent_review = {}
        self.all_review = {}
        self.date = get_full_date()
        # self.tags

    @staticmethod
    def clean_info(info):
        info = info.replace('\t', '').replace('\r', '').split('\n')
        while '' in info:
            info.remove('')
        print(info)

        for index, i in enumerate(info):
            if 'Recent Reviews' in i:
                print('Recent Reviews = ', info[index + 1])
            if 'All Reviews' in i:
                print('All Reviews = ', info[index + 1])

    def get_recent_review(self):
        info = self.soup.select(
            '#game_highlights > div > div > div.glance_ctn_responsive_left > div '
        )
        # print(info[0].text)
        self.clean_info(info[0].text)
