# 텍스트 문장이 영어인지 한글인지 판별 함수
def isEnglishOrKorean(input_s):

    # 입력받은 문자열의 문자를 하나씩 읽으면서 해당 문자가 한글인지 영어인지를 카운트
    # 한글이 하나라고 있을 경우, 한글로 간주
    k_count = 0
    e_count = 0
    for c in input_s:
        if ord('가') <= ord(c) <= ord('힣'):
            k_count+=1
        elif ord('a') <= ord(c.lower()) <= ord('z'):
            e_count+=1
    return 'kr' if k_count>1 else 'en'
