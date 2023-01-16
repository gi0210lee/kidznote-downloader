import os
import time
import re
import urllib.request
from src import config
from src import util
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def ScriptingAlbums():
    print('앨범 다운로더 시작')

    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    # 로그인
    print(f'로그인')
    driver.get(config.LOGIN_URL)
    time.sleep(config.CONST_DELAY_TIME)
    driver.find_element(By.NAME, 'username').send_keys(config.USERNAME)
    driver.find_element(By.NAME, 'password').send_keys(config.PASSWORD)
    driver.find_element(By.XPATH,
                        '/html/body/div[1]/div[1]/main/div/form/button').click()
    time.sleep(config.CONST_DELAY_TIME)

    # 구 버전 이동
    driver.get(config.OLD_VER_URL)
    time.sleep(config.CONST_DELAY_TIME)

    # 호칭설정
    driver.find_element(
        By.ID, 'roleSelect').click()
    time.sleep(config.CONST_DELAY_TIME)

    # 첫번재 호칭 선택
    driver.find_element(
        By.XPATH, '/html/body/header/div[5]/div[2]/div[2]/div/div[2]/div/div[1]/form').submit()
    time.sleep(config.CONST_DELAY_TIME)

    # 앨범으로 이동
    driver.get(config.ALNUMS_URL)
    time.sleep(config.CONST_DELAY_TIME)

    # 마지막 페이지 구하기
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    page_link_list = soup.find_all('a', class_='page-link')
    number = 0
    last_page = 0
    for i in page_link_list:
        number = number + 1
    last_page = page_link_list[number - 2].text

    page = 0
    while page <= int(last_page):
        page = page + 1

        # 앨범 페이지 별 목록
        albums_page_url = config.ALNUMS_URL + '?page=' + str(page)
        driver.get(albums_page_url)
        time.sleep(config.CONST_DELAY_TIME)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 앨범 페이지 내 상세정보
        album_list = soup.find(
            'div', class_='album-list-wrapper').find_all('a')

        # 앨범 상세정보 경로 찾기
        album_detail_list = []
        for album in album_list:
            album_detail_list.append(album['href'])

        # 앨범 상세정보 수집
        print(f'상세페이지 이동')
        for album_detail in album_detail_list:
            album_detail_url = config.BASE_URL + album_detail
            driver.get(album_detail_url)
            time.sleep(config.CONST_DELAY_TIME)

            # 페이지 파싱
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # 등록일 추출
            sCreated_at = soup.find('span', class_='date').text.strip()
            sCreated_at_list = re.findall(r'\d+', sCreated_at)
            sCreated_at = sCreated_at_list[0] + \
                sCreated_at_list[1].zfill(2) + sCreated_at_list[2].zfill(
                    2) + sCreated_at_list[3].zfill(2) + sCreated_at_list[4].zfill(2)
            dtCreated_at = datetime.strptime(sCreated_at, '%Y%m%d%I%M')
            sCreated_at = datetime.strftime(dtCreated_at, '%Y%m%d%I%M')

            # 저장경로 폴더생성
            path = config.OUTPUT_ALBUMS + sCreated_at + '/'
            util.createFolder(path)

            # 앨범페이지 스크린샷
            print(f'스크린샷 다운로드 시작')

            def S(X): return driver.execute_script(
                'return document.body.parentNode.scroll' + X)
            driver.set_window_size(S('Width'), S('Height'))
            screenshot_name = path + sCreated_at + '_screenshot' + '.png'
            driver.find_element(
                By.CLASS_NAME, 'page-inner').screenshot(screenshot_name)
            print(f'스크린샷 다운로드 완료')

            # 동영상 다운로드
            print(f'동영상 다운로드 시작')
            video_section = soup.find('div', class_='video-section')
            if video_section is not None:
                download_url = soup.find('source')['src']
                name, ext = os.path.splitext(download_url)
                video_name = sCreated_at + '_video' + ext
                fullPath = path + video_name

                print(f'{fullPath} 다운로드 시작')
                urllib.request.urlretrieve(download_url, fullPath)
                print(f'{fullPath} 다운로드 완료')
            print(f'동영상 다운로드 완료')

            # 이미지 다운로드
            print(f'이미지 다운로드 시작')
            img_grid = soup.find('div', class_='image-section')
            if img_grid is not None:
                imgs = img_grid.find_all('div', class_='grid')
                for img in imgs:
                    download_url = img.find('a')['data-download']
                    name, ext = os.path.splitext(download_url)
                    img_name = sCreated_at + '-' + img['data-index'] + ext
                    fullPath = path + img_name

                    print(f'{fullPath} 다운로드 시작')
                    urllib.request.urlretrieve(download_url, fullPath)
                    print(f'{fullPath} 다운로드 완료')
            print(f'이미지 다운로드 완료')

    driver.quit()
    print(f'앨범 다운로더 종료')
