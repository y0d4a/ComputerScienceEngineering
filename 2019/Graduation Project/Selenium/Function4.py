"""
    기능 4 : 태그 표시된 노드들만 볼 수 있는 기능

    태그 표시 노드 기능을 누를 시 DB에 있는 'document'들 중 'tagged'가 'Important'인 것만 출력시킨다.

    ※ 본 기능 4는 요청이 있을 경우 프로젝트 명을 입력받아 태그 노드를 반환한다.
"""

from pymongo import MongoClient

class Function4:

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
                        "visit_rate": 0,
                        "pageList": 0,
                        "relativeKeywordList": 0,
                        "level": 0,
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

    def tagged_Node(self):

        tagged_Data = []
        for data in self.dataList:
            if data['tagged'] == 'True':
                tagged_Data.append(data['_id'])

        return tagged_Data