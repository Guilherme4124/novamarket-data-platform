select *
from {{ source('novamarket', 'silver_vendas') }}