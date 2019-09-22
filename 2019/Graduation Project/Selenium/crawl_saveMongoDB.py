from pymongo import MongoClient

# 몽고 DB에 각종 정보 저장
def store_mongoDB(user_name, user_email, curr_url, prev_url, pageList, relativeKeywordList, level, paths, keyword, sub_keyword, pageContents, memo, screenshot, tagged, nowTime):

    client = MongoClient('mongodb+srv://dots_user:TzE66c5O0KB0bnjG@dots-test-x41en.mongodb.net/test?retryWrites=true&w=majority')
    db = client['JMH']

    collection_name = 'project_' + user_email
    collection = db[collection_name]

    crawl_info = {
        "user_name": user_name,
        "user_email": user_email,
        "curr_url": curr_url,
        "prev_url": prev_url,
        "pageList": pageList,
        "relativeKeywordList": relativeKeywordList,
        "level": int(level),
        "paths": paths,
        "keyword": keyword,
        "sub_keyword": sub_keyword,
        "pageContents": pageContents,
        "memo": memo,
        "tagged": tagged,
        "nowTime": nowTime,
        "screenshot": screenshot,
    }

    collection.insert_one(crawl_info)