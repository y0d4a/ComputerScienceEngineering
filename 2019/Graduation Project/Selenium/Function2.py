"""
    기능 2 : 모든 사용자들의 정보들을 하나로 합친 두 번째 통합 테이블(방문비율 포함 o)

    해당 URL의 방문비율 = 해당 URL의 방문횟수 / 총 사용자 수

    ※ 본 기능 2에는 어떠한 인자 값이 들어오지 않음
"""

from pymongo import MongoClient
import pandas as pd

# 몽고 DB 연결
conn = MongoClient('mongodb+srv://dots_user:TzE66c5O0KB0bnjG@dots-test-x41en.mongodb.net/test?retryWrites=true&w=majority')
db = conn['JMH']
collection = db['project_before_data']

# 통합 테이블 v1에서 현재 페이지만 모은 리스트
user_list = []
curr_url_list = []

dataList = collection.find()
for data in dataList:
    user_list.append(data['user_name'])
    curr_url_list.append(data['curr_url'])

# pandas로 data chart 만들기
pivot_data = {
    "curr_url": curr_url_list,
    "user_name": user_list,
}

columns = ["curr_url", "user_name"]
table = pd.DataFrame(pivot_data, columns=columns)

# 총 url 수
url_count = len(table['curr_url'].unique())
# 총 사용자 수
user_count = len(table['user_name'].unique())

# url 빈도수를 구해서 테이블에 추가
table['freq'] = table.groupby('curr_url')['curr_url'].transform('count') / user_count

frequency = table['freq'].values
visit_rate = []
for f in frequency:
    f = format(f, '.2f')
    visit_rate.append(f)

# 방문 비율을 첫 번째 통합 테이블에 추가한 새로운 통합 테이블
newCollection = db['project_after_data']
dataList = collection.find()

index = 0
for data in dataList:
    upload_data = {
        "_id": data['_id'],
        "user_name": data['user_name'],
        "user_email": data['user_email'],
        "curr_url": data['curr_url'],
        "prev_url": data['prev_url'],
        "visit_rate": visit_rate[index],
        "pageList": data['pageList'],
        "relativeKeywordList": data['relativeKeywordList'],
        "level": data['level'],
        "paths": data['paths'],
        "keyword": data['keyword'],
        "sub_keyword": data['sub_keyword'],
        "pageContents": data['pageContents'],
        "memo": data['memo'],
        "tagged": data['tagged'],
        "nowTime": data['nowTime'],
        "screenshot": data['screenshot'],
    }

    index += 1
    newCollection.insert_one(upload_data)