# 🃏 Poker Tournament Simulator & End-to-End Data Platform

![Status](https://img.shields.io/badge/Status-Architecture_Refactor-orange)
![Tech](https://img.shields.io/badge/Stack-Modern_Data_Stack-blue)

## 🚧 Project Status: Major Architectural Refactoring
The project is currently undergoing a complete migration from a **monolithic Python script** to a **decoupled, production-grade Data Engineering pipeline**. 

The goal is to move away from local DataFrame processing toward a scalable infrastructure using the **Modern Data Stack** (S3, SQL Warehouse, Containerization).

---

## 🏗️ Target Architecture
I am implementing a professional-grade data lifecycle to handle high-volume simulation results:



1. **Generation Layer:** Poker Simulator (Python) generating raw event data.
2. **Landing Zone (Data Lake):** Raw ingestion into **MinIO** (S3-compatible Object Storage) via Boto3 API.
3. **Processing Layer (ETL):** Automated transformation pipeline cleaning data and calculating KPIs (ROI, ITM%, Variance).
4. **Storage Layer (Warehouse):** Structured storage in **PostgreSQL**.
5. **Business Intelligence:** Interactive analytics dashboard built with **Streamlit** and **Matplotlib**.
6. **Orchestration:** Entire stack containerized using **Docker & Docker Compose**.

---

## 🛠️ Tech Stack (In Progress)
* **Infrastructure:** Docker, Docker Compose
* **Data Lake:** MinIO (AWS S3 Mock)
* **Database:** PostgreSQL
* **Processing:** Python / Pandas (Migrating to PySpark)
* **Visualization:** Streamlit, Matplotlib, Seaborn

---

## 📈 Roadmap & Milestones
- [x] **Core Engine:** High-performance poker tournament simulation logic.
- [🔄] **Infrastructure:** Setting up Dockerized environment (Postgres + MinIO).
- [ ] **Data Ingestion:** Refactoring simulator to push raw CSVs to S3/MinIO.
- [ ] **ETL Pipeline:** Developing the automated bridge between Data Lake and Warehouse.
- [ ] **BI Dashboard:** Building the final Streamlit UI for variance analysis.

---

## 🚀 Legacy Execution
*Note: The instructions below apply to the initial version. The new Docker-based launch procedure will be updated soon.*
