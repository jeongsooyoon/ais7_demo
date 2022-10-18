from re import X
import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 페이지 타이틀 및 로고 변경하기
st.set_page_config(
    page_title="Likelion AI School 자동차 연비 App",
    page_icon="🚗",
    layout="wide",
)

# 페이지 제목과 검색바 제목
st.markdown("# 자동차연비🚗")
st.sidebar.markdown("# 자동차 연비 🚗")

#내장데이터가 아니라 외부에서 가져오는 방법
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mpg.csv"
# data = pd.read_csv(url)

# 캐시를 사용하는 방법
# 이미 데이터를 한번 로드했다면 새로 로드하지 않고 기존 로드한 데이터를 사용하면 부담을 줄일 수 있습니다. 속도도 빠릅니다.


# 캐시로 가져오는 방법
@st.cache
def load_data(url):
    data = pd.read_csv(url)
    return data

# data 호출
data_load_state = st.text('Loading data...')
data = load_data(url)
data_load_state.text("Done! (using st.cache)")

# st.markdown("# MPG 🚗")
# st.sidebar.markdown("# MPG 🚗")

st.write("""### MPG 데이터의 자동차 연비""")

# mpg = sns.load_dataset("mpg")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year',
   list(reversed(range(data.model_year.min(),data.model_year.max())))
   )

# Sidebar - origin
sorted_unique_origin = sorted(data.origin.unique())
selected_origin = st.sidebar.multiselect('origin', sorted_unique_origin, sorted_unique_origin)


if selected_year > 0 :
   data = data[data.model_year == selected_year]

if len(selected_origin) > 0:
   data = data[data.origin.isin(selected_origin)]

st.dataframe(data)

st.line_chart(data["mpg"])

st.bar_chart(data["mpg"])

st.area_chart(data["mpg"])

fig, ax = plt.subplots(figsize=(10, 2))
sns.barplot(data = data, x = "cylinders", y = "mpg", hue = "origin", ci = None).set_title("실린더 개수, 지역별 mpg")
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 3))
sns.countplot(data=data, x="origin").set_title("지역별 자동차 연비 데이터 수")
st.pyplot(fig)

pxh = px.histogram(data, x = "origin", title = "지역별 자동차 연비 데이터 수")
pxh
