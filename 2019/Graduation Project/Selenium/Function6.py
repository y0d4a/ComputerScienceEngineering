"""
    기능 6 : 추천경로

    현재까지 졸업작품 수준을 고려했을 경우, 모든 사용자들의 통합 테이블을 가져와서 만든 전체 노드 그래프에서
    수식[]을 사용해서 각각의 노드의 최종 중요도 값을 구한다. 기준 중요도 값() 이상일 경우 추천 노드로 선정한다.
    즉, 압축된 형식의 노드 그래프를 만들어서 사용자에게 제공해준다.

    이후에는 새로운 리소스(내부에서 만들어진 노드만 이 아닌 외부 추천 키워드)를 가지고와서
    우리만의 새로운 노드 그래프를 만들어 제시해준다.
"""

from pprint import pprint
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
                # "visit_rate": 1,
                "pageList": 0,
                "relativeKeywordList": 0,
                # "level": 1,
                "parent_id": 0,
                "path": 0,
                "keyword": 0,
                "sub_keyword": 0,
                "pageContents": 0,
                # "tagged": 1,
                "nowTime": 0,
                "screenshot": 0,
            }
    },
])

for data in dataList:
    pprint(data)