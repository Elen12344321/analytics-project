with orders as (
    select * from {{ ref('stg_orders') }}
)

select
    customer_id,
    count(distinct order_id) as total_orders,
    sum(total_amount) as total_spent,
    min(order_date) as first_order_date,
    max(order_date) as last_order_date
from orders
group by 1