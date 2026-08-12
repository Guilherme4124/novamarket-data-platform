# 🛒 NovaMarket Data Platform

Pipeline de Engenharia de Dados criado para simular o processamento de vendas de uma empresa fictícia, desde a ingestão dos dados até a construção de um modelo dimensional para análise.

A ideia do projeto foi sair um pouco do cenário de scripts isolados e montar uma arquitetura mais próxima do que encontramos em projetos reais de dados, separando ingestão, armazenamento, processamento, transformação, qualidade e orquestração.

## 🏗️ Arquitetura

O fluxo do projeto ficou assim:

```text
ERP / Dados de Vendas
        │
        ▼
     Python
     Ingestão
        │
        ▼
Google Cloud Storage
       RAW
        │
        ▼
Databricks + PySpark
        │
        ▼
      SILVER
        │
        ▼
     BigQuery
        │
        ▼
       dbt
        │
        ▼
Modelo Dimensional
```

Para a parte de orquestração, utilizei Apache Airflow:

```text
ingestao
    │
    ▼
processamento_spark
    │
    ▼
transformacao_dbt
```

## 🧰 Tecnologias utilizadas

| Tecnologia | Uso no projeto |
|---|---|
| 🐍 Python | Ingestão e tratamento de dados |
| ☁️ Google Cloud Storage | Data Lake |
| ⚡ Apache Spark | Processamento distribuído |
| 🧱 Databricks | Execução do processamento Spark |
| 🔎 BigQuery | Data Warehouse |
| 🔧 dbt | Transformações, modelagem e testes |
| 🌬️ Apache Airflow | Orquestração |
| 🗃️ SQL | Transformações e regras de negócio |
| 🐙 GitHub | Versionamento |

## 📥 Ingestão e Data Lake

O pipeline começa com dados de vendas simulando uma origem operacional/ERP.

Os arquivos são enviados para o **Google Cloud Storage**, que funciona como Data Lake do projeto.

A ideia é manter os dados brutos separados das transformações:

```text
Origem → Ingestão → RAW → Processamento → SILVER
```

Isso permite preservar o dado recebido da origem e facilita possíveis reprocessamentos.

## ⚡ Processamento com Spark

Para o processamento utilizei **PySpark no Databricks**.

O Spark fica responsável pelas transformações da camada de processamento antes dos dados seguirem para a parte analítica.

Além do notebook, configurei o processamento como um **Databricks Job**.

Com isso, o processamento deixa de depender de executar manualmente uma célula do notebook e passa a existir como uma carga que pode ser disparada por outras ferramentas.

```text
RAW
 │
 ▼
PySpark
 │
 ├── leitura
 ├── tratamento
 ├── transformação
 └── validação
 │
 ▼
SILVER
```

## 🏢 BigQuery + Modelo Dimensional

O **BigQuery** foi utilizado como Data Warehouse.

Na camada analítica, construí um modelo dimensional simples de vendas:

```text
                 dim_cliente
                      │
                      │
dim_produto ───── fato_vendas ───── dim_data
```

A `fato_vendas` concentra os eventos e métricas das vendas, enquanto as dimensões representam os contextos utilizados nas análises.

## 🔧 Transformações com dbt

Uma das partes que mais quis explorar neste projeto foi o **dbt**.

Separei os modelos em duas camadas principais:

```text
models/
│
├── staging/
│
└── marts/
    ├── dim_cliente.sql
    ├── dim_produto.sql
    ├── dim_data.sql
    └── fato_vendas.sql
```

A ideia foi não misturar preparação dos dados com o modelo que será utilizado para consumo.

Também utilizei materialização **incremental** na tabela fato para evitar processar todo o histórico em cada execução.

## 🔄 Carga incremental

Em vez de reconstruir toda a `fato_vendas` sempre que chegam dados novos, o modelo trabalha de forma incremental.

O fluxo fica aproximadamente assim:

```text
Novos dados
    │
    ▼
Janela incremental
    │
    ▼
   MERGE
   /   \
  /     \
UPDATE  INSERT
```

Também considerei uma janela de dados recentes para permitir o tratamento de registros que possam chegar com atraso.

Foi uma parte interessante do projeto porque me fez pensar não só em **"como transformar os dados"**, mas também em **como evitar processamento desnecessário**.

## 🧪 Qualidade dos dados

Também adicionei testes com dbt.

Foram utilizados testes como:

- `not_null`
- `unique`
- `relationships`

Além deles, criei uma validação própria para uma regra de negócio:

```text
valor_total = quantidade × valor_unitario
```

Os testes de relacionamento foram especialmente úteis para validar se os IDs existentes na fato também estavam presentes nas respectivas dimensões.

Ou seja, além de transformar os dados, o pipeline também verifica se o modelo continua consistente.

## 🌬️ Orquestração com Airflow

Para estudar orquestração, configurei o **Apache Airflow utilizando WSL2**.

A DAG principal do projeto é:

```text
novamarket_pipeline
```

e representa a dependência:

```text
ingestao
    │
    ▼
processamento_spark
    │
    ▼
transformacao_dbt
```

Um comportamento que consegui validar na prática foi o controle de dependências.

Quando a task responsável pelo Spark falhou, a etapa seguinte ficou como:

```text
upstream_failed
```

Ou seja, o Airflow não deixou uma transformação dependente continuar depois de uma falha anterior.

Parece simples vendo o desenho pronto, mas foi uma das partes legais de ver funcionando na prática.

## 🔌 Airflow + Databricks

Também implementei a chamada do Databricks através do Airflow utilizando o:

```python
DatabricksRunNowOperator
```

A ideia da integração é:

```text
Airflow
   │
   ▼
Databricks Jobs API
   │
   ▼
Databricks Job
   │
   ▼
PySpark
```

Durante os testes no ambiente local, encontrei um problema de autenticação via Personal Access Token (`HTTP 401`).

Para isolar o problema, testei a autenticação separadamente e configurei **OAuth através do Databricks CLI**, conseguindo acessar a Jobs API e listar o Job normalmente.

Então ficou uma melhoria pendente no projeto: configurar a autenticação OAuth/Service Principal diretamente entre Airflow e Databricks.

Preferi manter essa limitação documentada em vez de simplesmente esconder uma integração que não terminou 100%.

## 📂 Estrutura

```text
novamarket-data-platform/
│
├── ingestion/
│
├── spark/
│
├── dbt/
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   └── tests/
│
├── airflow/
│
├── README.md
└── .gitignore
```

## 💡 O que pratiquei nesse projeto

Mais do que aprender comandos específicos de cada ferramenta, esse projeto serviu para juntar vários conceitos que eu vinha estudando separadamente:

- Data Lake e Data Warehouse
- arquitetura em camadas
- ETL / ELT
- PySpark
- processamento distribuído
- processamento incremental
- MERGE
- modelagem dimensional
- fato e dimensões
- testes de qualidade
- integridade referencial
- DAGs
- dependência entre tasks
- Jobs
- tratamento de falhas
- autenticação entre serviços
- Git e versionamento

## 🚀 Próximos passos

Ainda existem algumas coisas que quero evoluir futuramente:

- finalizar Airflow → Databricks utilizando OAuth/Service Principal;
- executar o dbt diretamente pelo Airflow;
- adicionar Docker;
- implementar CI/CD;
- adicionar monitoramento e alertas;
- testar o pipeline com volumes maiores.

---

### 📌 Sobre o projeto

O NovaMarket nasceu como um projeto de estudo para colocar em prática uma arquitetura de Engenharia de Dados de ponta a ponta.

Mais do que simplesmente utilizar várias ferramentas no mesmo repositório, meu objetivo foi entender **qual responsabilidade cada tecnologia deveria ter dentro do pipeline** e como elas se conectam.

Algumas coisas funcionaram de primeira, outras quebraram — principalmente integrações e autenticação — e justamente essas falhas acabaram fazendo parte do aprendizado do projeto. 😅
