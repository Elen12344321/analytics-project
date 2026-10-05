with source_data as (
    select * 
    from {{ source('raw_layer', 'raw_orders') }}
),

cleaned as (
    select
        safe_cast(order_id as int64) as order_id,
        safe_cast(customer_id as int64) as customer_id,
        safe_cast(product_id as int64) as product_id,
        cast(order_date as timestamp) as order_date,
        safe_cast(quantity as int64) as quantity,
        safe_cast(total_amount as numeric) as total_amount,
        row_number() over (
            partition by safe_cast(order_id as int64) 
            order by cast(order_date as timestamp) desc
        ) as row_num
    from source_data
)

select
    order_id,
    customer_id,
    product_id,
    order_date,
    quantity,
    total_amount
from cleaned
where row_num = 1
  and order_id is not null
  and customer_id is not null