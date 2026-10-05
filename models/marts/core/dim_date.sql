with date_spine as (
    select distinct cast(order_date as date) as date_day
    from {{ ref('stg_orders') }}
)

select
    date_day,
    extract(year from date_day) as year,
    extract(quarter from date_day) as quarter,
    extract(month from date_day) as month_number,
    format_date('%B', date_day) as month_name,
    extract(dayofweek from date_day) as day_of_week
from date_spine