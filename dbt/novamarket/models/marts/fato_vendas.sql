{{ config(
    materialized='incremental',
    unique_key='id_venda'
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

where data_venda > (
    select max(data_venda)
    from {{ this }}
)

{% endif %}