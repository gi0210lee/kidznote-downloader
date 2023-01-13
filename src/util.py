import os
import browser_cookie3
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# 파일 저장
def SaveFile(filename, content):
    f = open(filename, 'w', encoding='utf-8')
    f.write(content)
    f.close()


def createFolder(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print('Error: CreateFolder' + path)


# 쿠키 가져오기
def getCookiesFromDomain(domain, cookieName=''):

    Cookies = {}
    path_default = os.path.join(os.path.expandvars(
        "%userprofile%"), "AppData\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies")
    path_profile_7 = os.path.join(os.path.expandvars(
        "%userprofile%"), "AppData\\Local\\Google\\Chrome\\User Data\\Profile 7\\Network\\Cookies")
    tempChromeCookies = browser_cookie3.chrome(cookie_file=path_default)
    if tempChromeCookies is None:
        tempChromeCookies = browser_cookie3.chrome(cookie_file=path_profile_7)
    chromeCookies = list(tempChromeCookies)

    for cookie in chromeCookies:

        if (domain in cookie.domain):
            # print (cookie.name, cookie.domain,cookie.value)
            Cookies[cookie.name] = cookie.value

    if (cookieName != ''):
        try:
            return Cookies[cookieName]  # return specified cookie
        except:
            return {}  # if exception raised return an empty dictionary
    else:
        return Cookies  # return all cookies or nothing

# 이미지 저장


def HtmlToImageWithSelenium(header_url, url, output_file):
    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # options.add_argument(
    #     'User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36')
    # options.add_argument(
    #     'Accept-Language=ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7')
    # options.add_argument('Cookie=sessionid=v8but91g9z6mpvwijnrov1nh7evwlqpd; _hjSessionUser_3251788=eyJpZCI6IjNmZDdjZjE2LTBmN2ItNTlkMy05MDM2LTAzNGE5OGFjZjA2YSIsImNyZWF0ZWQiOjE2NzMzOTgwOTQ5ODcsImV4aXN0aW5nIjp0cnVlfQ==; csrftoken=GS4bUiUxOyMMQHoMFNj2Z8WdFv0eeYouZfU7kWnY4iHD7NFJs1S7lDelP2CPCscB; _gid=GA1.2.109501274.1673398107; current_user=dayomi; _ga_6HBPNX8FC2=GS1.1.1673419131.3.0.1673419137.0.0.0; _ga=GA1.2.687922305.1673398094')

    # driver = webdriver.Chrome(
    #     ChromeDriverManager().install(), options=options)
    # driver.implicitly_wait(10)
    # driver.get(url)
    # driver.get_screenshot_as_file(output_file)

    driver = webdriver.Chrome()
    driver.get('https://www.kidsnote.com/login')
    driver.implicitly_wait(5)
    driver.find_element(By.NAME, 'username').send_keys('dayomi')
    driver.find_element(By.NAME, 'password').send_keys('minggi1027!')

    # driver.find_element(By.NAME, 'remember_me').click()

    driver.find_element(By.XPATH,
                        '/html/body/div[1]/div[1]/main/div/form/button').click()

    driver.implicitly_wait(5)
    time.sleep(5)
    driver.get(url)
    driver.implicitly_wait(5)
    time.sleep(5)
    driver.find_element(
        By.XPATH, '/html/body/div/div[3]/div[2]/div/div/div/div[1]/form').submit()
    driver.implicitly_wait(5)
    time.sleep(5)
    driver.get_screenshot_as_file('1.png')
    driver.quit()
