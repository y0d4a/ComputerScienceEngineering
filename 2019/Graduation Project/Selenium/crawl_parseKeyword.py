import time

# 키워드 추출 함수(검색창인 경우에만)
def parseKeyword(driver):
    print('키워드 추출 중')
    for i in range(1, 40):
        print('▶', end="", flush=True)
        time.sleep(0.1)
    print('')

    crawl_keyword = driver.find_element_by_xpath('/html/head/title')
    keyword = crawl_keyword.get_attribute('text')
    split_keyword = keyword.split('-')

    return split_keyword[0]
