"""
    기능 1 : 모든 사용자들의 정보들을 하나로 합친 첫 번째 통합 테이블(방문비율 포함 x)

    사용자들의 이메일 정보를 인자로 받아서 각각에 해당하는 컬렉션들을 통합

    ※ 본 기능 1은 사용자들의 크롤링이 모두 끝나면 프론트 엔드에서 'stop' 시그널을 플라스크 서버로 요청한다.
    플라스크 서버에서 'stop' 시그널을 받으면 Function1.py를 실행시킨다.
"""

import sys
from pymongo import MongoClient

conn = MongoClient('mongodb+srv://dots_user:TzE66c5O0KB0bnjG@dots-test-x41en.mongodb.net/test?retryWrites=true&w=majority')
all_user_tableList = []

# 몽고 DB에 있는
db_user_email = [sys.argv[1], sys.argv[2], sys.argv[3]]
numOfUsers = len(db_user_email)

for i in range(numOfUsers):
    db = conn['JMH']
    db_collection_name = 'project' + '_' + db_user_email[i]
    collection = db[db_collection_name]

    integratedData = collection.find()

    user_tableList = []
    for data in integratedData:
        user_tableList.append(data)

    # 전체 사용자 통합 리스트 생성
    all_user_tableList.extend(user_tableList)

# 새로운 컬렉션 생성
db = conn['JMH']
newCollection = db['project_before_data']
for tableList in all_user_tableList:
    # tableList는 딕셔너리 형태
    upload_data = {
        "_id": tableList['_id'],
        "user_name": tableList['user_name'],
        "user_email": tableList['user_email'],
        "curr_url": tableList['curr_url'],
        "prev_url": tableList['prev_url'],
        "pageList": tableList['pageList'],
        "relativeKeywordList": tableList['relativeKeywordList'],
        "level": tableList['level'],
        "paths": tableList['paths'],
        "keyword": tableList['keyword'],
        "sub_keyword": tableList['sub_keyword'],
        "pageContents": tableList['pageContents'],
        "memo": tableList['memo'],
        "tagged": tableList['tagged'],
        "nowTime": tableList['nowTime'],
        "screenshot": tableList['screenshot']
    }

    newCollection.insert_one(upload_data)