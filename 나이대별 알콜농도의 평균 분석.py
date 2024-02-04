import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# 한글 깨짐을 위한 코드 [Mac 환경]
import os
path = os.getcwd()
from matplotlib import rc
rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False


# 데이터 불러오기
data = pd.read_csv('음주운전_데이터_처리.csv')

# 데이터 정제
data = data.dropna(subset=['나이', '알콜농도'])
data['나이'] = data['나이'].astype(int)

# 나이대별 알콜농도의 평균 계산
age_alcohol_mean = data.groupby('나이그룹')['알콜농도'].mean().reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(data=age_alcohol_mean, x='나이그룹', y='알콜농도',width=0.6)
# 바 그래프 안에 평균값 표시
for i, v in enumerate(age_alcohol_mean['알콜농도']):
    plt.text(i, v, f'{v:.3f}', ha='center', va='bottom')
plt.ylabel('알콜농도')
plt.title('나이대별 알콜농도의 평균 Bar Plot')
plt.show()