import streamlit as st
import pandas as pd
import os

# 1. ⚙️ ตั้งค่าหน้าเพจแบบ Minimal
st.set_page_config(
    page_title="Executive Snapshot",
    page_icon="📈",
    layout="centered" # ใช้ layout แบบ centered เพื่อให้ดูง่ายบนมือถือ
)

# ฟังก์ชันสำหรับโหลดข้อมูลสรุป
def load_summary():
    file_path = 'executive_dashboard.csv'
    
    # กรณีที่ยังไม่มีไฟล์ (จำลองข้อมูลให้ดูเพื่อการทดสอบ)
    if not os.path.exists(file_path):
        data = {
            'report_date': ['2024-05-20 09:00'],
            'data_period': ['2023-01-01 to 2023-12-31'],
            'total_revenue': [1524050.50],
            'total_orders': [18500],
            'total_customers': [4300],
            'total_products': [3800],
            'total_countries': [38],
            'avg_order_value': [82.38],
            'avg_items_per_order': [12.5],
            'top_product': ['WHITE HANGING HEART T-LIGHT HOLDER'],
            'top_country': ['United Kingdom'],
            'best_month': ['2023-11']
        }
        return pd.DataFrame(data)
    
    return pd.read_csv(file_path)

# โหลดข้อมูล
df = load_summary()
row = df.iloc[0] # ดึงแถวแรกออกมาเป็น Series เพื่อเรียกใช้ง่ายๆ

# 2. 🚀 ส่วนแสดงผลหน้าจอ
st.title("📊 Executive Daily Snapshot")
st.caption(f"ข้อมูล ณ วันที่: {row['report_date']} | ช่วงเวลา: {row['data_period']}")

st.markdown("---")

# แถวที่ 1: ตัวเลขหัวใจหลัก (Big 3 Metrics)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="💰 ยอดขายรวม", value=f"${row['total_revenue']:,.0f}")
with col2:
    st.metric(label="📦 จำนวนออเดอร์", value=f"{row['total_orders']:,}")
with col3:
    st.metric(label="👥 ลูกค้าทั้งหมด", value=f"{row['total_customers']:,}")

st.markdown("---")

# แถวที่ 2: ประสิทธิภาพการขาย (Efficiency)
st.subheader("💡 ประสิทธิภาพการขาย")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric(label="💵 ยอดเฉลี่ยต่อบิล", value=f"${row['avg_order_value']:,.2f}")
with c2:
    st.metric(label="🛍️ สินค้าเฉลี่ย/บิล", value=f"{row['avg_items_per_order']:.1f} ชิ้น")
with c3:
    st.metric(label="🌍 จำนวนประเทศ", value=row['total_countries'])

st.markdown("---")

# แถวที่ 3: ที่สุดของช่วงเวลา (Top Performers)
st.subheader("🏆 ที่สุดของช่วงเวลา")
# ใช้รูปแบบแสดงผลแบบ Info Box
st.info(f"**🥇 สินค้าขายดีที่สุด:** {row['top_product']}")

t1, t2 = st.columns(2)
with t1:
    st.success(f"**📍 ประเทศที่มียอดซื้อสูงสุด:** \n\n {row['top_country']}")
with t2:
    st.warning(f"**📅 เดือนที่ยอดขายปังที่สุด:** \n\n {row['best_month']}")

# ส่วนท้าย
st.markdown("---")
if st.button('🔄 รีเฟรชข้อมูล'):
    st.rerun()