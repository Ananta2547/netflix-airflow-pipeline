# Online Retail Analytics Pipeline

This project implements a complete ETL (Extract, Transform, Load) pipeline to process online retail data and provide actionable business insights through automated reports and an executive dashboard.

## 🚀 Overview

The pipeline processes the **Online Retail II** dataset, transforming raw transaction logs into high-level business metrics. It uses **Apache Airflow** for orchestration and **Streamlit** for the final visualization.

### 🛠️ Tech Stack
- **Orchestration**: Apache Airflow 2.7.3
- **Data Processing**: Python, Pandas, PyArrow (Parquet)
- **Database**: PostgreSQL (Airflow Metadata)
- **Visualization**: Streamlit
- **Infrastructure**: Docker & Docker Compose

## 🏗️ Pipeline Architecture

The pipeline is structured as a directed acyclic graph (DAG) in Airflow:

### 1. Extract
- Reads raw retail data from `data/raw/online_retail_II.csv`.
- Handles encoding issues (UTF-8/ISO-8859-1).
- Saves data as Parquet for optimized downstream processing.

### 2. Transform
- **Cleaning**: Removes duplicates, cancelled orders (Invoice 'C'), and invalid records (negative quantity/price).
- **Feature Engineering**:
  - Calculates total revenue.
  - Extracts time-based features (hour, weekday, quarter).
  - Categorizes revenue sizes.
- **Validation**: Performs quality checks on row counts, null values, and date ranges to ensure data integrity before loading.

### 3. Load
Generates four key business artifacts:
- **Product Report**: Analysis of top-selling products and revenue by item.
- **Customer Report**: RFM (Recency, Frequency, Monetary) analysis and customer segmentation (e.g., Champions, Loyal, At Risk).
- **Revenue Report**: Revenue trends by day, month, and country.
- **Executive Dashboard**: A high-level summary CSV containing critical KPIs.

### 4. Visualization
- A **Streamlit** application (`data/output/app_exec.py`) reads the executive summary to present a "Daily Snapshot" for stakeholders.

## 🚦 Getting Started

### Prerequisites
- Docker and Docker Compose installed.

### Installation & Execution
1. **Start the infrastructure**:
   ```bash
   docker-compose up -d
   ```
2. **Access Airflow**:
   - Open `http://localhost:8080` in your browser.
   - Login with: `admin` / `admin`.
3. **Run the Pipeline**:
   - Unpause the `retail_analytics_pipeline` DAG and trigger it manually.
4. **Launch the Dashboard**:
   - Once the pipeline completes, run the Streamlit app:
     ```bash
     streamlit run data/output/app_exec.py
     ```

## 📁 Project Structure
- `dags/`: Airflow DAG definitions.
- `data/raw/`: Source CSV files.
- `data/processed/`: Intermediate Parquet files.
- `data/output/`: Final business reports and the Streamlit app.
- `logs/`: Airflow task logs.
- `docker-compose.yaml` & `dockerfile`: Container configuration.
