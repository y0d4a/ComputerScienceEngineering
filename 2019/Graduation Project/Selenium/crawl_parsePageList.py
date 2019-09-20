from selenium.common.exceptions import NoSuchElementException

# 페이지 리스트 추출 함수(검색창인 경우에만)
def parsePageList(driver):

    pList = []

    try:
        pageList = driver.find_element_by_xpath("//div[@id='rso']")

        for p in pageList.find_elements_by_tag_name('cite'):
            p = p.text
            pList.append(p)

    except NoSuchElementException:
        print("페이지 리스트가 페이지 내에 없습니다")

    return pList
