# Data Inventory

## Purpose

This document records the datasets considered for the Australian Rental Pressure Intelligence project.

Datasets will be selected based on:

- Relevance to the research question
- Geographic coverage
- Time coverage
- Frequency
- Data quality
- Compatibility with other datasets
- Availability of downloadable data
- Licensing and usage conditions

---

## Core Dataset Candidates

| Dataset | Source | Main Variables | Geography | Time Coverage | Frequency | Status |
|---|---|---|---|---|---|---|
| Rental Market | ABS | Median rent, rental changes | State/Territory and selected regions | 2018–present | Quarterly/other available frequencies | Candidate |
| Regional Population | ABS | Population, population change | SA2/LGA and above | 2001–present | Annual | Candidate |
| Building Approvals | ABS | Dwelling approvals, value, building type | SA2/LGA and above | 2016–present depending on geography | Monthly | Candidate |
| Rental Stress | AIHW | Rental stress, CRA income units | State/Territory and national | Recent historical series | Periodic | Candidate |
| Income | ABS | Household/person income indicators | Regional geographies | Census and other available periods | Periodic | Investigate |
| Interest Rate | RBA | Cash rate target | Australia | 2008–present | Daily/monthly | Candidate |

---

## 1. Rental Market

### Source

Australian Bureau of Statistics (ABS)

### Purpose

Measure rental prices and rental-market changes across Australian regions.

### Potential Variables

- Median weekly rent
- Rental price changes
- Rental growth
- State/Territory
- Geographic region
- Reference period

### Role in Project

This will be one of the primary measures of rental pressure.

---

## 2. Regional Population

### Source

Australian Bureau of Statistics (ABS)

### Purpose

Measure population levels and population growth across Australian regions.

### Potential Variables

- Population
- Population change
- Population growth rate
- Region
- State/Territory
- Reference year

### Role in Project

Population growth will be examined as a potential demographic factor associated with rental pressure.

---

## 3. Building Approvals

### Source

Australian Bureau of Statistics (ABS)

### Purpose

Measure changes in housing construction activity and potential housing supply.

### Potential Variables

- Number of dwelling approvals
- Number of dwellings
- Approval value
- Building type
- Region
- Month
- State/Territory

### Derived Variables

Potential derived measures include:

- Approvals per 1,000 residents
- Annual approval growth
- Rolling approval totals

### Role in Project

Building approvals will be used as an indicator of housing supply activity.

---

## 4. Rental Stress

### Source

Australian Institute of Health and Welfare (AIHW)

### Purpose

Measure the proportion of relevant rental households experiencing rental stress.

### Potential Variables

- Rental stress
- Number of income units
- State/Territory
- Time period

### Role in Project

Rental stress can provide an affordability-related measure that complements rental prices.

---

## 5. Income

### Source

Australian Bureau of Statistics (ABS)

### Purpose

Measure household or personal income in order to assess rental affordability.

### Potential Variables

- Median household income
- Median personal income
- Regional income
- Income growth

### Role in Project

Income may be used to construct measures such as:

- Rent-to-income ratio
- Rental affordability pressure

### Status

Dataset and geographic compatibility require further investigation.

---

## 6. Interest Rates

### Source

Reserve Bank of Australia (RBA)

### Purpose

Capture broader economic conditions that may affect housing and rental markets.

### Potential Variables

- Cash rate target
- Monthly average cash rate
- Rate changes

### Role in Project

Interest rates may be included as a macroeconomic control variable.

---

## Data Compatibility Considerations

The datasets do not necessarily share the same:

- Geographic boundaries
- Time periods
- Frequency
- Definitions
- Reference dates

Therefore, the project will not automatically merge all datasets into a single table.

Two analytical layers may be used.

### Layer A — Regional/State Time Series

Potential variables:

```text
date
region
median_rent
rent_growth
population
population_growth
dwelling_approvals
income
rental_stress
interest_rate
```
### Layer B - Small-Area Analysis

```text
Potential Variables:
SA2/LGA
state
population
population_growth
dwelling_approvals
approvals_per_1000_people
income

```
### Data Quality Checks
```
Each dataset will be checked for:

Missing values
Duplicate records
Inconsistent geographic names
Boundary changes
Changes in methodology
Changes in variable definitions
Outliers
Unexpected time gaps
Incompatible reference periods
```

### Data Selection Principle

```
Datasets will only be included in the final analysis if their definitions, geographic coverage and time coverage are sufficiently compatible with the research question.

Where compatibility is limited, the dataset may be used for a separate analytical layer rather than being forced into the main dataset.
```

### Dataset Status
```

| Dataset | Source | Geography | Time Period | Status |
|---|---|---|---|---|
| Median weekly rent | ABS | State/Territory | Jun 2018 onward | Selected / Cleaned |
| Regional population | ABS | SA2 | 2001–2025 | Selected / Cleaned |
| Building approvals | ABS | SA2/LGA | To be acquired | Candidate |
| Rental stress | AIHW | State/Territory | To be acquired | Candidate |
| Income | ABS | Regional | To be acquired | Candidate |
| Interest rates | RBA | Australia | To be acquired | Candidate |

```
## Completed Data Processing

### Median Weekly Rent

- Source: Australian Bureau of Statistics
- Raw file: `data/raw/Median weekly rent.csv`
- Processed file: `data/processed/rental_market_clean.csv`
- Records: 664
- Geographic coverage: 8 states and territories
- Time period: June 2018 onward
- Missing values: None
- Duplicate records: None

### SA2 Population

- Source: Australian Bureau of Statistics
- Raw file: `data/raw/32180DS0003_2001-25.xlsx`
- Processed file: `data/processed/population_sa2_clean.csv`
- Records: 61,335
- SA2 regions: 2,454
- Time period: 2001–2025
- Missing values: None
- Duplicate SA2-year records: None

