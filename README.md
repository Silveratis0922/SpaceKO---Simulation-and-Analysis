# SpaceKO - Pipeline ETL Data End-to-End

![Status](https://img.shields.io/badge/Status-Terminé-green)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![PySpark](https://img.shields.io/badge/PySpark-3.x-orange)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)
![Airflow](https://img.shields.io/badge/Apache_Airflow-2.9-017CEE)
![dbt](https://img.shields.io/badge/dbt-1.x-FF694B)
![Metabase](https://img.shields.io/badge/Metabase-v0.52-509EE3)

## Description

Simulation de tournois SpaceKO (Winamax) et pipeline ETL complet pour répondre à une question analytique métier :

> **La dotation réelle distribuée dépasse-t-elle la dotation estimée ?**

## Architecture

```mermaid
flowchart LR
    subgraph Simulation
        A[Python Simulator\nPOO + Pandas]
    end

    subgraph MinIO - Data Lake
        B[(Bronze\nevents.parquet)]
        C[(Silver\nresults.parquet)]
    end

    subgraph Transformation
        D[PySpark\ntournament_replayer]
        E[dbt / SQL\nagrégations Gold]
    end

    subgraph PostgreSQL
        F[(silver_results\npublic)]
        G[(gold_results\ngold)]
    end

    subgraph Visualisation
        H[Metabase\nDashboards]
    end

    subgraph Orchestration
        I[Apache Airflow\nspaceko_pipeline]
    end

    A -->|events.parquet| B
    B --> D --> C
    C --> F --> E --> G
    G --> H
    I -.->|orchestrate| A
    I -.->|orchestrate| D
    I -.->|orchestrate| E
```

## Stack technique

| Couche | Technologie |
|---|---|
| Simulation | Python (POO), Pandas |
| Data Lake | MinIO (S3-compatible), architecture Medallion |
| Transformation | PySpark, dbt |
| Orchestration | Apache Airflow |
| Stockage | PostgreSQL |
| Visualisation | Metabase |
| Infrastructure | Docker, Docker Compose |

## Lancer le projet

```bash
docker compose up -d 
```
Accès :

- Airflow : http://localhost:8080
- Metabase : http://localhost:3000
- MinIO : http://localhost:9001

## Dashboards

![Dashboard 1](assets/Dashboard_1.png)
![Dashboard 2](assets/Dashboard_2.png)