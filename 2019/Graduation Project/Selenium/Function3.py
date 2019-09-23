"""
    기능 3 : 다수/소수의 노드 반환

    최대 방문비율(다수)을 가질 수록 파란색, 최소 방문비율(소수)을 가질 수록 빨간색으로 노드를 표시한다.
    최대 방문비율와 최소 방문비율의 결정 기준은 0.5이다.

    ※ 본 기능 3에는 노드의 ID가 입력되면 해당 노드 ID의 방문비율을 몽고 DB에서 가져와 결정 기준치 값 이상이면 'Blue'를, 미만이면 'Red'를 반환한다.
"""

from pymongo import MongoClient

# 몽고 DB 연결
conn = MongoClient('mongodb+srv://dots_user:TzE66c5O0KB0bnjG@dots-test-x41en.mongodb.net/test?retryWrites=true&w=majority')
db = conn['JMH']
collection = db['project_after_data']

dataList = collection.find()
for data in dataList:
    print(data)