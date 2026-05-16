from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import os

# ==================== CONFIG ====================
DATA_PATH = '/opt/airflow/data'
os.makedirs(f'{DATA_PATH}/raw', exist_ok=True)
os.makedirs(f'{DATA_PATH}/processed', exist_ok=True)
os.makedirs(f'{DATA_PATH}/output', exist_ok=True)
RAW_FILE = f'{DATA_PATH}/raw/netflix_titles.csv'

# ==================== 1. DE: EXTRACT & TRANSFORM ====================
# --- สายบน: ภาพยนตร์ (Movies) ---
def filter_movies():
    df = pd.read_csv(RAW_FILE)
    df_movies = df[df['type'] == 'Movie'].copy()
    df_movies.to_parquet(f'{DATA_PATH}/processed/raw_movies.parquet', index=False)

def clean_movies():
    df = pd.read_parquet(f'{DATA_PATH}/processed/raw_movies.parquet')
    df['duration_num'] = df['duration'].str.replace(' min', '').astype(float)
    df['director'] = df['director'].fillna('Unknown')
    df['country'] = df['country'].fillna('Unknown')
    df.to_parquet(f'{DATA_PATH}/processed/clean_movies.parquet', index=False)

# --- สายล่าง: ซีรีส์ (TV Shows) ---
def filter_tv_shows():
    df = pd.read_csv(RAW_FILE)
    df_tv = df[df['type'] == 'TV Show'].copy()
    df_tv.to_parquet(f'{DATA_PATH}/processed/raw_tv.parquet', index=False)

def clean_tv_shows():
    df = pd.read_parquet(f'{DATA_PATH}/processed/raw_tv.parquet')
    df['duration_num'] = df['duration'].str.extract(r'(\d+)').astype(float)
    df['director'] = df['director'].fillna('Unknown')
    df['country'] = df['country'].fillna('Unknown')
    df.to_parquet(f'{DATA_PATH}/processed/clean_tv.parquet', index=False)

# ==================== 2. DE: MERGE ====================
def merge_netflix_data():
    df_movies = pd.read_parquet(f'{DATA_PATH}/processed/clean_movies.parquet')
    df_tv = pd.read_parquet(f'{DATA_PATH}/processed/clean_tv.parquet')
    df_master = pd.concat([df_movies, df_tv], ignore_index=True)
    df_master.to_parquet(f'{DATA_PATH}/processed/netflix_master.parquet', index=False)

# ==================== 3. DA: ANALYZE (เพิ่มเป็น 2 งาน) ====================
# --- DA งานที่ 1: วิเคราะห์เทรนด์รายปี ---
def da_yearly_trend_analysis():
    df = pd.read_parquet(f'{DATA_PATH}/processed/netflix_master.parquet')
    trend_df = df.groupby(['release_year', 'type']).size().reset_index(name='content_count')
    trend_df = trend_df[trend_df['release_year'] >= 2010]
    trend_df.to_csv(f'{DATA_PATH}/output/netflix_yearly_trend.csv', index=False)
    print("DA 1: Exported netflix_yearly_trend.csv")

# --- DA งานที่ 2: วิเคราะห์ 10 อันดับประเทศ (เพิ่มใหม่) ---
def da_top_countries_analysis():
    df = pd.read_parquet(f'{DATA_PATH}/processed/netflix_master.parquet')
    
    # ข้อมูลประเทศใน Netflix มักจะมาเป็น "US, India, UK" เราจะดึงแค่ประเทศแรกสุดมาใช้วิเคราะห์
    df['primary_country'] = df['country'].apply(lambda x: str(x).split(',')[0].strip())
    
    # กรองคำว่า Unknown ออก และนับจำนวนคอนเทนต์
    country_df = df[df['primary_country'] != 'Unknown']
    top_countries = country_df.groupby('primary_country').size().nlargest(10).reset_index(name='content_count')
    
    top_countries.to_csv(f'{DATA_PATH}/output/netflix_top_10_countries.csv', index=False)
    print("DA 2: Exported netflix_top_10_countries.csv")


# ==================== DAG DEFINITION ====================
with DAG(
    dag_id='netflix_advanced_pipeline', 
    start_date=datetime(2024, 1, 1), 
    schedule_interval='@weekly', 
    catchup=False,
    tags=['netflix', 'etl', 'parallel']
) as dag:

    # 1. ประกาศ Tasks
    start = PythonOperator(task_id='start', python_callable=lambda: print("Start Pipeline"))
    
    t_filter_movies = PythonOperator(task_id='filter_movies', python_callable=filter_movies)
    t_clean_movies  = PythonOperator(task_id='clean_movies', python_callable=clean_movies)
    
    t_filter_tv = PythonOperator(task_id='filter_tv_shows', python_callable=filter_tv_shows)
    t_clean_tv  = PythonOperator(task_id='clean_tv_shows', python_callable=clean_tv_shows)
    
    t_merge = PythonOperator(task_id='merge_data', python_callable=merge_netflix_data)
    
    # ประกาศ DA Tasks ทั้ง 2 ตัว
    t_analyze_trend = PythonOperator(task_id='da_yearly_trend', python_callable=da_yearly_trend_analysis)
    t_analyze_country = PythonOperator(task_id='da_top_countries', python_callable=da_top_countries_analysis)
    
    end = PythonOperator(task_id='end', python_callable=lambda: print("End Pipeline"))

    # 2. จัดเรียง Flow
    start >> [t_filter_movies, t_filter_tv]
    
    t_filter_movies >> t_clean_movies
    t_filter_tv >> t_clean_tv
    
    [t_clean_movies, t_clean_tv] >> t_merge
    
    # --- จุดที่มีการเปลี่ยนแปลง ---
    # หลังจาก Merge เสร็จ ให้แตกสายให้ DA ไปทำ 2 งานพร้อมกันเลย!
    t_merge >> [t_analyze_trend, t_analyze_country]
    
    # เมื่อ DA ทั้ง 2 งานเสร็จเรียบร้อย ถึงจะจบ Pipeline
    [t_analyze_trend, t_analyze_country] >> end