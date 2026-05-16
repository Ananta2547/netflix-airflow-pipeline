# 🎬 Netflix Analytics Pipeline

โปรเจกต์นี้เป็นการจัดทำ ETL (Extract, Transform, Load) Pipeline แบบครบวงจร เพื่อประมวลผลข้อมูลภาพยนตร์และซีรีส์ของ Netflix และสรุปผลออกมาเป็นข้อมูลเชิงลึก (Business Insights) ผ่านระบบสร้างรายงานอัตโนมัติและ Dashboard สำหรับการนำไปใช้งานต่อ

## 🚀 Overview (ภาพรวมของโปรเจกต์)

ระบบจะประมวลผลชุดข้อมูล **Netflix Titles** โดยแปลงจากข้อมูลดิบให้กลายเป็นสถิติระดับสูงที่พร้อมใช้งาน มีการใช้ **Apache Airflow** ในการจัดการและควบคุมลำดับงาน (Orchestration) และแสดงผลลัพธ์การวิเคราะห์ผ่าน **Streamlit**

### 🛠️ Tech Stack (เทคโนโลยีที่ใช้)
- **Orchestration**: Apache Airflow
- **Data Processing**: Python, Pandas, PyArrow (Parquet)
- **Database**: PostgreSQL (สำหรับ Airflow Metadata)
- **Visualization**: Streamlit, Plotly
- **Infrastructure**: Docker & Docker Compose

## 🏗️ Pipeline Architecture (สถาปัตยกรรมข้อมูล)

การทำงานของ Pipeline ถูกจัดโครงสร้างแบบ Directed Acyclic Graph (DAG) ภายในระบบ Airflow ดังนี้:

### 1. Extract (การสกัดข้อมูล)
- อ่านข้อมูลดิบจากไฟล์ `data/raw/netflix_titles.csv`
- ทำการแยกสายข้อมูล (Filter) ออกเป็น 2 กลุ่ม คือ 'ภาพยนตร์' (Movies) และ 'ซีรีส์' (TV Shows)
- บันทึกข้อมูลชั่วคราวในรูปแบบ Parquet เพื่อเพิ่มประสิทธิภาพในการประมวลผลขั้นต่อไป

### 2. Transform (การแปลงและทำความสะอาดข้อมูล)
- **Cleaning**: จัดการค่าว่าง (Null) ในคอลัมน์ผู้กำกับ (Director) และประเทศ (Country) โดยแทนที่ด้วยคำว่า 'Unknown'
- **Feature Engineering**: แปลงข้อมูลคอลัมน์ระยะเวลา (Duration) จากรูปแบบข้อความ (String) ให้เป็นตัวเลข (Float) เพื่อให้สามารถนำไปคำนวณทางสถิติได้
- บันทึกไฟล์ที่ผ่านการทำความสะอาดแล้วเป็นฟอร์แมต Parquet

### 3. Merge & Analyze (การผสานข้อมูลและวิเคราะห์ผล)
ระบบจะสร้างไฟล์รายงานทางธุรกิจที่สำคัญ ได้แก่:
- **Master Dataset**: นำข้อมูลภาพยนตร์และซีรีส์ที่คลีนแล้วมารวมกัน (Concatenate) เป็นไฟล์ `netflix_master.parquet` ชุดเดียว
- **Yearly Trend Report**: วิเคราะห์และนับจำนวนคอนเทนต์ที่ถูกปล่อยออกมาในแต่ละปี (ตั้งแต่ปี 2010 เป็นต้นมา)
- **Top Countries Report**: สกัดชื่อประเทศหลัก (Primary Country) และจัดอันดับ 10 ประเทศที่เป็นผู้ผลิตคอนเทนต์สูงสุดลง Netflix

### 4. Visualization (การแสดงผลข้อมูล)
- มีการสร้างแอปพลิเคชัน **Streamlit** (`app.py`) เพื่อใช้อ่านไฟล์สรุปผล (Executive Summary) และแสดงผลเป็นหน้า Dashboard แบบอินเทอร์แอกทีฟให้กับผู้ใช้งาน

## 🚦 Getting Started (วิธีติดตั้งและใช้งาน)

### Prerequisites (สิ่งที่ต้องมี)
- ติดตั้ง Docker และ Docker Compose ในเครื่อง

### Installation & Execution (ขั้นตอนการรันโปรเจกต์)
1. **Start the infrastructure** (รันระบบฐานราก):
   ```bash
   docker-compose up -d

**Access Airflow** (เข้าสู่ระบบจัดการ Pipeline):
- เปิดเบราว์เซอร์และเข้าไปที่ `http://localhost:8080`
- ล็อกอินด้วย Username: `airflow` / Password: `airflow` (หรือตามที่ตั้งค่าไว้)

**Run the Pipeline** (สั่งรันข้อมูล):
- ทำการ Unpause ตัว DAG ที่ชื่อ `netflix_advanced_pipeline` และกด Trigger เพื่อเริ่มการทำงาน

**Launch the Dashboard** (เปิดหน้าแสดงผล):
- เมื่อ Pipeline ทำงานเสร็จสิ้น ให้รันแอปพลิเคชัน Streamlit:
  ```bash
  streamlit run app.py
## 📁 Project Structure
- `dags/`: Airflow DAG definitions.
- `data/raw/`: Source CSV files.
- `data/processed/`: Intermediate Parquet files.
- `data/output/`: Final business reports and the Streamlit app.
- `logs/`: Airflow task logs.
- `docker-compose.yaml` & `dockerfile`: Container configuration.
