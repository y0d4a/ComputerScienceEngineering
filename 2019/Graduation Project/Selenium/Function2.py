"""
    기능 2 : 사용자 수에 따른 노드의 방문 비율 반환

    사용자별로 접속한 페이지가 같을 경우 그 페이지의 방문횟수를 증가시키면서, 최대 방문횟수(다수)를 가질 수록
    파란색, 최소 방문횟수(소수)를 가질 수록 빨간색으로 노드를 표시한다.

    예시로 User1, User2, User3가 있다 하자. 우선, 각 사용자 개개인이 접속한 페이지에서 나온 값이 중복될 경우는 제외를 해주어야 한다.
    따라서, User1부터 User3까지 중복이 없는 현재 페이지 리스트를 만들고, 모두 합친다.
    통합된 리스트에서 중복된 페이지가 있다면 그 페이지가 최대 방문횟수를 가진 페이지이다.
"""
from pprint import pprint

from pymongo import MongoClient
import pandas as pd

# 몽고 DB 연결
conn = MongoClient('mongodb+srv://dots_user:TzE66c5O0KB0bnjG@dots-test-x41en.mongodb.net/test?retryWrites=true&w=majority')
db = conn['JMH']
collection = db['user1'] # first_integrated_user_table로 수정하기

# 통합 테이블 v1에서 현재 페이지만 모은 리스트
user_list = []
curr_url_list = []
dataList = collection.find()
for data in dataList:
    for idx, d in enumerate(data.values()):
        if idx == 1:
            user_list.append(d)
        elif idx == 2:
            curr_url_list.append(d)

# pandas로 data chart 만들기
pivot_data = {
    "curr_url": curr_url_list,
    "user_name": user_list,
}

columns = ["curr_url", "user_name"]
table = pd.DataFrame(pivot_data, columns=columns)

# 총 사용자 수
user_count = len(table['user_name'].unique())
# 방문자 수를 구하기 위한 그룹 테이블
group_table = table['user_name'].groupby(table['curr_url'])

print(group_table.value_counts())

for gt in group_table:
    for idx, g in enumerate(gt):
        if idx != 0:
            print(g.values)
#
# all_visit_member = []
# for gt in group_table:
#     visit_member = []
#     for idx, g in enumerate(gt):
#         if idx == 0:
#             continue
#         else:
#             visit_member.append(g.values)
#     all_visit_member.append(visit_member)
#
# for a in all_visit_member:
#     print(a[0])

# table['visit_member'] = table['user_name'].groupby(table['curr_url'])
#
# print(table)




# # url 빈도수를 구해서 테이블에 추가
# table['freq'] = table.groupby('curr_url')['curr_url'].transform('count') / user_count
#
# frequency = table['freq'].values
# visit_rate = []
# for f in frequency:
#     f = format(f, '.2f')
#     visit_rate.append(f)

# print(table.sort_values('curr_url'))


# # 방문 비율을 통합 테이블 v1에 추가한 새로운 통합 테이블 v2
# newCollection = db['second_integrated_user_table']
# dataList = collection.find()
# index = 0
# for data in dataList:
#     for idx, d in enumerate(data.values()):
#         if idx == 0:
#             id = d
#         elif idx == 1:
#             userName = d
#         elif idx == 2:
#             currURL = d
#         elif idx == 3:
#             prevURL = d
#         elif idx == 4:
#             relative = d
#         elif idx == 5:
#             level = d
#         elif idx == 6:
#             keyword = d
#
#     upload_data = {
#         "_id": id,
#         "user_name": userName,
#         # "user_email": d['user_email'],
#         "curr_url": currURL,
#         "prev_url": prevURL,
#         "visit_rate": visit_rate[index],
#         # "pageList": d['pageList'],
#         "relativeKeywordList": relative,
#         "level": level,
#         # "parent_id": d['parent_id'],
#         # "path": d['path'],
#         "keyword": keyword,
#         # "sub_keyword": d['sub_keyword'],
#         # "pageContents": d['pageContents'],
#         # "tagged": d['tagged'],
#         # "nowTime": d['nowTime'],
#         # "screenshot": d['screenshot'],
#     }
#
#     index += 1
#
#     newCollection.insert_one(upload_data)