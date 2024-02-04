import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 깨짐을 위한 코드 
import os
path = os.getcwd()
from matplotlib import rc
rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

# CSV 파일 읽기
df = pd.read_csv("음주운전_데이터_처리.csv")

# 요일 순서 정의 (월~일 순서)
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# 시간대와 요일별 빈도수 계산
heatmap_data = df.groupby(['시간대', '요일']).size().unstack()

# 요일 순서 변경
heatmap_data = heatmap_data[weekday_order]

# 히트맵 그리기 ㅠ
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, cmap='RdYlGn_r', annot=True, fmt='d', linewidths=.5)

# 그래프 제목과 축 제목 설정
plt.title('시간대-요일별 음주 빈도 분석')
plt.xlabel('요일')
plt.ylabel('시간대')

# 그래프 출력
plt.show()
