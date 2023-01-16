import os
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
