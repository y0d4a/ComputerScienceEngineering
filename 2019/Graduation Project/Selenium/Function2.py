"""
    기능 2 : 다수/소수의 노드 반환

    최대 방문비율(다수)을 가질 수록 파란색, 최소 방문비율(소수)을 가질 수록 빨간색으로 노드를 표시한다.
    최대 방문비율와 최소 방문비율의 결정 기준은 0.5이다.

    ※ 본 기능 2에는 프로젝트명과 노드의 ID가 입력되면 해당 노드 ID의 방문비율을 몽고 DB에서 가져와
    결정 기준치 값 이상이면 'Blue'를, 미만이면 'Red'를 반환한다.
"""

from pymongo import MongoClient

class Function2:

    def is_blue_or_red_node(self, project_name, object_id):
        conn = MongoClient('mongodb+srv://dots_user:TzE66c5O0KB0bnjG@dots-test-x41en.mongodb.net/test?retryWrites=true&w=majority')
        db = conn['JMH']
        collection = db[project_name + '_after_data']

        dataList = collection.find()
        for data in dataList:
            if str(data['_id']) == object_id:
                visit_rate = float(data['visit_rate'])

                if visit_rate >= 0.5:
                    return 'Blue'
                else:
                    return 'Red'