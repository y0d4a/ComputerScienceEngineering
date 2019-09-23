"""
    프론트엔드에서 사용자가 키워드를 입력하거나 페이지를 옮기면서 url이 변할 경우 메인 함수에 json 객체가 들어옴(현재 페이지, 이전 페이지, 레벨, 태그)
    url을 응답해서 그 url에 맞는 크롤링 방식 채택
"""

import json
import crawl_initiateChromeDriver
import crawl_parseKeyword
import crawl_parseKoreanContents
import crawl_parseEnglishContents
import crawl_isEnglishOrKorean
import crawl_parsePageList
import crawl_parseRelativeKeyword
import crawl_parseScreenshot
import crawl_saveMongoDB
import crawl_saveExcel
from datetime import datetime

def main(jsonFile):
    # 검색 페이지인 경우를 알기 위한 변수
    search_page = 'https://www.google.com/search?'

    # 메인 함수에 들어오는 json 객체 파일 열기
    with open(jsonFile) as f:
        data = json.loads(f.read())

        user_name = data['user_name']
        user_email = data['user_email']
        curr_url = data['curr_url']
        prev_url = data['prev_url']
        paths = data['paths']
        level = data['level']
        tagged = data['tagged']
        memo = data['memo']
        project_name = data['project_name']

    # 현재 페이지에 대한 크롤링 준비
    driver = crawl_initiateChromeDriver.initiateChromeDriver()
    driver.get(curr_url)
    driver.implicitly_wait(2)

    # 검색 페이지인 경우
    if search_page in curr_url:
        print('검색 페이지인 경우')
        user_name = user_name
        user_email = user_email
        keyword = crawl_parseKeyword.parseKeywordSearchPage(driver)
        curr_url = curr_url
        prev_url = prev_url
        pageList = crawl_parsePageList.parsePageList(driver)
        relativeKeywordList = crawl_parseRelativeKeyword.parseRelativeKeyword(driver)
        pageContents = []
        sub_keyword = []
        tagged = tagged
        screenshot = crawl_parseScreenshot.parseScreenshot(driver, user_name, keyword)
        nowTime = datetime.now()

    # 홈페이지인 경우
    else:
        print('홈페이지인 경우')
        user_name = user_name
        user_email = user_email
        keyword = crawl_parseKeyword.parseKeywordHomePage(driver)
        curr_url = curr_url
        prev_url = prev_url
        pageList = []
        relativeKeywordList = []

        # 서브 키워드 및 본문 요약은 키워드가 한글 또는 영어에 따라 다르다.
        if crawl_isEnglishOrKorean.isEnglishOrKorean(keyword) == 'kr':
            textrank = crawl_parseKoreanContents.TextRank(curr_url)
            pageContents = textrank.summarize(5)
            sub_keyword = textrank.keywords()
        else:
            textrank = crawl_parseEnglishContents.TextRank(curr_url)
            pageContents = textrank.summarize(5)
            sub_keyword = textrank.keywords()

        tagged = tagged
        memo = memo
        screenshot = crawl_parseScreenshot.parseScreenshot(driver, user_name, keyword)
        nowTime = datetime.now()

    # 추출된 아이템들을 몽고 DB에 저장
    crawl_saveMongoDB.store_mongoDB(user_name, user_email, curr_url, prev_url, pageList, relativeKeywordList, level, paths, keyword, sub_keyword, pageContents, memo, screenshot, tagged, nowTime, project_name)

    # 추출된 아이템들을 엑셀에 저장
    crawl_saveExcel.make_excel(user_name, keyword)
    crawl_saveExcel.crawl_saveExcel(user_name, user_email, curr_url, prev_url, pageList, relativeKeywordList, level, paths, keyword, sub_keyword, pageContents, memo, screenshot, tagged, str(nowTime))

    # 드라이버 연결 끊기
    driver.close()

if __name__ == '__main__':
    main()