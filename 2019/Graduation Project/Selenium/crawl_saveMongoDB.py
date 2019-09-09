import time
from pymongo import MongoClient

# 몽고 DB에 각종 정보 저장
def store_mongoDB(keyword, currUrl, prevUrl, pageList, relativeKeywordList, level, subkeyword, imgs, tags, nowTime):

    print('몽고 DB에 저장 중')
    for i in range(1, 40):
        print('▶', end="", flush=True)
        time.sleep(0.1)
    print('')

    client = MongoClient('mongodb+srv://dots_user:TzE66c5O0KB0bnjG@dots-test-x41en.mongodb.net/test?retryWrites=true&w=majority')
    db = client['BackEnd_Scraping']
    collection = db['before']

    crawl_info = {
        "키워드": keyword,
        "현재 페이지": currUrl,
        "이전 페이지": prevUrl,
        "페이지 리스트": [pageList],
        "연관 키워드 리스트(URL)": [relativeKeywordList],
        "레벨": int(level),
        "서브 키워드(빈도수)": [subkeyword],
        "스크린 샷": [imgs],
        "태그": tags,
        "추출 시간": nowTime,
    }

    collection.insert_one(crawl_info)
