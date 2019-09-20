from newspaper import Article
from konlpy.tag import Kkma
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np
from openpyxl import load_workbook

# Step1. 텍스트 크롤링 > 문장 단위 분리 > 명사 추출
# stopwords : 불용어로써 문장 내에서 내용을 나타내는데 의미를 가지지 않는 단어들의 집합
class SentenceTokenizer(object):
    def __init__(self):
        self.kkma = Kkma()
        self.okt = Okt()

        # 한국어 불용어 엑셀 파일을 로드
        self.load_wb = load_workbook('C:/Users/battl/PycharmProjects/myProject02/excel/korean_stopwords.xlsx')
        self.load_ws = self.load_wb['Sheet1']
        self.get_cells = self.load_ws['A1':'A677']

        self.excel = []
        for cell in self.get_cells:
            for c in cell:
                self.excel.append(c.value)

        self.stopwords = self.excel

    def url2sentences(self, url):
        article = Article(url, language='ko')
        article.download()
        article.parse()
        sentences = self.kkma.sentences(article.text)

        for idx in range(0, len(sentences)):
            if len(sentences[idx]) <= 10:
                sentences[idx - 1] += (' ' + sentences[idx])
                sentences[idx] = ''

        return sentences

    def text2sentences(self, text):
        sentences = self.kkma.sentences(text)

        for idx in range(0, len(sentences)):
            if len(sentences[idx]) <= 10:
                sentences[idx - 1] += (' ' + sentences[idx])
                sentences[idx] = ''

        return sentences

    # sentences는 본문 내용을 문장 단위로 나눈 리스트
    def get_nouns(self, sentences):
        nouns = []
        for sentence in sentences:
            if sentence is not '':
                nouns.append(' '.join([
                    noun for noun in self.okt.nouns(str(sentence))
                    if noun not in self.stopwords and len(noun) > 1]
                ))

        return nouns

# Step2. TF-IDF(Term Frequency-Inverse Document Frequency) 모델 생성 및 그래프 생성
# TF(Term Frequency) : 단어 빈도, 특정 단어가 문서 내에 얼만큼의 빈도로 등장하는지의 척도
# IDF(Inverse Document Freqeuncy) : 역문헌 빈도수, 문서 빈도의 역수로써 전체 문서 개수를 해당 단어가 포함된 문서의 개수로 나눈 것
class GraphMatrix(object):
    def __init__(self):
        self.tfidf = TfidfVectorizer()
        self.cnt_vec = CountVectorizer()
        self.graph_sentence = []

    def build_sent_graph(self, sentence):
        tfidf_mat = self.tfidf.fit_transform(sentence).toarray()
        self.graph_sentence = np.dot(tfidf_mat, tfidf_mat.T)

        return self.graph_sentence

    def build_words_graph(self, sentence):
        cnt_vec_mat = normalize(self.cnt_vec.fit_transform(sentence).toarray().astype(float), axis=0)
        vocab = self.cnt_vec.vocabulary_

        return np.dot(cnt_vec_mat.T, cnt_vec_mat), {vocab[word] : word for word in vocab}

# Step3. TextRank 알고리즘 적용
class Rank(object):
    def get_ranks(self, graph, d=0.85): # d = damping factor, 웹 서핑 이용자가 해당 페이지를 만족하지 못하고 다른 페이지로 가는 링크를 클릭할 확률
        A = graph
        matrix_size = A.shape[0]

        for id in range(matrix_size):
            A[id, id] = 0
            link_sum = np.sum(A[:, id])

            if link_sum != 0:
                A[:, id] /= link_sum

            A[:, id] *= -d
            A[id, id] = 1

        B = (1-d) * np.ones((matrix_size, 1))
        ranks = np.linalg.solve(A, B) # 연립방정식 Ax = b

        return {idx: r[0] for idx, r in enumerate(ranks)}

# Step4. TextRank Class 구현
class TextRank(object):
    def __init__(self, text):
        self.sent_tokenize = SentenceTokenizer()

        if text[: 5] in ('http:', 'https'):
            self.sentences = self.sent_tokenize.url2sentences(text)
        else:
            self.sentences = self.sent_tokenize.text2sentences(text)

        self.nouns = self.sent_tokenize.get_nouns(self.sentences)

        self.graph_matrix = GraphMatrix()
        self.sent_graph = self.graph_matrix.build_sent_graph(self.nouns)
        self.words_graph, self.idx2word = self.graph_matrix.build_words_graph(self.nouns)

        # 문장의 랭킹 체크
        self.rank = Rank()
        self.sent_rank_idx = self.rank.get_ranks(self.sent_graph)
        self.sorted_sent_rank_idx = sorted(self.sent_rank_idx, key=lambda k: self.sent_rank_idx[k], reverse=True)

        # 단어의 랭킹 체크
        self.word_rank_idx = self.rank.get_ranks(self.words_graph)
        self.sorted_word_rank_idx = sorted(self.word_rank_idx, key=lambda k: self.word_rank_idx[k], reverse=True)

    # 본문 요약(기본 3줄)
    def summarize(self, sent_num=3):
        summary = []
        index = []
        for idx in self.sorted_sent_rank_idx[:sent_num]:
            index.append(idx)

        index.sort()
        for idx in index:
            summary.append(self.sentences[idx])

        return summary

    # 상위 10개 키워드
    def keywords(self, word_num=10):
        rank = Rank()
        rank_idx = rank.get_ranks(self.words_graph)
        sorted_rank_idx = sorted(rank_idx, key=lambda k: rank_idx[k], reverse=True)

        keywords = []
        index = []
        for idx in sorted_rank_idx[:word_num]:
            index.append(idx)

        for idx in index:
            keywords.append(self.idx2word[idx])

        return keywords
