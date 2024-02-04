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
    '강남': '강남구',
    '관악': '관악구',
    '서부': '양천구',
    '금천': '금천구',
    '양천': '양천구',
    '성동': '성동구',
    '수서': '강남구',
    '방배': '서초구',
    '노원': '노원구',
    '구로': '구로구',
    '강동': '강동구',
    '동대문': '동대문구',
    '마포': '마포구',
    '용산': '용산구',
    '강북': '강북구',
    '중부': '중구',
    '광진': '광진구',
    '도봉': '도봉구',
    '영등포': '영등포구',
    '동작': '동작구',
    '강서': '강서구',
    '종로': '종로구',
    '중랑': '중랑구',
    '은평': '은평구',
    '서대문': '서대문구',
    '종암': '성북구',
    '성북': '성북구',
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