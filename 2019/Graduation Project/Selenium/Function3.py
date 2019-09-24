"""
    기능 3 : 특정 노드(키워드) 클릭 시 어느 키워드로부터 파생되었는지 경로 표시(DFS 함수 이용)

    저장된 데이터를 리스트로 반환하여 리스트 목록 중 자신의 레벨의 이전 페이지와 한 단계 낮은 레벨의 현재 페이지를 비교
    레벨이 1이 될 때까지 계속해서 비교하다, 레벨이 1이 되는 순간의 키워드를 자신의 데이터 리스트 키워드로 정한다.

    ※ 본 기능 3에는 프로젝트명과 노드의 ID가 입력되면 해당 노드 ID에 해당하는 파생 키워드까지의 경로와 키워드를 반환한다.
"""

from pymongo import MongoClient

class Function3:

    def __init__(self, project_name):
        conn = MongoClient('mongodb+srv://dots_user:TzE66c5O0KB0bnjG@dots-test-x41en.mongodb.net/test?retryWrites=true&w=majority')
        db = conn['JMH']
        collection = db[project_name + '_after_data']

        # 필요한 속성만 뽑아서 dataList에 추가
        self.dataList = collection.aggregate([
            {
                '$sort':
                    {
                        'level': -1
                    }
            },
            {  # 보고 싶은 속성만 출력(1은 보고 싶음, 0은 안보고 싶음)
                '$project':
                    {
                        # "_id": 1,
                        # "user_name": 1,
                        "user_email": 0,
                        # "curr_url": 1,
                        # "prev_url": 1,
                        "visit_rate": 0,
                        "pageList": 0,
                        "relativeKeywordList": 0,
                        # "level": 1,
                        "path": 0,
                        # "keyword": 1,
                        "sub_keyword": 0,
                        "pageContents": 0,
                        "memo": 0,
                        "tagged": 0,
                        "nowTime": 0,
                        "screenshot": 0,
                    }
            },
        ])

        self.result_origin_keyword_path_id = []
        self.result_origin_keyword = ""

    def find_keyword(self, user, lv, prev):

        for data in self.dataList:
            object_id = data['_id']
            user_name = data['user_name']
            keyword = data['keyword']
            curr_url = data['curr_url']
            prev_url = data['prev_url']
            level = int(data['level'])

            # 만약 입력받은 레벨(자신의 레벨)보다 한 단계 낮은 레벨의 현재 페이지와 입력받은 레벨(자신의 레벨)의 이전 페이지가 같을 경우
            if lv - 1 == level and curr_url == prev and user_name == user:
                # 경로를 얻기 위해 해당 노드의 ID를 얻는다.
                self.result_origin_keyword_path_id.append(object_id)

                # 레벨이 1인 경우 키워드를 반환한다.
                if level == 1:
                    self.result_origin_keyword = keyword
                else:
                    self.find_keyword(user, level, prev_url)
            else:
                continue

    def return_origin_keyword(self, find_node_id):

        for data in self.dataList:
            if str(data['_id']) == find_node_id:
                self.result_origin_keyword_path_id.append(data['_id'])
                self.find_keyword(data['user_name'], data['level'], data['prev_url'])
            else:
                continue

f3 = Function3('first_project')
f3.return_origin_keyword('5d88fa555c40847d78816bf7')

print(f3.result_origin_keyword_path_id)
print(f3.result_origin_keyword)