import pandas as pd
import matplotlib.pyplot as plt

# 한글 깨짐을 위한 코드 [Mac 환경]
import os
path = os.getcwd()
from matplotlib import rc
rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

# 데이터 불러오기
data = pd.read_csv('음주운전_데이터_처리.csv')

# 적발횟수가 2 이상인 데이터 필터링
filtered_data = data[data['적발횟수'] >= 2]
# 적발횟수가 1 인 데이터 필터링
basic_data = data[data['적발횟수'] == 1]

# 특징 정리
characteristics = {
    '평균_나이': filtered_data['나이'].mean(),
    '최소_알콜농도': filtered_data['알콜농도'].min(),
    '평균_알콜농도': round(filtered_data['알콜농도'].mean(),3),
    '최대_알콜농도': filtered_data['알콜농도'].max()
}

basics = {
    '평균_나이': basic_data['나이'].mean(),
    '최소_알콜농도': basic_data['알콜농도'].min(),
    '평균_알콜농도': round(basic_data['알콜농도'].mean(),3),
    '최대_알콜농도': basic_data['알콜농도'].max()
}
# 특징 출력
print(characteristics)
print(basics)

