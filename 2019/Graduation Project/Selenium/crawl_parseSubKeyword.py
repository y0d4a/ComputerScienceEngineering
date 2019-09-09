import time
from collections import Counter
from konlpy.tag import Kkma # 한글 데이터 추출
from nltk import word_tokenize # 영어 데이터 추출
from nltk import pos_tag # 영어 데이터 추출

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

# 서브 키워드 추출 함수
def parseSubKeyword(pageContents):

    print('서브 키워드 추출 중')
    for i in range(1, 40):
        print('▶', end="", flush=True)
        time.sleep(0.1)
    print('')

    tokenslist = []
    for p in pageContents.find_elements_by_tag_name('p'):
        content = p.text

        # content의 텍스트가 한글인지 영어인지 확인해보기
        if isEnglishOrKorean(content) == 'kr':
            tokenslist.extend(parseKoreanSubKeyword(content))
        else:
            tokenslist.extend(parseEnglishSubKeyword(content))

    frequency = Counter()
    frequency.update(tokenslist)

    # 상위 30개 단어 추출
    highFreqWord = {}
    for token, count in frequency.most_common(30):
        highFreqWord[token] = count

    return highFreqWord

# 서브 키워드 추출 함수(영어)
def parseEnglishSubKeyword(content):

    wordlist = word_tokenize(content)
    node = pos_tag(wordlist)
    tokens = []
    for (taeso, pumsa) in node:
        # 명사만 추출
        if pumsa in ('NN', 'NNS', 'NNP', 'NNPS'):
            tokens.append(taeso)

    return tokens

# 서브 키워드 추출 함수(한글)
def parseKoreanSubKeyword(content):

    kkma = Kkma()
    node = kkma.pos(content)
    tokens = []
    for (taeso, pumsa) in node:
        # 고유 명사와 일반 명사만 추출
        if pumsa in ('NNG', 'NNP'):
            tokens.append(taeso)

    return tokens
