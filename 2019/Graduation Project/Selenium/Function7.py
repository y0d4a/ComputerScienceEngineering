"""
    기능 7 : 크롤링된 데이터를 기반으로 데이터 시각화

    1) pie 차트로 방문 비율을 시각화
    2) 키워드 중심으로 키워드 분포도, 워드 클라우드 등 데이터 시각화 모델 생성
"""

from pymongo import MongoClient

class Function7:

    def __init__(self):
        conn = MongoClient('mongodb+srv://dots_user:TzE66c5O0KB0bnjG@dots-test-x41en.mongodb.net/test?retryWrites=true&w=majority')
        db = conn['JMH']
        collection = db['second_integrated_user_table']
