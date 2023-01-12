import os
import browser_cookie3


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
    path_cookies = os.path.join(os.path.expandvars(
        "%userprofile%"), "AppData\\Local\\Google\\Chrome\\User Data\\Profile 7\\Network\\Cookies")
    chromeCookies = list(browser_cookie3.chrome(cookie_file=path_cookies))

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
