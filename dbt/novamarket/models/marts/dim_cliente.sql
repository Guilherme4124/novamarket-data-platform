select distinct
    id_cliente
from {{ ref('stg_vendas') }}
where id_cliente  is not null