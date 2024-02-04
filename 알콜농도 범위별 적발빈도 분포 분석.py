import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 깨짐을 위한 코드 [Mac 환경]
import os
path = os.getcwd()
from matplotlib import rc
rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False


# 데이터 불러오기
data = pd.read_csv('음주운전_데이터_처리.csv')

# 알콜농도를 특정 범위로 분리
bins = [0.03, 0.06, 0.09, 0.12, 0.15, 0.18, 0.21]  # 범위 설정
labels = ['0.03-0.06', '0.06-0.09', '0.09-0.12', '0.12-0.15', '0.15-0.18', '0.18-0.21']  # 범위 라벨
data['알콜농도범위'] = pd.cut(data['알콜농도'], bins=bins, labels=labels, right=False)

# 각 범위별 빈도 계산
frequency = data['알콜농도범위'].value_counts(normalize=True) * 100

# 빈도별로 정렬
frequency = frequency.sort_index()

# 그래프 그리기
plt.figure(figsize=(10, 6))
sns.barplot(x=frequency.index, y=frequency.values,width=0.6)

plt.xlabel('알콜농도 범위')
plt.ylabel('빈도 (%)')
plt.title('알콜농도 범위별 빈도 분포')
plt.xticks(rotation=45)  # X축 라벨 회전

# 바 그래프 안에 값을 표시
for i, v in enumerate(frequency.values):
    plt.text(i, v, f'{v:.1f}%', ha='center', va='bottom')

plt.tight_layout()  # 그래프 간격 조정
plt.show()
