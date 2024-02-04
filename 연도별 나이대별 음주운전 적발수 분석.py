import pandas as pd
import matplotlib.pyplot as plt

# 한글 깨짐을 위한 코드 [Mac 환경]
import os
path = os.getcwd()
from matplotlib import rc
rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

# 데이터 불러오기
data = pd.read_csv('Data/경찰청_연령별 음주운전 적발기록 현황_20210326.csv', index_col=0)

# 그래프 그리기
plt.figure(figsize=(10, 6))
age_groups = data.columns
colors = ['red', 'blue', 'green', 'orange', 'purple']

for i, age_group in enumerate(age_groups):
    plt.plot(data.index, data[age_group], marker='o', color=colors[i], label=age_group)

plt.xlabel('연도')
plt.ylabel('적발수')
plt.title('연도별 나이대별 음주운전 적발수')
plt.legend()
plt.grid(True)
plt.show()
