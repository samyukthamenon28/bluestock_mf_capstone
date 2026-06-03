# Analytical SQL Report — Bluestock MF Capstone
This report compiles the results of the 10 analytical SQL queries executed on the Star Schema database.

## Query 1: Total Transaction Volume and Net Inflows by Fund House
*Summarizes total transaction counts, investments, redemptions, and net flows.*

### SQL Query
```sql
-- EXPLAIN: Grouping facts by dim_schemes.fund_house to understand market activity.
SELECT
    s.fund_house,
    COUNT(t.transaction_id) AS total_transaction_count,
    SUM(CASE WHEN t.transaction_type IN ('SIP', 'Lumpsum') THEN t.amount_inr ELSE 0 END) AS total_investment_amount_inr,
    SUM(CASE WHEN t.transaction_type = 'Redemption' THEN t.amount_inr ELSE 0 END) AS total_redemption_amount_inr,
    SUM(CASE WHEN t.transaction_type IN ('SIP', 'Lumpsum') THEN t.amount_inr ELSE -t.amount_inr END) AS net_inflow_inr
FROM fact_transactions t
JOIN dim_schemes s ON t.amfi_code = s.amfi_code
GROUP BY s.fund_house
ORDER BY net_inflow_inr DESC;
```

### Results
| fund_house               |   total_transaction_count |   total_investment_amount_inr |   total_redemption_amount_inr |   net_inflow_inr |
|:-------------------------|--------------------------:|------------------------------:|------------------------------:|-----------------:|
| SBI Mutual Fund          |                      3984 |                   2.87742e+08 |                   1.44635e+08 |      1.43108e+08 |
| ICICI Prudential MF      |                      4082 |                   2.83337e+08 |                   1.52439e+08 |      1.30898e+08 |
| Nippon India MF          |                      4092 |                   2.77869e+08 |                   1.51927e+08 |      1.25942e+08 |
| HDFC Mutual Fund         |                      4139 |                   2.83905e+08 |                   1.63227e+08 |      1.20678e+08 |
| Axis Mutual Fund         |                      3334 |                   2.37442e+08 |                   1.23419e+08 |      1.14024e+08 |
| UTI Mutual Fund          |                      2473 |                   1.88074e+08 |                   9.56e+07    |      9.24736e+07 |
| Kotak Mahindra MF        |                      3239 |                   2.20197e+08 |                   1.30189e+08 |      9.00073e+07 |
| DSP Mutual Fund          |                      2444 |                   1.61448e+08 |                   8.76481e+07 |      7.37995e+07 |
| Aditya Birla Sun Life MF |                      2504 |                   1.69069e+08 |                   9.61404e+07 |      7.29282e+07 |
| Mirae Asset MF           |                      2487 |                   1.67973e+08 |                   9.9302e+07  |      6.86712e+07 |

---

## Query 2: Top 3 Performing Schemes within Each Category (by 3-Year Return)
*Ranks schemes using window functions to find the top performers per category.*

### SQL Query
```sql
-- EXPLAIN: Window DENSE_RANK() partitioned by category to rank schemes dynamically.
WITH RankedSchemes AS (
    SELECT
        category,
        scheme_name,
        return_3yr_pct,
        sharpe_ratio,
        aum_crore,
        DENSE_RANK() OVER (PARTITION BY category ORDER BY return_3yr_pct DESC) as rank
    FROM dim_schemes
)
SELECT category, rank, scheme_name, return_3yr_pct, sharpe_ratio, aum_crore
FROM RankedSchemes
WHERE rank <= 3
ORDER BY category, rank;
```

### Results
| category   |   rank | scheme_name                                  |   return_3yr_pct |   sharpe_ratio |   aum_crore |
|:-----------|-------:|:---------------------------------------------|-----------------:|---------------:|------------:|
| Debt       |      1 | ICICI Pru Liquid Fund - Regular - Growth     |             7.68 |           7.68 |       39116 |
| Debt       |      2 | HDFC Short Term Debt Fund - Regular - Growth |             7.37 |           1.84 |       27953 |
| Debt       |      3 | Kotak Liquid Fund - Regular - Growth         |             6.18 |           6.18 |       27623 |
| Equity     |      1 | SBI Small Cap Fund - Regular Plan - Growth   |            23.39 |           0.94 |       19259 |
| Equity     |      2 | SBI Small Cap Fund - Direct Plan - Growth    |            23.14 |           0.93 |       36061 |
| Equity     |      3 | ABSL Small Cap Fund - Regular - Growth       |            22.38 |           0.9  |       41613 |

---

## Query 3: Underperforming Schemes Relative to Their 3-Year Benchmarks
*Highlights schemes where returns lag the benchmark, including risk statistics.*

### SQL Query
```sql
-- EXPLAIN: Comparative join of performance and benchmark returns to flag underperformance.
SELECT
    amfi_code,
    scheme_name,
    category,
    return_3yr_pct,
    benchmark_3yr_pct,
    ROUND((return_3yr_pct - benchmark_3yr_pct), 2) AS underperformance_pct,
    alpha,
    beta
FROM dim_schemes
WHERE return_3yr_pct < benchmark_3yr_pct
ORDER BY underperformance_pct ASC;
```

### Results
| amfi_code   | scheme_name   | category   | return_3yr_pct   | benchmark_3yr_pct   | underperformance_pct   | alpha   | beta   |
|-------------|---------------|------------|------------------|---------------------|------------------------|---------|--------|

---

## Query 4: Geographic Investment Distribution by State and City Tier
*Analyzes where the capital is flowing from, including average ticket size.*

### SQL Query
```sql
-- EXPLAIN: Joins transaction facts with dim_investors to show geographic contribution.
SELECT
    i.state,
    i.city_tier,
    COUNT(t.transaction_id) AS transaction_count,
    SUM(t.amount_inr) AS total_amount_inr,
    ROUND(AVG(t.amount_inr), 2) AS avg_transaction_amount_inr
FROM fact_transactions t
JOIN dim_investors i ON t.investor_id = i.investor_id
GROUP BY i.state, i.city_tier
ORDER BY total_amount_inr DESC;
```

### Results
| state          | city_tier   |   transaction_count |   total_amount_inr |   avg_transaction_amount_inr |
|:---------------|:------------|--------------------:|-------------------:|-----------------------------:|
| Gujarat        | T30         |                2780 |        2.98359e+08 |                     107323   |
| West Bengal    | T30         |                2748 |        2.97183e+08 |                     108145   |
| Telangana      | T30         |                2718 |        2.90219e+08 |                     106777   |
| Delhi          | T30         |                2677 |        2.89633e+08 |                     108193   |
| Uttar Pradesh  | B30         |                1777 |        1.92275e+08 |                     108202   |
| Maharashtra    | T30         |                1774 |        1.88947e+08 |                     106509   |
| Tamil Nadu     | B30         |                1478 |        1.70345e+08 |                     115254   |
| Madhya Pradesh | B30         |                1533 |        1.65606e+08 |                     108028   |
| Punjab         | B30         |                1528 |        1.59316e+08 |                     104264   |
| Punjab         | T30         |                1437 |        1.56465e+08 |                     108883   |
| Rajasthan      | T30         |                1354 |        1.53769e+08 |                     113566   |
| Haryana        | B30         |                1483 |        1.48078e+08 |                      99850.3 |
| Rajasthan      | B30         |                1223 |        1.44877e+08 |                     118460   |
| Tamil Nadu     | T30         |                1328 |        1.44832e+08 |                     109060   |
| Madhya Pradesh | T30         |                1398 |        1.42706e+08 |                     102079   |
| Karnataka      | B30         |                1287 |        1.41261e+08 |                     109760   |
| Karnataka      | T30         |                1334 |        1.32492e+08 |                      99319.5 |
| Haryana        | T30         |                1253 |        1.31556e+08 |                     104993   |
| Uttar Pradesh  | T30         |                 918 |        9.30938e+07 |                     101409   |
| Maharashtra    | B30         |                 750 |        8.05668e+07 |                     107422   |

---

## Query 5: Monthly Inflow Trends (SIP vs Lumpsum vs Redemption Counts & Volumes)
*Identifies seasonal trends and transaction behavior over time.*

### SQL Query
```sql
-- EXPLAIN: Utilizes shared dim_dates to aggregate facts month-over-month.
SELECT
    d.year,
    d.month,
    SUM(CASE WHEN t.transaction_type = 'SIP' THEN 1 ELSE 0 END) AS sip_count,
    SUM(CASE WHEN t.transaction_type = 'SIP' THEN t.amount_inr ELSE 0 END) AS sip_volume_inr,
    SUM(CASE WHEN t.transaction_type = 'Lumpsum' THEN 1 ELSE 0 END) AS lumpsum_count,
    SUM(CASE WHEN t.transaction_type = 'Lumpsum' THEN t.amount_inr ELSE 0 END) AS lumpsum_volume_inr,
    SUM(CASE WHEN t.transaction_type = 'Redemption' THEN 1 ELSE 0 END) AS redemption_count,
    SUM(CASE WHEN t.transaction_type = 'Redemption' THEN t.amount_inr ELSE 0 END) AS redemption_volume_inr
FROM fact_transactions t
JOIN dim_dates d ON t.transaction_date = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;
```

### Results
|   year |   month |   sip_count |   sip_volume_inr |   lumpsum_count |   lumpsum_volume_inr |   redemption_count |   redemption_volume_inr |
|-------:|--------:|------------:|-----------------:|----------------:|---------------------:|-------------------:|------------------------:|
|   2024 |       1 |        1146 |      1.26353e+07 |             492 |          1.2551e+08  |                311 |             7.95031e+07 |
|   2024 |       2 |        1154 |      1.26134e+07 |             439 |          1.11404e+08 |                268 |             6.9872e+07  |
|   2024 |       3 |        1177 |      1.20884e+07 |             498 |          1.2481e+08  |                299 |             7.6555e+07  |
|   2024 |       4 |        1186 |      1.35124e+07 |             484 |          1.27546e+08 |                282 |             6.74459e+07 |
|   2024 |       5 |        1155 |      1.32186e+07 |             438 |          1.1467e+08  |                308 |             7.72378e+07 |
|   2024 |       6 |        1155 |      1.31312e+07 |             494 |          1.24986e+08 |                340 |             8.41486e+07 |
|   2024 |       7 |        1235 |      1.35139e+07 |             465 |          1.17142e+08 |                268 |             6.70757e+07 |
|   2024 |       8 |        1154 |      1.25214e+07 |             511 |          1.34046e+08 |                320 |             8.12372e+07 |
|   2024 |       9 |        1142 |      1.22888e+07 |             447 |          1.13775e+08 |                244 |             6.24979e+07 |
|   2024 |      10 |        1167 |      1.24679e+07 |             503 |          1.27248e+08 |                287 |             7.39353e+07 |
|   2024 |      11 |        1108 |      1.23217e+07 |             473 |          1.14655e+08 |                282 |             6.99538e+07 |
|   2024 |      12 |        1179 |      1.29201e+07 |             521 |          1.31321e+08 |                278 |             7.08246e+07 |
|   2025 |       1 |        1234 |      1.30821e+07 |             472 |          1.18291e+08 |                314 |             7.52713e+07 |
|   2025 |       2 |        1041 |      1.13639e+07 |             445 |          1.06738e+08 |                268 |             6.48219e+07 |
|   2025 |       3 |        1196 |      1.34494e+07 |             466 |          1.28036e+08 |                311 |             7.81824e+07 |
|   2025 |       4 |        1086 |      1.2132e+07  |             473 |          1.19571e+08 |                300 |             7.63548e+07 |
|   2025 |       5 |        1201 |      1.3973e+07  |             474 |          1.20073e+08 |                287 |             6.96082e+07 |

---

## Query 6: Demographic Profiling (Age Group and Gender Investment Behaviors)
*Analyzes unique investor counts and ticket sizes by cohort.*

### SQL Query
```sql
-- EXPLAIN: Combines transaction values and unique investor counts across demographics.
SELECT
    i.age_group,
    i.gender,
    COUNT(DISTINCT t.investor_id) AS unique_investor_count,
    COUNT(t.transaction_id) AS total_transaction_count,
    SUM(t.amount_inr) AS total_amount_inr,
    ROUND(SUM(t.amount_inr) * 1.0 / COUNT(t.transaction_id), 2) AS avg_ticket_size_inr
FROM fact_transactions t
JOIN dim_investors i ON t.investor_id = i.investor_id
GROUP BY i.age_group, i.gender
ORDER BY i.age_group, i.gender;
```

### Results
| age_group   | gender   |   unique_investor_count |   total_transaction_count |   total_amount_inr |   avg_ticket_size_inr |
|:------------|:---------|------------------------:|--------------------------:|-------------------:|----------------------:|
| 18-25       | Female   |                     251 |                      1722 |        1.86667e+08 |                108401 |
| 18-25       | Male     |                     502 |                      3194 |        3.44972e+08 |                108006 |
| 26-35       | Female   |                     664 |                      4379 |        4.6516e+08  |                106225 |
| 26-35       | Male     |                    1369 |                      9084 |        9.8644e+08  |                108591 |
| 36-45       | Female   |                     413 |                      2705 |        2.93392e+08 |                108463 |
| 36-45       | Male     |                     824 |                      5441 |        5.78255e+08 |                106277 |
| 46-55       | Female   |                     200 |                      1270 |        1.40315e+08 |                110484 |
| 46-55       | Male     |                     389 |                      2509 |        2.65092e+08 |                105656 |
| 56+         | Female   |                     135 |                       893 |        9.08124e+07 |                101694 |
| 56+         | Male     |                     253 |                      1581 |        1.70474e+08 |                107827 |

---

## Query 7: Income Bracket Correlation with Transaction Sizes
*Groups investors into annual income brackets to observe ticket size variances.*

### SQL Query
```sql
-- EXPLAIN: Bins continuous income figures using a CTE, then runs aggregates.
WITH binned_income AS (
    SELECT
        CASE
            WHEN annual_income_lakh < 10 THEN '1. 0-10 Lakh'
            WHEN annual_income_lakh >= 10 AND annual_income_lakh < 25 THEN '2. 10-25 Lakh'
            WHEN annual_income_lakh >= 25 AND annual_income_lakh < 50 THEN '3. 25-50 Lakh'
            WHEN annual_income_lakh >= 50 AND annual_income_lakh < 75 THEN '4. 50-75 Lakh'
            ELSE '5. 75+ Lakh'
        END AS income_bracket,
        t.amount_inr
    FROM fact_transactions t
    JOIN dim_investors i ON t.investor_id = i.investor_id
)
SELECT
    income_bracket,
    COUNT(*) AS transaction_count,
    SUM(amount_inr) AS total_amount_inr,
    ROUND(AVG(amount_inr), 2) AS avg_transaction_amount_inr
FROM binned_income
GROUP BY income_bracket
ORDER BY income_bracket;
```

### Results
| income_bracket   |   transaction_count |   total_amount_inr |   avg_transaction_amount_inr |
|:-----------------|--------------------:|-------------------:|-----------------------------:|
| 1. 0-10 Lakh     |                7699 |        8.25711e+08 |                       107249 |
| 2. 10-25 Lakh    |               13757 |        1.48545e+09 |                       107977 |
| 3. 25-50 Lakh    |                6341 |        6.85637e+08 |                       108128 |
| 4. 50-75 Lakh    |                3602 |        3.8361e+08  |                       106499 |
| 5. 75+ Lakh      |                1379 |        1.41176e+08 |                       102375 |

---

## Query 8: Payment Mode Preferences by City Tier
*Displays distribution and share of payment methods in Top-30 vs Beyond-30 cities.*

### SQL Query
```sql
-- EXPLAIN: Grouping by tier and payment mode with window SUM to calculate percentages.
WITH tier_totals AS (
    SELECT
        i.city_tier,
        t.payment_mode,
        COUNT(t.transaction_id) AS transaction_count,
        SUM(t.amount_inr) AS total_amount_inr
    FROM fact_transactions t
    JOIN dim_investors i ON t.investor_id = i.investor_id
    GROUP BY i.city_tier, t.payment_mode
)
SELECT
    city_tier,
    payment_mode,
    transaction_count,
    total_amount_inr,
    ROUND(transaction_count * 100.0 / SUM(transaction_count) OVER(PARTITION BY city_tier), 2) AS tier_share_pct
FROM tier_totals
ORDER BY city_tier, transaction_count DESC;
```

### Results
| city_tier   | payment_mode   |   transaction_count |   total_amount_inr |   tier_share_pct |
|:------------|:---------------|--------------------:|-------------------:|-----------------:|
| B30         | Cheque         |                2809 |        3.03576e+08 |            25.4  |
| B30         | Net Banking    |                2802 |        3.0926e+08  |            25.34 |
| B30         | Mandate        |                2764 |        2.90147e+08 |            24.99 |
| B30         | UPI            |                2684 |        2.99344e+08 |            24.27 |
| T30         | UPI            |                5470 |        5.88897e+08 |            25.19 |
| T30         | Net Banking    |                5448 |        5.84233e+08 |            25.08 |
| T30         | Cheque         |                5419 |        5.88644e+08 |            24.95 |
| T30         | Mandate        |                5382 |        5.57481e+08 |            24.78 |

---

## Query 9: KYC Verification Status vs Investment Activity
*Investigates if KYC status affects transaction counts and investment volumes.*

### SQL Query
```sql
-- EXPLAIN: Aggregates total transactions and ticket size by KYC and transaction type.
SELECT
    t.kyc_status,
    t.transaction_type,
    COUNT(t.transaction_id) AS transaction_count,
    SUM(t.amount_inr) AS total_amount_inr,
    ROUND(AVG(t.amount_inr), 2) AS avg_amount_inr
FROM fact_transactions t
GROUP BY t.kyc_status, t.transaction_type
ORDER BY t.kyc_status, transaction_count DESC;
```

### Results
| kyc_status   | transaction_type   |   transaction_count |   total_amount_inr |   avg_amount_inr |
|:-------------|:-------------------|--------------------:|-------------------:|-----------------:|
| Pending      | SIP                |                1585 |        1.76262e+07 |          11120.6 |
| Pending      | Lumpsum            |                 669 |        1.76362e+08 |         263620   |
| Pending      | Redemption         |                 378 |        9.34199e+07 |         247143   |
| Verified     | SIP                |               18131 |        1.99607e+08 |          11009.2 |
| Verified     | Lumpsum            |                7426 |        1.88346e+09 |         253630   |
| Verified     | Redemption         |                4589 |        1.15111e+09 |         250840   |

---

## Query 10: Top 10 Stock Holdings Across All Portfolios by Market Value
*Integrates scheme facts with scheme portfolio holdings to find biggest positions.*

### SQL Query
```sql
-- EXPLAIN: Joins D1 portfolio_holdings with dim_schemes to find overall exposure.
SELECT
    h.stock_name,
    h.stock_symbol,
    h.sector,
    COUNT(DISTINCT h.amfi_code) AS holding_schemes_count,
    ROUND(SUM(h.market_value_cr), 2) AS total_market_value_cr,
    ROUND(AVG(h.weight_pct), 2) AS avg_weight_pct
FROM `09_portfolio_holdings` h
JOIN dim_schemes s ON h.amfi_code = s.amfi_code
GROUP BY h.stock_name, h.stock_symbol, h.sector
ORDER BY total_market_value_cr DESC
LIMIT 10;
```

### Results
| stock_name              | stock_symbol   | sector      |   holding_schemes_count |   total_market_value_cr |   avg_weight_pct |
|:------------------------|:---------------|:------------|------------------------:|------------------------:|-----------------:|
| Axis Bank Ltd           | AXISBANK       | Banking     |                      12 |                 16325.9 |            12.56 |
| Bharti Airtel Ltd       | BHARTIARTL     | Telecom     |                      15 |                 16051.5 |             9.71 |
| Reliance Industries Ltd | RELIANCE       | Energy      |                      13 |                 15286.5 |             9.07 |
| NTPC Ltd                | NTPC           | Utilities   |                      13 |                 13951.4 |            11.93 |
| Grasim Industries Ltd   | GRASIM         | Diversified |                      14 |                 13897.8 |            12.09 |
| Hindustan Unilever Ltd  | HINDUNILVR     | FMCG        |                      11 |                 12993.9 |            11.44 |
| Mahindra & Mahindra Ltd | M&M            | Automobile  |                      10 |                 12967.3 |            11.03 |
| HCL Technologies Ltd    | HCLTECH        | IT          |                      13 |                 12299.9 |            11.32 |
| Tata Motors Ltd         | TATAMOTOR      | Automobile  |                      12 |                 12296.8 |             9.56 |
| UltraTech Cement Ltd    | ULTRACEMCO     | Cement      |                      12 |                 11612   |             8.75 |

---
