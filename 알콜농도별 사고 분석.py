import pandas as pd
import matplotlib.pyplot as plt

# 한글 깨짐을 위한 코드 [Mac 환경]
import os
path = os.getcwd()
from matplotlib import rc
rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

# 데이터 로드
data = pd.read_csv('Data/알콜농도별 사고 분석.csv')

# 필요한 열 선택
columns = ['알콜농도', '사고 백분율(%)', '사망 백분율(%)', '부상 백분율(%)']
data = data[columns]

# 데이터 전처리
data[['사고 백분율(%)', '사망 백분율(%)', '부상 백분율(%)']] = data[['사고 백분율(%)', '사망 백분율(%)', '부상 백분율(%)']].astype(float)

# "소계"와 "측정불응" 제외
data = data[~data['알콜농도'].isin(['소계', '측정불응'])]

# 알콜농도로 정렬
data = data.sort_values('알콜농도')

# 그래프 그리기
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(data['알콜농도'], data['사고 백분율(%)'], label='사고 백분율', marker='o')
ax.plot(data['알콜농도'], data['사망 백분율(%)'], label='사망 백분율', marker='o')
ax.plot(data['알콜농도'], data['부상 백분율(%)'], label='부상 백분율', marker='o')

ax.set_xlabel('알콜농도')
ax.set_ylabel('백분율')
ax.set_title('알콜농도별 사고, 사망, 부상 백분율')
ax.legend()

plt.xticks(rotation=45)  # X축 라벨 회전

plt.tight_layout()
plt.show()
