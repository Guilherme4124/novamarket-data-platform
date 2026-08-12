select distinct
    id_produto
from {{ ref('stg_vendas') }}
where id_produto is not null