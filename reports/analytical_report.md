# Analytical SQL Report — Bluestock MF Capstone
This report compiles the results of the 10 analytical SQL queries executed on the Star Schema database.

## Query 1: Top 5 Funds by AUM
*Identifies the top 5 funds from fact_performance by their assets under management.*

### SQL Query
```sql
SELECT
    f.amfi_code,
    f.scheme_name,
    p.aum_crore,
    p.morningstar_rating
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
ORDER BY p.aum_crore DESC
LIMIT 5;
```

### Results
|   amfi_code | scheme_name                                           |   aum_crore |   morningstar_rating |
|------------:|:------------------------------------------------------|------------:|---------------------:|
|      148568 | Mirae Asset Emerging Bluechip Fund - Regular - Growth |       49046 |                    5 |
|      120842 | Kotak Emerging Equity Fund - Regular - Growth         |       47469 |                    4 |
|      118634 | Nippon India Small Cap Fund - Regular - Growth        |       43630 |                    4 |
|      149322 | DSP Top 100 Equity Fund - Regular - Growth            |       41828 |                    5 |
|      102886 | UTI Mid Cap Fund - Regular - Growth                   |       41728 |                    5 |

---

## Query 2: Average NAV Per Month for Each Fund
*Calculates the average NAV value per calendar month for each scheme.*

### SQL Query
```sql
SELECT
    f.scheme_name,
    d.year,
    d.month,
    ROUND(AVG(n.nav_value), 4) AS avg_nav_value
FROM fact_nav n
JOIN dim_fund f ON n.amfi_code = f.amfi_code
JOIN dim_date d ON n.nav_date = d.date_id
GROUP BY f.scheme_name, d.year, d.month
ORDER BY f.scheme_name, d.year, d.month;
```

### Results
| scheme_name                                           |   year |   month |   avg_nav_value |
|:------------------------------------------------------|-------:|--------:|----------------:|
| ABSL Frontline Equity Fund - Regular - Growth         |   2022 |       1 |        309.998  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2022 |       2 |        311.278  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2022 |       3 |        306.012  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2022 |       4 |        307.198  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2022 |       5 |        306.249  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2022 |       6 |        315.593  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2022 |       7 |        325.435  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2022 |       8 |        329.515  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2022 |       9 |        320.802  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2022 |      10 |        310.121  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2022 |      11 |        329.758  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2022 |      12 |        341.369  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2023 |       1 |        346.108  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2023 |       2 |        353.315  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2023 |       3 |        350.918  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2023 |       4 |        359.247  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2023 |       5 |        364.095  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2023 |       6 |        339.068  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2023 |       7 |        336.394  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2023 |       8 |        343.64   |
| ABSL Frontline Equity Fund - Regular - Growth         |   2023 |       9 |        356.948  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2023 |      10 |        379.416  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2023 |      11 |        377.372  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2023 |      12 |        384.31   |
| ABSL Frontline Equity Fund - Regular - Growth         |   2024 |       1 |        399.997  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2024 |       2 |        404.595  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2024 |       3 |        421.038  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2024 |       4 |        409.82   |
| ABSL Frontline Equity Fund - Regular - Growth         |   2024 |       5 |        436.248  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2024 |       6 |        445.733  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2024 |       7 |        432.82   |
| ABSL Frontline Equity Fund - Regular - Growth         |   2024 |       8 |        421.551  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2024 |       9 |        435.042  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2024 |      10 |        426.489  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2024 |      11 |        449.214  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2024 |      12 |        457.695  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2025 |       1 |        461.872  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2025 |       2 |        456.291  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2025 |       3 |        485.588  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2025 |       4 |        492.142  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2025 |       5 |        519.361  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2025 |       6 |        528.301  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2025 |       7 |        535.556  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2025 |       8 |        566.847  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2025 |       9 |        569.527  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2025 |      10 |        574.201  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2025 |      11 |        573.997  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2025 |      12 |        561.645  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2026 |       1 |        594.178  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2026 |       2 |        659.706  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2026 |       3 |        733.198  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2026 |       4 |        771.602  |
| ABSL Frontline Equity Fund - Regular - Growth         |   2026 |       5 |        780.474  |
| ABSL Liquid Fund - Regular - Growth                   |   2022 |       1 |        311.679  |
| ABSL Liquid Fund - Regular - Growth                   |   2022 |       2 |        313.718  |
| ABSL Liquid Fund - Regular - Growth                   |   2022 |       3 |        315.966  |
| ABSL Liquid Fund - Regular - Growth                   |   2022 |       4 |        317.608  |
| ABSL Liquid Fund - Regular - Growth                   |   2022 |       5 |        319.223  |
| ABSL Liquid Fund - Regular - Growth                   |   2022 |       6 |        320.079  |
| ABSL Liquid Fund - Regular - Growth                   |   2022 |       7 |        321.894  |
| ABSL Liquid Fund - Regular - Growth                   |   2022 |       8 |        324.045  |
| ABSL Liquid Fund - Regular - Growth                   |   2022 |       9 |        325.659  |
| ABSL Liquid Fund - Regular - Growth                   |   2022 |      10 |        327.642  |
| ABSL Liquid Fund - Regular - Growth                   |   2022 |      11 |        329.461  |
| ABSL Liquid Fund - Regular - Growth                   |   2022 |      12 |        331.765  |
| ABSL Liquid Fund - Regular - Growth                   |   2023 |       1 |        334.052  |
| ABSL Liquid Fund - Regular - Growth                   |   2023 |       2 |        335.916  |
| ABSL Liquid Fund - Regular - Growth                   |   2023 |       3 |        337.348  |
| ABSL Liquid Fund - Regular - Growth                   |   2023 |       4 |        338.647  |
| ABSL Liquid Fund - Regular - Growth                   |   2023 |       5 |        340.472  |
| ABSL Liquid Fund - Regular - Growth                   |   2023 |       6 |        342.319  |
| ABSL Liquid Fund - Regular - Growth                   |   2023 |       7 |        344.21   |
| ABSL Liquid Fund - Regular - Growth                   |   2023 |       8 |        346.133  |
| ABSL Liquid Fund - Regular - Growth                   |   2023 |       9 |        346.906  |
| ABSL Liquid Fund - Regular - Growth                   |   2023 |      10 |        348.625  |
| ABSL Liquid Fund - Regular - Growth                   |   2023 |      11 |        350.639  |
| ABSL Liquid Fund - Regular - Growth                   |   2023 |      12 |        352.762  |
| ABSL Liquid Fund - Regular - Growth                   |   2024 |       1 |        354.836  |
| ABSL Liquid Fund - Regular - Growth                   |   2024 |       2 |        356.124  |
| ABSL Liquid Fund - Regular - Growth                   |   2024 |       3 |        358.551  |
| ABSL Liquid Fund - Regular - Growth                   |   2024 |       4 |        360.234  |
| ABSL Liquid Fund - Regular - Growth                   |   2024 |       5 |        361.59   |
| ABSL Liquid Fund - Regular - Growth                   |   2024 |       6 |        363.639  |
| ABSL Liquid Fund - Regular - Growth                   |   2024 |       7 |        365.408  |
| ABSL Liquid Fund - Regular - Growth                   |   2024 |       8 |        366.59   |
| ABSL Liquid Fund - Regular - Growth                   |   2024 |       9 |        368.196  |
| ABSL Liquid Fund - Regular - Growth                   |   2024 |      10 |        370.105  |
| ABSL Liquid Fund - Regular - Growth                   |   2024 |      11 |        372.035  |
| ABSL Liquid Fund - Regular - Growth                   |   2024 |      12 |        373.817  |
| ABSL Liquid Fund - Regular - Growth                   |   2025 |       1 |        375.49   |
| ABSL Liquid Fund - Regular - Growth                   |   2025 |       2 |        377.144  |
| ABSL Liquid Fund - Regular - Growth                   |   2025 |       3 |        378.777  |
| ABSL Liquid Fund - Regular - Growth                   |   2025 |       4 |        379.863  |
| ABSL Liquid Fund - Regular - Growth                   |   2025 |       5 |        381.656  |
| ABSL Liquid Fund - Regular - Growth                   |   2025 |       6 |        383.764  |
| ABSL Liquid Fund - Regular - Growth                   |   2025 |       7 |        385.55   |
| ABSL Liquid Fund - Regular - Growth                   |   2025 |       8 |        387.604  |
| ABSL Liquid Fund - Regular - Growth                   |   2025 |       9 |        389.732  |
| ABSL Liquid Fund - Regular - Growth                   |   2025 |      10 |        391.935  |
| ABSL Liquid Fund - Regular - Growth                   |   2025 |      11 |        394.757  |
| ABSL Liquid Fund - Regular - Growth                   |   2025 |      12 |        397.544  |
| ABSL Liquid Fund - Regular - Growth                   |   2026 |       1 |        399.842  |
| ABSL Liquid Fund - Regular - Growth                   |   2026 |       2 |        402.111  |
| ABSL Liquid Fund - Regular - Growth                   |   2026 |       3 |        404.473  |
| ABSL Liquid Fund - Regular - Growth                   |   2026 |       4 |        406.435  |
| ABSL Liquid Fund - Regular - Growth                   |   2026 |       5 |        408.829  |
| ABSL Small Cap Fund - Regular - Growth                |   2022 |       1 |         38.7224 |
| ABSL Small Cap Fund - Regular - Growth                |   2022 |       2 |         39.6213 |
| ABSL Small Cap Fund - Regular - Growth                |   2022 |       3 |         40.2075 |
| ABSL Small Cap Fund - Regular - Growth                |   2022 |       4 |         42.7833 |
| ABSL Small Cap Fund - Regular - Growth                |   2022 |       5 |         40.4933 |
| ABSL Small Cap Fund - Regular - Growth                |   2022 |       6 |         39.0659 |
| ABSL Small Cap Fund - Regular - Growth                |   2022 |       7 |         43.8419 |
| ABSL Small Cap Fund - Regular - Growth                |   2022 |       8 |         48.2908 |
| ABSL Small Cap Fund - Regular - Growth                |   2022 |       9 |         51.7697 |
| ABSL Small Cap Fund - Regular - Growth                |   2022 |      10 |         56.162  |
| ABSL Small Cap Fund - Regular - Growth                |   2022 |      11 |         51.259  |
| ABSL Small Cap Fund - Regular - Growth                |   2022 |      12 |         50.5852 |
| ABSL Small Cap Fund - Regular - Growth                |   2023 |       1 |         52.2434 |
| ABSL Small Cap Fund - Regular - Growth                |   2023 |       2 |         53.0568 |
| ABSL Small Cap Fund - Regular - Growth                |   2023 |       3 |         56.7666 |
| ABSL Small Cap Fund - Regular - Growth                |   2023 |       4 |         54.2032 |
| ABSL Small Cap Fund - Regular - Growth                |   2023 |       5 |         59.4111 |
| ABSL Small Cap Fund - Regular - Growth                |   2023 |       6 |         59.9523 |
| ABSL Small Cap Fund - Regular - Growth                |   2023 |       7 |         60.8845 |
| ABSL Small Cap Fund - Regular - Growth                |   2023 |       8 |         60.6729 |
| ABSL Small Cap Fund - Regular - Growth                |   2023 |       9 |         56.9123 |
| ABSL Small Cap Fund - Regular - Growth                |   2023 |      10 |         57.4946 |
| ABSL Small Cap Fund - Regular - Growth                |   2023 |      11 |         56.5507 |
| ABSL Small Cap Fund - Regular - Growth                |   2023 |      12 |         59.6065 |
| ABSL Small Cap Fund - Regular - Growth                |   2024 |       1 |         58.8467 |
| ABSL Small Cap Fund - Regular - Growth                |   2024 |       2 |         58.0863 |
| ABSL Small Cap Fund - Regular - Growth                |   2024 |       3 |         61.4654 |
| ABSL Small Cap Fund - Regular - Growth                |   2024 |       4 |         60.0773 |
| ABSL Small Cap Fund - Regular - Growth                |   2024 |       5 |         67.1393 |
| ABSL Small Cap Fund - Regular - Growth                |   2024 |       6 |         65.8938 |
| ABSL Small Cap Fund - Regular - Growth                |   2024 |       7 |         62.8803 |
| ABSL Small Cap Fund - Regular - Growth                |   2024 |       8 |         60.4545 |
| ABSL Small Cap Fund - Regular - Growth                |   2024 |       9 |         64.8549 |
| ABSL Small Cap Fund - Regular - Growth                |   2024 |      10 |         71.1481 |
| ABSL Small Cap Fund - Regular - Growth                |   2024 |      11 |         77.3559 |
| ABSL Small Cap Fund - Regular - Growth                |   2024 |      12 |         71.8948 |
| ABSL Small Cap Fund - Regular - Growth                |   2025 |       1 |         72.031  |
| ABSL Small Cap Fund - Regular - Growth                |   2025 |       2 |         77.0485 |
| ABSL Small Cap Fund - Regular - Growth                |   2025 |       3 |         74.4197 |
| ABSL Small Cap Fund - Regular - Growth                |   2025 |       4 |         71.5333 |
| ABSL Small Cap Fund - Regular - Growth                |   2025 |       5 |         73.5543 |
| ABSL Small Cap Fund - Regular - Growth                |   2025 |       6 |         71.0492 |
| ABSL Small Cap Fund - Regular - Growth                |   2025 |       7 |         65.2818 |
| ABSL Small Cap Fund - Regular - Growth                |   2025 |       8 |         64.3806 |
| ABSL Small Cap Fund - Regular - Growth                |   2025 |       9 |         61.9497 |
| ABSL Small Cap Fund - Regular - Growth                |   2025 |      10 |         60.4472 |
| ABSL Small Cap Fund - Regular - Growth                |   2025 |      11 |         64.5792 |
| ABSL Small Cap Fund - Regular - Growth                |   2025 |      12 |         65.487  |
| ABSL Small Cap Fund - Regular - Growth                |   2026 |       1 |         63.9546 |
| ABSL Small Cap Fund - Regular - Growth                |   2026 |       2 |         59.0096 |
| ABSL Small Cap Fund - Regular - Growth                |   2026 |       3 |         59.3687 |
| ABSL Small Cap Fund - Regular - Growth                |   2026 |       4 |         55.6294 |
| ABSL Small Cap Fund - Regular - Growth                |   2026 |       5 |         53.1598 |
| Axis Bluechip Fund - Direct - Growth                  |   2022 |       1 |         40.4955 |
| Axis Bluechip Fund - Direct - Growth                  |   2022 |       2 |         41.014  |
| Axis Bluechip Fund - Direct - Growth                  |   2022 |       3 |         39.7123 |
| Axis Bluechip Fund - Direct - Growth                  |   2022 |       4 |         39.2449 |
| Axis Bluechip Fund - Direct - Growth                  |   2022 |       5 |         37.9619 |
| Axis Bluechip Fund - Direct - Growth                  |   2022 |       6 |         38.3315 |
| Axis Bluechip Fund - Direct - Growth                  |   2022 |       7 |         35.9974 |
| Axis Bluechip Fund - Direct - Growth                  |   2022 |       8 |         35.8062 |
| Axis Bluechip Fund - Direct - Growth                  |   2022 |       9 |         37.0165 |
| Axis Bluechip Fund - Direct - Growth                  |   2022 |      10 |         36.4006 |
| Axis Bluechip Fund - Direct - Growth                  |   2022 |      11 |         36.4243 |
| Axis Bluechip Fund - Direct - Growth                  |   2022 |      12 |         35.5248 |
| Axis Bluechip Fund - Direct - Growth                  |   2023 |       1 |         35.3616 |
| Axis Bluechip Fund - Direct - Growth                  |   2023 |       2 |         34.7661 |
| Axis Bluechip Fund - Direct - Growth                  |   2023 |       3 |         34.7288 |
| Axis Bluechip Fund - Direct - Growth                  |   2023 |       4 |         34.9314 |
| Axis Bluechip Fund - Direct - Growth                  |   2023 |       5 |         33.6343 |
| Axis Bluechip Fund - Direct - Growth                  |   2023 |       6 |         33.7558 |
| Axis Bluechip Fund - Direct - Growth                  |   2023 |       7 |         34.2177 |
| Axis Bluechip Fund - Direct - Growth                  |   2023 |       8 |         35.8786 |
| Axis Bluechip Fund - Direct - Growth                  |   2023 |       9 |         38.5882 |
| Axis Bluechip Fund - Direct - Growth                  |   2023 |      10 |         38.0376 |
| Axis Bluechip Fund - Direct - Growth                  |   2023 |      11 |         38.6733 |
| Axis Bluechip Fund - Direct - Growth                  |   2023 |      12 |         40.9998 |
| Axis Bluechip Fund - Direct - Growth                  |   2024 |       1 |         42.0692 |
| Axis Bluechip Fund - Direct - Growth                  |   2024 |       2 |         42.9556 |
| Axis Bluechip Fund - Direct - Growth                  |   2024 |       3 |         44.6395 |
| Axis Bluechip Fund - Direct - Growth                  |   2024 |       4 |         45.5719 |
| Axis Bluechip Fund - Direct - Growth                  |   2024 |       5 |         45.7445 |
| Axis Bluechip Fund - Direct - Growth                  |   2024 |       6 |         47.8085 |
| Axis Bluechip Fund - Direct - Growth                  |   2024 |       7 |         45.9378 |
| Axis Bluechip Fund - Direct - Growth                  |   2024 |       8 |         45.8986 |
| Axis Bluechip Fund - Direct - Growth                  |   2024 |       9 |         47.517  |
| Axis Bluechip Fund - Direct - Growth                  |   2024 |      10 |         48.5079 |
| Axis Bluechip Fund - Direct - Growth                  |   2024 |      11 |         48.1009 |
| Axis Bluechip Fund - Direct - Growth                  |   2024 |      12 |         47.3882 |
| Axis Bluechip Fund - Direct - Growth                  |   2025 |       1 |         45.4268 |
| Axis Bluechip Fund - Direct - Growth                  |   2025 |       2 |         45.8292 |
| Axis Bluechip Fund - Direct - Growth                  |   2025 |       3 |         49.767  |
| Axis Bluechip Fund - Direct - Growth                  |   2025 |       4 |         48.2386 |
| Axis Bluechip Fund - Direct - Growth                  |   2025 |       5 |         47.9401 |
| Axis Bluechip Fund - Direct - Growth                  |   2025 |       6 |         49.8289 |
| Axis Bluechip Fund - Direct - Growth                  |   2025 |       7 |         51.0903 |
| Axis Bluechip Fund - Direct - Growth                  |   2025 |       8 |         53.6958 |
| Axis Bluechip Fund - Direct - Growth                  |   2025 |       9 |         53.1544 |
| Axis Bluechip Fund - Direct - Growth                  |   2025 |      10 |         52.9139 |
| Axis Bluechip Fund - Direct - Growth                  |   2025 |      11 |         56.1586 |
| Axis Bluechip Fund - Direct - Growth                  |   2025 |      12 |         57.7009 |
| Axis Bluechip Fund - Direct - Growth                  |   2026 |       1 |         55.5213 |
| Axis Bluechip Fund - Direct - Growth                  |   2026 |       2 |         52.4642 |
| Axis Bluechip Fund - Direct - Growth                  |   2026 |       3 |         51.4375 |
| Axis Bluechip Fund - Direct - Growth                  |   2026 |       4 |         52.8938 |
| Axis Bluechip Fund - Direct - Growth                  |   2026 |       5 |         56.1706 |
| Axis Bluechip Fund - Regular - Growth                 |   2022 |       1 |         38.9021 |
| Axis Bluechip Fund - Regular - Growth                 |   2022 |       2 |         39.8856 |
| Axis Bluechip Fund - Regular - Growth                 |   2022 |       3 |         38.1884 |
| Axis Bluechip Fund - Regular - Growth                 |   2022 |       4 |         36.0476 |
| Axis Bluechip Fund - Regular - Growth                 |   2022 |       5 |         36.2173 |
| Axis Bluechip Fund - Regular - Growth                 |   2022 |       6 |         36.916  |
| Axis Bluechip Fund - Regular - Growth                 |   2022 |       7 |         37.6962 |
| Axis Bluechip Fund - Regular - Growth                 |   2022 |       8 |         38.3575 |
| Axis Bluechip Fund - Regular - Growth                 |   2022 |       9 |         39.8699 |
| Axis Bluechip Fund - Regular - Growth                 |   2022 |      10 |         42.7173 |
| Axis Bluechip Fund - Regular - Growth                 |   2022 |      11 |         44.4971 |
| Axis Bluechip Fund - Regular - Growth                 |   2022 |      12 |         45.9983 |
| Axis Bluechip Fund - Regular - Growth                 |   2023 |       1 |         46.3405 |
| Axis Bluechip Fund - Regular - Growth                 |   2023 |       2 |         46.6976 |
| Axis Bluechip Fund - Regular - Growth                 |   2023 |       3 |         46.2791 |
| Axis Bluechip Fund - Regular - Growth                 |   2023 |       4 |         47.7005 |
| Axis Bluechip Fund - Regular - Growth                 |   2023 |       5 |         49.3689 |
| Axis Bluechip Fund - Regular - Growth                 |   2023 |       6 |         49.2557 |
| Axis Bluechip Fund - Regular - Growth                 |   2023 |       7 |         50.6077 |
| Axis Bluechip Fund - Regular - Growth                 |   2023 |       8 |         51.5629 |
| Axis Bluechip Fund - Regular - Growth                 |   2023 |       9 |         52.2384 |
| Axis Bluechip Fund - Regular - Growth                 |   2023 |      10 |         53.5109 |
| Axis Bluechip Fund - Regular - Growth                 |   2023 |      11 |         52.3471 |
| Axis Bluechip Fund - Regular - Growth                 |   2023 |      12 |         52.4784 |
| Axis Bluechip Fund - Regular - Growth                 |   2024 |       1 |         51.8068 |
| Axis Bluechip Fund - Regular - Growth                 |   2024 |       2 |         50.7087 |
| Axis Bluechip Fund - Regular - Growth                 |   2024 |       3 |         50.9949 |
| Axis Bluechip Fund - Regular - Growth                 |   2024 |       4 |         50.449  |
| Axis Bluechip Fund - Regular - Growth                 |   2024 |       5 |         49.7615 |
| Axis Bluechip Fund - Regular - Growth                 |   2024 |       6 |         49.5245 |
| Axis Bluechip Fund - Regular - Growth                 |   2024 |       7 |         50.4606 |
| Axis Bluechip Fund - Regular - Growth                 |   2024 |       8 |         50.2716 |
| Axis Bluechip Fund - Regular - Growth                 |   2024 |       9 |         49.5088 |
| Axis Bluechip Fund - Regular - Growth                 |   2024 |      10 |         50.7253 |
| Axis Bluechip Fund - Regular - Growth                 |   2024 |      11 |         50.0767 |
| Axis Bluechip Fund - Regular - Growth                 |   2024 |      12 |         48.4574 |
| Axis Bluechip Fund - Regular - Growth                 |   2025 |       1 |         48.9126 |
| Axis Bluechip Fund - Regular - Growth                 |   2025 |       2 |         48.3892 |
| Axis Bluechip Fund - Regular - Growth                 |   2025 |       3 |         48.3251 |
| Axis Bluechip Fund - Regular - Growth                 |   2025 |       4 |         47.6311 |
| Axis Bluechip Fund - Regular - Growth                 |   2025 |       5 |         50.0844 |
| Axis Bluechip Fund - Regular - Growth                 |   2025 |       6 |         49.798  |
| Axis Bluechip Fund - Regular - Growth                 |   2025 |       7 |         51.397  |
| Axis Bluechip Fund - Regular - Growth                 |   2025 |       8 |         52.1869 |
| Axis Bluechip Fund - Regular - Growth                 |   2025 |       9 |         50.0357 |
| Axis Bluechip Fund - Regular - Growth                 |   2025 |      10 |         51.5654 |
| Axis Bluechip Fund - Regular - Growth                 |   2025 |      11 |         51.9512 |
| Axis Bluechip Fund - Regular - Growth                 |   2025 |      12 |         53.3357 |
| Axis Bluechip Fund - Regular - Growth                 |   2026 |       1 |         55.6395 |
| Axis Bluechip Fund - Regular - Growth                 |   2026 |       2 |         55.0476 |
| Axis Bluechip Fund - Regular - Growth                 |   2026 |       3 |         51.4386 |
| Axis Bluechip Fund - Regular - Growth                 |   2026 |       4 |         51.8856 |
| Axis Bluechip Fund - Regular - Growth                 |   2026 |       5 |         50.7831 |
| Axis Midcap Fund - Regular - Growth                   |   2022 |       1 |         67.4752 |
| Axis Midcap Fund - Regular - Growth                   |   2022 |       2 |         70.066  |
| Axis Midcap Fund - Regular - Growth                   |   2022 |       3 |         72.7894 |
| Axis Midcap Fund - Regular - Growth                   |   2022 |       4 |         74.0708 |
| Axis Midcap Fund - Regular - Growth                   |   2022 |       5 |         72.0758 |
| Axis Midcap Fund - Regular - Growth                   |   2022 |       6 |         66.6196 |
| Axis Midcap Fund - Regular - Growth                   |   2022 |       7 |         65.5541 |
| Axis Midcap Fund - Regular - Growth                   |   2022 |       8 |         64.7301 |
| Axis Midcap Fund - Regular - Growth                   |   2022 |       9 |         67.8715 |
| Axis Midcap Fund - Regular - Growth                   |   2022 |      10 |         66.3177 |
| Axis Midcap Fund - Regular - Growth                   |   2022 |      11 |         69.5192 |
| Axis Midcap Fund - Regular - Growth                   |   2022 |      12 |         71.866  |
| Axis Midcap Fund - Regular - Growth                   |   2023 |       1 |         77.8484 |
| Axis Midcap Fund - Regular - Growth                   |   2023 |       2 |         82.3499 |
| Axis Midcap Fund - Regular - Growth                   |   2023 |       3 |         84.2842 |
| Axis Midcap Fund - Regular - Growth                   |   2023 |       4 |         85.8858 |
| Axis Midcap Fund - Regular - Growth                   |   2023 |       5 |         83.5645 |
| Axis Midcap Fund - Regular - Growth                   |   2023 |       6 |         80.2767 |
| Axis Midcap Fund - Regular - Growth                   |   2023 |       7 |         82.6122 |
| Axis Midcap Fund - Regular - Growth                   |   2023 |       8 |         87.0227 |
| Axis Midcap Fund - Regular - Growth                   |   2023 |       9 |         91.5658 |
| Axis Midcap Fund - Regular - Growth                   |   2023 |      10 |         99.9199 |
| Axis Midcap Fund - Regular - Growth                   |   2023 |      11 |        105.688  |
| Axis Midcap Fund - Regular - Growth                   |   2023 |      12 |        104.588  |
| Axis Midcap Fund - Regular - Growth                   |   2024 |       1 |        104.319  |
| Axis Midcap Fund - Regular - Growth                   |   2024 |       2 |        101.407  |
| Axis Midcap Fund - Regular - Growth                   |   2024 |       3 |        104.253  |
| Axis Midcap Fund - Regular - Growth                   |   2024 |       4 |        111.037  |
| Axis Midcap Fund - Regular - Growth                   |   2024 |       5 |        117.611  |
| Axis Midcap Fund - Regular - Growth                   |   2024 |       6 |        117.205  |
| Axis Midcap Fund - Regular - Growth                   |   2024 |       7 |        125.348  |
| Axis Midcap Fund - Regular - Growth                   |   2024 |       8 |        133.009  |
| Axis Midcap Fund - Regular - Growth                   |   2024 |       9 |        134.259  |
| Axis Midcap Fund - Regular - Growth                   |   2024 |      10 |        138.588  |
| Axis Midcap Fund - Regular - Growth                   |   2024 |      11 |        159.099  |
| Axis Midcap Fund - Regular - Growth                   |   2024 |      12 |        150.897  |
| Axis Midcap Fund - Regular - Growth                   |   2025 |       1 |        154.669  |
| Axis Midcap Fund - Regular - Growth                   |   2025 |       2 |        170.021  |
| Axis Midcap Fund - Regular - Growth                   |   2025 |       3 |        165.033  |
| Axis Midcap Fund - Regular - Growth                   |   2025 |       4 |        157.91   |
| Axis Midcap Fund - Regular - Growth                   |   2025 |       5 |        163.902  |
| Axis Midcap Fund - Regular - Growth                   |   2025 |       6 |        162.549  |
| Axis Midcap Fund - Regular - Growth                   |   2025 |       7 |        164.772  |
| Axis Midcap Fund - Regular - Growth                   |   2025 |       8 |        164.828  |
| Axis Midcap Fund - Regular - Growth                   |   2025 |       9 |        170.955  |
| Axis Midcap Fund - Regular - Growth                   |   2025 |      10 |        187.579  |
| Axis Midcap Fund - Regular - Growth                   |   2025 |      11 |        198.822  |
| Axis Midcap Fund - Regular - Growth                   |   2025 |      12 |        201.654  |
| Axis Midcap Fund - Regular - Growth                   |   2026 |       1 |        190.961  |
| Axis Midcap Fund - Regular - Growth                   |   2026 |       2 |        202.986  |
| Axis Midcap Fund - Regular - Growth                   |   2026 |       3 |        200.558  |
| Axis Midcap Fund - Regular - Growth                   |   2026 |       4 |        193.207  |
| Axis Midcap Fund - Regular - Growth                   |   2026 |       5 |        197.51   |
| Axis Small Cap Fund - Regular - Growth                |   2022 |       1 |         52.715  |
| Axis Small Cap Fund - Regular - Growth                |   2022 |       2 |         49.5339 |
| Axis Small Cap Fund - Regular - Growth                |   2022 |       3 |         52.4921 |
| Axis Small Cap Fund - Regular - Growth                |   2022 |       4 |         53.2788 |
| Axis Small Cap Fund - Regular - Growth                |   2022 |       5 |         58.1126 |
| Axis Small Cap Fund - Regular - Growth                |   2022 |       6 |         65.6451 |
| Axis Small Cap Fund - Regular - Growth                |   2022 |       7 |         75.6721 |
| Axis Small Cap Fund - Regular - Growth                |   2022 |       8 |         71.0264 |
| Axis Small Cap Fund - Regular - Growth                |   2022 |       9 |         74.3854 |
| Axis Small Cap Fund - Regular - Growth                |   2022 |      10 |         77.3488 |
| Axis Small Cap Fund - Regular - Growth                |   2022 |      11 |         74.2752 |
| Axis Small Cap Fund - Regular - Growth                |   2022 |      12 |         74.6317 |
| Axis Small Cap Fund - Regular - Growth                |   2023 |       1 |         78.1176 |
| Axis Small Cap Fund - Regular - Growth                |   2023 |       2 |         79.616  |
| Axis Small Cap Fund - Regular - Growth                |   2023 |       3 |         85.3588 |
| Axis Small Cap Fund - Regular - Growth                |   2023 |       4 |         80.4303 |
| Axis Small Cap Fund - Regular - Growth                |   2023 |       5 |         82.0805 |
| Axis Small Cap Fund - Regular - Growth                |   2023 |       6 |         80.7505 |
| Axis Small Cap Fund - Regular - Growth                |   2023 |       7 |         77.8666 |
| Axis Small Cap Fund - Regular - Growth                |   2023 |       8 |         85.8194 |
| Axis Small Cap Fund - Regular - Growth                |   2023 |       9 |         91.9613 |
| Axis Small Cap Fund - Regular - Growth                |   2023 |      10 |         94.3315 |
| Axis Small Cap Fund - Regular - Growth                |   2023 |      11 |         90.3172 |
| Axis Small Cap Fund - Regular - Growth                |   2023 |      12 |         78.9598 |
| Axis Small Cap Fund - Regular - Growth                |   2024 |       1 |         73.7894 |
| Axis Small Cap Fund - Regular - Growth                |   2024 |       2 |         71.6118 |
| Axis Small Cap Fund - Regular - Growth                |   2024 |       3 |         75.5503 |
| Axis Small Cap Fund - Regular - Growth                |   2024 |       4 |         76.5462 |
| Axis Small Cap Fund - Regular - Growth                |   2024 |       5 |         75.2453 |
| Axis Small Cap Fund - Regular - Growth                |   2024 |       6 |         70.9264 |
| Axis Small Cap Fund - Regular - Growth                |   2024 |       7 |         73.1109 |
| Axis Small Cap Fund - Regular - Growth                |   2024 |       8 |         73.3218 |
| Axis Small Cap Fund - Regular - Growth                |   2024 |       9 |         74.6744 |
| Axis Small Cap Fund - Regular - Growth                |   2024 |      10 |         78.5021 |
| Axis Small Cap Fund - Regular - Growth                |   2024 |      11 |         81.0483 |
| Axis Small Cap Fund - Regular - Growth                |   2024 |      12 |         75.2753 |
| Axis Small Cap Fund - Regular - Growth                |   2025 |       1 |         78.8971 |
| Axis Small Cap Fund - Regular - Growth                |   2025 |       2 |         79.4336 |
| Axis Small Cap Fund - Regular - Growth                |   2025 |       3 |         90.4368 |
| Axis Small Cap Fund - Regular - Growth                |   2025 |       4 |         94.2404 |
| Axis Small Cap Fund - Regular - Growth                |   2025 |       5 |        102.83   |
| Axis Small Cap Fund - Regular - Growth                |   2025 |       6 |         97.2784 |
| Axis Small Cap Fund - Regular - Growth                |   2025 |       7 |         86.7794 |
| Axis Small Cap Fund - Regular - Growth                |   2025 |       8 |         84.9968 |
| Axis Small Cap Fund - Regular - Growth                |   2025 |       9 |         73.6795 |
| Axis Small Cap Fund - Regular - Growth                |   2025 |      10 |         72.4156 |
| Axis Small Cap Fund - Regular - Growth                |   2025 |      11 |         73.0901 |
| Axis Small Cap Fund - Regular - Growth                |   2025 |      12 |         68.908  |
| Axis Small Cap Fund - Regular - Growth                |   2026 |       1 |         66.7387 |
| Axis Small Cap Fund - Regular - Growth                |   2026 |       2 |         66.5923 |
| Axis Small Cap Fund - Regular - Growth                |   2026 |       3 |         67.9901 |
| Axis Small Cap Fund - Regular - Growth                |   2026 |       4 |         64.0152 |
| Axis Small Cap Fund - Regular - Growth                |   2026 |       5 |         54.5126 |
| DSP Midcap Fund - Regular - Growth                    |   2022 |       1 |         79.3253 |
| DSP Midcap Fund - Regular - Growth                    |   2022 |       2 |         81.1739 |
| DSP Midcap Fund - Regular - Growth                    |   2022 |       3 |         79.661  |
| DSP Midcap Fund - Regular - Growth                    |   2022 |       4 |         79.0696 |
| DSP Midcap Fund - Regular - Growth                    |   2022 |       5 |         82.0495 |
| DSP Midcap Fund - Regular - Growth                    |   2022 |       6 |         83.0694 |
| DSP Midcap Fund - Regular - Growth                    |   2022 |       7 |         81.9429 |
| DSP Midcap Fund - Regular - Growth                    |   2022 |       8 |         80.7572 |
| DSP Midcap Fund - Regular - Growth                    |   2022 |       9 |         79.8182 |
| DSP Midcap Fund - Regular - Growth                    |   2022 |      10 |         76.989  |
| DSP Midcap Fund - Regular - Growth                    |   2022 |      11 |         77.7575 |
| DSP Midcap Fund - Regular - Growth                    |   2022 |      12 |         86.1296 |
| DSP Midcap Fund - Regular - Growth                    |   2023 |       1 |         87.8692 |
| DSP Midcap Fund - Regular - Growth                    |   2023 |       2 |         86.5733 |
| DSP Midcap Fund - Regular - Growth                    |   2023 |       3 |         98.0593 |
| DSP Midcap Fund - Regular - Growth                    |   2023 |       4 |        110.264  |
| DSP Midcap Fund - Regular - Growth                    |   2023 |       5 |        117.614  |
| DSP Midcap Fund - Regular - Growth                    |   2023 |       6 |        126.796  |
| DSP Midcap Fund - Regular - Growth                    |   2023 |       7 |        129.666  |
| DSP Midcap Fund - Regular - Growth                    |   2023 |       8 |        137.17   |
| DSP Midcap Fund - Regular - Growth                    |   2023 |       9 |        137.913  |
| DSP Midcap Fund - Regular - Growth                    |   2023 |      10 |        138.503  |
| DSP Midcap Fund - Regular - Growth                    |   2023 |      11 |        134.253  |
| DSP Midcap Fund - Regular - Growth                    |   2023 |      12 |        132.917  |
| DSP Midcap Fund - Regular - Growth                    |   2024 |       1 |        139.593  |
| DSP Midcap Fund - Regular - Growth                    |   2024 |       2 |        142.791  |
| DSP Midcap Fund - Regular - Growth                    |   2024 |       3 |        133.956  |
| DSP Midcap Fund - Regular - Growth                    |   2024 |       4 |        129.861  |
| DSP Midcap Fund - Regular - Growth                    |   2024 |       5 |        125.403  |
| DSP Midcap Fund - Regular - Growth                    |   2024 |       6 |        125.719  |
| DSP Midcap Fund - Regular - Growth                    |   2024 |       7 |        133.492  |
| DSP Midcap Fund - Regular - Growth                    |   2024 |       8 |        151.601  |
| DSP Midcap Fund - Regular - Growth                    |   2024 |       9 |        168.329  |
| DSP Midcap Fund - Regular - Growth                    |   2024 |      10 |        186.398  |
| DSP Midcap Fund - Regular - Growth                    |   2024 |      11 |        193.2    |
| DSP Midcap Fund - Regular - Growth                    |   2024 |      12 |        201.503  |
| DSP Midcap Fund - Regular - Growth                    |   2025 |       1 |        218.309  |
| DSP Midcap Fund - Regular - Growth                    |   2025 |       2 |        211.296  |
| DSP Midcap Fund - Regular - Growth                    |   2025 |       3 |        204.558  |
| DSP Midcap Fund - Regular - Growth                    |   2025 |       4 |        195.135  |
| DSP Midcap Fund - Regular - Growth                    |   2025 |       5 |        198.316  |
| DSP Midcap Fund - Regular - Growth                    |   2025 |       6 |        203.476  |
| DSP Midcap Fund - Regular - Growth                    |   2025 |       7 |        213.537  |
| DSP Midcap Fund - Regular - Growth                    |   2025 |       8 |        219.253  |
| DSP Midcap Fund - Regular - Growth                    |   2025 |       9 |        222.875  |
| DSP Midcap Fund - Regular - Growth                    |   2025 |      10 |        228.189  |
| DSP Midcap Fund - Regular - Growth                    |   2025 |      11 |        241.256  |
| DSP Midcap Fund - Regular - Growth                    |   2025 |      12 |        225.167  |
| DSP Midcap Fund - Regular - Growth                    |   2026 |       1 |        226.202  |
| DSP Midcap Fund - Regular - Growth                    |   2026 |       2 |        245.694  |
| DSP Midcap Fund - Regular - Growth                    |   2026 |       3 |        242.051  |
| DSP Midcap Fund - Regular - Growth                    |   2026 |       4 |        247.407  |
| DSP Midcap Fund - Regular - Growth                    |   2026 |       5 |        250.275  |
| DSP Small Cap Fund - Regular - Growth                 |   2022 |       1 |         80.894  |
| DSP Small Cap Fund - Regular - Growth                 |   2022 |       2 |         80.8333 |
| DSP Small Cap Fund - Regular - Growth                 |   2022 |       3 |         84.4066 |
| DSP Small Cap Fund - Regular - Growth                 |   2022 |       4 |         79.7679 |
| DSP Small Cap Fund - Regular - Growth                 |   2022 |       5 |         82.0899 |
| DSP Small Cap Fund - Regular - Growth                 |   2022 |       6 |         83.0981 |
| DSP Small Cap Fund - Regular - Growth                 |   2022 |       7 |         77.9907 |
| DSP Small Cap Fund - Regular - Growth                 |   2022 |       8 |         77.8929 |
| DSP Small Cap Fund - Regular - Growth                 |   2022 |       9 |         80.8635 |
| DSP Small Cap Fund - Regular - Growth                 |   2022 |      10 |         81.0944 |
| DSP Small Cap Fund - Regular - Growth                 |   2022 |      11 |         91.6916 |
| DSP Small Cap Fund - Regular - Growth                 |   2022 |      12 |        106.02   |
| DSP Small Cap Fund - Regular - Growth                 |   2023 |       1 |        116.408  |
| DSP Small Cap Fund - Regular - Growth                 |   2023 |       2 |        121.891  |
| DSP Small Cap Fund - Regular - Growth                 |   2023 |       3 |        118.772  |
| DSP Small Cap Fund - Regular - Growth                 |   2023 |       4 |        132.755  |
| DSP Small Cap Fund - Regular - Growth                 |   2023 |       5 |        136.471  |
| DSP Small Cap Fund - Regular - Growth                 |   2023 |       6 |        141.584  |
| DSP Small Cap Fund - Regular - Growth                 |   2023 |       7 |        136.826  |
| DSP Small Cap Fund - Regular - Growth                 |   2023 |       8 |        129.341  |
| DSP Small Cap Fund - Regular - Growth                 |   2023 |       9 |        117.055  |
| DSP Small Cap Fund - Regular - Growth                 |   2023 |      10 |        112.844  |
| DSP Small Cap Fund - Regular - Growth                 |   2023 |      11 |        115.151  |
| DSP Small Cap Fund - Regular - Growth                 |   2023 |      12 |        134.905  |
| DSP Small Cap Fund - Regular - Growth                 |   2024 |       1 |        150.054  |
| DSP Small Cap Fund - Regular - Growth                 |   2024 |       2 |        149.281  |
| DSP Small Cap Fund - Regular - Growth                 |   2024 |       3 |        142.788  |
| DSP Small Cap Fund - Regular - Growth                 |   2024 |       4 |        158.505  |
| DSP Small Cap Fund - Regular - Growth                 |   2024 |       5 |        167.282  |
| DSP Small Cap Fund - Regular - Growth                 |   2024 |       6 |        163.294  |
| DSP Small Cap Fund - Regular - Growth                 |   2024 |       7 |        157.079  |
| DSP Small Cap Fund - Regular - Growth                 |   2024 |       8 |        140.918  |
| DSP Small Cap Fund - Regular - Growth                 |   2024 |       9 |        141.243  |
| DSP Small Cap Fund - Regular - Growth                 |   2024 |      10 |        131.967  |
| DSP Small Cap Fund - Regular - Growth                 |   2024 |      11 |        127.322  |
| DSP Small Cap Fund - Regular - Growth                 |   2024 |      12 |        128.57   |
| DSP Small Cap Fund - Regular - Growth                 |   2025 |       1 |        133.744  |
| DSP Small Cap Fund - Regular - Growth                 |   2025 |       2 |        143.668  |
| DSP Small Cap Fund - Regular - Growth                 |   2025 |       3 |        151.41   |
| DSP Small Cap Fund - Regular - Growth                 |   2025 |       4 |        164.149  |
| DSP Small Cap Fund - Regular - Growth                 |   2025 |       5 |        169.298  |
| DSP Small Cap Fund - Regular - Growth                 |   2025 |       6 |        174.296  |
| DSP Small Cap Fund - Regular - Growth                 |   2025 |       7 |        170.993  |
| DSP Small Cap Fund - Regular - Growth                 |   2025 |       8 |        179.654  |
| DSP Small Cap Fund - Regular - Growth                 |   2025 |       9 |        198.637  |
| DSP Small Cap Fund - Regular - Growth                 |   2025 |      10 |        216.82   |
| DSP Small Cap Fund - Regular - Growth                 |   2025 |      11 |        247.119  |
| DSP Small Cap Fund - Regular - Growth                 |   2025 |      12 |        253.557  |
| DSP Small Cap Fund - Regular - Growth                 |   2026 |       1 |        253.408  |
| DSP Small Cap Fund - Regular - Growth                 |   2026 |       2 |        249.45   |
| DSP Small Cap Fund - Regular - Growth                 |   2026 |       3 |        263.092  |
| DSP Small Cap Fund - Regular - Growth                 |   2026 |       4 |        305.802  |
| DSP Small Cap Fund - Regular - Growth                 |   2026 |       5 |        304.867  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2022 |       1 |        332.019  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2022 |       2 |        304.833  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2022 |       3 |        315.994  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2022 |       4 |        332.075  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2022 |       5 |        345.138  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2022 |       6 |        338.07   |
| DSP Top 100 Equity Fund - Regular - Growth            |   2022 |       7 |        331.721  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2022 |       8 |        342.302  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2022 |       9 |        343.84   |
| DSP Top 100 Equity Fund - Regular - Growth            |   2022 |      10 |        335.098  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2022 |      11 |        351.752  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2022 |      12 |        358.823  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2023 |       1 |        371.117  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2023 |       2 |        380.885  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2023 |       3 |        384.381  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2023 |       4 |        360.099  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2023 |       5 |        362.138  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2023 |       6 |        386.619  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2023 |       7 |        390.874  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2023 |       8 |        395.607  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2023 |       9 |        382.465  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2023 |      10 |        366.058  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2023 |      11 |        364.353  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2023 |      12 |        383.283  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2024 |       1 |        393.453  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2024 |       2 |        399.478  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2024 |       3 |        421.673  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2024 |       4 |        403.203  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2024 |       5 |        416.515  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2024 |       6 |        420.814  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2024 |       7 |        467.302  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2024 |       8 |        489.179  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2024 |       9 |        468.018  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2024 |      10 |        478.651  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2024 |      11 |        464.922  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2024 |      12 |        450.532  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2025 |       1 |        474.267  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2025 |       2 |        493.508  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2025 |       3 |        494.43   |
| DSP Top 100 Equity Fund - Regular - Growth            |   2025 |       4 |        519.014  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2025 |       5 |        512.259  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2025 |       6 |        509.52   |
| DSP Top 100 Equity Fund - Regular - Growth            |   2025 |       7 |        513.597  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2025 |       8 |        524.875  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2025 |       9 |        542.69   |
| DSP Top 100 Equity Fund - Regular - Growth            |   2025 |      10 |        556.721  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2025 |      11 |        588.76   |
| DSP Top 100 Equity Fund - Regular - Growth            |   2025 |      12 |        616.82   |
| DSP Top 100 Equity Fund - Regular - Growth            |   2026 |       1 |        634.917  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2026 |       2 |        628.218  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2026 |       3 |        612.015  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2026 |       4 |        605.501  |
| DSP Top 100 Equity Fund - Regular - Growth            |   2026 |       5 |        614.12   |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2022 |       1 |        113.695  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2022 |       2 |        109.935  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2022 |       3 |        103.726  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2022 |       4 |        103.167  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2022 |       5 |        102.471  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2022 |       6 |        104.979  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2022 |       7 |        106.282  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2022 |       8 |        112.808  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2022 |       9 |        111.243  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2022 |      10 |        115.167  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2022 |      11 |        117.334  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2022 |      12 |        114.785  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2023 |       1 |        115.515  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2023 |       2 |        116.585  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2023 |       3 |        125.38   |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2023 |       4 |        132.55   |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2023 |       5 |        134.268  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2023 |       6 |        131.939  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2023 |       7 |        129.998  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2023 |       8 |        128.98   |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2023 |       9 |        133.859  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2023 |      10 |        143.228  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2023 |      11 |        143.202  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2023 |      12 |        144.753  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2024 |       1 |        141.553  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2024 |       2 |        139.627  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2024 |       3 |        134.448  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2024 |       4 |        135.546  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2024 |       5 |        136.735  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2024 |       6 |        131.729  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2024 |       7 |        133.207  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2024 |       8 |        137.705  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2024 |       9 |        145.364  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2024 |      10 |        154.355  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2024 |      11 |        153.526  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2024 |      12 |        156.663  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2025 |       1 |        151.229  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2025 |       2 |        153.55   |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2025 |       3 |        164.795  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2025 |       4 |        162.666  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2025 |       5 |        162.534  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2025 |       6 |        159.686  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2025 |       7 |        160.171  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2025 |       8 |        143.961  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2025 |       9 |        137.401  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2025 |      10 |        148.598  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2025 |      11 |        160.223  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2025 |      12 |        157.155  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2026 |       1 |        159.243  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2026 |       2 |        168.219  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2026 |       3 |        172.16   |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2026 |       4 |        179.429  |
| HDFC Mid-Cap Opportunities Fund - Direct - Growth     |   2026 |       5 |        187.997  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2022 |       1 |        104.701  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2022 |       2 |        105.953  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2022 |       3 |        105.162  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2022 |       4 |         96.786  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2022 |       5 |         96.542  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2022 |       6 |         99.1645 |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2022 |       7 |        106.896  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2022 |       8 |        107.441  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2022 |       9 |        106.762  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2022 |      10 |        109.231  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2022 |      11 |        109.364  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2022 |      12 |        117.774  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2023 |       1 |        128.575  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2023 |       2 |        134.641  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2023 |       3 |        139.904  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2023 |       4 |        138.826  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2023 |       5 |        147.105  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2023 |       6 |        144.586  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2023 |       7 |        143.749  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2023 |       8 |        141.881  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2023 |       9 |        148.114  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2023 |      10 |        154.508  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2023 |      11 |        156.489  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2023 |      12 |        166.539  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2024 |       1 |        168.112  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2024 |       2 |        171      |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2024 |       3 |        176.378  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2024 |       4 |        178.302  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2024 |       5 |        187.547  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2024 |       6 |        201.272  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2024 |       7 |        216.594  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2024 |       8 |        226.721  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2024 |       9 |        232.231  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2024 |      10 |        246.839  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2024 |      11 |        241.817  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2024 |      12 |        247.761  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2025 |       1 |        248.944  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2025 |       2 |        233.567  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2025 |       3 |        224.408  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2025 |       4 |        223.691  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2025 |       5 |        221.297  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2025 |       6 |        229.381  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2025 |       7 |        236.137  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2025 |       8 |        258.116  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2025 |       9 |        259.702  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2025 |      10 |        264.497  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2025 |      11 |        259.754  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2025 |      12 |        273.873  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2026 |       1 |        295.078  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2026 |       2 |        329.77   |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2026 |       3 |        340.903  |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2026 |       4 |        359.96   |
| HDFC Mid-Cap Opportunities Fund - Regular - Growth    |   2026 |       5 |        352.148  |
| HDFC Short Term Debt Fund - Regular - Growth          |   2022 |       1 |         26.2604 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2022 |       2 |         26.4528 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2022 |       3 |         26.722  |
| HDFC Short Term Debt Fund - Regular - Growth          |   2022 |       4 |         27.0313 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2022 |       5 |         27.1765 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2022 |       6 |         27.3498 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2022 |       7 |         27.5118 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2022 |       8 |         27.6024 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2022 |       9 |         27.5188 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2022 |      10 |         27.2985 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2022 |      11 |         27.399  |
| HDFC Short Term Debt Fund - Regular - Growth          |   2022 |      12 |         27.4755 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2023 |       1 |         27.8574 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2023 |       2 |         28.1297 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2023 |       3 |         28.2411 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2023 |       4 |         28.28   |
| HDFC Short Term Debt Fund - Regular - Growth          |   2023 |       5 |         28.5239 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2023 |       6 |         28.254  |
| HDFC Short Term Debt Fund - Regular - Growth          |   2023 |       7 |         27.6648 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2023 |       8 |         28.199  |
| HDFC Short Term Debt Fund - Regular - Growth          |   2023 |       9 |         28.5432 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2023 |      10 |         28.6084 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2023 |      11 |         28.5247 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2023 |      12 |         28.4012 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2024 |       1 |         28.6261 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2024 |       2 |         28.5086 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2024 |       3 |         28.1765 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2024 |       4 |         28.1208 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2024 |       5 |         28.1316 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2024 |       6 |         28.5235 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2024 |       7 |         28.8833 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2024 |       8 |         29.0247 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2024 |       9 |         29.2462 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2024 |      10 |         29.2784 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2024 |      11 |         29.4564 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2024 |      12 |         29.5637 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2025 |       1 |         29.6977 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2025 |       2 |         29.829  |
| HDFC Short Term Debt Fund - Regular - Growth          |   2025 |       3 |         30.0277 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2025 |       4 |         30.2213 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2025 |       5 |         30.7195 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2025 |       6 |         31.0285 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2025 |       7 |         31.3451 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2025 |       8 |         31.7492 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2025 |       9 |         31.2081 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2025 |      10 |         31.6493 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2025 |      11 |         32.3849 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2025 |      12 |         32.4208 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2026 |       1 |         32.1394 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2026 |       2 |         31.9793 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2026 |       3 |         31.5663 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2026 |       4 |         31.9156 |
| HDFC Short Term Debt Fund - Regular - Growth          |   2026 |       5 |         31.9019 |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2022 |       1 |        553.751  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2022 |       2 |        544.245  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2022 |       3 |        548.501  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2022 |       4 |        578.366  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2022 |       5 |        597.774  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2022 |       6 |        658.095  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2022 |       7 |        646.699  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2022 |       8 |        648.421  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2022 |       9 |        675.112  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2022 |      10 |        667.355  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2022 |      11 |        663.37   |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2022 |      12 |        649.631  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2023 |       1 |        645.922  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2023 |       2 |        657.507  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2023 |       3 |        671.452  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2023 |       4 |        684.213  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2023 |       5 |        694.246  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2023 |       6 |        737.883  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2023 |       7 |        728.938  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2023 |       8 |        702.668  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2023 |       9 |        745.667  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2023 |      10 |        767.278  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2023 |      11 |        804.247  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2023 |      12 |        833.923  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2024 |       1 |        814.39   |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2024 |       2 |        828.245  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2024 |       3 |        812.151  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2024 |       4 |        818.492  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2024 |       5 |        815.344  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2024 |       6 |        798.838  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2024 |       7 |        821.56   |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2024 |       8 |        792.463  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2024 |       9 |        775.331  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2024 |      10 |        763.115  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2024 |      11 |        765.645  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2024 |      12 |        766.288  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2025 |       1 |        762.08   |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2025 |       2 |        784.346  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2025 |       3 |        801.721  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2025 |       4 |        854.539  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2025 |       5 |        916.995  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2025 |       6 |        920.396  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2025 |       7 |        923.948  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2025 |       8 |        950.872  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2025 |       9 |        947.799  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2025 |      10 |        995.337  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2025 |      11 |        968.556  |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2025 |      12 |       1007.94   |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2026 |       1 |       1049.89   |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2026 |       2 |       1099.25   |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2026 |       3 |       1158.78   |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2026 |       4 |       1238.89   |
| HDFC Top 100 Fund - Direct Plan - Growth              |   2026 |       5 |       1202.96   |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2022 |       1 |        511.923  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2022 |       2 |        514.538  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2022 |       3 |        522.287  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2022 |       4 |        526.115  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2022 |       5 |        504.336  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2022 |       6 |        465.377  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2022 |       7 |        436.773  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2022 |       8 |        420.921  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2022 |       9 |        422.428  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2022 |      10 |        431.346  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2022 |      11 |        463.836  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2022 |      12 |        480.874  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2023 |       1 |        490.846  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2023 |       2 |        492.447  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2023 |       3 |        545.736  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2023 |       4 |        567.038  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2023 |       5 |        565.489  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2023 |       6 |        570.71   |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2023 |       7 |        578.383  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2023 |       8 |        569.721  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2023 |       9 |        577.082  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2023 |      10 |        575.173  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2023 |      11 |        572.596  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2023 |      12 |        582.917  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2024 |       1 |        598.985  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2024 |       2 |        602.895  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2024 |       3 |        635.051  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2024 |       4 |        640.184  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2024 |       5 |        634.463  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2024 |       6 |        654.603  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2024 |       7 |        645.131  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2024 |       8 |        631.404  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2024 |       9 |        582.932  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2024 |      10 |        550.379  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2024 |      11 |        564.304  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2024 |      12 |        587.642  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2025 |       1 |        589.529  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2025 |       2 |        601.053  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2025 |       3 |        619.422  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2025 |       4 |        611.928  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2025 |       5 |        614.53   |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2025 |       6 |        602.966  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2025 |       7 |        602.346  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2025 |       8 |        589.971  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2025 |       9 |        594.822  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2025 |      10 |        617.653  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2025 |      11 |        601.675  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2025 |      12 |        618.352  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2026 |       1 |        632.08   |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2026 |       2 |        593.424  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2026 |       3 |        588.373  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2026 |       4 |        609.896  |
| HDFC Top 100 Fund - Regular Plan - Growth             |   2026 |       5 |        592.367  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2022 |       1 |         61.9065 |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2022 |       2 |         61.7086 |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2022 |       3 |         62.1624 |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2022 |       4 |         63.9535 |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2022 |       5 |         65.7703 |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2022 |       6 |         67.8819 |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2022 |       7 |         69.3996 |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2022 |       8 |         70.4881 |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2022 |       9 |         71.7158 |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2022 |      10 |         71.2591 |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2022 |      11 |         69.8138 |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2022 |      12 |         67.8438 |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2023 |       1 |         67.3266 |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2023 |       2 |         66.352  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2023 |       3 |         68.8655 |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2023 |       4 |         69.2187 |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2023 |       5 |         66.1959 |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2023 |       6 |         67.5639 |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2023 |       7 |         73.8536 |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2023 |       8 |         81.6809 |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2023 |       9 |         86.0884 |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2023 |      10 |         85.6077 |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2023 |      11 |         86.1263 |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2023 |      12 |         87.95   |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2024 |       1 |         91.5995 |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2024 |       2 |         93.6953 |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2024 |       3 |        100.814  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2024 |       4 |        103.047  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2024 |       5 |        106.475  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2024 |       6 |        108.817  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2024 |       7 |        111.094  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2024 |       8 |        114.665  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2024 |       9 |        111.319  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2024 |      10 |        108.884  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2024 |      11 |        112.351  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2024 |      12 |        110.714  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2025 |       1 |        112.743  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2025 |       2 |        115.97   |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2025 |       3 |        118.034  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2025 |       4 |        123.465  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2025 |       5 |        128.75   |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2025 |       6 |        134.283  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2025 |       7 |        128.023  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2025 |       8 |        125.412  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2025 |       9 |        131.921  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2025 |      10 |        129.801  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2025 |      11 |        133.393  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2025 |      12 |        150.551  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2026 |       1 |        156.947  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2026 |       2 |        155.256  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2026 |       3 |        158.815  |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2026 |       4 |        156.42   |
| ICICI Pru Bluechip Fund - Direct - Growth             |   2026 |       5 |        151.763  |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2022 |       1 |         58.8013 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2022 |       2 |         58.8808 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2022 |       3 |         63.1021 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2022 |       4 |         64.5053 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2022 |       5 |         65.9852 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2022 |       6 |         66.0044 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2022 |       7 |         72.1007 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2022 |       8 |         75.8673 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2022 |       9 |         73.098  |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2022 |      10 |         74.399  |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2022 |      11 |         77.218  |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2022 |      12 |         78.8703 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2023 |       1 |         79.5594 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2023 |       2 |         77.749  |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2023 |       3 |         78.4846 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2023 |       4 |         80.4175 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2023 |       5 |         79.7675 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2023 |       6 |         78.6815 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2023 |       7 |         76.9909 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2023 |       8 |         75.7958 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2023 |       9 |         80.3787 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2023 |      10 |         77.0492 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2023 |      11 |         74.3046 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2023 |      12 |         74.0353 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2024 |       1 |         76.8241 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2024 |       2 |         80.8069 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2024 |       3 |         84.093  |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2024 |       4 |         87.961  |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2024 |       5 |         90.6673 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2024 |       6 |         94.3666 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2024 |       7 |         95.1524 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2024 |       8 |         92.7937 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2024 |       9 |         96.3206 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2024 |      10 |         99.0025 |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2024 |      11 |        105.166  |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2024 |      12 |        104.385  |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2025 |       1 |        105.969  |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2025 |       2 |        112.781  |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2025 |       3 |        111.776  |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2025 |       4 |        108.528  |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2025 |       5 |        110.297  |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2025 |       6 |        112.287  |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2025 |       7 |        112.07   |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2025 |       8 |        110.806  |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2025 |       9 |        110.995  |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2025 |      10 |        113.668  |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2025 |      11 |        112.51   |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2025 |      12 |        113.802  |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2026 |       1 |        109.168  |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2026 |       2 |        102.82   |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2026 |       3 |        106.212  |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2026 |       4 |        112.601  |
| ICICI Pru Bluechip Fund - Regular - Growth            |   2026 |       5 |        114.751  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2022 |       1 |        287.064  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2022 |       2 |        288.958  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2022 |       3 |        290.461  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2022 |       4 |        291.719  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2022 |       5 |        293.294  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2022 |       6 |        295.497  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2022 |       7 |        297.399  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2022 |       8 |        299.025  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2022 |       9 |        300.667  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2022 |      10 |        301.989  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2022 |      11 |        303.585  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2022 |      12 |        305.031  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2023 |       1 |        306.143  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2023 |       2 |        307.522  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2023 |       3 |        309.645  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2023 |       4 |        310.997  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2023 |       5 |        312.842  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2023 |       6 |        315.053  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2023 |       7 |        317.341  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2023 |       8 |        319.334  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2023 |       9 |        321.028  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2023 |      10 |        322.763  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2023 |      11 |        324.937  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2023 |      12 |        326.576  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2024 |       1 |        328.625  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2024 |       2 |        330.978  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2024 |       3 |        332.74   |
| ICICI Pru Liquid Fund - Regular - Growth              |   2024 |       4 |        334.558  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2024 |       5 |        336.622  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2024 |       6 |        338.043  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2024 |       7 |        340.383  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2024 |       8 |        342.052  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2024 |       9 |        344.394  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2024 |      10 |        346.329  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2024 |      11 |        348.437  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2024 |      12 |        350.658  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2025 |       1 |        352.486  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2025 |       2 |        355.094  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2025 |       3 |        357.27   |
| ICICI Pru Liquid Fund - Regular - Growth              |   2025 |       4 |        359.47   |
| ICICI Pru Liquid Fund - Regular - Growth              |   2025 |       5 |        361.04   |
| ICICI Pru Liquid Fund - Regular - Growth              |   2025 |       6 |        363.177  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2025 |       7 |        365.474  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2025 |       8 |        367.378  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2025 |       9 |        369.567  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2025 |      10 |        371.728  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2025 |      11 |        373.227  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2025 |      12 |        374.853  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2026 |       1 |        377.921  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2026 |       2 |        379.982  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2026 |       3 |        381.889  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2026 |       4 |        384.664  |
| ICICI Pru Liquid Fund - Regular - Growth              |   2026 |       5 |        387.446  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2022 |       1 |        139.889  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2022 |       2 |        154.492  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2022 |       3 |        171.029  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2022 |       4 |        184.387  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2022 |       5 |        186.962  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2022 |       6 |        180.498  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2022 |       7 |        176.553  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2022 |       8 |        193.528  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2022 |       9 |        199.5    |
| ICICI Pru Midcap Fund - Regular - Growth              |   2022 |      10 |        201.807  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2022 |      11 |        207.132  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2022 |      12 |        208.523  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2023 |       1 |        206.004  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2023 |       2 |        203.927  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2023 |       3 |        200.443  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2023 |       4 |        194.771  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2023 |       5 |        198.336  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2023 |       6 |        215.273  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2023 |       7 |        211.746  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2023 |       8 |        226.999  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2023 |       9 |        246.804  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2023 |      10 |        276.181  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2023 |      11 |        277.535  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2023 |      12 |        278.022  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2024 |       1 |        269.779  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2024 |       2 |        273.412  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2024 |       3 |        283.45   |
| ICICI Pru Midcap Fund - Regular - Growth              |   2024 |       4 |        303.726  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2024 |       5 |        296.655  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2024 |       6 |        299.459  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2024 |       7 |        308.389  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2024 |       8 |        298.263  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2024 |       9 |        302.458  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2024 |      10 |        326.233  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2024 |      11 |        332.799  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2024 |      12 |        318.546  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2025 |       1 |        290.823  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2025 |       2 |        310.723  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2025 |       3 |        338.845  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2025 |       4 |        344.048  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2025 |       5 |        356.919  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2025 |       6 |        363.999  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2025 |       7 |        375.708  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2025 |       8 |        376.387  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2025 |       9 |        375.608  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2025 |      10 |        385.203  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2025 |      11 |        374.03   |
| ICICI Pru Midcap Fund - Regular - Growth              |   2025 |      12 |        390.779  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2026 |       1 |        407.271  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2026 |       2 |        433.017  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2026 |       3 |        447.039  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2026 |       4 |        453.903  |
| ICICI Pru Midcap Fund - Regular - Growth              |   2026 |       5 |        467.626  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2022 |       1 |        205.301  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2022 |       2 |        215.202  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2022 |       3 |        225.32   |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2022 |       4 |        233.264  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2022 |       5 |        226.904  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2022 |       6 |        226.547  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2022 |       7 |        218.571  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2022 |       8 |        222.151  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2022 |       9 |        224.022  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2022 |      10 |        219.969  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2022 |      11 |        215.047  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2022 |      12 |        220.037  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2023 |       1 |        242.251  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2023 |       2 |        256.735  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2023 |       3 |        266.813  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2023 |       4 |        265.76   |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2023 |       5 |        252.752  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2023 |       6 |        248.382  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2023 |       7 |        239.654  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2023 |       8 |        227.231  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2023 |       9 |        230.85   |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2023 |      10 |        239.123  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2023 |      11 |        245.012  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2023 |      12 |        263.725  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2024 |       1 |        272.358  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2024 |       2 |        281.026  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2024 |       3 |        295.715  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2024 |       4 |        289.163  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2024 |       5 |        263.388  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2024 |       6 |        257.898  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2024 |       7 |        264.177  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2024 |       8 |        275.237  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2024 |       9 |        270.979  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2024 |      10 |        270.127  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2024 |      11 |        270.747  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2024 |      12 |        266.278  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2025 |       1 |        260.768  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2025 |       2 |        276.506  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2025 |       3 |        275.355  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2025 |       4 |        265.282  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2025 |       5 |        275.228  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2025 |       6 |        302.731  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2025 |       7 |        317.612  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2025 |       8 |        328.511  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2025 |       9 |        330.911  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2025 |      10 |        330.096  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2025 |      11 |        346.439  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2025 |      12 |        362.831  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2026 |       1 |        370.347  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2026 |       2 |        392.143  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2026 |       3 |        403.096  |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2026 |       4 |        398.95   |
| ICICI Pru Value Discovery Fund - Regular - Growth     |   2026 |       5 |        396.187  |
| Kotak Bluechip Fund - Regular - Growth                |   2022 |       1 |        276.184  |
| Kotak Bluechip Fund - Regular - Growth                |   2022 |       2 |        268.617  |
| Kotak Bluechip Fund - Regular - Growth                |   2022 |       3 |        269.557  |
| Kotak Bluechip Fund - Regular - Growth                |   2022 |       4 |        259.38   |
| Kotak Bluechip Fund - Regular - Growth                |   2022 |       5 |        257.55   |
| Kotak Bluechip Fund - Regular - Growth                |   2022 |       6 |        258.451  |
| Kotak Bluechip Fund - Regular - Growth                |   2022 |       7 |        251.62   |
| Kotak Bluechip Fund - Regular - Growth                |   2022 |       8 |        255.015  |
| Kotak Bluechip Fund - Regular - Growth                |   2022 |       9 |        264.25   |
| Kotak Bluechip Fund - Regular - Growth                |   2022 |      10 |        267.485  |
| Kotak Bluechip Fund - Regular - Growth                |   2022 |      11 |        272.827  |
| Kotak Bluechip Fund - Regular - Growth                |   2022 |      12 |        271.697  |
| Kotak Bluechip Fund - Regular - Growth                |   2023 |       1 |        276.671  |
| Kotak Bluechip Fund - Regular - Growth                |   2023 |       2 |        281.334  |
| Kotak Bluechip Fund - Regular - Growth                |   2023 |       3 |        285.703  |
| Kotak Bluechip Fund - Regular - Growth                |   2023 |       4 |        289.039  |
| Kotak Bluechip Fund - Regular - Growth                |   2023 |       5 |        295.789  |
| Kotak Bluechip Fund - Regular - Growth                |   2023 |       6 |        304.375  |
| Kotak Bluechip Fund - Regular - Growth                |   2023 |       7 |        306.482  |
| Kotak Bluechip Fund - Regular - Growth                |   2023 |       8 |        310.8    |
| Kotak Bluechip Fund - Regular - Growth                |   2023 |       9 |        340.081  |
| Kotak Bluechip Fund - Regular - Growth                |   2023 |      10 |        364.851  |
| Kotak Bluechip Fund - Regular - Growth                |   2023 |      11 |        395.941  |
| Kotak Bluechip Fund - Regular - Growth                |   2023 |      12 |        409.358  |
| Kotak Bluechip Fund - Regular - Growth                |   2024 |       1 |        422.897  |
| Kotak Bluechip Fund - Regular - Growth                |   2024 |       2 |        398.967  |
| Kotak Bluechip Fund - Regular - Growth                |   2024 |       3 |        378.941  |
| Kotak Bluechip Fund - Regular - Growth                |   2024 |       4 |        385.358  |
| Kotak Bluechip Fund - Regular - Growth                |   2024 |       5 |        392.581  |
| Kotak Bluechip Fund - Regular - Growth                |   2024 |       6 |        396.766  |
| Kotak Bluechip Fund - Regular - Growth                |   2024 |       7 |        406.595  |
| Kotak Bluechip Fund - Regular - Growth                |   2024 |       8 |        396.524  |
| Kotak Bluechip Fund - Regular - Growth                |   2024 |       9 |        415.07   |
| Kotak Bluechip Fund - Regular - Growth                |   2024 |      10 |        414.966  |
| Kotak Bluechip Fund - Regular - Growth                |   2024 |      11 |        408.556  |
| Kotak Bluechip Fund - Regular - Growth                |   2024 |      12 |        397.034  |
| Kotak Bluechip Fund - Regular - Growth                |   2025 |       1 |        387.236  |
| Kotak Bluechip Fund - Regular - Growth                |   2025 |       2 |        369.655  |
| Kotak Bluechip Fund - Regular - Growth                |   2025 |       3 |        390.202  |
| Kotak Bluechip Fund - Regular - Growth                |   2025 |       4 |        401.654  |
| Kotak Bluechip Fund - Regular - Growth                |   2025 |       5 |        414.35   |
| Kotak Bluechip Fund - Regular - Growth                |   2025 |       6 |        406.358  |
| Kotak Bluechip Fund - Regular - Growth                |   2025 |       7 |        385.55   |
| Kotak Bluechip Fund - Regular - Growth                |   2025 |       8 |        372.077  |
| Kotak Bluechip Fund - Regular - Growth                |   2025 |       9 |        374.275  |
| Kotak Bluechip Fund - Regular - Growth                |   2025 |      10 |        390.47   |
| Kotak Bluechip Fund - Regular - Growth                |   2025 |      11 |        420.689  |
| Kotak Bluechip Fund - Regular - Growth                |   2025 |      12 |        434.841  |
| Kotak Bluechip Fund - Regular - Growth                |   2026 |       1 |        434.072  |
| Kotak Bluechip Fund - Regular - Growth                |   2026 |       2 |        447.527  |
| Kotak Bluechip Fund - Regular - Growth                |   2026 |       3 |        433.854  |
| Kotak Bluechip Fund - Regular - Growth                |   2026 |       4 |        439.376  |
| Kotak Bluechip Fund - Regular - Growth                |   2026 |       5 |        465.631  |
| Kotak Emerging Equity Fund - Regular - Growth         |   2022 |       1 |         65.1637 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2022 |       2 |         69.2654 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2022 |       3 |         69.3032 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2022 |       4 |         63.261  |
| Kotak Emerging Equity Fund - Regular - Growth         |   2022 |       5 |         60.4265 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2022 |       6 |         62.6256 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2022 |       7 |         59.4234 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2022 |       8 |         60.3854 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2022 |       9 |         62.188  |
| Kotak Emerging Equity Fund - Regular - Growth         |   2022 |      10 |         61.8025 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2022 |      11 |         60.8207 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2022 |      12 |         64.1933 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2023 |       1 |         65.7721 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2023 |       2 |         63.7096 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2023 |       3 |         63.9289 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2023 |       4 |         65.1873 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2023 |       5 |         65.7195 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2023 |       6 |         64.3532 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2023 |       7 |         63.3607 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2023 |       8 |         69.4514 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2023 |       9 |         73.7774 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2023 |      10 |         75.765  |
| Kotak Emerging Equity Fund - Regular - Growth         |   2023 |      11 |         76.5055 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2023 |      12 |         69.1811 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2024 |       1 |         67.1598 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2024 |       2 |         65.8457 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2024 |       3 |         63.7222 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2024 |       4 |         62.6771 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2024 |       5 |         63.4091 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2024 |       6 |         64.7439 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2024 |       7 |         64.989  |
| Kotak Emerging Equity Fund - Regular - Growth         |   2024 |       8 |         62.4376 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2024 |       9 |         65.6068 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2024 |      10 |         63.7618 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2024 |      11 |         67.1499 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2024 |      12 |         63.9006 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2025 |       1 |         70.4526 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2025 |       2 |         68.4635 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2025 |       3 |         71.4438 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2025 |       4 |         74.4591 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2025 |       5 |         70.7721 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2025 |       6 |         69.0463 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2025 |       7 |         69.6323 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2025 |       8 |         73.1967 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2025 |       9 |         72.9715 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2025 |      10 |         79.345  |
| Kotak Emerging Equity Fund - Regular - Growth         |   2025 |      11 |         77.5761 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2025 |      12 |         73.6773 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2026 |       1 |         69.3294 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2026 |       2 |         67.8868 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2026 |       3 |         71.7423 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2026 |       4 |         76.2261 |
| Kotak Emerging Equity Fund - Regular - Growth         |   2026 |       5 |         79.6063 |
| Kotak Flexicap Fund - Regular - Growth                |   2022 |       1 |         49.2312 |
| Kotak Flexicap Fund - Regular - Growth                |   2022 |       2 |         48.4893 |
| Kotak Flexicap Fund - Regular - Growth                |   2022 |       3 |         49.2229 |
| Kotak Flexicap Fund - Regular - Growth                |   2022 |       4 |         45.6445 |
| Kotak Flexicap Fund - Regular - Growth                |   2022 |       5 |         46.543  |
| Kotak Flexicap Fund - Regular - Growth                |   2022 |       6 |         48.4147 |
| Kotak Flexicap Fund - Regular - Growth                |   2022 |       7 |         48.5021 |
| Kotak Flexicap Fund - Regular - Growth                |   2022 |       8 |         48.5039 |
| Kotak Flexicap Fund - Regular - Growth                |   2022 |       9 |         50.7046 |
| Kotak Flexicap Fund - Regular - Growth                |   2022 |      10 |         54.6825 |
| Kotak Flexicap Fund - Regular - Growth                |   2022 |      11 |         56.2551 |
| Kotak Flexicap Fund - Regular - Growth                |   2022 |      12 |         57.5763 |
| Kotak Flexicap Fund - Regular - Growth                |   2023 |       1 |         60.7443 |
| Kotak Flexicap Fund - Regular - Growth                |   2023 |       2 |         67.2305 |
| Kotak Flexicap Fund - Regular - Growth                |   2023 |       3 |         71.8076 |
| Kotak Flexicap Fund - Regular - Growth                |   2023 |       4 |         72.3295 |
| Kotak Flexicap Fund - Regular - Growth                |   2023 |       5 |         74.993  |
| Kotak Flexicap Fund - Regular - Growth                |   2023 |       6 |         78.7903 |
| Kotak Flexicap Fund - Regular - Growth                |   2023 |       7 |         81.6638 |
| Kotak Flexicap Fund - Regular - Growth                |   2023 |       8 |         79.7674 |
| Kotak Flexicap Fund - Regular - Growth                |   2023 |       9 |         81.8347 |
| Kotak Flexicap Fund - Regular - Growth                |   2023 |      10 |         83.153  |
| Kotak Flexicap Fund - Regular - Growth                |   2023 |      11 |         85.7092 |
| Kotak Flexicap Fund - Regular - Growth                |   2023 |      12 |         87.5177 |
| Kotak Flexicap Fund - Regular - Growth                |   2024 |       1 |         85.7306 |
| Kotak Flexicap Fund - Regular - Growth                |   2024 |       2 |         85.1053 |
| Kotak Flexicap Fund - Regular - Growth                |   2024 |       3 |         87.4978 |
| Kotak Flexicap Fund - Regular - Growth                |   2024 |       4 |         93.7363 |
| Kotak Flexicap Fund - Regular - Growth                |   2024 |       5 |         91.9803 |
| Kotak Flexicap Fund - Regular - Growth                |   2024 |       6 |         97.8299 |
| Kotak Flexicap Fund - Regular - Growth                |   2024 |       7 |         96.7357 |
| Kotak Flexicap Fund - Regular - Growth                |   2024 |       8 |         94.32   |
| Kotak Flexicap Fund - Regular - Growth                |   2024 |       9 |         95.4429 |
| Kotak Flexicap Fund - Regular - Growth                |   2024 |      10 |        111.536  |
| Kotak Flexicap Fund - Regular - Growth                |   2024 |      11 |        130.364  |
| Kotak Flexicap Fund - Regular - Growth                |   2024 |      12 |        131.456  |
| Kotak Flexicap Fund - Regular - Growth                |   2025 |       1 |        130.957  |
| Kotak Flexicap Fund - Regular - Growth                |   2025 |       2 |        134.796  |
| Kotak Flexicap Fund - Regular - Growth                |   2025 |       3 |        128.114  |
| Kotak Flexicap Fund - Regular - Growth                |   2025 |       4 |        125.28   |
| Kotak Flexicap Fund - Regular - Growth                |   2025 |       5 |        127.466  |
| Kotak Flexicap Fund - Regular - Growth                |   2025 |       6 |        126.678  |
| Kotak Flexicap Fund - Regular - Growth                |   2025 |       7 |        127.256  |
| Kotak Flexicap Fund - Regular - Growth                |   2025 |       8 |        132.627  |
| Kotak Flexicap Fund - Regular - Growth                |   2025 |       9 |        131.836  |
| Kotak Flexicap Fund - Regular - Growth                |   2025 |      10 |        136.44   |
| Kotak Flexicap Fund - Regular - Growth                |   2025 |      11 |        148.377  |
| Kotak Flexicap Fund - Regular - Growth                |   2025 |      12 |        164.102  |
| Kotak Flexicap Fund - Regular - Growth                |   2026 |       1 |        164.257  |
| Kotak Flexicap Fund - Regular - Growth                |   2026 |       2 |        166.31   |
| Kotak Flexicap Fund - Regular - Growth                |   2026 |       3 |        161.905  |
| Kotak Flexicap Fund - Regular - Growth                |   2026 |       4 |        176.706  |
| Kotak Flexicap Fund - Regular - Growth                |   2026 |       5 |        171.585  |
| Kotak Liquid Fund - Regular - Growth                  |   2022 |       1 |       3193.2    |
| Kotak Liquid Fund - Regular - Growth                  |   2022 |       2 |       3214.07   |
| Kotak Liquid Fund - Regular - Growth                  |   2022 |       3 |       3235.76   |
| Kotak Liquid Fund - Regular - Growth                  |   2022 |       4 |       3260.57   |
| Kotak Liquid Fund - Regular - Growth                  |   2022 |       5 |       3274.69   |
| Kotak Liquid Fund - Regular - Growth                  |   2022 |       6 |       3291.08   |
| Kotak Liquid Fund - Regular - Growth                  |   2022 |       7 |       3312.63   |
| Kotak Liquid Fund - Regular - Growth                  |   2022 |       8 |       3331.12   |
| Kotak Liquid Fund - Regular - Growth                  |   2022 |       9 |       3352.72   |
| Kotak Liquid Fund - Regular - Growth                  |   2022 |      10 |       3373.91   |
| Kotak Liquid Fund - Regular - Growth                  |   2022 |      11 |       3391.09   |
| Kotak Liquid Fund - Regular - Growth                  |   2022 |      12 |       3405.29   |
| Kotak Liquid Fund - Regular - Growth                  |   2023 |       1 |       3428.84   |
| Kotak Liquid Fund - Regular - Growth                  |   2023 |       2 |       3446.67   |
| Kotak Liquid Fund - Regular - Growth                  |   2023 |       3 |       3467.41   |
| Kotak Liquid Fund - Regular - Growth                  |   2023 |       4 |       3492.16   |
| Kotak Liquid Fund - Regular - Growth                  |   2023 |       5 |       3513.07   |
| Kotak Liquid Fund - Regular - Growth                  |   2023 |       6 |       3519.42   |
| Kotak Liquid Fund - Regular - Growth                  |   2023 |       7 |       3539.91   |
| Kotak Liquid Fund - Regular - Growth                  |   2023 |       8 |       3565.81   |
| Kotak Liquid Fund - Regular - Growth                  |   2023 |       9 |       3583.9    |
| Kotak Liquid Fund - Regular - Growth                  |   2023 |      10 |       3609.22   |
| Kotak Liquid Fund - Regular - Growth                  |   2023 |      11 |       3632.92   |
| Kotak Liquid Fund - Regular - Growth                  |   2023 |      12 |       3653.39   |
| Kotak Liquid Fund - Regular - Growth                  |   2024 |       1 |       3671.03   |
| Kotak Liquid Fund - Regular - Growth                  |   2024 |       2 |       3689.73   |
| Kotak Liquid Fund - Regular - Growth                  |   2024 |       3 |       3712.46   |
| Kotak Liquid Fund - Regular - Growth                  |   2024 |       4 |       3734.81   |
| Kotak Liquid Fund - Regular - Growth                  |   2024 |       5 |       3739.42   |
| Kotak Liquid Fund - Regular - Growth                  |   2024 |       6 |       3759.23   |
| Kotak Liquid Fund - Regular - Growth                  |   2024 |       7 |       3780.67   |
| Kotak Liquid Fund - Regular - Growth                  |   2024 |       8 |       3796.86   |
| Kotak Liquid Fund - Regular - Growth                  |   2024 |       9 |       3810.29   |
| Kotak Liquid Fund - Regular - Growth                  |   2024 |      10 |       3825.91   |
| Kotak Liquid Fund - Regular - Growth                  |   2024 |      11 |       3842.45   |
| Kotak Liquid Fund - Regular - Growth                  |   2024 |      12 |       3865.44   |
| Kotak Liquid Fund - Regular - Growth                  |   2025 |       1 |       3888.73   |
| Kotak Liquid Fund - Regular - Growth                  |   2025 |       2 |       3902.6    |
| Kotak Liquid Fund - Regular - Growth                  |   2025 |       3 |       3927.82   |
| Kotak Liquid Fund - Regular - Growth                  |   2025 |       4 |       3950.11   |
| Kotak Liquid Fund - Regular - Growth                  |   2025 |       5 |       3972.89   |
| Kotak Liquid Fund - Regular - Growth                  |   2025 |       6 |       3994.87   |
| Kotak Liquid Fund - Regular - Growth                  |   2025 |       7 |       4014.62   |
| Kotak Liquid Fund - Regular - Growth                  |   2025 |       8 |       4034.9    |
| Kotak Liquid Fund - Regular - Growth                  |   2025 |       9 |       4052      |
| Kotak Liquid Fund - Regular - Growth                  |   2025 |      10 |       4076.7    |
| Kotak Liquid Fund - Regular - Growth                  |   2025 |      11 |       4108      |
| Kotak Liquid Fund - Regular - Growth                  |   2025 |      12 |       4134.53   |
| Kotak Liquid Fund - Regular - Growth                  |   2026 |       1 |       4155.13   |
| Kotak Liquid Fund - Regular - Growth                  |   2026 |       2 |       4181.71   |
| Kotak Liquid Fund - Regular - Growth                  |   2026 |       3 |       4204.9    |
| Kotak Liquid Fund - Regular - Growth                  |   2026 |       4 |       4227.02   |
| Kotak Liquid Fund - Regular - Growth                  |   2026 |       5 |       4254      |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2022 |       1 |         83.9796 |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2022 |       2 |         81.2621 |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2022 |       3 |         83.3301 |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2022 |       4 |         84.9726 |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2022 |       5 |         83.4524 |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2022 |       6 |         83.3397 |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2022 |       7 |         82.507  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2022 |       8 |         85.4823 |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2022 |       9 |         93.8592 |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2022 |      10 |        101.195  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2022 |      11 |        113.684  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2022 |      12 |        119.399  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2023 |       1 |        122.532  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2023 |       2 |        125.882  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2023 |       3 |        123.786  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2023 |       4 |        128.057  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2023 |       5 |        133.176  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2023 |       6 |        140.723  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2023 |       7 |        140.513  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2023 |       8 |        142.897  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2023 |       9 |        150.543  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2023 |      10 |        148.381  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2023 |      11 |        147.417  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2023 |      12 |        141.383  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2024 |       1 |        135.123  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2024 |       2 |        140.121  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2024 |       3 |        149.644  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2024 |       4 |        151.204  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2024 |       5 |        157.148  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2024 |       6 |        163.388  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2024 |       7 |        168.142  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2024 |       8 |        173.369  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2024 |       9 |        171.352  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2024 |      10 |        176.975  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2024 |      11 |        176.723  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2024 |      12 |        171.493  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2025 |       1 |        166.976  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2025 |       2 |        168.236  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2025 |       3 |        177.137  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2025 |       4 |        182.251  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2025 |       5 |        181.832  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2025 |       6 |        189.169  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2025 |       7 |        190.931  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2025 |       8 |        182.138  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2025 |       9 |        176.611  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2025 |      10 |        181.752  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2025 |      11 |        186.639  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2025 |      12 |        184.666  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2026 |       1 |        197.799  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2026 |       2 |        193.829  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2026 |       3 |        190.893  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2026 |       4 |        201.454  |
| Mirae Asset Emerging Bluechip Fund - Regular - Growth |   2026 |       5 |        200.025  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2022 |       1 |         76.1067 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2022 |       2 |         79.6865 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2022 |       3 |         80.4925 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2022 |       4 |         83.1742 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2022 |       5 |         84.2439 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2022 |       6 |         86.5416 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2022 |       7 |         87.5379 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2022 |       8 |         87.9246 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2022 |       9 |         90.1837 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2022 |      10 |         92.9963 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2022 |      11 |         95.6736 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2022 |      12 |         97.9357 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2023 |       1 |         98.1815 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2023 |       2 |         95.4447 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2023 |       3 |         94.3645 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2023 |       4 |         92.7388 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2023 |       5 |         94.4504 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2023 |       6 |         97.2871 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2023 |       7 |         98.5201 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2023 |       8 |         95.4281 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2023 |       9 |         92.6843 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2023 |      10 |         91.5888 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2023 |      11 |         96.0442 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2023 |      12 |         96.5829 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2024 |       1 |         95.5798 |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2024 |       2 |        101.218  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2024 |       3 |        112.297  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2024 |       4 |        118.492  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2024 |       5 |        117.414  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2024 |       6 |        120.671  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2024 |       7 |        123.333  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2024 |       8 |        127.477  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2024 |       9 |        130.643  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2024 |      10 |        132.342  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2024 |      11 |        147.475  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2024 |      12 |        160.006  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2025 |       1 |        169.233  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2025 |       2 |        164.255  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2025 |       3 |        169.907  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2025 |       4 |        180.976  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2025 |       5 |        189.743  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2025 |       6 |        200.46   |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2025 |       7 |        208.647  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2025 |       8 |        209.686  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2025 |       9 |        219.016  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2025 |      10 |        222.615  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2025 |      11 |        223.094  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2025 |      12 |        231.611  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2026 |       1 |        229.257  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2026 |       2 |        225.59   |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2026 |       3 |        232.72   |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2026 |       4 |        244.408  |
| Mirae Asset Large Cap Fund - Regular - Growth         |   2026 |       5 |        238.774  |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2022 |       1 |         29.355  |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2022 |       2 |         29.3306 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2022 |       3 |         30.395  |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2022 |       4 |         33.4149 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2022 |       5 |         33.336  |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2022 |       6 |         34.9514 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2022 |       7 |         35.6386 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2022 |       8 |         36.5088 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2022 |       9 |         35.8926 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2022 |      10 |         36.5478 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2022 |      11 |         37.7738 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2022 |      12 |         41.0743 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2023 |       1 |         42.4169 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2023 |       2 |         45.776  |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2023 |       3 |         48.4846 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2023 |       4 |         47.1948 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2023 |       5 |         45.5584 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2023 |       6 |         48.3236 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2023 |       7 |         52.384  |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2023 |       8 |         53.5121 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2023 |       9 |         50.6866 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2023 |      10 |         47.3587 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2023 |      11 |         46.5382 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2023 |      12 |         49.0373 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2024 |       1 |         49.2949 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2024 |       2 |         48.4906 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2024 |       3 |         50.6553 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2024 |       4 |         55.7384 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2024 |       5 |         55.2909 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2024 |       6 |         53.9343 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2024 |       7 |         56.7054 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2024 |       8 |         59.225  |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2024 |       9 |         58.607  |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2024 |      10 |         58.394  |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2024 |      11 |         61.0593 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2024 |      12 |         59.1074 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2025 |       1 |         58.0102 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2025 |       2 |         62.06   |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2025 |       3 |         65.8887 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2025 |       4 |         70.1372 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2025 |       5 |         69.3566 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2025 |       6 |         67.7899 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2025 |       7 |         70.5445 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2025 |       8 |         69.5717 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2025 |       9 |         69.8867 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2025 |      10 |         68.8981 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2025 |      11 |         74.6011 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2025 |      12 |         75.0795 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2026 |       1 |         74.7622 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2026 |       2 |         77.7433 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2026 |       3 |         80.2019 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2026 |       4 |         85.2645 |
| Mirae Asset Tax Saver Fund - Regular - Growth         |   2026 |       5 |         90.6994 |
| Nippon India ETF Nifty 50 BeES                        |   2022 |       1 |        162.407  |
| Nippon India ETF Nifty 50 BeES                        |   2022 |       2 |        162.888  |
| Nippon India ETF Nifty 50 BeES                        |   2022 |       3 |        162.912  |
| Nippon India ETF Nifty 50 BeES                        |   2022 |       4 |        164.554  |
| Nippon India ETF Nifty 50 BeES                        |   2022 |       5 |        160.127  |
| Nippon India ETF Nifty 50 BeES                        |   2022 |       6 |        156.153  |
| Nippon India ETF Nifty 50 BeES                        |   2022 |       7 |        158.711  |
| Nippon India ETF Nifty 50 BeES                        |   2022 |       8 |        160.731  |
| Nippon India ETF Nifty 50 BeES                        |   2022 |       9 |        162.62   |
| Nippon India ETF Nifty 50 BeES                        |   2022 |      10 |        158.875  |
| Nippon India ETF Nifty 50 BeES                        |   2022 |      11 |        156.637  |
| Nippon India ETF Nifty 50 BeES                        |   2022 |      12 |        163.052  |
| Nippon India ETF Nifty 50 BeES                        |   2023 |       1 |        170.67   |
| Nippon India ETF Nifty 50 BeES                        |   2023 |       2 |        176.731  |
| Nippon India ETF Nifty 50 BeES                        |   2023 |       3 |        185      |
| Nippon India ETF Nifty 50 BeES                        |   2023 |       4 |        189.421  |
| Nippon India ETF Nifty 50 BeES                        |   2023 |       5 |        187.977  |
| Nippon India ETF Nifty 50 BeES                        |   2023 |       6 |        203.053  |
| Nippon India ETF Nifty 50 BeES                        |   2023 |       7 |        210.246  |
| Nippon India ETF Nifty 50 BeES                        |   2023 |       8 |        214.663  |
| Nippon India ETF Nifty 50 BeES                        |   2023 |       9 |        211.307  |
| Nippon India ETF Nifty 50 BeES                        |   2023 |      10 |        208.284  |
| Nippon India ETF Nifty 50 BeES                        |   2023 |      11 |        221.164  |
| Nippon India ETF Nifty 50 BeES                        |   2023 |      12 |        223.067  |
| Nippon India ETF Nifty 50 BeES                        |   2024 |       1 |        221.88   |
| Nippon India ETF Nifty 50 BeES                        |   2024 |       2 |        218.255  |
| Nippon India ETF Nifty 50 BeES                        |   2024 |       3 |        220.626  |
| Nippon India ETF Nifty 50 BeES                        |   2024 |       4 |        225.046  |
| Nippon India ETF Nifty 50 BeES                        |   2024 |       5 |        225.034  |
| Nippon India ETF Nifty 50 BeES                        |   2024 |       6 |        222.625  |
| Nippon India ETF Nifty 50 BeES                        |   2024 |       7 |        226.81   |
| Nippon India ETF Nifty 50 BeES                        |   2024 |       8 |        243.091  |
| Nippon India ETF Nifty 50 BeES                        |   2024 |       9 |        247.151  |
| Nippon India ETF Nifty 50 BeES                        |   2024 |      10 |        248.403  |
| Nippon India ETF Nifty 50 BeES                        |   2024 |      11 |        255.421  |
| Nippon India ETF Nifty 50 BeES                        |   2024 |      12 |        247.857  |
| Nippon India ETF Nifty 50 BeES                        |   2025 |       1 |        249.679  |
| Nippon India ETF Nifty 50 BeES                        |   2025 |       2 |        258.82   |
| Nippon India ETF Nifty 50 BeES                        |   2025 |       3 |        262.298  |
| Nippon India ETF Nifty 50 BeES                        |   2025 |       4 |        263.804  |
| Nippon India ETF Nifty 50 BeES                        |   2025 |       5 |        259.059  |
| Nippon India ETF Nifty 50 BeES                        |   2025 |       6 |        265.612  |
| Nippon India ETF Nifty 50 BeES                        |   2025 |       7 |        282.754  |
| Nippon India ETF Nifty 50 BeES                        |   2025 |       8 |        293.39   |
| Nippon India ETF Nifty 50 BeES                        |   2025 |       9 |        293.24   |
| Nippon India ETF Nifty 50 BeES                        |   2025 |      10 |        291.941  |
| Nippon India ETF Nifty 50 BeES                        |   2025 |      11 |        303.792  |
| Nippon India ETF Nifty 50 BeES                        |   2025 |      12 |        314.418  |
| Nippon India ETF Nifty 50 BeES                        |   2026 |       1 |        326.706  |
| Nippon India ETF Nifty 50 BeES                        |   2026 |       2 |        327.498  |
| Nippon India ETF Nifty 50 BeES                        |   2026 |       3 |        323.083  |
| Nippon India ETF Nifty 50 BeES                        |   2026 |       4 |        321.537  |
| Nippon India ETF Nifty 50 BeES                        |   2026 |       5 |        326.399  |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2022 |       1 |         30.3266 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2022 |       2 |         30.7838 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2022 |       3 |         31.2528 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2022 |       4 |         32.0028 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2022 |       5 |         32.631  |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2022 |       6 |         32.4409 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2022 |       7 |         32.883  |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2022 |       8 |         33.0391 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2022 |       9 |         32.9029 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2022 |      10 |         33.2768 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2022 |      11 |         33.4726 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2022 |      12 |         33.687  |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2023 |       1 |         33.8326 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2023 |       2 |         33.972  |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2023 |       3 |         33.8824 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2023 |       4 |         33.6274 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2023 |       5 |         33.4854 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2023 |       6 |         33.8869 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2023 |       7 |         33.4164 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2023 |       8 |         32.7163 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2023 |       9 |         32.5013 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2023 |      10 |         32.354  |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2023 |      11 |         32.4424 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2023 |      12 |         32.3871 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2024 |       1 |         31.9305 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2024 |       2 |         31.5116 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2024 |       3 |         31.8708 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2024 |       4 |         32.0678 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2024 |       5 |         32.2071 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2024 |       6 |         31.8383 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2024 |       7 |         32.0447 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2024 |       8 |         32.6807 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2024 |       9 |         33.032  |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2024 |      10 |         33.6878 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2024 |      11 |         34.6701 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2024 |      12 |         34.6865 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2025 |       1 |         34.5162 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2025 |       2 |         34.1098 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2025 |       3 |         33.4917 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2025 |       4 |         33.9203 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2025 |       5 |         34.1568 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2025 |       6 |         34.2219 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2025 |       7 |         34.1182 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2025 |       8 |         34.7824 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2025 |       9 |         35.0621 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2025 |      10 |         35.1597 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2025 |      11 |         35.8555 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2025 |      12 |         36.5452 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2026 |       1 |         37.1215 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2026 |       2 |         37.3361 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2026 |       3 |         37.1525 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2026 |       4 |         37.1062 |
| Nippon India Gilt Securities Fund - Regular - Growth  |   2026 |       5 |         37.485  |
| Nippon India Large Cap Fund - Direct - Growth         |   2022 |       1 |         46.1369 |
| Nippon India Large Cap Fund - Direct - Growth         |   2022 |       2 |         47.8156 |
| Nippon India Large Cap Fund - Direct - Growth         |   2022 |       3 |         48.9004 |
| Nippon India Large Cap Fund - Direct - Growth         |   2022 |       4 |         51.0257 |
| Nippon India Large Cap Fund - Direct - Growth         |   2022 |       5 |         52.3622 |
| Nippon India Large Cap Fund - Direct - Growth         |   2022 |       6 |         52.981  |
| Nippon India Large Cap Fund - Direct - Growth         |   2022 |       7 |         51.5161 |
| Nippon India Large Cap Fund - Direct - Growth         |   2022 |       8 |         53.7836 |
| Nippon India Large Cap Fund - Direct - Growth         |   2022 |       9 |         54.8647 |
| Nippon India Large Cap Fund - Direct - Growth         |   2022 |      10 |         54.5951 |
| Nippon India Large Cap Fund - Direct - Growth         |   2022 |      11 |         53.3533 |
| Nippon India Large Cap Fund - Direct - Growth         |   2022 |      12 |         54.0255 |
| Nippon India Large Cap Fund - Direct - Growth         |   2023 |       1 |         53.44   |
| Nippon India Large Cap Fund - Direct - Growth         |   2023 |       2 |         52.9425 |
| Nippon India Large Cap Fund - Direct - Growth         |   2023 |       3 |         53.0847 |
| Nippon India Large Cap Fund - Direct - Growth         |   2023 |       4 |         51.5809 |
| Nippon India Large Cap Fund - Direct - Growth         |   2023 |       5 |         51.8692 |
| Nippon India Large Cap Fund - Direct - Growth         |   2023 |       6 |         51.1678 |
| Nippon India Large Cap Fund - Direct - Growth         |   2023 |       7 |         54.9934 |
| Nippon India Large Cap Fund - Direct - Growth         |   2023 |       8 |         59.036  |
| Nippon India Large Cap Fund - Direct - Growth         |   2023 |       9 |         58.784  |
| Nippon India Large Cap Fund - Direct - Growth         |   2023 |      10 |         61.1726 |
| Nippon India Large Cap Fund - Direct - Growth         |   2023 |      11 |         59.4584 |
| Nippon India Large Cap Fund - Direct - Growth         |   2023 |      12 |         58.2032 |
| Nippon India Large Cap Fund - Direct - Growth         |   2024 |       1 |         53.4305 |
| Nippon India Large Cap Fund - Direct - Growth         |   2024 |       2 |         52.8127 |
| Nippon India Large Cap Fund - Direct - Growth         |   2024 |       3 |         52.9501 |
| Nippon India Large Cap Fund - Direct - Growth         |   2024 |       4 |         54.4871 |
| Nippon India Large Cap Fund - Direct - Growth         |   2024 |       5 |         55.8649 |
| Nippon India Large Cap Fund - Direct - Growth         |   2024 |       6 |         58.1003 |
| Nippon India Large Cap Fund - Direct - Growth         |   2024 |       7 |         61.8616 |
| Nippon India Large Cap Fund - Direct - Growth         |   2024 |       8 |         62.1251 |
| Nippon India Large Cap Fund - Direct - Growth         |   2024 |       9 |         61.7408 |
| Nippon India Large Cap Fund - Direct - Growth         |   2024 |      10 |         60.0366 |
| Nippon India Large Cap Fund - Direct - Growth         |   2024 |      11 |         59.2215 |
| Nippon India Large Cap Fund - Direct - Growth         |   2024 |      12 |         57.4828 |
| Nippon India Large Cap Fund - Direct - Growth         |   2025 |       1 |         62.2575 |
| Nippon India Large Cap Fund - Direct - Growth         |   2025 |       2 |         65.994  |
| Nippon India Large Cap Fund - Direct - Growth         |   2025 |       3 |         68.0345 |
| Nippon India Large Cap Fund - Direct - Growth         |   2025 |       4 |         70.175  |
| Nippon India Large Cap Fund - Direct - Growth         |   2025 |       5 |         70.6346 |
| Nippon India Large Cap Fund - Direct - Growth         |   2025 |       6 |         72.5956 |
| Nippon India Large Cap Fund - Direct - Growth         |   2025 |       7 |         75.264  |
| Nippon India Large Cap Fund - Direct - Growth         |   2025 |       8 |         77.5039 |
| Nippon India Large Cap Fund - Direct - Growth         |   2025 |       9 |         78.0391 |
| Nippon India Large Cap Fund - Direct - Growth         |   2025 |      10 |         82.8465 |
| Nippon India Large Cap Fund - Direct - Growth         |   2025 |      11 |         81.5502 |
| Nippon India Large Cap Fund - Direct - Growth         |   2025 |      12 |         79.3529 |
| Nippon India Large Cap Fund - Direct - Growth         |   2026 |       1 |         82.5268 |
| Nippon India Large Cap Fund - Direct - Growth         |   2026 |       2 |         86.2047 |
| Nippon India Large Cap Fund - Direct - Growth         |   2026 |       3 |         86.0774 |
| Nippon India Large Cap Fund - Direct - Growth         |   2026 |       4 |         86.1852 |
| Nippon India Large Cap Fund - Direct - Growth         |   2026 |       5 |         89.4791 |
| Nippon India Large Cap Fund - Regular - Growth        |   2022 |       1 |         44.0709 |
| Nippon India Large Cap Fund - Regular - Growth        |   2022 |       2 |         46.2249 |
| Nippon India Large Cap Fund - Regular - Growth        |   2022 |       3 |         47.6934 |
| Nippon India Large Cap Fund - Regular - Growth        |   2022 |       4 |         51.4092 |
| Nippon India Large Cap Fund - Regular - Growth        |   2022 |       5 |         54.1248 |
| Nippon India Large Cap Fund - Regular - Growth        |   2022 |       6 |         53.1347 |
| Nippon India Large Cap Fund - Regular - Growth        |   2022 |       7 |         54.1228 |
| Nippon India Large Cap Fund - Regular - Growth        |   2022 |       8 |         53.0576 |
| Nippon India Large Cap Fund - Regular - Growth        |   2022 |       9 |         53.1992 |
| Nippon India Large Cap Fund - Regular - Growth        |   2022 |      10 |         53.2597 |
| Nippon India Large Cap Fund - Regular - Growth        |   2022 |      11 |         50.9291 |
| Nippon India Large Cap Fund - Regular - Growth        |   2022 |      12 |         50.7311 |
| Nippon India Large Cap Fund - Regular - Growth        |   2023 |       1 |         55.3833 |
| Nippon India Large Cap Fund - Regular - Growth        |   2023 |       2 |         58.66   |
| Nippon India Large Cap Fund - Regular - Growth        |   2023 |       3 |         60.9074 |
| Nippon India Large Cap Fund - Regular - Growth        |   2023 |       4 |         62.9627 |
| Nippon India Large Cap Fund - Regular - Growth        |   2023 |       5 |         60.7248 |
| Nippon India Large Cap Fund - Regular - Growth        |   2023 |       6 |         64.7208 |
| Nippon India Large Cap Fund - Regular - Growth        |   2023 |       7 |         68.4302 |
| Nippon India Large Cap Fund - Regular - Growth        |   2023 |       8 |         72.2795 |
| Nippon India Large Cap Fund - Regular - Growth        |   2023 |       9 |         72.8241 |
| Nippon India Large Cap Fund - Regular - Growth        |   2023 |      10 |         75.7593 |
| Nippon India Large Cap Fund - Regular - Growth        |   2023 |      11 |         78.2496 |
| Nippon India Large Cap Fund - Regular - Growth        |   2023 |      12 |         80.2421 |
| Nippon India Large Cap Fund - Regular - Growth        |   2024 |       1 |         80.1568 |
| Nippon India Large Cap Fund - Regular - Growth        |   2024 |       2 |         78.8944 |
| Nippon India Large Cap Fund - Regular - Growth        |   2024 |       3 |         77.5857 |
| Nippon India Large Cap Fund - Regular - Growth        |   2024 |       4 |         76.0818 |
| Nippon India Large Cap Fund - Regular - Growth        |   2024 |       5 |         73.6776 |
| Nippon India Large Cap Fund - Regular - Growth        |   2024 |       6 |         70.587  |
| Nippon India Large Cap Fund - Regular - Growth        |   2024 |       7 |         68.7875 |
| Nippon India Large Cap Fund - Regular - Growth        |   2024 |       8 |         69.9839 |
| Nippon India Large Cap Fund - Regular - Growth        |   2024 |       9 |         72.9117 |
| Nippon India Large Cap Fund - Regular - Growth        |   2024 |      10 |         72.9762 |
| Nippon India Large Cap Fund - Regular - Growth        |   2024 |      11 |         77.8543 |
| Nippon India Large Cap Fund - Regular - Growth        |   2024 |      12 |         79.0401 |
| Nippon India Large Cap Fund - Regular - Growth        |   2025 |       1 |         77.3875 |
| Nippon India Large Cap Fund - Regular - Growth        |   2025 |       2 |         78.7748 |
| Nippon India Large Cap Fund - Regular - Growth        |   2025 |       3 |         79.0729 |
| Nippon India Large Cap Fund - Regular - Growth        |   2025 |       4 |         79.2676 |
| Nippon India Large Cap Fund - Regular - Growth        |   2025 |       5 |         81.4768 |
| Nippon India Large Cap Fund - Regular - Growth        |   2025 |       6 |         89.3215 |
| Nippon India Large Cap Fund - Regular - Growth        |   2025 |       7 |         90.7414 |
| Nippon India Large Cap Fund - Regular - Growth        |   2025 |       8 |         94.5986 |
| Nippon India Large Cap Fund - Regular - Growth        |   2025 |       9 |         94.7015 |
| Nippon India Large Cap Fund - Regular - Growth        |   2025 |      10 |         97.4038 |
| Nippon India Large Cap Fund - Regular - Growth        |   2025 |      11 |         97.4104 |
| Nippon India Large Cap Fund - Regular - Growth        |   2025 |      12 |         96.0467 |
| Nippon India Large Cap Fund - Regular - Growth        |   2026 |       1 |         97.5942 |
| Nippon India Large Cap Fund - Regular - Growth        |   2026 |       2 |        100.429  |
| Nippon India Large Cap Fund - Regular - Growth        |   2026 |       3 |        104.159  |
| Nippon India Large Cap Fund - Regular - Growth        |   2026 |       4 |        111.996  |
| Nippon India Large Cap Fund - Regular - Growth        |   2026 |       5 |        109.563  |
| Nippon India Small Cap Fund - Regular - Growth        |   2022 |       1 |         62.3008 |
| Nippon India Small Cap Fund - Regular - Growth        |   2022 |       2 |         62.915  |
| Nippon India Small Cap Fund - Regular - Growth        |   2022 |       3 |         67.0563 |
| Nippon India Small Cap Fund - Regular - Growth        |   2022 |       4 |         71.0442 |
| Nippon India Small Cap Fund - Regular - Growth        |   2022 |       5 |         75.8891 |
| Nippon India Small Cap Fund - Regular - Growth        |   2022 |       6 |         72.6024 |
| Nippon India Small Cap Fund - Regular - Growth        |   2022 |       7 |         70.4813 |
| Nippon India Small Cap Fund - Regular - Growth        |   2022 |       8 |         71.9688 |
| Nippon India Small Cap Fund - Regular - Growth        |   2022 |       9 |         77.5312 |
| Nippon India Small Cap Fund - Regular - Growth        |   2022 |      10 |         78.0881 |
| Nippon India Small Cap Fund - Regular - Growth        |   2022 |      11 |         88.6666 |
| Nippon India Small Cap Fund - Regular - Growth        |   2022 |      12 |         93.5058 |
| Nippon India Small Cap Fund - Regular - Growth        |   2023 |       1 |        109.089  |
| Nippon India Small Cap Fund - Regular - Growth        |   2023 |       2 |        116.263  |
| Nippon India Small Cap Fund - Regular - Growth        |   2023 |       3 |        111.345  |
| Nippon India Small Cap Fund - Regular - Growth        |   2023 |       4 |        118.015  |
| Nippon India Small Cap Fund - Regular - Growth        |   2023 |       5 |        111.43   |
| Nippon India Small Cap Fund - Regular - Growth        |   2023 |       6 |        102.443  |
| Nippon India Small Cap Fund - Regular - Growth        |   2023 |       7 |        105.581  |
| Nippon India Small Cap Fund - Regular - Growth        |   2023 |       8 |        100.19   |
| Nippon India Small Cap Fund - Regular - Growth        |   2023 |       9 |        105.507  |
| Nippon India Small Cap Fund - Regular - Growth        |   2023 |      10 |        110.529  |
| Nippon India Small Cap Fund - Regular - Growth        |   2023 |      11 |        114.87   |
| Nippon India Small Cap Fund - Regular - Growth        |   2023 |      12 |        102.748  |
| Nippon India Small Cap Fund - Regular - Growth        |   2024 |       1 |        101.359  |
| Nippon India Small Cap Fund - Regular - Growth        |   2024 |       2 |        101.91   |
| Nippon India Small Cap Fund - Regular - Growth        |   2024 |       3 |        106.679  |
| Nippon India Small Cap Fund - Regular - Growth        |   2024 |       4 |        117.847  |
| Nippon India Small Cap Fund - Regular - Growth        |   2024 |       5 |        115.017  |
| Nippon India Small Cap Fund - Regular - Growth        |   2024 |       6 |        119.047  |
| Nippon India Small Cap Fund - Regular - Growth        |   2024 |       7 |        117.253  |
| Nippon India Small Cap Fund - Regular - Growth        |   2024 |       8 |        119.248  |
| Nippon India Small Cap Fund - Regular - Growth        |   2024 |       9 |        112.911  |
| Nippon India Small Cap Fund - Regular - Growth        |   2024 |      10 |        109.18   |
| Nippon India Small Cap Fund - Regular - Growth        |   2024 |      11 |        109.517  |
| Nippon India Small Cap Fund - Regular - Growth        |   2024 |      12 |        107.512  |
| Nippon India Small Cap Fund - Regular - Growth        |   2025 |       1 |        109.489  |
| Nippon India Small Cap Fund - Regular - Growth        |   2025 |       2 |        116.07   |
| Nippon India Small Cap Fund - Regular - Growth        |   2025 |       3 |        116.463  |
| Nippon India Small Cap Fund - Regular - Growth        |   2025 |       4 |        122.172  |
| Nippon India Small Cap Fund - Regular - Growth        |   2025 |       5 |        120.068  |
| Nippon India Small Cap Fund - Regular - Growth        |   2025 |       6 |        112.536  |
| Nippon India Small Cap Fund - Regular - Growth        |   2025 |       7 |        103.907  |
| Nippon India Small Cap Fund - Regular - Growth        |   2025 |       8 |        101.73   |
| Nippon India Small Cap Fund - Regular - Growth        |   2025 |       9 |        104.286  |
| Nippon India Small Cap Fund - Regular - Growth        |   2025 |      10 |        105.655  |
| Nippon India Small Cap Fund - Regular - Growth        |   2025 |      11 |        110.535  |
| Nippon India Small Cap Fund - Regular - Growth        |   2025 |      12 |        110.645  |
| Nippon India Small Cap Fund - Regular - Growth        |   2026 |       1 |        108.082  |
| Nippon India Small Cap Fund - Regular - Growth        |   2026 |       2 |        100.536  |
| Nippon India Small Cap Fund - Regular - Growth        |   2026 |       3 |        110.78   |
| Nippon India Small Cap Fund - Regular - Growth        |   2026 |       4 |        125.79   |
| Nippon India Small Cap Fund - Regular - Growth        |   2026 |       5 |        135.611  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2022 |       1 |         58.7945 |
| SBI Bluechip Fund - Direct Plan - Growth              |   2022 |       2 |         60.3818 |
| SBI Bluechip Fund - Direct Plan - Growth              |   2022 |       3 |         59.0773 |
| SBI Bluechip Fund - Direct Plan - Growth              |   2022 |       4 |         60.1732 |
| SBI Bluechip Fund - Direct Plan - Growth              |   2022 |       5 |         62.8803 |
| SBI Bluechip Fund - Direct Plan - Growth              |   2022 |       6 |         62.7211 |
| SBI Bluechip Fund - Direct Plan - Growth              |   2022 |       7 |         64.3436 |
| SBI Bluechip Fund - Direct Plan - Growth              |   2022 |       8 |         66.0381 |
| SBI Bluechip Fund - Direct Plan - Growth              |   2022 |       9 |         66.3692 |
| SBI Bluechip Fund - Direct Plan - Growth              |   2022 |      10 |         64.4048 |
| SBI Bluechip Fund - Direct Plan - Growth              |   2022 |      11 |         63.1493 |
| SBI Bluechip Fund - Direct Plan - Growth              |   2022 |      12 |         67.101  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2023 |       1 |         71.3078 |
| SBI Bluechip Fund - Direct Plan - Growth              |   2023 |       2 |         74.5768 |
| SBI Bluechip Fund - Direct Plan - Growth              |   2023 |       3 |         80.2166 |
| SBI Bluechip Fund - Direct Plan - Growth              |   2023 |       4 |         81.4576 |
| SBI Bluechip Fund - Direct Plan - Growth              |   2023 |       5 |         88.4767 |
| SBI Bluechip Fund - Direct Plan - Growth              |   2023 |       6 |         91.4508 |
| SBI Bluechip Fund - Direct Plan - Growth              |   2023 |       7 |         90.1543 |
| SBI Bluechip Fund - Direct Plan - Growth              |   2023 |       8 |         88.8519 |
| SBI Bluechip Fund - Direct Plan - Growth              |   2023 |       9 |         86.3233 |
| SBI Bluechip Fund - Direct Plan - Growth              |   2023 |      10 |         86.8783 |
| SBI Bluechip Fund - Direct Plan - Growth              |   2023 |      11 |         91.9895 |
| SBI Bluechip Fund - Direct Plan - Growth              |   2023 |      12 |         98.8382 |
| SBI Bluechip Fund - Direct Plan - Growth              |   2024 |       1 |        101.812  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2024 |       2 |        106.093  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2024 |       3 |        110.795  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2024 |       4 |        113.669  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2024 |       5 |        120.494  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2024 |       6 |        116.511  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2024 |       7 |        113.097  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2024 |       8 |        111.126  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2024 |       9 |        112.902  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2024 |      10 |        115.287  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2024 |      11 |        116.509  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2024 |      12 |        117.239  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2025 |       1 |        119.558  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2025 |       2 |        124.284  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2025 |       3 |        128.234  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2025 |       4 |        129.4    |
| SBI Bluechip Fund - Direct Plan - Growth              |   2025 |       5 |        125.385  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2025 |       6 |        126.463  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2025 |       7 |        128.309  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2025 |       8 |        126.371  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2025 |       9 |        125.776  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2025 |      10 |        129.048  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2025 |      11 |        128.294  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2025 |      12 |        130.75   |
| SBI Bluechip Fund - Direct Plan - Growth              |   2026 |       1 |        132.402  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2026 |       2 |        135.592  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2026 |       3 |        136.625  |
| SBI Bluechip Fund - Direct Plan - Growth              |   2026 |       4 |        135.52   |
| SBI Bluechip Fund - Direct Plan - Growth              |   2026 |       5 |        134.46   |
| SBI Bluechip Fund - Regular Plan - Growth             |   2022 |       1 |         55.0386 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2022 |       2 |         52.4312 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2022 |       3 |         50.837  |
| SBI Bluechip Fund - Regular Plan - Growth             |   2022 |       4 |         51.8935 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2022 |       5 |         51.8872 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2022 |       6 |         52.6761 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2022 |       7 |         52.694  |
| SBI Bluechip Fund - Regular Plan - Growth             |   2022 |       8 |         53.8042 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2022 |       9 |         56.5077 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2022 |      10 |         57.8759 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2022 |      11 |         60.8367 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2022 |      12 |         61.376  |
| SBI Bluechip Fund - Regular Plan - Growth             |   2023 |       1 |         60.2519 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2023 |       2 |         61.238  |
| SBI Bluechip Fund - Regular Plan - Growth             |   2023 |       3 |         64.5104 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2023 |       4 |         67.3629 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2023 |       5 |         66.1658 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2023 |       6 |         69.5883 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2023 |       7 |         70.9299 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2023 |       8 |         73.7764 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2023 |       9 |         73.9769 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2023 |      10 |         71.2205 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2023 |      11 |         72.9876 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2023 |      12 |         72.123  |
| SBI Bluechip Fund - Regular Plan - Growth             |   2024 |       1 |         68.299  |
| SBI Bluechip Fund - Regular Plan - Growth             |   2024 |       2 |         66.7861 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2024 |       3 |         67.5201 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2024 |       4 |         69.2337 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2024 |       5 |         72.8752 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2024 |       6 |         73.6868 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2024 |       7 |         73.7028 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2024 |       8 |         72.6418 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2024 |       9 |         73.0163 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2024 |      10 |         72.5559 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2024 |      11 |         71.4867 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2024 |      12 |         74.4956 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2025 |       1 |         76.904  |
| SBI Bluechip Fund - Regular Plan - Growth             |   2025 |       2 |         78.6389 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2025 |       3 |         81.9144 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2025 |       4 |         84.2085 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2025 |       5 |         88.8723 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2025 |       6 |         99.6928 |
| SBI Bluechip Fund - Regular Plan - Growth             |   2025 |       7 |        106.254  |
| SBI Bluechip Fund - Regular Plan - Growth             |   2025 |       8 |        105.156  |
| SBI Bluechip Fund - Regular Plan - Growth             |   2025 |       9 |        110.615  |
| SBI Bluechip Fund - Regular Plan - Growth             |   2025 |      10 |        107.068  |
| SBI Bluechip Fund - Regular Plan - Growth             |   2025 |      11 |        113.51   |
| SBI Bluechip Fund - Regular Plan - Growth             |   2025 |      12 |        121.243  |
| SBI Bluechip Fund - Regular Plan - Growth             |   2026 |       1 |        126.863  |
| SBI Bluechip Fund - Regular Plan - Growth             |   2026 |       2 |        124.834  |
| SBI Bluechip Fund - Regular Plan - Growth             |   2026 |       3 |        130.049  |
| SBI Bluechip Fund - Regular Plan - Growth             |   2026 |       4 |        137.677  |
| SBI Bluechip Fund - Regular Plan - Growth             |   2026 |       5 |        148.172  |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2022 |       1 |         42.4326 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2022 |       2 |         42.443  |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2022 |       3 |         42.2394 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2022 |       4 |         42.6578 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2022 |       5 |         42.7899 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2022 |       6 |         43.6172 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2022 |       7 |         43.9626 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2022 |       8 |         44.1839 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2022 |       9 |         43.9745 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2022 |      10 |         43.3531 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2022 |      11 |         43.3747 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2022 |      12 |         43.5756 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2023 |       1 |         43.9414 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2023 |       2 |         44.2128 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2023 |       3 |         44.0851 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2023 |       4 |         45.0223 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2023 |       5 |         45.657  |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2023 |       6 |         45.7222 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2023 |       7 |         46.2673 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2023 |       8 |         46.6332 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2023 |       9 |         47.583  |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2023 |      10 |         47.7963 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2023 |      11 |         48.305  |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2023 |      12 |         48.5496 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2024 |       1 |         48.7116 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2024 |       2 |         49.3747 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2024 |       3 |         49.3987 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2024 |       4 |         49.2451 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2024 |       5 |         49.8077 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2024 |       6 |         50.8264 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2024 |       7 |         50.7572 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2024 |       8 |         51.4342 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2024 |       9 |         52.2247 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2024 |      10 |         52.1228 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2024 |      11 |         51.6883 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2024 |      12 |         51.2588 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2025 |       1 |         51.0947 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2025 |       2 |         50.733  |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2025 |       3 |         50.4472 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2025 |       4 |         50.5416 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2025 |       5 |         51.0823 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2025 |       6 |         51.4754 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2025 |       7 |         51.3266 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2025 |       8 |         52.179  |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2025 |       9 |         52.8083 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2025 |      10 |         52.994  |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2025 |      11 |         53.4804 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2025 |      12 |         53.7532 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2026 |       1 |         54.3601 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2026 |       2 |         54.7665 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2026 |       3 |         54.627  |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2026 |       4 |         54.7349 |
| SBI Magnum Gilt Fund - Regular Plan - Growth          |   2026 |       5 |         54.4541 |
| SBI Small Cap Fund - Direct Plan - Growth             |   2022 |       1 |         95.5875 |
| SBI Small Cap Fund - Direct Plan - Growth             |   2022 |       2 |         92.2937 |
| SBI Small Cap Fund - Direct Plan - Growth             |   2022 |       3 |         91.8838 |
| SBI Small Cap Fund - Direct Plan - Growth             |   2022 |       4 |         91.2135 |
| SBI Small Cap Fund - Direct Plan - Growth             |   2022 |       5 |        100.293  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2022 |       6 |        103.762  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2022 |       7 |        109.832  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2022 |       8 |        117.588  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2022 |       9 |        116.72   |
| SBI Small Cap Fund - Direct Plan - Growth             |   2022 |      10 |        115.908  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2022 |      11 |        124.892  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2022 |      12 |        145.918  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2023 |       1 |        154.561  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2023 |       2 |        145.99   |
| SBI Small Cap Fund - Direct Plan - Growth             |   2023 |       3 |        143.669  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2023 |       4 |        130.439  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2023 |       5 |        118.134  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2023 |       6 |        107.771  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2023 |       7 |        107.478  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2023 |       8 |        102.972  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2023 |       9 |         99.1951 |
| SBI Small Cap Fund - Direct Plan - Growth             |   2023 |      10 |        103.672  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2023 |      11 |        109.325  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2023 |      12 |        114.096  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2024 |       1 |        127.483  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2024 |       2 |        119.677  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2024 |       3 |        110.288  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2024 |       4 |        108.846  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2024 |       5 |        115.344  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2024 |       6 |        113.122  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2024 |       7 |        118.225  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2024 |       8 |        123.347  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2024 |       9 |        126.993  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2024 |      10 |        123.434  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2024 |      11 |        115.341  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2024 |      12 |        100.988  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2025 |       1 |        103.375  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2025 |       2 |        108.661  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2025 |       3 |        102.956  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2025 |       4 |         94.6978 |
| SBI Small Cap Fund - Direct Plan - Growth             |   2025 |       5 |         94.4866 |
| SBI Small Cap Fund - Direct Plan - Growth             |   2025 |       6 |         93.0492 |
| SBI Small Cap Fund - Direct Plan - Growth             |   2025 |       7 |         92.8845 |
| SBI Small Cap Fund - Direct Plan - Growth             |   2025 |       8 |         91.1984 |
| SBI Small Cap Fund - Direct Plan - Growth             |   2025 |       9 |         90.677  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2025 |      10 |         81.8853 |
| SBI Small Cap Fund - Direct Plan - Growth             |   2025 |      11 |         83.961  |
| SBI Small Cap Fund - Direct Plan - Growth             |   2025 |      12 |         93.4877 |
| SBI Small Cap Fund - Direct Plan - Growth             |   2026 |       1 |         89.4147 |
| SBI Small Cap Fund - Direct Plan - Growth             |   2026 |       2 |         89.9668 |
| SBI Small Cap Fund - Direct Plan - Growth             |   2026 |       3 |         95.3254 |
| SBI Small Cap Fund - Direct Plan - Growth             |   2026 |       4 |         98.5555 |
| SBI Small Cap Fund - Direct Plan - Growth             |   2026 |       5 |        101.639  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2022 |       1 |         98.9478 |
| SBI Small Cap Fund - Regular Plan - Growth            |   2022 |       2 |        109.555  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2022 |       3 |        111.232  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2022 |       4 |        107.057  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2022 |       5 |         98.7202 |
| SBI Small Cap Fund - Regular Plan - Growth            |   2022 |       6 |        100.277  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2022 |       7 |        104.551  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2022 |       8 |        106.264  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2022 |       9 |        116.385  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2022 |      10 |        119.866  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2022 |      11 |        126.998  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2022 |      12 |        130.959  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2023 |       1 |        128.704  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2023 |       2 |        139.249  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2023 |       3 |        132.089  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2023 |       4 |        150.811  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2023 |       5 |        154.395  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2023 |       6 |        149.375  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2023 |       7 |        160.205  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2023 |       8 |        184.459  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2023 |       9 |        212.408  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2023 |      10 |        215.755  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2023 |      11 |        198.573  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2023 |      12 |        191.834  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2024 |       1 |        205.951  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2024 |       2 |        210.952  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2024 |       3 |        200.077  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2024 |       4 |        181.884  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2024 |       5 |        192.598  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2024 |       6 |        211.027  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2024 |       7 |        210.188  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2024 |       8 |        214.236  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2024 |       9 |        215.132  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2024 |      10 |        195.166  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2024 |      11 |        187.11   |
| SBI Small Cap Fund - Regular Plan - Growth            |   2024 |      12 |        188.735  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2025 |       1 |        198.591  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2025 |       2 |        204.218  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2025 |       3 |        204.002  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2025 |       4 |        186.005  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2025 |       5 |        167.247  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2025 |       6 |        173.253  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2025 |       7 |        189.354  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2025 |       8 |        196.711  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2025 |       9 |        215.968  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2025 |      10 |        224.512  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2025 |      11 |        231.27   |
| SBI Small Cap Fund - Regular Plan - Growth            |   2025 |      12 |        249.321  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2026 |       1 |        260.812  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2026 |       2 |        244.005  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2026 |       3 |        263.973  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2026 |       4 |        277.728  |
| SBI Small Cap Fund - Regular Plan - Growth            |   2026 |       5 |        309.94   |
| UTI Flexi Cap Fund - Regular - Growth                 |   2022 |       1 |        183.077  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2022 |       2 |        176.947  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2022 |       3 |        174.673  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2022 |       4 |        171.09   |
| UTI Flexi Cap Fund - Regular - Growth                 |   2022 |       5 |        170.376  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2022 |       6 |        157.893  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2022 |       7 |        159.161  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2022 |       8 |        155.147  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2022 |       9 |        156.823  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2022 |      10 |        164.814  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2022 |      11 |        173.11   |
| UTI Flexi Cap Fund - Regular - Growth                 |   2022 |      12 |        175.849  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2023 |       1 |        171.541  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2023 |       2 |        176.691  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2023 |       3 |        190.853  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2023 |       4 |        196.389  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2023 |       5 |        194.701  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2023 |       6 |        190.988  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2023 |       7 |        188.201  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2023 |       8 |        189.313  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2023 |       9 |        179.719  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2023 |      10 |        182.242  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2023 |      11 |        181.333  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2023 |      12 |        184.117  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2024 |       1 |        194.565  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2024 |       2 |        212.813  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2024 |       3 |        228.648  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2024 |       4 |        222.905  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2024 |       5 |        235.968  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2024 |       6 |        237.989  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2024 |       7 |        246.021  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2024 |       8 |        232.125  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2024 |       9 |        257.382  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2024 |      10 |        254.335  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2024 |      11 |        264.35   |
| UTI Flexi Cap Fund - Regular - Growth                 |   2024 |      12 |        266.832  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2025 |       1 |        288.522  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2025 |       2 |        295.407  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2025 |       3 |        306.763  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2025 |       4 |        311.696  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2025 |       5 |        329.159  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2025 |       6 |        344.043  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2025 |       7 |        358.062  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2025 |       8 |        389.769  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2025 |       9 |        409.072  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2025 |      10 |        400.872  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2025 |      11 |        399.469  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2025 |      12 |        392.587  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2026 |       1 |        391.339  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2026 |       2 |        393.826  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2026 |       3 |        372.92   |
| UTI Flexi Cap Fund - Regular - Growth                 |   2026 |       4 |        376.022  |
| UTI Flexi Cap Fund - Regular - Growth                 |   2026 |       5 |        366.245  |
| UTI Mid Cap Fund - Regular - Growth                   |   2022 |       1 |        122.767  |
| UTI Mid Cap Fund - Regular - Growth                   |   2022 |       2 |        128.979  |
| UTI Mid Cap Fund - Regular - Growth                   |   2022 |       3 |        132.234  |
| UTI Mid Cap Fund - Regular - Growth                   |   2022 |       4 |        128.422  |
| UTI Mid Cap Fund - Regular - Growth                   |   2022 |       5 |        127.291  |
| UTI Mid Cap Fund - Regular - Growth                   |   2022 |       6 |        130.14   |
| UTI Mid Cap Fund - Regular - Growth                   |   2022 |       7 |        130.391  |
| UTI Mid Cap Fund - Regular - Growth                   |   2022 |       8 |        122.506  |
| UTI Mid Cap Fund - Regular - Growth                   |   2022 |       9 |        122.376  |
| UTI Mid Cap Fund - Regular - Growth                   |   2022 |      10 |        123.381  |
| UTI Mid Cap Fund - Regular - Growth                   |   2022 |      11 |        122.247  |
| UTI Mid Cap Fund - Regular - Growth                   |   2022 |      12 |        117.439  |
| UTI Mid Cap Fund - Regular - Growth                   |   2023 |       1 |        120.022  |
| UTI Mid Cap Fund - Regular - Growth                   |   2023 |       2 |        127.998  |
| UTI Mid Cap Fund - Regular - Growth                   |   2023 |       3 |        125.002  |
| UTI Mid Cap Fund - Regular - Growth                   |   2023 |       4 |        127.334  |
| UTI Mid Cap Fund - Regular - Growth                   |   2023 |       5 |        124.526  |
| UTI Mid Cap Fund - Regular - Growth                   |   2023 |       6 |        128.291  |
| UTI Mid Cap Fund - Regular - Growth                   |   2023 |       7 |        128.939  |
| UTI Mid Cap Fund - Regular - Growth                   |   2023 |       8 |        132.385  |
| UTI Mid Cap Fund - Regular - Growth                   |   2023 |       9 |        131.23   |
| UTI Mid Cap Fund - Regular - Growth                   |   2023 |      10 |        126.229  |
| UTI Mid Cap Fund - Regular - Growth                   |   2023 |      11 |        121.236  |
| UTI Mid Cap Fund - Regular - Growth                   |   2023 |      12 |        127.282  |
| UTI Mid Cap Fund - Regular - Growth                   |   2024 |       1 |        131.215  |
| UTI Mid Cap Fund - Regular - Growth                   |   2024 |       2 |        134.076  |
| UTI Mid Cap Fund - Regular - Growth                   |   2024 |       3 |        145.464  |
| UTI Mid Cap Fund - Regular - Growth                   |   2024 |       4 |        144.735  |
| UTI Mid Cap Fund - Regular - Growth                   |   2024 |       5 |        141.219  |
| UTI Mid Cap Fund - Regular - Growth                   |   2024 |       6 |        141.958  |
| UTI Mid Cap Fund - Regular - Growth                   |   2024 |       7 |        145.159  |
| UTI Mid Cap Fund - Regular - Growth                   |   2024 |       8 |        149.48   |
| UTI Mid Cap Fund - Regular - Growth                   |   2024 |       9 |        161.064  |
| UTI Mid Cap Fund - Regular - Growth                   |   2024 |      10 |        155.204  |
| UTI Mid Cap Fund - Regular - Growth                   |   2024 |      11 |        157.497  |
| UTI Mid Cap Fund - Regular - Growth                   |   2024 |      12 |        159.756  |
| UTI Mid Cap Fund - Regular - Growth                   |   2025 |       1 |        164.512  |
| UTI Mid Cap Fund - Regular - Growth                   |   2025 |       2 |        156.89   |
| UTI Mid Cap Fund - Regular - Growth                   |   2025 |       3 |        150.38   |
| UTI Mid Cap Fund - Regular - Growth                   |   2025 |       4 |        157.86   |
| UTI Mid Cap Fund - Regular - Growth                   |   2025 |       5 |        154.29   |
| UTI Mid Cap Fund - Regular - Growth                   |   2025 |       6 |        149.195  |
| UTI Mid Cap Fund - Regular - Growth                   |   2025 |       7 |        157.578  |
| UTI Mid Cap Fund - Regular - Growth                   |   2025 |       8 |        148.373  |
| UTI Mid Cap Fund - Regular - Growth                   |   2025 |       9 |        149.819  |
| UTI Mid Cap Fund - Regular - Growth                   |   2025 |      10 |        143.925  |
| UTI Mid Cap Fund - Regular - Growth                   |   2025 |      11 |        126.631  |
| UTI Mid Cap Fund - Regular - Growth                   |   2025 |      12 |        135.793  |
| UTI Mid Cap Fund - Regular - Growth                   |   2026 |       1 |        142.222  |
| UTI Mid Cap Fund - Regular - Growth                   |   2026 |       2 |        137.509  |
| UTI Mid Cap Fund - Regular - Growth                   |   2026 |       3 |        142.423  |
| UTI Mid Cap Fund - Regular - Growth                   |   2026 |       4 |        127.302  |
| UTI Mid Cap Fund - Regular - Growth                   |   2026 |       5 |        125.481  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2022 |       1 |         91.238  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2022 |       2 |         92.1976 |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2022 |       3 |         85.708  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2022 |       4 |         88.3619 |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2022 |       5 |         92.93   |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2022 |       6 |         92.5849 |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2022 |       7 |         91.5368 |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2022 |       8 |         93.7864 |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2022 |       9 |         94.916  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2022 |      10 |         95.1083 |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2022 |      11 |        103.967  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2022 |      12 |        102.076  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2023 |       1 |        101.443  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2023 |       2 |        102.109  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2023 |       3 |        104.034  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2023 |       4 |        105.157  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2023 |       5 |        106.917  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2023 |       6 |        112.075  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2023 |       7 |        113.618  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2023 |       8 |        113.784  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2023 |       9 |        117.865  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2023 |      10 |        120.775  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2023 |      11 |        124.328  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2023 |      12 |        129.012  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2024 |       1 |        130.258  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2024 |       2 |        130.417  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2024 |       3 |        130.435  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2024 |       4 |        127.927  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2024 |       5 |        129.125  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2024 |       6 |        127.548  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2024 |       7 |        124.542  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2024 |       8 |        125.266  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2024 |       9 |        126.963  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2024 |      10 |        132.394  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2024 |      11 |        129.638  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2024 |      12 |        130.544  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2025 |       1 |        141.211  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2025 |       2 |        141.451  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2025 |       3 |        146.342  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2025 |       4 |        153.841  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2025 |       5 |        155.526  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2025 |       6 |        159.026  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2025 |       7 |        159.212  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2025 |       8 |        158.03   |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2025 |       9 |        164.845  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2025 |      10 |        163.27   |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2025 |      11 |        169.429  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2025 |      12 |        173.917  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2026 |       1 |        177.421  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2026 |       2 |        181.13   |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2026 |       3 |        180.555  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2026 |       4 |        179.774  |
| UTI Nifty 50 Index Fund - Regular - Growth            |   2026 |       5 |        184.514  |

---

## Query 3: SIP YoY Growth
*Computes the Year-on-Year growth rate of SIP inflows comparing 2024 vs 2025.*

### SQL Query
```sql
WITH sip_yearly AS (
    SELECT
        d.year,
        SUM(t.amount_inr) AS total_sip_amount
    FROM fact_transactions t
    JOIN dim_date d ON t.transaction_date = d.date_id
    WHERE t.transaction_type = 'SIP'
    GROUP BY d.year
)
SELECT
    curr.year AS current_year,
    curr.total_sip_amount AS current_year_sip,
    prev.year AS previous_year,
    prev.total_sip_amount AS previous_year_sip,
    ROUND((curr.total_sip_amount - prev.total_sip_amount) * 100.0 / prev.total_sip_amount, 2) AS yoy_growth_pct
FROM sip_yearly curr
JOIN sip_yearly prev ON curr.year = prev.year + 1;
```

### Results
|   current_year |   current_year_sip |   previous_year |   previous_year_sip |   yoy_growth_pct |
|---------------:|-------------------:|----------------:|--------------------:|-----------------:|
|           2025 |        6.40004e+07 |            2024 |         1.53233e+08 |           -58.23 |

---

## Query 4: Total Transaction Count and Volume by State
*Summarizes transactions and aggregate investment amounts for each state.*

### SQL Query
```sql
SELECT
    state,
    COUNT(transaction_id) AS total_transactions,
    SUM(amount_inr) AS total_amount_inr,
    ROUND(AVG(amount_inr), 2) AS avg_transaction_amount_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_amount_inr DESC;
```

### Results
| state          |   total_transactions |   total_amount_inr |   avg_transaction_amount_inr |
|:---------------|---------------------:|-------------------:|-----------------------------:|
| Punjab         |                 2965 |        3.1578e+08  |                       106503 |
| Tamil Nadu     |                 2806 |        3.15177e+08 |                       112323 |
| Madhya Pradesh |                 2931 |        3.08312e+08 |                       105190 |
| Rajasthan      |                 2577 |        2.98646e+08 |                       115889 |
| Gujarat        |                 2780 |        2.98359e+08 |                       107323 |
| West Bengal    |                 2748 |        2.97183e+08 |                       108145 |
| Telangana      |                 2718 |        2.90219e+08 |                       106777 |
| Delhi          |                 2677 |        2.89633e+08 |                       108193 |
| Uttar Pradesh  |                 2695 |        2.85369e+08 |                       105888 |
| Haryana        |                 2736 |        2.79634e+08 |                       102206 |
| Karnataka      |                 2621 |        2.73754e+08 |                       104446 |
| Maharashtra    |                 2524 |        2.69513e+08 |                       106780 |

---

## Query 5: Funds with Expense Ratio < 1%
*Retrieves schemes with low operating costs (< 1.0%), sorted by efficiency.*

### SQL Query
```sql
SELECT
    f.amfi_code,
    f.scheme_name,
    p.expense_ratio_pct,
    p.aum_crore
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
WHERE p.expense_ratio_pct < 1.0
ORDER BY p.expense_ratio_pct ASC;
```

### Results
|   amfi_code | scheme_name                                          |   expense_ratio_pct |   aum_crore |
|------------:|:-----------------------------------------------------|--------------------:|------------:|
|      118636 | Nippon India Gilt Securities Fund - Regular - Growth |                0.55 |       30030 |
|      100025 | HDFC Short Term Debt Fund - Regular - Growth         |                0.56 |       27953 |
|      120844 | Kotak Liquid Fund - Regular - Growth                 |                0.6  |       27623 |
|      119552 | SBI Bluechip Fund - Direct Plan - Growth             |                0.66 |        1231 |
|      118633 | Nippon India Large Cap Fund - Direct - Growth        |                0.72 |       39475 |
|      119599 | SBI Small Cap Fund - Direct Plan - Growth            |                0.72 |       36061 |
|      120507 | ICICI Pru Liquid Fund - Regular - Growth             |                0.74 |       39116 |
|      119093 | Axis Bluechip Fund - Direct - Growth                 |                0.75 |       15866 |
|      119120 | SBI Magnum Gilt Fund - Regular Plan - Growth         |                0.77 |       24101 |
|      125498 | HDFC Mid-Cap Opportunities Fund - Direct - Growth    |                0.78 |       18792 |
|      101208 | ABSL Liquid Fund - Regular - Growth                  |                0.79 |       38995 |
|      120504 | ICICI Pru Bluechip Fund - Direct - Growth            |                0.8  |       41553 |
|      118635 | Nippon India ETF Nifty 50 BeES                       |                0.89 |       20284 |
|      125497 | HDFC Top 100 Fund - Direct Plan - Growth             |                0.92 |       10611 |

---

## Query 6: KYC Verification Status vs Transaction Metrics (Custom)
*Compares count and average sizes of transactions by KYC status and type.*

### SQL Query
```sql
SELECT
    t.kyc_status,
    t.transaction_type,
    COUNT(t.transaction_id) AS transaction_count,
    SUM(t.amount_inr) AS total_amount_inr,
    ROUND(AVG(t.amount_inr), 2) AS avg_transaction_amount_inr
FROM fact_transactions t
GROUP BY t.kyc_status, t.transaction_type
ORDER BY t.kyc_status, transaction_count DESC;
```

### Results
| kyc_status   | transaction_type   |   transaction_count |   total_amount_inr |   avg_transaction_amount_inr |
|:-------------|:-------------------|--------------------:|-------------------:|-----------------------------:|
| Pending      | SIP                |                1585 |        1.76262e+07 |                      11120.6 |
| Pending      | Lumpsum            |                 669 |        1.76362e+08 |                     263620   |
| Pending      | Redemption         |                 378 |        9.34199e+07 |                     247143   |
| Verified     | SIP                |               18131 |        1.99607e+08 |                      11009.2 |
| Verified     | Lumpsum            |                7426 |        1.88346e+09 |                     253630   |
| Verified     | Redemption         |                4589 |        1.15111e+09 |                     250840   |

---

## Query 7: Risk Category Performance Profile (Custom)
*Groups funds by risk category to observe average 3y return and Sharpe ratios.*

### SQL Query
```sql
SELECT
    f.risk_category,
    COUNT(f.amfi_code) AS fund_count,
    ROUND(AVG(p.return_3yr_pct), 2) AS avg_3yr_return_pct,
    ROUND(AVG(p.sharpe_ratio), 2) AS avg_sharpe_ratio,
    ROUND(AVG(p.beta), 2) AS avg_beta
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
GROUP BY f.risk_category
ORDER BY avg_3yr_return_pct DESC;
```

### Results
| risk_category   |   fund_count |   avg_3yr_return_pct |   avg_sharpe_ratio |   avg_beta |
|:----------------|-------------:|---------------------:|-------------------:|-----------:|
| Very High       |            6 |                21.69 |               0.87 |       0.99 |
| High            |            8 |                16.21 |               0.86 |       0.98 |
| Moderately High |            4 |                15.08 |               0.96 |       0.97 |
| Moderate        |           16 |                12.85 |               0.93 |       0.95 |
| Low             |            6 |                 6.29 |               3.95 |       0.37 |

---

## Query 8: Payment Mode Preference by City Tier (Custom)
*Analyzes payment mode adoption share within Top-30 vs Beyond-30 city tiers.*

### SQL Query
```sql
WITH tier_totals AS (
    SELECT
        city_tier,
        payment_mode,
        COUNT(transaction_id) AS transaction_count,
        SUM(amount_inr) AS total_amount_inr
    FROM fact_transactions
    GROUP BY city_tier, payment_mode
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

## Query 9: Top 10 Portfolio Stock Exposures Across All Funds (Custom)
*Evaluates the largest underlying equity holdings aggregated across funds.*

### SQL Query
```sql
SELECT
    ph.stock_name,
    ph.stock_symbol,
    ph.sector,
    COUNT(DISTINCT ph.amfi_code) AS holding_funds_count,
    ROUND(SUM(ph.market_value_cr), 2) AS aggregate_market_value_cr,
    ROUND(AVG(ph.weight_pct), 2) AS avg_weight_pct
FROM portfolio_holdings ph
JOIN dim_fund f ON ph.amfi_code = f.amfi_code
GROUP BY ph.stock_name, ph.stock_symbol, ph.sector
ORDER BY aggregate_market_value_cr DESC
LIMIT 10;
```

### Results
| stock_name              | stock_symbol   | sector      |   holding_funds_count |   aggregate_market_value_cr |   avg_weight_pct |
|:------------------------|:---------------|:------------|----------------------:|----------------------------:|-----------------:|
| Axis Bank Ltd           | AXISBANK       | Banking     |                    12 |                     16325.9 |            12.56 |
| Bharti Airtel Ltd       | BHARTIARTL     | Telecom     |                    15 |                     16051.5 |             9.71 |
| Reliance Industries Ltd | RELIANCE       | Energy      |                    13 |                     15286.5 |             9.07 |
| NTPC Ltd                | NTPC           | Utilities   |                    13 |                     13951.4 |            11.93 |
| Grasim Industries Ltd   | GRASIM         | Diversified |                    14 |                     13897.8 |            12.09 |
| Hindustan Unilever Ltd  | HINDUNILVR     | FMCG        |                    11 |                     12993.9 |            11.44 |
| Mahindra & Mahindra Ltd | M&M            | Automobile  |                    10 |                     12967.3 |            11.03 |
| HCL Technologies Ltd    | HCLTECH        | IT          |                    13 |                     12299.9 |            11.32 |
| Tata Motors Ltd         | TATAMOTOR      | Automobile  |                    12 |                     12296.8 |             9.56 |
| UltraTech Cement Ltd    | ULTRACEMCO     | Cement      |                    12 |                     11612   |             8.75 |

---

## Query 10: Index Benchmark Correlation with Monthly Scheme NAV (Custom)
*Compares average scheme NAVs with index values (NIFTY50/NIFTY100) over time.*

### SQL Query
```sql
SELECT
    d.year,
    d.month,
    f.scheme_name,
    ROUND(AVG(n.nav_value), 2) AS avg_nav_value,
    ROUND(AVG(bi.close_value), 2) AS avg_benchmark_value
FROM fact_nav n
JOIN dim_fund f ON n.amfi_code = f.amfi_code
JOIN dim_date d ON n.nav_date = d.date_id
LEFT JOIN benchmark_indices bi ON bi.date = n.nav_date AND bi.index_name = (
    CASE
        WHEN f.benchmark LIKE '%100%' THEN 'NIFTY100'
        ELSE 'NIFTY50'
    END
)
GROUP BY d.year, d.month, f.scheme_name
ORDER BY f.scheme_name, d.year, d.month
LIMIT 20;
```

### Results
|   year |   month | scheme_name                                   |   avg_nav_value |   avg_benchmark_value |
|-------:|--------:|:----------------------------------------------|----------------:|----------------------:|
|   2022 |       1 | ABSL Frontline Equity Fund - Regular - Growth |          310    |               17939.6 |
|   2022 |       2 | ABSL Frontline Equity Fund - Regular - Growth |          311.28 |               17338.3 |
|   2022 |       3 | ABSL Frontline Equity Fund - Regular - Growth |          306.01 |               18443.6 |
|   2022 |       4 | ABSL Frontline Equity Fund - Regular - Growth |          307.2  |               18993.6 |
|   2022 |       5 | ABSL Frontline Equity Fund - Regular - Growth |          306.25 |               19264.7 |
|   2022 |       6 | ABSL Frontline Equity Fund - Regular - Growth |          315.59 |               19841   |
|   2022 |       7 | ABSL Frontline Equity Fund - Regular - Growth |          325.43 |               19728   |
|   2022 |       8 | ABSL Frontline Equity Fund - Regular - Growth |          329.52 |               20117.4 |
|   2022 |       9 | ABSL Frontline Equity Fund - Regular - Growth |          320.8  |               20651.1 |
|   2022 |      10 | ABSL Frontline Equity Fund - Regular - Growth |          310.12 |               20249.3 |
|   2022 |      11 | ABSL Frontline Equity Fund - Regular - Growth |          329.76 |               19067.4 |
|   2022 |      12 | ABSL Frontline Equity Fund - Regular - Growth |          341.37 |               17797.2 |
|   2023 |       1 | ABSL Frontline Equity Fund - Regular - Growth |          346.11 |               16755.8 |
|   2023 |       2 | ABSL Frontline Equity Fund - Regular - Growth |          353.31 |               15802.8 |
|   2023 |       3 | ABSL Frontline Equity Fund - Regular - Growth |          350.92 |               16054   |
|   2023 |       4 | ABSL Frontline Equity Fund - Regular - Growth |          359.25 |               16038.8 |
|   2023 |       5 | ABSL Frontline Equity Fund - Regular - Growth |          364.1  |               15396.4 |
|   2023 |       6 | ABSL Frontline Equity Fund - Regular - Growth |          339.07 |               15212.6 |
|   2023 |       7 | ABSL Frontline Equity Fund - Regular - Growth |          336.39 |               16145.6 |
|   2023 |       8 | ABSL Frontline Equity Fund - Regular - Growth |          343.64 |               17016.2 |

---
