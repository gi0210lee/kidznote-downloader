import os
import requests
import time
from src import util
from src import config
import re
from datetime import datetime
from bs4 import BeautifulSoup
import imgkit
from html2image import Html2Image

print(f'앨범 시작')

# 앨범 마지막 페이지 구하기
res = requests.get(config.ALNUMS_URL, headers=config.CUSTOM_HEADERS)
soup = BeautifulSoup(res.content, 'html.parser')

page_list = soup.find_all('a', class_='page-link')

number = 0
last_page = 0
for i in page_list:
    number = number + 1
last_page = page_list[number - 2].text

page = 0
while page <= int(last_page):
    page = page + 1

    # 앨범 페이지 별 목록
    albums_page_url = config.ALNUMS_URL + '?page=' + str(page)
    res = requests.get(albums_page_url, headers=config.CUSTOM_HEADERS)
    soup = BeautifulSoup(res.content, 'html.parser')
    a_list = soup.find('div', class_='album-list-wrapper').find_all('a')

    href_list = []
    for href in a_list:
        href_list.append(href['href'])

    for href_item in href_list:
        # 알림장 상세 페이지
        detail_url = config.BASE_URL + href_item
        res = requests.get(detail_url, headers=config.CUSTOM_HEADERS)
        soup = BeautifulSoup(res.content, 'html.parser')

        # 등록일 추출
        sCreated_at = soup.find('span', class_='date').text.strip()
        sCreated_at_list = re.findall(r'\d+', sCreated_at)
        sCreated_at = sCreated_at_list[0] + \
            sCreated_at_list[1].zfill(2) + sCreated_at_list[2].zfill(
                2) + sCreated_at_list[3].zfill(2) + sCreated_at_list[4].zfill(2)
        dtCreated_at = datetime.strptime(sCreated_at, '%Y%m%d%I%M')
        sCreated_at = datetime.strftime(dtCreated_at, '%Y%m%d%I%M')

        # 타이틀(제목 추출)
        sTitle = soup.find('h3', class_='sub-header-title').text.strip()

        # 타이틀 명으로 폴더 생성
        path = config.OUTPUT_ROOT + 'albums/' + sCreated_at + '/'
        util.createFolder(path)

        # 본문 이쁘게
        contentString = soup.find('div', class_='content-text')
        contentString_list = []
        for s in contentString:
            contentString_list.append(s.text)
        content_body = '\n'.join(contentString_list)

        # 댓글
        comment_list = soup.find(
            'ul', class_='comment-list').find_all('li', class_='comment')
        if comment_list is not None:
            comment_body_list = []
            for comment_item in comment_list:
                comment_author = comment_item.find(
                    'span', class_='author-name').text
                comment_time = comment_item.find(
                    'span', class_='date-written').text
                commentString = comment_item.find('p')
                commentString_list = []
                for s in commentString:
                    commentString_list.append(s.text)
                commentStr = '<br/>'.join(commentString_list)
                comment_body_list.append('↪️' + comment_author + '<br/>' +
                                         comment_time + '<br/>' + commentStr + '<br/>')
            comment_body = '<br/>'.join(comment_body_list)

        # 텍스트 파일로 본문 댓글 저장
        # filename = path + sCreated_at + '.txt'
        # report = '🕧 일시' + '\n' + sCreated_at + '\n\n' + \
        #     '🟠 제목' + '\n' + sTitle + '\n\n' + \
        #     '🟠 본문' + '\n' + content_body + '\n\n' + \
        #     '🟠 댓글' + '\n' + comment_body

        # print(f'{filename} 생성')
        # util.SaveFile(filename, report)

        # 스크린샷 파일 생성
        htmlFile = f'{path}{sCreated_at}.html'
        ImgFile = f'{sCreated_at}_screenshot.jpg'
        print(f'{path}{ImgFile} 화면 생성')
        # util.SaveFile(htmlFile, res.text)

        util.HtmlToImageWithSelenium(
            header_url=util.getCookiesFromDomain(
                'kidsnote', ''), url=detail_url, output_file='1.png')
        # hti = Html2Image(output_path=path)
        # hti.screenshot(html_file=htmlFile, size=[2000, 2000], save_as=ImgFile)

        exit()

        # 동영상 다운로드
        video_section = soup.find('div', class_='video-section')
        if video_section is not None:
            source = soup.find('source')['src']

            download_url = source
            name, ext = os.path.splitext(download_url)
            video_name = sCreated_at + ext
            fullPath = path + video_name

            print(f'{fullPath} 생성')
            os.system(f'curl "{download_url}" --output {fullPath}')

        # 이미지 다운로드
        img_grid = soup.find('div', class_='image-section')
        if img_grid is not None:
            imgs = img_grid.find_all('div', class_='grid')
            for img in imgs:
                download_url = img.find('a')['data-download']
                name, ext = os.path.splitext(download_url)
                img_name = sCreated_at + '-' + img['data-index'] + ext

                fullPath = path + img_name
                res = requests.get(download_url)

                print(f'{fullPath} 생성')
                os.system(f'curl "{download_url}" --output {fullPath}')

print(f'종료')
