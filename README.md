# Climate-O-Metric 🌍📊
*A Hackathon Project on Climate Data Analytics*

This project was developed as part of the Climate-O-Metric Hackathon, which consisted of 3 rounds focused on data analytics (first two rounds) and predictive insights (third round).
The challenge provided real-world climate datasets, and the goal was to clean, preprocess, analyze, and present actionable insights.

---

## Overview
Climate-O-Metric brings together multi-round analyses across climate indicators, energy systems, and emissions to surface trends and insights that matter. The work spans:
- Round 1: Foundational analytics and country-level sustainability insights
- Round 2: Thematic deep-dives with dedicated dashboards
- Round 3: Light predictive modeling for forward-looking insight

No setup instructions are included here by design—this document focuses on the project’s structure, scope, methods, and outcomes.

---

## Repository Structure
- `Round 1/`
  - `datasets/`: Country-level climate and energy datasets (raw and preprocessed)
  - `images/`: Exported visuals from the Round 1 report
  - Key artifacts: [`Sustainability_report.pdf`](Round%201/Sustainability_report.pdf), [`Sustainability_report.pbix`](Round%201/Sustainability_report.pbix)

- `Round 2/`
  - Thematic tracks with their own `dataset/` and `images/` folders, plus PBIX reports:
    - `Climate & Temperatures/` → [`Climate & Temperatures.pbix`](Round%202/Climate%20&%20Temperatures/Climate%20%26%20Temperatures.pbix)
    - `Consumption & Generation/` → [`Consumption and Generation.pbix`](Round%202/Consumption%20&%20Generation/Consumption%20and%20Generation.pbix)
    - `Emissions and Pollutions/` → [`Emissions and Pollutions.pbix`](Round%202/Emissions%20and%20Pollutions/Emissions%20and%20Pollutions.pbix)
    - `General energy data/` → [`General_Energy_Data.pbix`](Round%202/General%20energy%20data/General_Energy_Data.pbix)
    - `Powerplants/` → [`Power_Plants.pbix`](Round%202/Powerplants/Power_Plants.pbix)

- `Round 3/`
  - `Country_Pollution_Stats.csv`: Cleaned dataset used for lightweight modeling
  - `l3.ipynb`: Notebook with preprocessing and predictive exploration

---

## Round 1 — Sustainability & Core Indicators
Country-level analytics built from multiple public datasets (CO₂ per capita, renewable electricity share, greenhouse gas emissions, agricultural land %, and electricity consumption per capita). Core steps included:
- Data cleaning and reformatting; deriving comparable time-series per country
- Lightweight preprocessing to align temporal coverage across datasets
- Consolidated visuals for cross-metric context and benchmarking

### Visual snapshots
<p align="center">
  <img src="Round%201/images/Sustainability_report_page-0002.jpg" alt="Round 1 Report Page 2" width="48%" />
  <img src="Round%201/images/Sustainability_report_page-0004.jpg" alt="Round 1 Report Page 4" width="48%" />
</p>

---

## Round 2 — Thematic Deep-Dives (Dashboards)
Each subproject focuses on a distinct aspect of the climate-energy system with curated datasets, preprocessing, and a dedicated dashboard.

- Climate & Temperatures
  - Global and country-level temperature trends and anomalies
  - Annual means and multi-decade patterns for context

- Consumption & Generation
  - Power generation mixes (renewables vs. non-renewables)
  - Country comparisons and changes over time

- Emissions and Pollutions
  - Emissions footprints and forest/carbon context
  - Trendlines to highlight inflection points

- General energy data
  - Broad energy KPIs for orientation across countries
  - Harmonized views to support comparisons

- Powerplants
  - Country-level plant counts and capacity trends
  - Summary visuals of infrastructure concentration

### Visual snapshots
<p align="center">
  <img src="Round%202/Climate%20%26%20Temperatures/images/Climate%20%26%20Temperatures_page-0001.jpg" alt="Climate & Temperatures Dashboard" width="32%" />
  <img src="Round%202/Emissions%20and%20Pollutions/images/Emissions%20and%20Pollutions_page-0001.jpg" alt="Emissions and Pollutions Dashboard" width="32%" />
  <img src="Round%202/General%20energy%20data/images/General_Energy_Data_page-0001.jpg" alt="General Energy Data Dashboard" width="32%" />
</p>

---

## Round 3 — Predictive Insight 
In the final round, we were provided with a dataset named Country_Pollution_Stats.csv, containing climate and pollution-related statistics for different countries.

The dataset had 217 rows and 20 columns, with information such as:

Country-level details: region_id, country_name, population_population_number_of_people, gdp.

Waste composition percentages: food/organic, glass, metal, paper/cardboard, plastic, rubber/leather, wood, yard/garden, and others.

Special waste data (tons/year): agricultural, construction/demolition, e-waste, hazardous, industrial, and medical.

Climate impact: Temperature Change.

A Jupyter Notebook (l3.ipynb) demonstrating the preprocessing, analysis, and model training steps.

Predicted future trends and insights for climate-related decision-making.

---

## Data & Assets
Representative datasets used across rounds include:
- CO₂ emissions per capita, total greenhouse gas emissions
- Renewable electricity share of generation
- Agricultural land percentage
- Global and country temperature time-series
- Power generation and consumption by source
- Forest and carbon summaries

Dashboards and visuals are provided as PBIX files and exported images for quick review.

---

## Tooling & Methods
- Data wrangling and preprocessing: Python (pandas, NumPy), Excel
- Visualization and dashboards: Power BI (PBIX), Customed Themes
- Modeling (Round 3): scikit-learn in Jupyter Notebook

---

## Credits
Developed for the Climate-O-Metric Hackathon — awarded 2nd place (🥈). Datasets compiled from publicly available climate and energy sources and organized for analysis and storytelling.
