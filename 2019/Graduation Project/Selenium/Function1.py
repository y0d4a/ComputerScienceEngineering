"""
    처음 사용자들의 정보들을 하나로 합친 통합 테이블 v1
"""

from pymongo import MongoClient

numOfUsers = 3

conn = MongoClient('mongodb+srv://dots_user:TzE66c5O0KB0bnjG@dots-test-x41en.mongodb.net/test?retryWrites=true&w=majority')
all_user_tableList = []

for i in range(numOfUsers):
    dbName = 'user' + str(i + 1)
    db = conn['JMH']
    collection = db[dbName]

    integratedData = collection.aggregate([
        # { # 보고 싶은 속성만 출력(1은 보고 싶음, 0은 안보고 싶음)
        #     '$project':
        #         {
        #             "_id": 0,
        #             "user_name": 0,
        #             "user_email": 0,
        #             "curr_url": 0,
        #             "prev_url": 0,
        #             "pageList": 0,
        #             "relativeKeywordList": 0,
        #             "level": 0,
        #             "parent_id": 0,
        #             "path": 0,
        #             "keyword": 0,
        #             "sub_keyword": 0,
        #             "pageContents": 0,
        #             "tagged": 0,
        #             "nowTime": 0,
        #             "screenshot": 0,
        #         }
        # },
    ])

    user_tableList = []
    for data in integratedData:
        user_tableList.append(data)

    # 전체 사용자 통합 리스트 생성
    all_user_tableList.extend(user_tableList)

db = conn['JMH']
newCollection = db['first_integrated_user_table']
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
        "parent_id": tableList['parent_id'],
        "path": tableList['path'],
        "keyword": tableList['keyword'],
        "sub_keyword": tableList['sub_keyword'],
        "pageContents": tableList['pageContents'],
        "tagged": tableList['tagged'],
        "nowTime": tableList['nowTime'],
        "screenshot": tableList['screenshot'],
    }

    newCollection.insert_one(upload_data)