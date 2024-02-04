import numpy as np
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
from datetime import datetime

# 한글 깨짐을 위한 코드 [Mac 환경]
import os
path = os.getcwd()
from matplotlib import rc
rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False


# 음주운전 단속 기록 파일 읽어옴
# 해당 파일에서 21~22_7월 데이터의 경우 구분자로 \t가 사용되어 따로 구분자를 입력했다.
drunk_drv_21 = pd.read_csv('Data/경찰청_음주운전_21년.csv', header=0, sep = '\t', engine='python', encoding='utf-16')
drunk_drv_22_1_6 = pd.read_csv('Data/경찰청_음주운전_22년1월_6월.csv', header=0, sep = '\t', engine='python', encoding='utf-16')
drunk_drv_22_7 = pd.read_csv('Data/경찰청_음주운전_22년7월.csv', header=0, sep = '\t', engine='python', encoding='utf-16')
drunk_drv_16 = pd.read_csv('Data/경찰청_음주운전적발기록_2016.csv',header=0, engine='python', encoding='cp949')

# 음주움전 단속 기록을 통합 [21~22_7]
drunk_drv_total = pd.concat([drunk_drv_21,drunk_drv_22_1_6, drunk_drv_22_7], ignore_index=True)
# '측정일시' 를 기준으로 다시 정렬
drunk_drv_total = drunk_drv_total.sort_values('측정일시',ignore_index=True)
# 확인
print(tabulate(drunk_drv_total.head(), headers='keys', tablefmt='plain', showindex=True))
print(drunk_drv_total.loc[drunk_drv_total['나이'] == '불명'])
print(drunk_drv_total.loc[drunk_drv_total['알콜농도'] == '측정거부'])
drunk_drv_total.loc[drunk_drv_total['나이'] == '불명', ['나이']] = np.nan
drunk_drv_total.loc[drunk_drv_total['알콜농도'] == '측정거부', ['알콜농도']] = np.nan
drunk_drv_total['나이'] = drunk_drv_total['나이'].astype(float).astype(pd.Int64Dtype())
drunk_drv_total=drunk_drv_total.astype({'알콜농도':'float'})
drunk_drv_total=drunk_drv_total.astype({'성별':'string'})

drunk_drv_total.dtypes
drunk_drv_total['성별'].value_counts()
drunk_drv_total['나이'].value_counts()
drunk_drv_total.loc[drunk_drv_total['나이'] >= 90]
drunk_drv_total.loc[drunk_drv_total['나이']<=10]
drunk_drv_total = drunk_drv_total.drop(drunk_drv_total.loc[drunk_drv_total['나이']<=10].index.dropna(), axis='rows')
drunk_drv_total = drunk_drv_total.drop(drunk_drv_total[drunk_drv_total['나이'] >= 90].index.dropna(), axis='rows')

# 나이 그룹별 알콜농도 분포
age_groups = pd.cut(drunk_drv_total['나이'], bins=range(10, 91, 10), right=False, labels=['10대','20대', '30대', '40대', '50대','60대','70대','80대'])

# 날짜 입력받아서 달과 요일, 시간대를 출력하는 함수
def extract_data_info(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    # 달 추출
    month = dt.month
    # 요일 추출
    weekday = dt.strftime("%A")
    # 시간대 추출
    hour = dt.hour
    time_range = f"{hour:02d}-{hour+1:02d}"
    return month, weekday, time_range
# 측정일시 데이터를 바탕으로 달, 요일, 시간대 열 추가.
month_list = []
weekday_list = []
time_range_list = []
for date_str in drunk_drv_total['측정일시']:
    month, weekday, time_range = extract_data_info(date_str)
    month_list.append(month)
    weekday_list.append(weekday)
    time_range_list.append(time_range)

drunk_drv_total['월'] = month_list
drunk_drv_total['요일'] = weekday_list
drunk_drv_total['시간대'] = time_range_list
drunk_drv_total['나이그룹'] = age_groups

drunk_drv_total.to_csv("음주운전_데이터_처리.csv", index=False)

drunk_drv_total = pd.read_csv('음주운전_데이터_처리.csv', header=0 ,encoding='utf-8')

