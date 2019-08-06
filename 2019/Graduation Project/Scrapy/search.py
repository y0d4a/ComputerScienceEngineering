import scrapy
import sys
import os
from ..items import SearchtutorialItem
from glob import glob
from collections import Counter
from konlpy.tag import Kkma

class SearchSpider(scrapy.Spider):
    name = 'search'
    start_url = ['https://www.google.com/search']
    allowed_domains = ['www.google.com']
    prevUrl = start_url
    currUrl = ''

    def main():
        input_dir = sys.arg[1]
        kkma = Kkma()

        # 단어의 빈도를 저장하기 위한 Counter 객체 생성
        frequency = Counter()
        count_proccessed = 0

        # glob()으로 와일드카드 매치 파일 목록을 추출하고 매치한 모든 파일을 처리
        for path in glob(os.path.join(input_dir, '*', 'wiki_*')):
            print('Processing {0}...'.format(path), file=sys.stderr)

            with open(path) as file:
                for content in iter_docs(file):
                    # 페이지에서 명사 리스트 추출
                    tokens = get_tokens(kkma, content)
                    frequency.update(tokens)
                    count_proccessed += 1
                    if count_proccessed % 10000 == 0:
                        print('{0} documents were processed.'.format(count_proccessed), file=sys.stderr)

        # 모든 기사의 처리가 끝나면 상위 30개의 단어 추출
        for token, count in frequency.most_common(30):
            print(token, count)

    # 문장 내부에 출현한 명사 리스트를 추출하는 함수
    def get_tokens(kkma, content):
        tokens = []
        node = kkma.pos(content)
        for (taeso, pumsa) in node:
            # 고유 명사와 일반 명사만 추출
            if pumsa in ('NNG', 'NNP'):
                tokens.append(taeso)
        return tokens

    # if 시작 버튼 누르면
    #     if 사용자가 키워드 입력후, 페이지 변환 시(Level 0)
    #         keywordParse()
    #         parsePageList()
    #         currUrl = parsePageUrl()

    # 키워드 추출 함수
    def parseKeyword(self, response):
        keyword = response.css('.gsfi::attr(value)').extract()
        yield keyword

    # 페이지 url 추출 함수
    def parsePageUrl(self, response):
        pageUrl = response.css('').extract()
        yield pageUrl

    # 페이지 리스트 추출 함수
    def parsePageList(self, response):
        pageList = response.css('.iUh30::text').extract()
        yield pageList

    # 본문 내용 추출 함수
    def parseContents(self, response):
        contents = response.css('').extract()
        print(contents)
