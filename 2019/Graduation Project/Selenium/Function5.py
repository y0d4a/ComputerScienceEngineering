"""
    기능 5 : 노드의 연관성(Word2Vector 사용)

    몽고 DB에 있는 데이터에서 모든 키워드를 대상으로 유사도가 높은 키워드만을 강조 표시하도록 한다.
    미리 학습된 영어와 한국어 파일을 이용해서 입력되는 키워드의 유사도를 계산하여 결과값으로 반환한다.
    반환된 유사도가 85% 이상의 값을 가지면 강조 노드로 표시해준다.
"""

from gensim.models import Word2Vec

# 한국어 Word2Vector 유사도 계산
def korDataSimilarity(keyword1, keyword2):

    model = Word2Vec.load(r'C:\Users\battl\PycharmProjects\ComputerScienceEngineering\2019\Graduation Project\Selenium\LearningDataSet\word2vecko.model')
    return model.wv.similarity(keyword1, keyword2)

# 한국어 Word2Vector 유사 단어 출력
def korDataSimilar(keyword):

    model = Word2Vec.load(r'C:\Users\battl\PycharmProjects\ComputerScienceEngineering\2019\Graduation Project\Selenium\LearningDataSet\word2vecko.model')
    similar_keyword = model.wv.most_similar(keyword)
    return similar_keyword

# 영어 Word2Vector 유사도 계산
def engDataSimilarity(keyword1, keyword2):

    model = Word2Vec.load(r'C:\Users\battl\PycharmProjects\ComputerScienceEngineering\2019\Graduation Project\Selenium\LearningDataSet\word2vecen.model')
    return model.wv.similarity(keyword1, keyword2)

# 영어 Word2Vector 유사 단어 출력
def engDataSimilar(keyword):

    model = Word2Vec.load(r'C:\Users\battl\PycharmProjects\ComputerScienceEngineering\2019\Graduation Project\Selenium\LearningDataSet\word2vecen.model')
    keyword = keyword.lower()
    keyword = keyword.replace(" ", "")
    similar_keyword = model.wv.most_similar(keyword)

    return similar_keyword