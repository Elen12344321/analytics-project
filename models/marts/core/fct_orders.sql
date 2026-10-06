with orders as (
    select * from {{ ref('stg_orders') }}
),

products as (
    select * from {{ ref('stg_products') }}
)

select
    o.order_id,
    o.customer_id,
    o.product_id,
    p.category as product_category,
    o.order_date,
    o.quantity,
    o.total_amount,
    round(o.total_amount / nullif(o.quantity, 0), 2) as calculated_unit_price
from orders o
left join products p on o.product_id = p.product_id