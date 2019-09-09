import time
from pymongo import MongoClient
from pprint import pprint

conn = MongoClient('mongodb+srv://dots_user:TzE66c5O0KB0bnjG@dots-test-x41en.mongodb.net/test?retryWrites=true&w=majority')
db = conn['BackEnd_Scraping']
collection = db['before']

# 레벨 순으로 정렬하기
integratedData = collection.aggregate([
    { # 원하는 속성으로 정렬(1은 오름차순, -1은 내림차순)
        '$sort':
            {
                '레벨': -1,
            }
    },
    # { # 보고 싶은 속성만 출력(1은 보고 싶음, 0은 안보고 싶음)
    #     '$project':
    #         {
    #             '_id': 0,
    #             # '키워드': 1,
    #             # '현재 페이지': 1,
    #             # '이전 페이지': 1,
    #             '페이지 리스트': 0,
    #             '연관 키워드 리스트(URL)': 0,
    #             # '레벨': 1,
    #             '서브 키워드(빈도수)': 0,
    #             '이미지': 0,
    #             '추출 시간': 0
    #         }
    # },
])
#
# dataList = []
# for data in integratedData:
#     dataList.append(list(data.values()))
#
# """
#     기능 5 : 특정 노드(키워드) 클릭 시 어느 키워드로부터 파생되었는지 경로 표시(DFS 함수 이용)
#
#     저장된 데이터를 리스트로 반환하여 리스트 목록 중 자신의 레벨의 이전 페이지와 한 단계 낮은 레벨의 현재 페이지를 비교
#     레벨이 1이 될 때까지 계속해서 비교하다, 레벨이 1이 되는 순간의 키워드를 자신의 데이터 리스트 키워드로 정한다.
# """
# def find_keyword(lv, prev):
#
#     for d in dataList:
#         keyword = d[0]
#         currUrl = d[1]
#         prevUrl = d[2]
#         level = int(d[3])
#
#         # 만약 입력받은 레벨(자신의 레벨)보다 한 단계 낮은 레벨의 현재 페이지와 입력받은 레벨(자신의 레벨)의 이전 페이지가 같을 경우
#         if lv - 1 == level and currUrl == prev:
#             # 레벨이 1인 경우 키워드를 자신의 데이터 리스트 키워드로 변경한다.
#             if level == 1:
#                 print("변경 할 키워드: " + keyword)
#
#             # 레벨이 1이 아닌 경우 반복해서 비교한다.
#             else:
#                 find_keyword(level, prevUrl)
#
# # 원하는 노드의 레벨 입력
# find_level = int(input())
# for d in dataList:
#     level = int(d[3])
#     if level == find_level:
#         find_keyword(level, d[2])
#     elif level < find_level:
#         break

#
# 정리된 테이블을 새로운 collection에 저장하기

print('몽고 DB에 저장 중')
for i in range(1, 40):
    print('▶', end="", flush=True)
    time.sleep(0.1)
print('')

newCollection = db['after']
for col in integratedData:
    crawl_data = {
        "키워드": col['키워드'],
        "레벨": col['레벨'],
        "현재 페이지": col['현재 페이지'],
        "이전 페이지": col['이전 페이지'],
        "페이지 리스트": col['페이지 리스트'],
        "연관 키워드 리스트(URL)": col['연관 키워드 리스트(URL)'],
        "서브 키워드(빈도수)": col['서브 키워드(빈도수)'],
        "스크린 샷": col['스크린 샷'],
        "태그": col['태그'],
        "추출 시간": col['추출 시간'],
    }

    newCollection.insert_one(crawl_data)

print("몽고 DB에 저장 완료!")
