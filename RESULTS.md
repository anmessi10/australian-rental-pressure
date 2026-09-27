# Results and Findings

## 1. Project Overview

### Research Question

> What demographic, housing-supply and economic factors are associated with rental pressure across Australian regions, and how have these relationships changed over time?

### Project Objective

This project analyses rental market conditions across Australian regions using publicly available data from the Australian Bureau of Statistics (ABS), Australian Institute of Health and Welfare (AIHW), and Reserve Bank of Australia (RBA).

The analysis combines rental prices, population growth, household and employee income, housing approvals and other demographic characteristics to investigate patterns associated with rental pressure.

The project includes:

- Rental market trend analysis
- Rental affordability analysis
- Population growth analysis
- Housing supply analysis using dwelling approvals
- A custom Historical Rental Pressure Index
- SA2-level rental prediction using machine learning
- Interactive Power BI dashboard

The project does not attempt to establish causal relationships or evaluate government housing policy. It investigates statistical associations between rental pressure and selected demographic, economic and housing-market variables using publicly available Australian data.

## 2. Data Sources and Methodology

### Data Sources

The project uses publicly available Australian datasets, primarily from the Australian Bureau of Statistics (ABS).

The main datasets used were:

| Dataset | Geographic level | Period used | Purpose |
|---|---|---|---|
| ABS Latest Insights into the Rental Market | State/Territory | 2019–2023 | Rental price trends |
| ABS Regional Population | SA2 | 2001–2025 | Population levels and growth |
| ABS Building Approvals | SA2 | July 2025–June 2026 | New residential dwelling approvals |
| ABS Data by Region | SA2 | 2019–2023 | Median employee income |
| 2021 Census General Community Profile | SA2 | 2021 | Rental and demographic modelling |

### Data Processing

Python was used for data ingestion, cleaning, validation and transformation.

The general workflow was:

1. Obtain raw data from official Australian government sources.
2. Clean and standardise geographic identifiers.
3. Convert datasets into analysis-ready formats.
4. Validate missing values and duplicate records.
5. Join datasets using nine-digit SA2 codes where appropriate.
6. Generate derived measures for rental affordability, population growth and housing approvals.
7. Store processed datasets as CSV files for analysis and dashboard development.

### Rental Affordability

A project-specific affordability measure was calculated as:

**Annualised median weekly rent ÷ median employee income × 100**

The annualised rent was calculated by multiplying the mean monthly median weekly rent by 52.

This measure represents the proportion of annual median employee income that would be required to cover the annualised median rent. It is a project-created measure and should not be interpreted as an official rental-stress statistic.

### Housing Supply

Housing supply was represented using **new residential dwelling approvals per 1,000 residents** for July 2025–June 2026.

This measures approved residential dwelling activity rather than completed housing construction. It should therefore be interpreted as an indicator of approved potential supply rather than actual housing additions.

### Historical Rental Pressure Index

A custom Historical Rental Pressure Index was developed for the 2019–2023 period using three equally weighted indicators:

- Rental growth
- Population growth
- Change in the rental affordability ratio

Each indicator was standardised using a z-score before being combined.

The resulting score was then scaled from 0 to 100 across the eight Australian states and territories.

The index is a project-created relative measure. A higher value indicates a higher combined score across the selected indicators during 2019–2023; it does not represent an official measure of rental pressure.

## 3. Rental Market and Affordability Results

### Rental Market Trends

Median weekly rents increased across all eight states and territories between 2019 and 2023.

The largest percentage increases were observed in:

| State/Territory | 2019 Rent ($/week) | 2023 Rent ($/week) | Change (%) |
|---|---:|---:|---:|
| Tasmania | 282.50 | 399.58 | +41.45% |
| Western Australia | 350.00 | 472.08 | +34.88% |
| Queensland | 379.58 | 467.50 | +23.16% |
| South Australia | 324.83 | 400.00 | +23.14% |
| Northern Territory | 424.58 | 514.58 | +21.20% |
| Australian Capital Territory | 486.00 | 568.17 | +16.91% |
| New South Wales | 480.83 | 558.33 | +16.12% |
| Victoria | 389.00 | 433.67 | +11.48% |

The results show that rental growth varied considerably between jurisdictions. Tasmania recorded the largest percentage increase over the period, while Victoria recorded the smallest.

### Rental Affordability

The project-created rent-to-median-employee-income measure also changed differently across jurisdictions.

Between 2019 and 2023:

| State/Territory | 2019 Ratio (%) | 2023 Ratio (%) | Change (percentage points) |
|---|---:|---:|---:|
| Tasmania | 30.64 | 36.77 | +6.14 |
| Western Australia | 32.87 | 37.39 | +4.52 |
| Queensland | 38.87 | 41.20 | +2.33 |
| Northern Territory | 37.06 | 39.14 | +2.07 |
| South Australia | 33.65 | 35.59 | +1.94 |
| Australian Capital Territory | 37.49 | 37.31 | -0.19 |
| New South Wales | 47.84 | 47.05 | -0.79 |
| Victoria | 39.15 | 36.55 | -2.60 |

Although median rents increased in every jurisdiction, the rent-to-income ratio did not increase everywhere.

For example, Tasmania experienced the largest rent increase and also a substantial increase in the project-created affordability ratio. In contrast, Victoria's ratio decreased despite an increase in median rent.

This demonstrates why rental price growth alone does not fully describe changes in rental affordability.

## 4. Population Growth and Housing Supply

### Population Growth

Between 2019 and 2023, population growth varied across the eight states and territories.

| State/Territory | Population Growth (%) |
|---|---:|
| Western Australia | +8.70% |
| Australian Capital Territory | +8.17% |
| Queensland | +7.10% |
| South Australia | +5.11% |
| Tasmania | +4.73% |
| Northern Territory | +4.44% |
| Victoria | +3.98% |
| New South Wales | +3.85% |

An exploratory Pearson correlation between population growth and the change in the project's affordability ratio was **0.305** across the eight jurisdictions.

This is a relatively small number of observations (n = 8), so the result should be treated as exploratory rather than as evidence of a general relationship or causation.

### Residential Dwelling Approvals

Housing supply activity was examined using new residential dwelling approvals between July 2025 and June 2026.

The number of approved dwellings per 1,000 residents was:

| State/Territory | Approved Dwellings | Approvals per 1,000 Residents |
|---|---:|---:|
| Australian Capital Territory | 4,127 | 11.06 |
| Queensland | 48,585 | 8.68 |
| Western Australia | 25,594 | 8.48 |
| South Australia | 15,110 | 7.97 |
| Victoria | 55,701 | 7.95 |
| New South Wales | 52,017 | 6.10 |
| Tasmania | 2,683 | 4.66 |
| Northern Territory | 843 | 4.18 |

At the SA2 level, the distribution was highly uneven. The median approval rate was **3.59 approvals per 1,000 residents**, compared with a mean of **6.92**. The difference between the mean and median reflects the presence of SA2s with particularly high approval rates.

The highest rates were concentrated in some areas experiencing substantial development activity. For example, Eagle Farm-Pinkenba in Queensland recorded approximately 195.92 approvals per 1,000 residents during the period.

These figures represent dwelling approvals rather than completed dwellings. They should therefore be interpreted as an indicator of approved residential development activity rather than a direct measure of housing stock added to the market.

## 5. Historical Rental Pressure Index

A Historical Rental Pressure Index was developed to combine three dimensions of rental-market pressure over the same 2019–2023 period:

1. Rental growth
2. Population growth
3. Change in the project-created rental affordability ratio

Each indicator was standardised using a z-score and given equal weight. The combined score was then rescaled from 0 to 100 across the eight states and territories.

### Results

| State/Territory | Index |
|---|---:|
| Western Australia | 100.00 |
| Tasmania | 88.73 |
| Queensland | 62.03 |
| Australian Capital Territory | 48.84 |
| South Australia | 45.97 |
| Northern Territory | 39.24 |
| New South Wales | 14.21 |
| Victoria | 0.00 |

Western Australia recorded the highest value on the project's Historical Rental Pressure Index for 2019–2023, while Victoria recorded the lowest.

The index should be interpreted as a **relative project-specific measure**. A score of 100 does not represent an absolute maximum level of rental pressure, and a score of 0 does not mean that rental pressure was absent. The values indicate relative positions within the eight state and territory observations used to construct the index.

### Sensitivity Analysis

The index was also tested using alternative weighting schemes:

- Equal weighting: ⅓ rental growth, ⅓ population growth, ⅓ affordability change
- Rental-focused: 50% rental growth, 25% population growth, 25% affordability change
- Population-focused: 25% rental growth, 50% population growth, 25% affordability change
- Affordability-focused: 25% rental growth, 25% population growth, 50% affordability change

Western Australia, Tasmania, Queensland, New South Wales and Victoria retained their relative positions across all four weighting scenarios. The relative positions of the Australian Capital Territory, South Australia and Northern Territory varied depending on the weighting assigned to the three indicators.

This sensitivity analysis indicates that some positions are more sensitive to the choice of weighting than others. The index should therefore be viewed as an analytical framework rather than an official ranking of rental-market conditions.

## 6. Machine Learning Results

### Objective

A machine-learning model was developed to predict estimated median weekly rent at the Statistical Area Level 2 (SA2) level using 2021 Census and ABS regional characteristics.

The target variable was the estimated median weekly rent derived from Census rent-band data. Because the Census data provides grouped rent bands rather than an exact median for every SA2, the target should be interpreted as an estimate.

SA2s without usable rental estimates or employee-income data were excluded from the modelling dataset. The final dataset contained **2,343 SA2 observations**.

### Baseline Model

The initial model used two predictors:

- Population
- Median employee income

A Linear Regression model and Random Forest Regression model were compared using an 80/20 train-test split.

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Linear Regression | 72.94 | 100.36 | 0.271 |
| Random Forest | 72.65 | 98.79 | 0.293 |

The Random Forest provided a modest improvement over Linear Regression, but the predictive performance was limited when using only population and employee income.

### Expanded Model

The feature set was expanded using additional 2021 Census demographic and economic variables:

- Population
- Median employee income
- Median age
- Median mortgage repayment
- Median total personal income
- Median total family income
- Average persons per bedroom
- Median total household income
- Average household size

The Census `Median_rent_weekly` variable was deliberately excluded from the predictors because it would directly overlap with the rental target and introduce target leakage.

Using the same 80/20 train-test split:

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Linear Regression | 40.92 | 86.90 | 0.453 |
| Random Forest | 34.29 | 60.48 | 0.735 |

The expanded Random Forest substantially outperformed the baseline models on the held-out test set.

### Cross-Validation

To assess whether the result depended heavily on a single train-test split, five-fold shuffled cross-validation was performed using the same folds for both models.

| Model | Mean MAE | Mean RMSE | Mean R² | R² SD |
|---|---:|---:|---:|---:|
| Linear Regression | 37.17 | 58.06 | 0.694 | 0.135 |
| Random Forest | 30.69 | 46.94 | 0.802 | 0.042 |

The Random Forest achieved a mean R² of **0.802** across the five folds, compared with **0.694** for Linear Regression. It also recorded lower mean MAE and RMSE.

The lower standard deviation of Random Forest R² across the folds indicates more consistent performance under the selected cross-validation procedure.

### Feature Importance

Random Forest feature importance showed that median mortgage repayment was the strongest individual predictor.

Test-set permutation importance also identified median mortgage repayment as the strongest predictor, followed by median household income.

However, the predictors are highly correlated with one another. For example, several income measures have strong correlations with household and employee income.

Therefore, feature importance is interpreted as **predictive importance rather than causal influence**. The model does not demonstrate that mortgage repayments or income cause higher or lower rents.

### Prediction Error

Prediction errors were substantially larger among very small SA2s.

SA2s with populations below 1,000 had considerably higher mean absolute errors than larger SA2s, although the number of observations in these groups was small.

The Pearson correlation between population and absolute prediction error was **-0.252**, indicating a modest negative relationship between population size and prediction error.

This suggests that model predictions may be less reliable for sparsely populated SA2s.

### Model Limitations

The machine-learning analysis has several limitations:

- The rental target is estimated from grouped Census rent bands.
- The modelling data represents the 2021 Census period.
- Random cross-validation does not explicitly account for possible spatial dependence between neighbouring SA2s.
- Several income variables are strongly correlated, making individual feature importance difficult to interpret independently.
- The model predicts statistical patterns and does not establish causal relationships.
- Performance should not automatically be assumed to generalise to other years or future rental markets.

## 7. Dashboard and Project Outputs

An interactive Power BI dashboard was developed to present the main findings of the analysis.

The dashboard contains four primary visualisations:

1. **Historical Rental Pressure Index (2019–2023)**
   - Displays the project-created relative rental pressure index across the eight states and territories.

2. **Rental Affordability — Rent-to-Median-Employee-Income (2023)**
   - Shows the project-created ratio between annualised median rent and median employee income.

3. **Population Growth (2019–2023)**
   - Shows the percentage change in population between 2019 and 2023.

4. **New Residential Dwelling Approvals per 1,000 Residents (July 2025–June 2026)**
   - Shows approved residential dwelling activity relative to population.

The dashboard also includes a **state/territory slicer**, allowing users to filter the visualisations interactively.

### Project Outputs

The project produces several reusable outputs:

- Cleaned rental market dataset
- Cleaned SA2 population dataset
- Cleaned SA2 income dataset
- Cleaned SA2 building approval dataset
- SA2 rental modelling dataset
- Historical Rental Pressure Index dataset
- Housing supply analysis datasets
- Machine-learning evaluation results
- Model diagnostic datasets and figures
- Power BI interactive dashboard

The Power BI dashboard intentionally labels the analysis periods because the historical rental, population and affordability analysis covers **2019–2023**, while the dwelling approval analysis covers **July 2025–June 2026**.

## 8. Limitations and Future Improvements

### Limitations

Several limitations should be considered when interpreting the results.

#### Different time periods

The project combines datasets covering different periods. The main historical analysis uses 2019–2023 data, while the dwelling approval analysis covers July 2025–June 2026.

The two periods are deliberately presented separately and should not be interpreted as evidence that recent dwelling approvals caused historical rental outcomes.

#### Estimated Census rental target

The SA2-level machine-learning target was estimated from Census rent-band data. The Census provides grouped rental ranges rather than an exact median for every SA2, meaning the derived rental target contains estimation uncertainty.

#### Aggregated affordability measure

The rent-to-median-employee-income measure is a project-created indicator. It uses annualised median weekly rent and a state-level aggregation of SA2 median employee incomes. It is not equivalent to an official household rental-stress measure.

#### Rental Pressure Index

The Historical Rental Pressure Index is a custom analytical measure rather than an official Australian statistic. Its results depend on the selected indicators, standardisation method and weighting scheme.

Although sensitivity analysis was performed, alternative indicator choices or weighting methods could produce different results.

#### Small number of state-level observations

The population-growth and affordability correlation uses only eight state and territory observations. The correlation is therefore exploratory and should not be interpreted as strong evidence of a general relationship.

#### Machine-learning generalisation

The machine-learning models were trained using 2021 SA2-level data. Their performance may not generalise to other years, regions or future rental-market conditions.

Random cross-validation also does not explicitly account for spatial relationships between neighbouring SA2s.

### Future Improvements

Potential extensions to the project include:

- Incorporating longer historical SA2-level rental series.
- Adding dwelling completion data rather than relying primarily on approvals.
- Including vacancy rates and rental listings where consistent regional data is available.
- Incorporating interest rates and broader economic indicators.
- Testing spatial cross-validation methods to better evaluate geographic generalisation.
- Comparing additional machine-learning algorithms such as Gradient Boosting and XGBoost.
- Applying hyperparameter optimisation to the Random Forest model.
- Developing a Streamlit version of the dashboard alongside Power BI.
- Automating the data ingestion pipeline so that datasets can be refreshed as new official releases become available.
- Expanding the analysis from state-level comparisons to longitudinal SA2-level analysis where compatible historical data is available.

## 9. Conclusion

This project investigated demographic, economic and housing-market factors associated with rental pressure across Australian regions using publicly available data.

The analysis found substantial variation in rental growth, affordability, population growth and dwelling approval activity across Australian states and territories between the periods examined.

Between 2019 and 2023, median weekly rents increased across all eight states and territories, while changes in the project-created rent-to-income measure varied between jurisdictions. Population growth also differed considerably, with Western Australia, the Australian Capital Territory and Queensland recording the largest percentage increases over the period.

At the SA2 level, the machine-learning analysis demonstrated that demographic and economic characteristics can provide useful predictive information about estimated rental prices. The Random Forest model achieved stronger predictive performance than Linear Regression under the selected cross-validation procedure, although the results should not be interpreted as causal relationships.

The project also demonstrated the importance of validating results across different modelling approaches and recognising limitations in the underlying data. In particular, the different time periods of the datasets, estimated Census rental targets, correlated predictors and spatial structure of Australian regions limit how broadly the findings should be interpreted.

Overall, the project provides a reproducible data-analysis workflow combining data engineering, statistical analysis, index construction, machine learning and interactive visualisation to investigate rental-market patterns across Australia.