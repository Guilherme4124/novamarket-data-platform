{{ config(
    materialized='incremental',
    unique_key='id_venda',
    partition_by={
        "field": "data_venda",
        "data_type": "date",
        "granularity": "day"
    }
) }}
select
    id_venda,
    id_cliente,
    id_produto,
    data_venda,
    quantidade,
    valor_unitario,
    valor_total
from {{ ref('stg_vendas') }}

{% if is_incremental() %}

where data_venda >= (
    select date_sub(max(data_venda), interval 2 day)
    from {{ this }}
)

{% endif %}