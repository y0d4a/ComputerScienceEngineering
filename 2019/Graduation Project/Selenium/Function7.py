"""
    기능 7 : 크롤링된 데이터를 기반으로 데이터 시각화

    1) pie 차트로 방문 비율을 시각화
    2) 키워드 중심으로 키워드 분포도, 워드 클라우드 등 데이터 시각화 모델 생성
"""

import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from matplotlib import style
from matplotlib import colors as mcolors
from pymongo import MongoClient
import pandas as pd

# 몽고 DB 연결
conn = MongoClient('mongodb+srv://dots_user:TzE66c5O0KB0bnjG@dots-test-x41en.mongodb.net/test?retryWrites=true&w=majority')
db = conn['JMH']
collection = db['second_integrated_user_table']

# 폰트 설정
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)
style.use('ggplot')

# 데이터 시각화
colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
plt.rcParams["figure.figsize"] = (10,4)     # 그림 크기
plt.rcParams['lines.linewidth'] = 2         # 선의 두께
plt.rcParams['axes.grid'] = True            # 차트 내 격자선 표시 여부
plt.pie(table['freq'], labels=table['curr_url'], colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
plt.show()