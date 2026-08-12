# NovaMarket Data Platform

Projeto de Engenharia de Dados desenvolvido para simular uma arquitetura moderna de processamento e transformação de dados de vendas, utilizando conceitos de Data Lake, processamento distribuído, modelagem analítica, qualidade de dados e orquestração.

O objetivo do projeto é construir um pipeline de dados próximo de um cenário real, partindo da ingestão de dados de um ERP simulado até a disponibilização de dados estruturados para consumo analítico.

---

## Arquitetura

O pipeline foi estruturado utilizando diferentes ferramentas para cada responsabilidade:

- **Python** — geração e ingestão dos dados
- **Cloud Storage / Data Lake** — armazenamento dos dados
- **Databricks + Apache Spark** — processamento distribuído
- **BigQuery** — armazenamento analítico
- **dbt** — transformação, modelagem e testes de qualidade
- **Apache Airflow** — orquestração do pipeline

Fluxo simplificado:

```text
ERP Simulator
      |
      v
Data Lake / Raw
      |
      v
Databricks
Apache Spark
      |
      v
Camada Silver
      |
      v
BigQuery
      |
      v
dbt
      |
      v
Modelo Dimensional
      |
      +---- dim_cliente
      +---- dim_produto
      +---- dim_data
      +---- fato_vendas

Apache Airflow
      |
      +---- ingestao
      |
      +---- processamento_spark
      |
      +---- transformacao_dbt
```

---

## Data Lake

Os dados gerados pelo ERP simulado são armazenados inicialmente na camada de dados brutos, preservando os dados antes das transformações.

Essa separação permite manter os dados originais disponíveis para reprocessamento e auditoria do pipeline.

### Evidência do armazenamento

![Data Lake](docs/evidencias/01_storage_raw.png)

---

## Processamento com Apache Spark

O processamento distribuído foi implementado utilizando **Apache Spark no Databricks**.

O Spark é responsável pela leitura dos dados ingeridos e pela aplicação das transformações necessárias antes da disponibilização dos dados para as etapas analíticas.

O processamento também foi configurado como um **Databricks Job**, permitindo que o notebook de processamento seja executado como uma carga independente.

### Execução do processamento Spark

![Databricks Spark](docs/evidencias/02_databricks_spark.png)

### Databricks Job

![Databricks Job](docs/evidencias/03_databricks_job_success.png)

---

## Data Warehouse — BigQuery

Após o processamento, os dados são disponibilizados no **Google BigQuery**, utilizado como camada analítica da plataforma.

Sobre essa camada são executadas as transformações do dbt responsáveis pela construção do modelo dimensional.

### Modelo analítico

O modelo final contém:

```text
dim_cliente
dim_produto
dim_data
fato_vendas
```

A tabela `fato_vendas` concentra as métricas do processo de vendas, enquanto as dimensões fornecem os contextos necessários para análise.

### Evidência no BigQuery

![BigQuery](docs/evidencias/04_bigquery_modelo.png)

---

## Transformações com dbt

O **dbt** foi utilizado para organizar as transformações SQL e construir a camada analítica do projeto.

A estrutura foi separada em modelos de staging e marts.

```text
dbt/novamarket/
|
+-- models/
|   |
|   +-- staging/
|   |
|   +-- marts/
|       +-- dim_cliente.sql
|       +-- dim_produto.sql
|       +-- dim_data.sql
|       +-- fato_vendas.sql
|
+-- tests/
    +-- valor_total_consistente.sql
```

Essa organização separa a preparação dos dados da camada destinada ao consumo analítico.

---

## Qualidade de Dados

Foram implementados testes utilizando dbt para validar regras importantes do modelo.

Entre as validações estão:

- valores obrigatórios (`not_null`);
- unicidade de identificadores (`unique`);
- integridade entre fato e dimensões (`relationships`);
- consistência dos valores calculados.

Também foi criado um teste SQL customizado para validar a consistência do valor total das vendas.

Exemplo da regra:

```text
valor_total = quantidade * valor_unitario
```

### Execução dos testes

![dbt Tests](docs/evidencias/05_dbt_tests.png)

---

## Orquestração com Apache Airflow

O Apache Airflow foi configurado localmente utilizando WSL2 para representar a camada de orquestração da plataforma.

Foi criada a DAG:

```text
novamarket_pipeline
```

com a seguinte sequência de dependências:

```text
ingestao
    |
    v
processamento_spark
    |
    v
transformacao_dbt
```

A DAG garante que uma etapa somente seja iniciada após a conclusão da etapa anterior.

### Airflow DAG

![Airflow DAG](docs/evidencias/06_airflow_dag.png)

---

## Integração Airflow + Databricks

A integração com o Databricks foi implementada utilizando o provider oficial do Databricks para Apache Airflow e o operador responsável por iniciar um Job existente.

O Job de processamento Spark foi configurado no Databricks e pode ser executado diretamente pela plataforma.

Durante a integração do ambiente local do Airflow com o Databricks, a autenticação utilizando Personal Access Token retornou **HTTP 401 Unauthorized**.

Como parte da investigação, a autenticação OAuth foi configurada utilizando o Databricks CLI e validada com sucesso contra a Jobs API, permitindo listar e acessar o Job criado.

Dessa forma, o processamento Spark e o Job Databricks foram validados, enquanto a autenticação direta entre o Airflow local e o Databricks permaneceu como uma limitação do ambiente utilizado.

Em um cenário produtivo, essa comunicação seria configurada utilizando uma identidade de serviço e OAuth, evitando dependência de credenciais pessoais.

---

## Estrutura do Projeto

```text
novamarket-data-platform/
|
+-- dbt/
|   +-- novamarket/
|       +-- models/
|       +-- tests/
|
+-- ingestion/
|   +-- erp_simulator/
|
+-- spark/
|   +-- processamento_vendas.py
|
+-- docs/
|   +-- evidencias/
|
+-- README.md
+-- .gitignore
```

---

## Tecnologias

| Tecnologia | Utilização |
|---|---|
| Python | Ingestão e processamento |
| Google Cloud | Infraestrutura de dados |
| Cloud Storage | Data Lake |
| BigQuery | Data Warehouse |
| Databricks | Plataforma de processamento |
| Apache Spark | Processamento distribuído |
| dbt | Transformação e modelagem |
| Apache Airflow | Orquestração |
| SQL | Transformações e regras de negócio |
| Git / GitHub | Versionamento |

---

## Conceitos aplicados

O projeto aplica conceitos importantes de Engenharia de Dados:

- Data Lake
- Data Warehouse
- ETL / ELT
- processamento distribuído
- arquitetura em camadas
- modelagem dimensional
- tabela fato e dimensões
- qualidade de dados
- testes automatizados
- orquestração de pipelines
- dependência entre tarefas
- Jobs
- autenticação entre serviços
- versionamento de código

---

## Melhorias Futuras

Algumas evoluções planejadas para o projeto:

- autenticação Airflow → Databricks utilizando Service Principal/OAuth;
- execução do dbt diretamente pela DAG;
- containerização do Airflow com Docker;
- CI/CD;
- monitoramento e alertas;
- parametrização das execuções;
- processamento incremental;
- maior volume de dados para testes de performance.

---

## Objetivo

Este projeto foi desenvolvido como parte dos meus estudos em Engenharia de Dados, com foco em aplicar ferramentas utilizadas em ambientes modernos de dados e compreender não apenas cada tecnologia isoladamente, mas como elas se integram dentro de uma plataforma de dados.

O foco principal foi trabalhar conceitos de arquitetura, processamento distribuído, transformação, qualidade e orquestração de dados em um único projeto.
