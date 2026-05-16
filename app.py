import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 1. ตั้งค่าหน้าเว็บ (Page Configuration)
# ==========================================
st.set_page_config(
    page_title="Netflix Analytics Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. โหลดข้อมูล (Data Loading)
# ==========================================
df_trend = pd.read_csv('data/output/netflix_yearly_trend.csv')
df_country = pd.read_csv('data/output/netflix_top_10_countries.csv')
# ==========================================
# 3. สร้าง UI ของ Dashboard
# ==========================================
# ส่วนหัว (Header)
st.title("🎬 Netflix Data Pipeline Dashboard")
st.markdown("รายงานสรุปข้อมูลภาพยนตร์และซีรีส์ที่ผ่านการประมวลผลจาก **Apache Airflow**")
st.divider()

# ส่วนของ KPI (ตัวเลขสรุปผล)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="🎥 Total Movies", value="6,131", delta="Updated")
with col2:
    st.metric(label="📺 Total TV Shows", value="2,676", delta="Updated")
with col3:
    st.metric(label="🌍 Countries Covered", value="86")

st.divider()

# ส่วนของกราฟ (Charts)
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📈 แนวโน้มการผลิตคอนเทนต์รายปี")
    # สร้างกราฟเส้นด้วย Plotly
    fig_trend = px.line(
        df_trend, 
        x='release_year', 
        y='content_count', 
        markers=True,
        labels={'release_year': 'ปีที่ฉาย', 'content_count': 'จำนวน (เรื่อง)'}
    )
    # เปลี่ยนสีเส้นเป็นสีแดง Netflix
    fig_trend.update_traces(line_color='#E50914', marker=dict(size=8))
    st.plotly_chart(fig_trend, use_container_width=True)

with col_chart2:
    st.subheader("🏆 10 อันดับประเทศที่ผลิตคอนเทนต์สูงสุด")
    # สร้างกราฟแท่งแนวนอนด้วย Plotly
    fig_country = px.bar(
        df_country, 
        x='content_count', 
        y='primary_country', 
        orientation='h',
        labels={'primary_country': 'ประเทศ', 'content_count': 'จำนวน (เรื่อง)'}
    )
    # จัดเรียงข้อมูลให้แท่งยาวสุดอยู่ด้านบน และเปลี่ยนเป็นสีแดง
    fig_country.update_layout(yaxis={'categoryorder':'total ascending'})
    fig_country.update_traces(marker_color='#E50914')
    st.plotly_chart(fig_country, use_container_width=True)