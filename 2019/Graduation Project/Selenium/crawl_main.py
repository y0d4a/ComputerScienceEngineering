import sys
import json
import crawl_initiateChromeDriver
import crawl_parseKeyword
import crawl_parseSubKeyword
import crawl_parsePageList
import crawl_parseRelativeKeyword
import crawl_parseScreenshot
import crawl_saveMongoDB
import crawl_saveExcel
from datetime import datetime

"""
    프론트엔드에서 사용자가 키워드를 입력하거나 페이지를 옮기면서 url이 변할 경우 메인 함수에 json 객체가 들어옴(현재 페이지, 이전 페이지, 레벨, 태그)
    url을 응답해서 그 url에 맞는 크롤링 방식 채택
    
    몽고 DB에 들어갈 속성 : 사용자 번호, 프로젝트 방 번호, 키워드, 현재 페이지, 이전 페이지, 페이지 리스트, 레벨, 서브 키워드, 태그, 이미지, 추출 시간
"""

def main():

    # 검색 페이지인 경우를 알기 위한 변수
    search_page = 'https://www.google.com/search?'

    # # 메인 함수에 들어오는 json 객체 파일 열기
    # jsonFile = sys.argv[1]
    # with open(jsonFile) as f:
    #     data = json.loads(f.read())
    #
    #     currUrl = data['currUrl']
    #     prevUrl = data['prevUrl']
    #     level = data['level']
    #     tag = data['tag']

    currUrl = sys.argv[1]  # 메인함수 첫 번째 인자로 현재 페이지 입력 받기
    prevUrl = sys.argv[2] # 메인함수 두 번째 인자로 이전 페이지 입력 받기
    level = sys.argv[3] # 메인함수 세 번째 인자로 레벨 입력 받기
    tag = sys.argv[4] # 메인함수 네 번째 인자로 태그 입력 받기(태그 설정 유무)

    # 현재 페이지에 대한 크롤링 준비
    driver = crawl_initiateChromeDriver.initiateChromeDriver()
    driver.get(currUrl)
    driver.implicitly_wait(2)

    # 페이지 본문 내용 추출을 위한 변수
    pageContents = driver.find_element_by_xpath('/html/body')

    # 만약 현재 페이지가 키워드를 입력하고 난 검색 페이지인 경우
    # 키워드, url 리스트, 서브 키워드 추출
    if search_page in currUrl:
        print('===========검색 페이지인 경우===========')
        keyword = crawl_parseKeyword.parseKeyword(driver)
        currUrl = currUrl
        prevUrl = prevUrl
        pageList = crawl_parsePageList.parsePageList(driver)
        relativeKeywordList = crawl_parseRelativeKeyword.parseRelativeKeyword(driver)
        subkeyword = []
        imgs = crawl_parseScreenshot.parseScreenshot(driver, keyword + ".png")
        tags = tag
        nowTime = datetime.now()

    # 만약 현재 페이지가 홈페이지인 경우
    # 서브 키워드 추출
    else:
        print('============홈페이지인 경우============')
        keyword = crawl_parseKeyword.parseKeyword(driver)
        currUrl = currUrl
        prevUrl = prevUrl
        pageList = []
        relativeKeywordList = []
        subkeyword = crawl_parseSubKeyword.parseSubKeyword(pageContents)
        imgs = crawl_parseScreenshot.parseScreenshot(driver, keyword + ".png")
        tags = tag
        nowTime = datetime.now()

    # 추출된 아이템들을 몽고 DB에 저장
    crawl_saveMongoDB.store_mongoDB(keyword, currUrl, prevUrl, pageList, relativeKeywordList, level, subkeyword, imgs, tags, nowTime)

    # 추출된 아이템들을 엑셀에 저장
    crawl_saveExcel.make_excel()
    crawl_saveExcel.crawl_saveExcel(keyword, currUrl, prevUrl, pageList, relativeKeywordList, level, subkeyword, tags, str(nowTime), imgs)

    # 드라이버 연결 끊기
    driver.close()

if __name__ == '__main__':
    main()
