import time

# 페이지 리스트 추출 함수(검색창인 경우에만)
def parsePageList(driver):
    print('페이지 리스트 추출 중')
    for i in range(1, 40):
        print('▶', end="", flush=True)
        time.sleep(0.1)
    print('')

    pList = []
    pageList = driver.find_element_by_xpath("//div[@id='rso']")
    for p in pageList.find_elements_by_tag_name('cite'):
        p = p.text
        pList.append(p)

    return pList
