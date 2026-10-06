with source as (
    select * from {{ source('raw_layer', 'raw_orders') }}
)

select
    cast(order_id as string) as order_id,
    cast(customer_id as string) as customer_id,
    cast(product_id as int64) as product_id,
    cast(quantity as int64) as quantity,
    cast(total_amount as numeric) as total_amount,
    cast(order_date as timestamp) as order_date,
    cast(status as string) as status
from source