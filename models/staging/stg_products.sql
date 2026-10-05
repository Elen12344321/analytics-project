with source_data as (
    select * 
    from {{ source('raw_layer', 'raw_products') }}
)

select
    safe_cast(product_id as int64) as product_id,
    trim(product_name) as product_name,
    trim(category) as category,
    safe_cast(price as numeric) as price
from source_data
where product_id is not null