SELECT *
FROM {{ ref('fato_vendas') }}
WHERE 
    valor_total != quantidade * valor_unitarios 