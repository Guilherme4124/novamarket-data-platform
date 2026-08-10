# NovaMarket Data Platform

## 📖 Sobre o Projeto

A NovaMarket Data Platform é um projeto de Engenharia de Dados desenvolvido para simular uma arquitetura moderna de processamento e análise de dados.

O projeto implementa diferentes etapas de um pipeline de dados, incluindo ingestão, armazenamento em Data Lake, processamento distribuído com Apache Spark, arquitetura em camadas, Data Warehouse e transformação analítica com dbt.

O objetivo é aplicar, na prática, conceitos e tecnologias utilizadas em ambientes modernos de Engenharia de Dados.

---

## 🏗️ Arquitetura

Fluxo implementado até o momento:

ERP Simulado
    ↓
Python
    ↓
Google Cloud Storage
    ↓
Databricks / Apache Spark
    ↓
Bronze
    ↓
Silver
    ↓
BigQuery
    ↓
dbt
    ↓
Staging
    ↓
Data Marts
    ├── dim_data
    └── fato_vendas

### Camadas

**Ingestion**
- Geração de dados simulando uma origem ERP.
- Ingestão utilizando Python.
- Armazenamento dos dados no Google Cloud Storage.

**Processing**
- Processamento utilizando Apache Spark no Databricks.
- Persistência utilizando Delta Lake.
- Organização dos dados utilizando arquitetura Bronze e Silver.

**Data Warehouse**
- Disponibilização dos dados tratados no BigQuery.

**Transformation**
- Transformações analíticas utilizando dbt.
- Criação da camada de staging.
- Modelagem dimensional.
- Criação de dimensão e tabela fato.
- Implementação de modelo incremental.

**Data Quality**
- Testes automatizados com dbt.
- Validação de valores nulos e unicidade.
- Documentação e lineage das transformações.

---

## 🚀 Stack Tecnológica

### Implementado

- Python
- Google Cloud Platform (GCP)
- Google Cloud Storage
- Apache Spark
- Databricks
- Delta Lake
- BigQuery
- dbt
- Git / GitHub

### Próximas etapas

- Apache Airflow
- Docker
- Orquestração do pipeline
- Expansão da camada Gold
- Novas regras de Data Quality

---

## 📂 Estrutura do Projeto

```text
novamarket-data-platform/
│
├── ingestion/
│   └── erp/
│       ├── erp_simulator/
│       └── upload_to_gcs.py
│
├── dbt/
│   └── novamarket/
│       └── models/
│           ├── staging/
│           │   ├── sources.yml
│           │   └── stg_vendas.sql
│           │
│           └── marts/
│               ├── dim_data.sql
│               ├── fato_vendas.sql
│               └── schema.yml
│
├── requirements.txt
└── README.md
