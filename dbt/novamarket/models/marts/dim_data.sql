select distinct
    data_venda,
    extract(day from data_venda) as dia,
    extract(month from data_venda) as mes,
    extract(year from data_venda) as ano,
    extract(quarter from data_venda) as trimestre
from {{ ref('stg_vendas') }}
where data_venda is not null