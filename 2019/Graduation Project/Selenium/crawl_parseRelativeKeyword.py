import time

# 연관 키워드, url 추출 함수(검색창인 경우에만)
def parseRelativeKeyword(driver):
    print('연관 키워드 및 URL 추출 중')
    for i in range(1, 40):
        print('▶', end="", flush=True)
        time.sleep(0.1)
    print('')

    relativeKeyword = {}
    relativeKeywordList = driver.find_element_by_xpath("//div[@id='brs']")
    for r in relativeKeywordList.find_elements_by_tag_name('a'):
        text = r.get_attribute('text')
        href = r.get_attribute('href')

        relativeKeyword[text] = href

    return relativeKeyword
