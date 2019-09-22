"""
    기능 5 : 태그 표시된 노드들만 볼 수 있는 기능

    태그 표시 노드 기능을 누를 시 DB에 있는 document들 중 tagged가 Important인 것만 출력시킨다.
"""

from pymongo import MongoClient

# 몽고 DB 연결
conn = MongoClient('mongodb+srv://dots_user:TzE66c5O0KB0bnjG@dots-test-x41en.mongodb.net/test?retryWrites=true&w=majority')
db = conn['JMH']
collection = db['second_integrated_user_table']

# 필요한 속성만 뽑아서 dataList에 추가
dataList = collection.aggregate([
    { # 보고 싶은 속성만 출력(1은 보고 싶음, 0은 안보고 싶음)
        '$project':
            {
                # "_id": 1,
                "user_name": 0,
                "user_email": 0,
                "curr_url": 0,
                "prev_url": 0,
                "visit_rate": 0,
                "pageList": 0,
                "relativeKeywordList": 0,
                "level": 0,
                "parent_id": 0,
                "path": 0,
                # "keyword": 1,
                "sub_keyword": 0,
                "pageContents": 0,
                # "tagged": 1,
                "nowTime": 0,
                "screenshot": 0,
            }
    },
])

def tagged_Node():

    tagged_Data = []
    for data in dataList:
        if data['tagged'] == 'Important':
            tagged_Data.append(data['_id'])

    print(tagged_Data)

tagged_Node()