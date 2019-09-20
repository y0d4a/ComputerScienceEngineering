import re

# 키워드 추출 함수(검색창인 경우에만)
def parseKeywordSearchPage(driver):

    crawl_keyword = driver.find_element_by_xpath('//*[@id="cdr_opt"]/div/div[2]/div[2]/div[3]/form/input[1]')
    keyword = crawl_keyword.get_attribute('value')

    return keyword

# 키워드 추출 함수(홈페이지인 경우에만)
def parseKeywordHomePage(driver):

    crawl_keyword = driver.find_element_by_xpath('/html/head/title')
    keyword = crawl_keyword.get_attribute('text')

    # 키워드 내에 특수문자 제거
    keyword = re.sub('[\/]', '', keyword)

    return keyword
