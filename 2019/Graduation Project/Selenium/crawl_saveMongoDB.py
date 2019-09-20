from pymongo import MongoClient

# 몽고 DB에 각종 정보 저장
def store_mongoDB(user_name, user_email, keyword, currUrl, prevUrl, pageList, relativeKeywordList, level, subkeyword, pageContents, screenshot, tags, nowTime):

    client = MongoClient('mongodb+srv://dots_user:TzE66c5O0KB0bnjG@dots-test-x41en.mongodb.net/test?retryWrites=true&w=majority')
    db = client['JMH']
    collection = db['user3']

    crawl_info = {
        "사용자명": user_name,
        "이메일": user_email,
        "현재 페이지": currUrl,
        "이전 페이지": prevUrl,
        "페이지 리스트": pageList,
        "연관 검색어 : URL 리스트": relativeKeywordList,
        "레벨": int(level),
        "키워드": keyword,
        "서브 키워드": subkeyword,
        "본문 요약": pageContents,
        "태그": tags,
        "추출 시간": nowTime,
        "스크린 샷": screenshot,
    }

    collection.insert_one(crawl_info)
