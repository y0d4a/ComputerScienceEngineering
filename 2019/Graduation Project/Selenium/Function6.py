"""
    기능 6 : 추천 노드(경로)

    현재까지 졸업작품 수준을 고려했을 경우, 모든 사용자들의 통합 테이블을 가져와서 만든 전체 노드 그래프에서
    수식[0.5 * 태그 유무(없으면 0, 있으면 1) + 0.5 * 방문비율]을 사용해서 각각의 노드의 최종 중요도 값을 구한다.
    기준 중요도 값[1 / 노드 레벨] 이상일 경우 추천 노드로 선정한다.
    즉, 압축된 형식의 노드 그래프를 만들어서 사용자에게 제공해준다. 단, 노드 레벨이 1인 경우는 모두 표시한다.

    이후에는 새로운 리소스(내부에서 만들어진 노드만 이 아닌 외부 추천 검색어)를 가지고와서 새로운 노드 그래프를 만들어 제시해준다.

    ※ 본 기능 6은 통합 테이블이 모두 만들어진 이후에 추천 경로의 기능을 입력받으면 실행한다.
"""

from pymongo import MongoClient

class Function6:

    def __init__(self, project_name):
        conn = MongoClient('mongodb+srv://dots_user:TzE66c5O0KB0bnjG@dots-test-x41en.mongodb.net/test?retryWrites=true&w=majority')
        db = conn['JMH']
        collection = db[project_name + '_after_data']

        # 필요한 속성만 뽑아서 dataList에 추가
        self.dataList = collection.aggregate([
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
                        "paths": 0,
                        "keyword": 0,
                        "sub_keyword": 0,
                        "pageContents": 0,
                        "memo": 0,
                        # "tagged": 1,
                        "nowTime": 0,
                        "screenshot": 0,
                    }
            },
        ])

    def recommend_path_node(self):
        recommend_node = []

        for data in self.dataList:
            object_id = data['_id']
            tagged = data['tagged']
            visit_rate = float(data['visit_rate'])
            level = float(data['level'])

            if tagged == 'Important':
                recommend_value_tagged = 1
            else:
                recommend_value_tagged = 0

            recommend_value_total = 0.5 * float(recommend_value_tagged) + 0.5 * visit_rate

            if recommend_value_total >= float(1 / level):
                recommend_node.append(object_id)

        return recommend_node