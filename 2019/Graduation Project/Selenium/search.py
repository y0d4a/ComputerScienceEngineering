import re
import string
import sys
import requests
import time
from collections import Counter
from random import randint
from urllib.request import urlopen
from datetime import datetime
from pymongo import MongoClient
from selenium import webdriver
from konlpy.tag import Kkma
from glob import glob

chrome_options = webdriver.ChromeOptions() # 크롬 옵션 객체 생성
chrome_options.add_argument('headless') # headless 모드 설정
chrome_options.add_argument("--disable-gpu") # gpu 허용 안함
chrome_options.add_argument("lang=ko_KR") # 한국어 설정

# User-Agent 설정
chrome_options.add_argument(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
)

driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe', chrome_options=chrome_options)
driver.implicitly_wait(3)

########################################################################################################################
# 프론트엔드에서 사용자가 키워드를 입력하거나 페이지를 옮기면서 url이 변할 경우
# 메인 함수에 url이 인자로 들어옴(이전 페이지, 현재 페이지)
def main():

    # url을 응답해서 그 url에 맞는 크롤링 방식 채택
    # 몽고 DB에 들어갈 속성 : 사용자 번호, 프로젝트 방 번호, 키워드, 현재 페이지, 이전 페이지, 페이지 리스트, 레벨, 서브 키워드
    currUrl = "https://www.google.com/search?safe=active&ei=SbhfXY7UN6zxhwPfirKICA&q=%ED%95%9C%EA%B5%AD%EA%B8%B0%EC%88%A0%EA%B5%90%EC%9C%A1%EB%8C%80%ED%95%99%EA%B5%90&oq=%ED%95%9C%EA%B5%AD%EA%B8%B0%EC%88%A0%EA%B5%90%EC%9C%A1%EB%8C%80%ED%95%99%EA%B5%90&gs_l=psy-ab.3..35i39j0l9.72262.75171..75311...5.1..4.118.2383.16j8......0....1..gws-wiz.......0i71j0i20i263j0i131j0i131i67j0i67.s8br1WxmPf0&ved=0ahUKEwjOnJeO3ZjkAhWs-GEKHV-FDIEQ4dUDCAo&uact=5"
    speech = "http://pythonscraping.com/files/inaugurationSpeech.txt"
    default_page = 'https://www.google.com/'
    search_page = 'https://www.google.com/search?'


    # 현재 페이지에 대한 크롤링 준비
    driver.get(currUrl)
    driver.implicitly_wait(2)
    pageContents = driver.find_element_by_xpath('/html/body')
    parseEnglishSubKeyword(pageContents)


    # 만약 현재 페이지가 새 탭으로 넘어가거나 키워드가 없는 검색창인 경우
#     if currUrl == default_page:
#         print('==============검색창인 경우==============')
#         keyword = ''
#         currUrl = currUrl
# #        prevUrl = prevUrl
#         pageList = []
#         level = 0
#         subkeyword = []
#         nowTime = datetime.now()

    # 만약 현재 페이지가 키워드를 입력하고 난 검색 페이지인 경우
    # 키워드, url 리스트 추출
#    if search_page in currUrl:
#          print('==============검색 페이지인 경우==============')
#          keyword = parseKeyword()
#          print(keyword)
#        currUrl = currUrl
#        prevUrl = prevUrl
#        pageList = parsePageList(currUrl)
#        level = 1
#        subkeyword = []
#        nowTime = datetime.now()

    # 만약 현재 페이지가 홈페이지인 경우(레벨 2)
    # 현재 url, 서브 키워드 추출
#     else:
#         print('==============홈페이지인 경우==============')
#         keyword = parseKeyword()
#         currUrl = currUrl
# #        prevUrl = prevUrl
#         pageList = []
#         level = 2
#         subkeyword = parseSubKeyword(currUrl)
#         nowTime = datetime.now()

    # 만약 현재 페이지가 홈페이지인 경우(레벨 3 ~ )


    # 추출된 아이템들을 몽고 DB에 저장
#    print('추출된 아이템들 몽고 DB로 저장하기')
#    store_mongoDB(keyword, prevUrl, currUrl, pageList, level, subkeyword, nowTime)
#    store_mongoDB(keyword, currUrl, pageList, level, subkeyword, nowTime)
    return 0

########################################################################################################################
# 키워드 추출 함수(검색창인 경우에만)
def parseKeyword():

    print('키워드 추출 중')
    for i in range(1, 40):
        print('▶', end="", flush=True)
        time.sleep(0.1)
    print('')

    crawl_keyword = driver.find_element_by_xpath('/html/head/title')
    keyword = crawl_keyword.get_attribute('text')
    split_keyword = keyword.split(' ')
    print(split_keyword[0])

########################################################################################################################
# 서브 키워드 추출 함수(한글)
def parseKoreanSubKeyword(pageContents):

    print('서브 키워드 추출 중')
    for i in range(1, 40):
        print('▶', end="", flush=True)
        time.sleep(0.1)
    print('')

    wordlist = ""
    for p in pageContents.find_elements_by_tag_name('p'):
        content = p.text
        wordlist += content

    ########## 한글 서브 키워드 추출 ##########
    kkma = Kkma()
    node = kkma.pos(wordlist)
    tokens = []
    for (taeso, pumsa) in node:
        # 고유 명사와 일반 명사만 추출
        if pumsa in ('NNG', 'NNP'):
            tokens.append(taeso)

    frequency = Counter()
    frequency.update(tokens)

    # 상위 30개 단어 추출
    for token, count in frequency.most_common(30):
        print(token, count)

########################################################################################################################
# 서브 키워드 추출 함수(영어)
def parseEnglishSubKeyword(pageContents):

    print('서브 키워드 추출 중')
    for i in range(1, 40):
        print('▶', end="", flush=True)
        time.sleep(0.1)
    print('')

    wordlist = ""
    for p in pageContents.find_elements_by_tag_name('p'):
        content = p.text
        wordlist += content

    ########## 영어 서브 키워드 추출 ##########
    




########################################################################################################################
# 페이지 리스트 추출 함수
def parsePageList():

    print('페이지 리스트 추출 중')
    for i in range(1, 40):
        print('▶', end="", flush=True)
        time.sleep(0.1)
    print('')

    pageList = driver.find_element_by_xpath("//div[@id='rso']")
    for p in pageList.find_elements_by_tag_name('cite'):
        print(p.text)

########################################################################################################################
# 정규화(연결되어 있는 공백을 하나의 공백으로 변경하고 삭제)
def normalize_spaces(s) :
    return re.sub(r'\s+', ' ', s).strip()

########################################################################################################################
# # 몽고 DB에 각종 정보 저장
# # def store_mongoDB(keyword, prevUrl, currUrl, pageList, level, subkeyword, nowTime):
# def store_mongoDB(keyword, currUrl, pageList, level, subkeyword, nowTime):
#     print("몽고 DB에 저장 중...")
#
#     client = MongoClient(
#         'mongodb+srv://dots_user:TzE66c5O0KB0bnjG@dots-test-x41en.mongodb.net/test?retryWrites=true&w=majority')
#     db = client['Project']
#     collection = db['JMH']
#
#     crawl_info = {
#         "키워드": keyword,
# #        "이전 페이지": prevUrl,
#         "현재 페이지": currUrl,
#         "페이지 리스트": pageList,
#         "레벨": level,
#         "서브 키워드": subkeyword,
#         "추출 시간": nowTime,
#     }
#
#     print(crawl_info)
#
#     collection.insert_one(crawl_info)
#
#     print("몽고 DB에 저장 완료!")

if __name__ == '__main__':
    main()
