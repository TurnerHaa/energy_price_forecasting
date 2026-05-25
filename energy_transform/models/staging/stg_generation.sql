with source as (
    SELECT * FROM {{source('local_raw', 'generation')}}
),

flattened AS (
    SELECT
        startTime::timestamp as start_time,
        settlementPeriod::integer as settlement_period,
        unnest(data) as generation_types
    FROM source
),

final as (
    SELECT
        start_time,
        settlement_period,
        generation_types.fuelType::varchar as fuel_type,
        generation_types.generation::varchar as generation_mw
    FROM flattened
)

SELECT * FROM final