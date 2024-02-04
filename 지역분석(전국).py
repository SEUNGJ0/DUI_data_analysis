from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 깨짐을 위한 코드 [Mac 환경]
import os
path = os.getcwd()
from matplotlib import rc
rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

# 데이터 전처리
drunk_drv_total = pd.read_csv('음주운전_데이터_처리.csv', header=0 ,encoding='utf-8')
Total_count_list = []
drunk_drv_total['관할경찰서'].value_counts()
for i in drunk_drv_total['관할경찰서']:
    Total_count_list.append(i[0:2])
Total_count_dict = dict(Counter(Total_count_list))
# Dict -> DataFrame
Total_count_df = pd.DataFrame(list(Total_count_dict.items()), columns=['지역명', '적발건수'])
# 적발건수로 내림차순 정렬
Total_count_df = Total_count_df.sort_values(by=["적발건수"],ascending=False)\
# 상위 20개 추출
Total_count_df = Total_count_df.head(20).reset_index(drop=True)

population = [9428372, 2967314, 2363691, 1431050, 3317812, 1190964, 1110663, 578529, 1446072, 790128, 1074971, 849573, 910814, 641660, 657559, 512912, 678159, 737353, 651495, 495315]
Total_count_df['인구수'] = population
Total_count_df['적발건수/인구수'] = 0
for i in range(20):
    Total_count_df['적발건수/인구수'][i] = Total_count_df['적발건수'][i]/Total_count_df['인구수'][i]*100
print(Total_count_df)


# Bar plot
plt.figure(figsize=(20,8))
sns.barplot(data = Total_count_df, x = '지역명', y = '적발건수')
plt.title("<전국 음주운전 적발건수 상위 20 >",fontsize=30,fontweight='bold')
for index, value in enumerate(Total_count_df["적발건수"]):
    plt.text(index-0.2,value+8,value)

# Line plot
ax2 = plt.twinx()
sns.lineplot(data=Total_count_df, x='지역명', y='적발건수/인구수', color='red', marker='o', ax=ax2)
ax2.set_ylim(0, Total_count_df['적발건수/인구수'].max() + 1)
ax2.set_ylabel('적발건수/인구수(%)', color='red')

plt.show()