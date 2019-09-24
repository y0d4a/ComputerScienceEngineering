"""
    기능 8 : 사용자의 요청에 따라 몽고 DB에 있는 컬렉션의 태그 수정 기능

    사용자가 프로그램을 사용하는 중에 태그 기능에서 필요하다고 생각되어 눌렀다가 이후 취소햇을 경우, 혹은 반대인 경우에
    태그의 유무를 테이블에서 즉시 바꿀 수 있도록 개인 테이블의 업데이트 기능이 있어야 한다.

    ※ 본 기능 8은 입력으로 수정하고자 하는 프로젝트 명, 수정하고자 하는 사용자의 이메일, 수장하고자 하는 노드 ID, 수정하고자 하는 태그가
    입력으로 들어오고, 해당 컬렉션의 정보를 업데이트 해준다.
"""

from pymongo import MongoClient
from bson import ObjectId

class Function8:

    def update_user_collection(self, project_name, user_email, object_id, re_tagged, re_memo):
        conn = MongoClient('mongodb+srv://dots_user:TzE66c5O0KB0bnjG@dots-test-x41en.mongodb.net/test?retryWrites=true&w=majority')
        db = conn['JMH']
        collection = db[project_name + '_' + user_email]

        # object_id는 객체 ObjectID로 변환을 해줘야 한다.
        collection.update_one({'_id': ObjectId(object_id)}, {'$set': {'tagged': re_tagged, 'memo': re_memo}})

    def update_all_user_collection(self, project_name, object_id, re_tagged, re_memo):
        conn = MongoClient('mongodb+srv://dots_user:TzE66c5O0KB0bnjG@dots-test-x41en.mongodb.net/test?retryWrites=true&w=majority')
        db = conn['JMH']
        collection = db[project_name + '_after_data']

        # object_id는 객체 ObjectID로 변환을 해줘야 한다.
        collection.update_one({'_id': ObjectId(object_id)}, {'$set': {'tagged': re_tagged, 'memo': re_memo}})