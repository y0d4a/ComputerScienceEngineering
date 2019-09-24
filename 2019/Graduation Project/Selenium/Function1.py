"""
    기능 1 : 모든 사용자들의 정보들을 하나로 합친 통합 테이블

    사용자들의 이메일 정보를 인자로 받아서 각각에 해당하는 컬렉션들을 통합

    ※ 본 기능 1은 사용자들의 크롤링이 모두 끝나면 프론트 엔드에서 'stop' 시그널을 플라스크 서버로 요청한다.
    플라스크 서버에서 'stop' 시그널을 받으면 프로젝트 명을 입력으로 받아 기능 1을 실행시킨다.
"""

import pandas as pd
from pymongo import MongoClient

class Function1:

    def create_integrated_collection(self, project_name):
        self.conn = MongoClient('mongodb+srv://dots_user:TzE66c5O0KB0bnjG@dots-test-x41en.mongodb.net/test?retryWrites=true&w=majority')
        self.db = self.conn['JMH']

        list_collection_names = self.db.list_collection_names()
        collection_names = []
        for list in list_collection_names:
            if project_name in list:
                collection_names.append(list)

        # 총 사용자 수
        numOfUsers = len(collection_names)

        self.all_user_tableList = []
        for i in range(numOfUsers):
            self.collection = self.db[collection_names[i]]

            integratedData = self.collection.find()

            user_tableList = []
            for data in integratedData:
                user_tableList.append(data)

            # 전체 사용자 통합 리스트 생성
            self.all_user_tableList.extend(user_tableList)

        # 통합 테이블에서 현재 페이지만 모은 리스트
        user_list = []
        curr_url_list = []

        for data in self.all_user_tableList:
            user_list.append(data['user_name'])
            curr_url_list.append(data['curr_url'])


        # pandas로 data chart 만들기
        pivot_data = {
            "curr_url": curr_url_list,
            "user_name": user_list,
        }

        columns = ["curr_url", "user_name"]
        table = pd.DataFrame(pivot_data, columns=columns)

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
        newCollection = self.db['project_after_data']

        index = 0
        for data in self.all_user_tableList:
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

f1 = Function1('first_project')