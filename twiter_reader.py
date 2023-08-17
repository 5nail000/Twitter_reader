from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import warnings
import logging
import os
import time
import json
import pickle
import pprint

pp = pprint.PrettyPrinter(indent=3)


def cookie_getter_by_hands(cookie_filename):

    url0 = 'https://twitter.com/'

    # '''
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36")
    # -------------  disable webdriver mode -------------
    options.add_argument("--disable-blink-features=AutomationControlled")
    # -------- TurnOff webdriver log in terminal --------
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    logging.getLogger('WDM').setLevel(logging.NOTSET)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    do_repeat = True

    while do_repeat:

        try:
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.maximize_window()
            driver.get(url=url0)
            driver.implicitly_wait(1)
            time.sleep(120)
        except Exception as _ex:
            print('is Exception')
            print(_ex)
            True
        else:
            do_repeat = False

    # cookies save after just 1st login
    pickle.dump(driver.get_cookies(), open(cookie_filename, "wb"))
    driver.quit()

    return


def cookie_getter_autologin(cookie_filename, personal_data):

    email = personal_data['email']
    login = personal_data['login']
    password = personal_data['password']

    url0 = 'https://twitter.com/i/flow/login'

    # '''
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36")
    # -------------  disable webdriver mode -------------
    options.add_argument("--disable-blink-features=AutomationControlled")
    # -----------------  TurnOff window -----------------
    options.add_argument('--headless=new')
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    options.add_argument('--disable-gpu')

    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # -------- TurnOff webdriver log in terminal --------
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    logging.getLogger('WDM').setLevel(logging.NOTSET)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    do_repeat = True

    while do_repeat:

        try:
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.maximize_window()
            driver.get(url=url0)
            driver.implicitly_wait(3)
        except Exception as _ex:
            print('is Exception')
            print(_ex)
            True
        else:
            do_repeat = False

        # button = driver.find_element(By.XPATH, '//button[text()="Принять все файлы cookie"]')
        # button.click()
        username_field = driver.find_element(By.XPATH, '//input[@name="text"]')
        username_field.send_keys(email)
        driver.implicitly_wait(3)
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='button']/div/span/span[text()='Далее']"))
            )
        button.click()
        driver.implicitly_wait(3)
        header = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#modal-header"))
            )
        if header.text == "Введите номер телефона или имя пользователя":
            input_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@data-testid="ocfEnterTextTextInput"]'))
            )
            input_field.send_keys(login)
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='button']/div/span/span[text()='Далее']"))
                )
            button.click()
            header = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#modal-header"))
                )
            if header.text == "Введите пароль":
                password_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@name="password"]'))
                    )
                password_field.send_keys(password)

                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='button']/div/span/span[text()='Войти']"))
                    )
                button.click()

        elif header.text == "Введите пароль":
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@name="password"]'))
                )
            password_field.send_keys(password)

            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='button']/div/span/span[text()='Войти']"))
                )
            button.click()

        time.sleep(10)

    # cookies save after just 1st login
    pickle.dump(driver.get_cookies(), open(cookie_filename, "wb"))
    driver.quit()
    print('yeah! cookies are saved')

    return


def webdriver_start(cookie_filename):

    areShown = False

    global driver
    try:
        driver.close()
    except Exception:
        True

    url0 = 'https://twitter.com/'

    # '''
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36")
    # -------------  disable webdriver mode -------------
    options.add_argument("--disable-blink-features=AutomationControlled")
    # -----------------  TurnOff window -----------------
    if not areShown:
        options.add_argument('--headless=new')
        options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        options.add_argument('--disable-gpu')

        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
    # -------- TurnOff webdriver log in terminal --------
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    logging.getLogger('WDM').setLevel(logging.NOTSET)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    do_repeat = True

    while do_repeat:

        try:
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.maximize_window()
            driver.get(url=url0)
            # Загрузка куки, если они существуют
            if os.path.isfile(cookie_filename):
                cookies = pickle.load(open(cookie_filename, "rb"))
                driver.add_cookie(cookies[1])
                driver.add_cookie(cookies[4])
                driver.implicitly_wait(1)
                driver.get(url=url0)
                '''
                count = 0
                for cookie in cookies:
                    count += 1
                    print(count)
                    print(cookie)
                    driver.add_cookie(cookie)
                    driver.implicitly_wait(1)
                    driver.get(url=url0)
                    time.sleep(3)
                print('Cookie over')
                # '''
            else:
                print('cookie has broken')
            driver.implicitly_wait(1)
        except Exception as _ex:
            print('is Exception')
            print(_ex)
            True
        else:
            do_repeat = False

    return driver


def get_page(driver: webdriver.Chrome, url, num_page_downs=10):
    driver.get(url=url)
    time.sleep(3)  # let the page load

    # simulate pressing Page Down key num_page_downs times
    actions = ActionChains(driver)
    for _ in range(num_page_downs):
        actions.send_keys(Keys.PAGE_DOWN).perform()
        driver.implicitly_wait(2)  # wait for the new content to load
        actions.send_keys(Keys.END).perform()
        driver.implicitly_wait(2)  # wait for the new content to load
        time.sleep(2)  # let the page load

    soup_page = BeautifulSoup(driver.page_source, 'lxml')
    return soup_page


def get_tweets(soup):
    divs = soup.find_all('div', class_='css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu')
    tweets_data = []  # list to hold dictionaries

    for div in divs:
        # find tweet text
        tweet_div = div.find('div', attrs={'data-testid': 'tweetText'})
        tweet = tweet_div.get_text() if tweet_div else None

        # find link and datetime
        link_div = div.find('div', class_='css-1dbjc4n r-18u37iz r-1q142lx')
        if link_div:
            a_tag = link_div.find('a')
            href = a_tag['href'] if a_tag else None
            time_tag = link_div.find('time')
            datetime = time_tag['datetime'] if time_tag else None
        else:
            href = datetime = None

        # add tweet data to list
        tweets_data.append({
            'tweet': tweet,
            'href': href,
            'datetime': datetime,
        })

    return tweets_data


def main():
    cookie_filename = '_cookies'
    twitter_url = 'https://twitter.com/'

    # read channels file
    channels_file = 'channels.txt'
    channel_list = []
    if os.path.isfile(channels_file):
        with open(channels_file, "r", encoding="utf-8") as f:
            channel_list = f.readlines()
        channel_list = [c.rstrip() for c in channel_list]

    # read json personalization data file
    json_file = 'personalization_data.json'
    personalization_data = False
    if os.path.isfile(json_file):
        with open(json_file, encoding='utf_8') as file:
            personalization_data = json.load(file)

    # get cookies
    if not os.path.isfile(cookie_filename):
        print('we have no cookies')
        if personalization_data['email'] and personalization_data['login'] and personalization_data['password']:
            print('we have all email/login/password for automatic logining')
            cookie_getter_autologin(cookie_filename, personalization_data)
        else:
            print('you dont gave email/login/password for automatic logining')
            print('gotta roll up your sleeves')
            cookie_getter_by_hands(cookie_filename)

    # mineing
    driver = webdriver_start(cookie_filename)
    while True:  # infinite loop
        for channel in channel_list:
            url = os.path.join(twitter_url, channel)
            soup_page = get_page(driver, url)
            tweet_texts = get_tweets(soup_page)
            pp.pprint(tweet_texts)
            print('channel:', channel, len(tweet_texts), 'tweets mined')

        print('taking a pause...')
        time.sleep(300)  # wait for 5 minutes (300 seconds)

    driver.quit()


if __name__ == '__main__':
    main()
