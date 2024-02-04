# 주제
: 음주운전 통계 분석을 통한 음주운전의 전반적인 동향과 그 문제의 원인에 대한 고찰

# 분석 데이터 셋

- **경찰청_음주운전 적발 기록 현황**
    - **[성별, 적발횟수, 나이, 알콜농도, 측정일시, 관할경찰서]로 구성**
    - 21년~22년 7월까지의 적발 기록 데이터
    - **출처** : 공공데이터 포털

- **경찰청_연령별 음주운전 적발 기록 현황**
    - **2010년부터 20년도까지의 연령대별 적발 기록**
    - **출처** : 공공데이터 포털

- **2021년의 교통사고_제1절 교통사고 현황의 알콜 농도별 사고 분석 데이터**
    - **알콜농도별 사고, 사망, 부상 건수 등으로 구성**
    - **출처** : 경찰청 홈페이지

# 데이터 전처리 과정

1. **음주운전 단속 기록 파일 읽어오기**

   : 주어진 CSV 파일들을 읽어와 데이터프레임으로 저장
2. **음주운전 단속 기록 통합**

   : 21년부터 22년 7월까지의 데이터를 하나로 통합
3. **데이터 정렬**

   : '측정일시' 열을 기준으로 데이터를 다시 정렬
4. **결측치 처리**

   : '나이'와 '알콜농도' 열의 결측치를 NaN으로 처리
5. **데이터 형식 변환**
   
    : '나이' 열을 정수형으로, '알콜농도' 열을 실수형으로 변환
6. **데이터프레임 정보 확인**

    : 데이터프레임의 열별 데이터 형식을 확인
7. **성별, 나이 그룹별 분포 확인**

    : '성별'과 '나이' 열을 기준으로 분포를 확인
8. **이상치 제거**

    : 나이가 10보다 작거나 90보다 큰 데이터를 제거
9. **나이 그룹별 알콜농도 분포**

    : 나이를 그룹으로 나누어 알콜농도의 분포를 확인
10. **날짜 정보 추출 함수**

    : 측정일시에서 달, 요일, 시간대를 추출하는 함수를 정의
11. **측정일시 데이터를 바탕으로 달, 요일, 시간대 열 추가**

    : 데이터프레임에 달, 요일, 시간대 열을 추가
12. **데이터 저장**

    : 처리된 데이터를 CSV 파일로 저장

# 진행한 데이터 분석

- **나이대별 알콜농도 평균 분석**
- **알콜농도 범위별 적발빈도 분포 분석**
- **알콜농도별 사고율 분석**
- **연도-나이대별 음주운전 적발건수 분석**
- **적발횟수 상관관계 분석**
- **시간대-요일별 사고 분석**
- **지역분석**
    - **전국**
    - **서울**
    - **서울 [요일]**

## 나이대별 알콜농도 평균 분석

- **코드**
    
    ```python
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
    ```
    
- **결과**
  
  ![나이대별 알콜농도의 평균](https://github.com/SEUNGJ0/DUI_data_analysis/assets/101918371/31a44ff0-109b-4c57-b3ac-03afa37f6669)

- **결과 분석**
    - 해당 분석에서 30대에서 가장 높은 알콜농도 평균값을 보여주었으며, 40대와 50대는 유사한 수준을 나타냈습니다.
    - 전체 연령대에서 평균값이 0.1을 넘어서고 있으며, 이러한 수치는 면허 취소와 1년 이상 2년 이하의 징역 또는 500만원 이상 1천만원 이하의 벌금에 해당합니다.

## 알콜농도 범위별 적발빈도 분포 분석

- **코드**
    
    ```python
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
    ```
    

- **결과**
  
    ![알콜농도 범위별 빈도 분포](https://github.com/SEUNGJ0/DUI_data_analysis/assets/101918371/b31d3700-4e0f-4731-8bd3-77c0970160a0)

- **결과 분석**
    - 적발빈도 분석에서는 0.09%에서 0.12% 범위가 전체의 약 21.5%로 가장 높은 빈도를 보였으며, 그 뒤를 0.06%에서 0.09% 범위와 0.12%에서 0.15% 범위가 각각 20%, 20.2%의 비중을 차지했습니다.

## 알콜농도별 사고율 분석

- **코드**
    
    ```python
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
    ```
    
- **결과**

    ![알콜농도별 사고,사망, 부상 백분율](https://github.com/SEUNGJ0/DUI_data_analysis/assets/101918371/1cbcb672-886c-4043-89b5-a5387f2ef569)

    
- **결과 분석**
    - 사고율 분석에서는 부상과 사고의 비율이 거의 동일한 양상을 보이고 있으며, 사망자 비율 또한 유사한 양상을 나타냈습니다.
    - 전체의 약 80%가 0.05%에서 0.199% 범위에 집중되어 있는데, 이는 앞서 분석 결과와 같이 단속이 가장 빈번한 알콜농도 범위에 실제로 사고가 가장 빈번하게 발생하고, 이로 인해 부상과 사망자도 가장 많이 발생한다는 것을 의미합니다.

## 연도-나이대별 음주운전 적발건수 분석

- **코드**
    
    ```python
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
    ```
    
- **결과**
    
    ![연도별 나이대별 음주운전 적발수](https://github.com/SEUNGJ0/DUI_data_analysis/assets/101918371/e6b65b4e-7687-4890-8694-106462c72647)

- **결과 분석**
    - 해당 분석 결과를 보면 2010년 이후 적발건수가 점차 감소하는 경향을 보입니다.
    - 또한 30대와 40대의 적발건수가 다른 연령대에 비해 상대적으로 높은 것을 확인할 수 있습니다.

## 적발횟수 상관관계 분석

- **코드**
    
    ```python
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
    print("적발횟수 2회 이상 : ",characteristics)
    print("적발횟수 1회 : ",basics)
    ```
    
- **결과**
    
    ```python
    적발횟수 2회 이상 :  {'평균_나이': 42.40986646884273, '최소_알콜농도': 0.03, '평균_알콜농도': 0.131, '최대_알콜농도': 0.88}
    적발횟수 1회 :  {'평균_나이': 42.27666497702634, '최소_알콜농도': 0.03, '평균_알콜농도': 0.118, '최대_알콜농도': 1.83}
    ```
    
- **결과 분석**
    - 적발횟수 상관관계 분석에서는 다회 적발자의 평균 알콜농도가 1회 적발자보다 조금 더 높은 것으로 나타났으나, 두 그룹 사이에는 특별한 상관관계가 나타나지 않았습니다.
    

## 시간대-요일별 사고 분석

- **코드**
        
    ```python
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
    ```
    
- **결과**
    
    ![시간대-요일별 음주 빈도 분석](https://github.com/SEUNGJ0/DUI_data_analysis/assets/101918371/dd84a759-e430-4b38-b111-e095a790082f)
    
- **결과 분석**
    - 시간대-요일별 사고 분석에서는 모든 요일에서 야간 시간인 21시부터 24시까지 음주운전 적발률이 가장 높았으며, 특히 금요일 21시부터 토요일 2시까지의 적발률이 가장 높았습니다.
    - 그러나 일요일 야간의 적발률은 다른 평일에 비해 낮은 수준을 보였습니다.

## 지역분석

지역분석은 전국과 서울, 두 가지 유형으로 진행되었습니다. 

해당 분석은 `경찰청_음주운전 적발 기록현황`의 **관할 경찰서 위치**를 기반으로 분석되었습니다

### **전국**

- **코드**
    
    ```python
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
    ```
    
- **결과**
    
    ![전국 음주운전 적발건수 분석](https://github.com/SEUNGJ0/DUI_data_analysis/assets/101918371/d158153d-0ca1-4929-9a0c-fde54fcc5f26)

    
    전국 상위 20곳의 **적발건수[**막대 그래프**]**와 **인구 대비 적발건수[**라인 그래프**] 값**
    
- **결과 분석**
    - 적발건수 기준으로는 서울이 가장 높은 수치를 보여주었으며, 그 뒤를 이어 인천, 대구, 광주, 부산 등 광역시들이 순서대로 나타났습니다.
    - 그러나 단순 적발건수만을 고려할 때 서울이 압도적으로 높은 수치를 보여주지만, 인구 대비 적발건수를 비교해보면 의외로 낮은 수치임을 확인할 수 있습니다.
    - 인구 대비 적발율에서는 평택이 가장 높은 수치를 보여주었으며, 그 뒤를 이어 시흥과 광주광역시가 순서대로 나타났습니다.

### **서울**

- **코드**
    
    ```python
    from collections import Counter
    import pandas as pd
    import folium
    from branca.colormap import linear
    
    drunk_drv_total = pd.read_csv('음주운전_데이터_처리.csv', header=0 ,encoding='utf-8')
    seoul_count_list = []
    drunk_drv_total['관할경찰서'].value_counts()
    for i in drunk_drv_total['관할경찰서']:
        if i[0:2] == '서울':
            seoul_count_list.append(i[2:-3])
    
    seoul_count_dict = dict(Counter(seoul_count_list))
    location_district_mapping = {
        '송파': '송파구',
        '서초': '서초구',
        ...
        '남대문': '중구',
        '혜화': '종로구'
    }
    seen_values = set()
    duplicate_values = []
    
    for keys, value in location_district_mapping.items():
        if value in seen_values:
            duplicate_values.append(value)
        seen_values.add(value)
    
    for value in duplicate_values:
        duplicate_keys = [k for k, v in location_district_mapping.items() if v == value]
        seoul_count_dict[duplicate_keys[0]] = seoul_count_dict[duplicate_keys[0]]+seoul_count_dict[duplicate_keys[1]]
        del seoul_count_dict[duplicate_keys[1]]
    
    seoul_count_dict = {location_district_mapping[key]: value for key, value in seoul_count_dict.items()}
    
    # 지도 생성
    m = folium.Map(location=[37.541, 126.986], zoom_start=12, tiles="Stamen Toner")
    
    # 색상 설정
    colormap = linear.YlGnBu_09.scale(min(seoul_count_dict.values()), max(seoul_count_dict.values()))
    colormap.caption = '서울 음주운전 적발 건수'
    
    # 경계 데이터 GeoJSON 파일 경로
    geojson_path = 'Data/서울_자치구_경계_2017.geojson'  # Replace with the actual path to your GeoJSON file
    
    # 자치구 중심점 데이터
    Seoul_Gu_Center = pd.read_csv('Data/서울시_자치구_중심점_2017.csv', encoding='cp949')
    
    # Choropleth 지도 시각화
    seoul_choropleth = folium.Choropleth(
        geo_data=geojson_path,
        name='choropleth',
        data=seoul_count_dict,
        columns=['Location', 'Count'],
        key_on='feature.properties.SIG_KOR_NM',
        fill_color='YlGnBu',
        fill_opacity=1,
        line_opacity=1,
        legend_name='서울 음주운전 적발 건수',
        bins=20
    ).add_to(m)
    
    # 텍스트 표시
    style_function = "font-size: 20px; font-weight: bold"
    for feature in seoul_choropleth.geojson.data['features']:
        properties = feature['properties']
        sig_kor_nm = properties['SIG_KOR_NM']
        count = seoul_count_dict[sig_kor_nm]
        Gu_Location = Seoul_Gu_Center[Seoul_Gu_Center['시군구명'] == sig_kor_nm]
        folium.Marker(
            location=[Gu_Location.values[0][4]+0.001, Gu_Location.values[0][3]-0.02],
            icon=folium.DivIcon(
                icon_size=(100, 20),
                icon_anchor=(0, 0),
                html=f'<div style="{style_function}">{sig_kor_nm}: {count}</div>'
            )
        ).add_to(m)
    
    # Save to html
    m.save('Map_HTML/Total_seoul.html')
    ```
    
    ```python
    from collections import Counter
    import pandas as pd
    import folium
    from branca.colormap import linear
    drunk_drv_total = pd.read_csv('음주운전_데이터_처리.csv', header=0 ,encoding='utf-8')
    seoul_count_dict = {}
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for weekday in weekday_order:
        T_list = [i[2:-3] for i in drunk_drv_total.loc[drunk_drv_total['요일'] == weekday, '관할경찰서'] if i.startswith('서울')]
        seoul_count_dict[weekday] = dict(Counter(T_list))
    
    location_district_mapping = {
        location_district_mapping = {
        '송파': '송파구',
        '서초': '서초구',
        ...
        '남대문': '중구',
        '혜화': '종로구'
    }
    seen_values = set()
    duplicate_values = []
    
    for keys, value in location_district_mapping.items():
        if value in seen_values:
            duplicate_values.append(value)
        seen_values.add(value)
    
    for weekday in weekday_order:
        for value in duplicate_values:
            duplicate_keys = [k for k, v in location_district_mapping.items() if v == value]
            seoul_count_dict[weekday][duplicate_keys[0]] = seoul_count_dict[weekday][duplicate_keys[0]]+seoul_count_dict[weekday][duplicate_keys[1]]
            del seoul_count_dict[weekday][duplicate_keys[1]]
    
        seoul_count_dict[weekday] = {location_district_mapping[key]: value for key, value in seoul_count_dict[weekday].items()}
    
    # 경계 데이터 GeoJSON 파일 경로
    geojson_path = 'Data/서울_자치구_경계_2017.geojson'  # Replace with the actual path to your GeoJSON file
    
    # 자치구 중심점 데이터
    Seoul_Gu_Center = pd.read_csv('Data/서울시_자치구_중심점_2017.csv', encoding='cp949')
    
    for weekday in weekday_order:
        # 지도 생성
        m = folium.Map(location=[37.541, 126.986], zoom_start=12, tiles="Stamen Toner")
    
        # 색상 설정
        colormap = linear.YlGnBu_09.scale(min(seoul_count_dict[weekday].values()), max(seoul_count_dict[weekday].values()))
        colormap.caption = '서울 음주운전 적발 건수'
    
        # Choropleth 지도 시각화
        seoul_choropleth = folium.Choropleth(
            geo_data=geojson_path,
            name='choropleth',
            data=seoul_count_dict[weekday],
            columns=['Location', 'Count'],
            key_on='feature.properties.SIG_KOR_NM',
            fill_color='YlGnBu',
            fill_opacity=1,
            line_opacity=1,
            legend_name=f'[{weekday}]서울 음주운전 적발 건수',
            threshold_scale = list(range(0,500, 10))
        ).add_to(m)
    
        # 텍스트 표시
        style_function = "font-size: 20px; font-weight: bold"
        for feature in seoul_choropleth.geojson.data['features']:
            properties = feature['properties']
            sig_kor_nm = properties['SIG_KOR_NM']
            count = seoul_count_dict[weekday][sig_kor_nm]
            Gu_Location = Seoul_Gu_Center[Seoul_Gu_Center['시군구명'] == sig_kor_nm]
            folium.Marker(
                location=[Gu_Location.values[0][4]+0.001, Gu_Location.values[0][3]-0.02],
                icon=folium.DivIcon(
                    icon_size=(100, 20),
                    icon_anchor=(0, 0),
                    html=f'<div style="{style_function}">{sig_kor_nm}: {count}</div>'
                )
            ).add_to(m)
        # Save to html
        m.save(f'Map_HTML/{weekday}_seoul.html')
    ```
    
- **결과**
    
    ![서울 통합 분석](https://github.com/SEUNGJ0/DUI_data_analysis/assets/101918371/d57b6da4-41c9-4d23-af35-ab77c2851645)

    
    서울 통합 분석
    
    ![서울 요일별 분석](https://github.com/SEUNGJ0/DUI_data_analysis/assets/101918371/f1667541-3419-4ae8-8d68-f2882a312b52)

    
    서울 요일별 분석
    
- **결과 분석**
    - 서울의 경우, 강남구가 압도적으로 높은 음주운전 적발 수치를 보였으며, 그 인근인 서초구와 송파구도 높은 수치를 보여준다. 또한, 전반적으로 강북 지역보다는 강남 지역에서 음주운전 적발이 더 많이 이루어지고 있으며, 서울의 모든 구에서 월요일부터 토요일까지 음주운전이 점점 증가하는 경향을 확인할 수 있다.

# 결론

1. 음주운전 적발자의 평균 혈중알콜농도는 3~50대가 제일 높았고, 전체적으로 0.1% 이상이였다.
2. 음주운전 적발자의 혈중알콜농도는 0.05%에서 0.15%라는 비교적 높지 않은 범위에  60%가 치중되어있다.
3. 음주운전 적발자의 사고율은 0.05%에서 0.199%사이에 약 80%가 집중되어있다.
4. 음주운전 적발건수는 시간이 지날수록 감소하고 있으며 전반적으로 3~40대의 적발건수가 높다.
5. 음주운전 적발건수는 요일과 상관없이 야간 시간대에 집중되어있으며 특히 금요일 저녁과 토요일 새벽시간대에 제일 높은 수치를 보인다. 일요일 야간의 경우 평일보다도 낮은 수치가 나온다. 
6. 전국에서 서울의 적발률이 제일 높았으나 인구대비로 보면 상당히 낮은 수치를 보인다.
7. 강남구와 그 인근 구역들은 음주운전 적발 수치가 높고, 서울의 모든 구에서 월요일부터 토요일까지 음주운전이 점차 증가하는 경향이 있다.

해당 주제로 음주운전 적발 기록 데이터를 분석한 결과, 30대부터 50대까지의 연령대가 가장 높은 평균 알콜농도를 보이며, 이 연령대에서 많은 적발건이 발생했다. 또한, 전 연령대에서 평균 혈중 알콜농도가 0.1% 이상이었으며, 이는 사고율이 가장 높은 알콜농도 범위에 해당한다.

이렇게 비교적 낮은 알콜농도에서도 많은 음주적발이 있고 사고율이 높은 것으로 나타나는 현상은 흔히하는 "한 잔정도는 괜찮겠지"같은 안일한 생각에서 비롯한 안전 불감증으로 인한 결과로 해석된다.

또한, 30대부터 40대까지의 연령대와 금요일, 야간 시간대에 음주운전 적발이 빈번하게 발생하는 것은 해당 연령대가 경제 및 사회적 활동이 가장 활발한 시기이며, 직장 내 술 강요 문화가 원인 중 하나일 수 있다는 것을 시사한다.

그리고 금요일뿐 아니라 매일, 특히 21시부터 02시까지 음주단속을 강화하고, 이러한 음주운전 단속은 강남구와 송파구, 서초구뿐 아니라 주요 구들에도 집중적으로 실시되어야 한다. 이를 통해 더 많은 음주운전 차량을 적발할 수 있고, 그 결과로 사고를 미연에 예방할 가능성을 높일 수 있다고 생각한다.
