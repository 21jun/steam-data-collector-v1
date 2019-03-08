from selenium import webdriver
from bs4 import BeautifulSoup
from src.utills.dateFormatter import get_full_date
from src.utills.MonthConverter import month_converter
import odbc
import time


class DataBaseConnector:

    def __init__(self):
        connect = odbc.odbc('oasis')
        db = connect.cursor()
        self.db = db

    def db_get_apps(self, table):
        """
        :param table: Which table you want to use
        :return: app data (appid, name)
        """
        sql = '''SELECT appid, name FROM oasis.''' + str(table)
        self.db.execute(sql)
        apps = self.db.fetchall()
        return apps

    def __db_insert_data(self, data):
        sql = '''INSERT INTO oasis.app_info(appid, name, developer, publisher, release_date,
        recent_review_evaluation, recent_review_count, recent_review_positive_percentage,
        all_review_evaluation, all_review_count, all_review_positive_percentage, tags, date) 
        VALUES ("%d","%s","%s","%s","%s","%s","%d","%d","%s","%d","%d","%s","%s") '''
        self.db.execute(sql % (int(data['appid']), data['name'], data['developer'],
                               data['publisher'], data['release_date'],
                               data['recent_review']['evaluation'], int(data['recent_review']['count']),
                               int(data['recent_review']['positive_percentage']),
                               data['all_review']['evaluation'], int(data['all_review']['count']),
                               int(data['all_review']['positive_percentage']),
                               data['tags'], data['date']))

    def db_update_app_data(self, data):
        try:
            self.__db_insert_data(data)
            print(data['appid'], data['name'])
        except:
            pass
        print('--------------------------')


class HeadlessChrome:

    def __init__(self, driver_path='C:/chromedriver_win32/chromedriver'):
        self.driverPath = driver_path
        self.driver = self.__load_webdriver()
        self.soup = None

    def __del__(self):
        self.driver.quit()
        print("quit")

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
            # agecheck 후 다음 페이지로 넘어갔는지 체크...(다른 간단한 방법은?)
            timeout = 0
            while 'agecheck' in self.driver.current_url:
                time.sleep(0.1)
                timeout += 0.1
                if timeout >= 5:
                    print("Time out...")
                    raise TimeoutError

    def __get_soup(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup)
        return soup

    # Core
    def parse_url(self, url):

        self.__request_url(url)
        try:
            self.__age_check()
        except:
            return TimeoutError
        self.soup = self.__get_soup()
        return self.soup


class GetAppInfo:

    def __init__(self, soup, info):
        self.soup = soup
        self.name = info['name']
        self.appid = info['appid']
        self.recent_review = {
            'count': 0,
            'evaluation': 'None',
            'positive_percentage': 0
        }
        self.all_review = {
            'count': 0,
            'evaluation': 'None',
            'positive_percentage': 0
        }
        self.developer = 'None'
        self.publisher = 'None'
        self.release_date = '0000-00-00'
        self.date = get_full_date()
        self.tags = ''

    @staticmethod
    def clean_info(info):
        info = info.replace('\t', '').replace('\r', '').split('\n')
        while '' in info:
            info.remove('')
        print(info)
        return info

    @staticmethod
    def clean_number(num):
        num = num.replace('(', '')
        num = num.replace(')', '')
        num = num.replace(',', '')
        return num

    @staticmethod
    def clean_percentage(input_string):
        for i in range(len(input_string)):
            if input_string[i] == '%':
                percentage = input_string[i - 2:i]
                return percentage
        return 0

    @staticmethod
    def clean_date(release_date):
        release_date = release_date.replace(',', '')
        release_date = release_date.split(' ')
        # print(release_date)
        day = release_date[0]
        month = month_converter(release_date[1])
        year = release_date[2]
        date = '%s-%s-%s' % (year, month, day)
        return date

    @staticmethod
    def clean_tags(tags):
        result = tags.replace('\t', '')
        result = result.replace('\r', '')
        result = result.replace('\n', ' ')
        result = result.replace('+', '')
        result = result.replace('  ', '')
        result = result.split(' ')
        result.remove('')

        # Free to Play Exception
        if 'Free' in result:
            result.remove('Free')
            result.remove('to')
            result.remove('Play')
            result.append('Free to Play')

        return result

    def get_info(self):
        try:
            tags = self.soup.select(
                '#game_highlights > div > div > div > div > div.glance_tags.popular_tags'
            )
            if tags:
                self.tags = ','.join(self.clean_tags(tags[0].text))

            info = self.soup.select(
                '#game_highlights > div > div > div.glance_ctn_responsive_left > div '
            )
            if info:
                info = self.clean_info(info[0].text)

            for index, i in enumerate(info):
                if 'Recent Reviews' in i:
                    if not self.clean_number(info[index + 2]).isdigit():
                        # Miss Recent Review count
                        pass
                    else:
                        self.recent_review['evaluation'] = info[index + 1]
                        self.recent_review['count'] = self.clean_number(info[index + 2])
                        self.recent_review['positive_percentage'] = self.clean_percentage(info[index + 3])

                if 'All Reviews' in i:
                    if not self.clean_number(info[index + 2]).isdigit():
                        # Need more review to generate evaluation
                        pass
                    else:
                        self.all_review['evaluation'] = info[index + 1]
                        self.all_review['count'] = self.clean_number(info[index + 2])
                        self.all_review['positive_percentage'] = self.clean_percentage(info[index + 3])

                if 'Developer' in i:
                    self.developer = info[index + 1]

                if 'Publisher' in i:
                    self.publisher = info[index + 1]

                if 'Release Date' in i:
                    self.release_date = self.clean_date(info[index + 1])

            result = {
                'name': self.name,
                'appid': self.appid,
                'recent_review': self.recent_review,
                'all_review': self.all_review,
                'developer': self.developer,
                'publisher': self.publisher,
                'tags': self.tags,
                'release_date': self.release_date,
                'date': self.date
            }
            return result
        except:
            return TimeoutError

