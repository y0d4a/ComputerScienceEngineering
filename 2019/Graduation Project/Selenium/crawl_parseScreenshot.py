import os
import time
import io
from PIL import Image # 모듈 설치 시 Pillow로 설치해야함

# 스크린 샷 추출 함수(바이너리 형태로 몽고 DB에 저장)
def parseScreenshot(driver, user_name, keyword):

    # 스크린 샷 화면 크기 조정
    total_width = driver.execute_script("return document.body.offsetWidth")
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    viewport_width = driver.execute_script("return document.body.clientWidth")
    viewport_height = driver.execute_script("return window.innerHeight")
    rectangles = []

    i = 0
    while i < total_height:
        ii = 0
        top_height = i + viewport_height

        if top_height > total_height:
            top_height = total_height

        while ii < total_width:
            top_width = ii + viewport_width

            if top_width > total_width:
                top_width = total_width

            rectangles.append((ii, i, top_width, top_height))

            ii = ii + viewport_width

        i = i + viewport_height

    # 스크린 샷 결과 이미지
    stitched_image = Image.new('RGB', (total_width, total_height))
    previous = None
    part = 0

    # 여러 번 캡처해서 하나로 통합시키기
    for rectangle in rectangles:
        if not previous is None:
            driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
            time.sleep(0.2)

        file_name = "part_{0}.png".format(part)
        driver.get_screenshot_as_file(file_name)
        screenshot = Image.open(file_name)

        if rectangle[1] + viewport_height > total_height:
            offset = (rectangle[0], total_height - viewport_height)
        else:
            offset = (rectangle[0], rectangle[1])

        stitched_image.paste(screenshot, offset)

        del screenshot
        os.remove(file_name)
        part = part + 1
        previous = rectangle

    # 통합된 스크린 샷 통합해서 저장하기
    stitched_image.save('C:/Users/battl/PycharmProjects/myProject02/screenshot/' + user_name + '_' + keyword + '.png')
    # 바이너리 형태로 파일 저장하기
    output = io.BytesIO()
    stitched_image.save(output, format='PNG')
    binary_data = output.getvalue()

    return binary_data
