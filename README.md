# airbnb
Airbnb analysis framework


### Brainstorming
Questions to answer/hypotheses:

- Is there a type of rental that might be connected to a criminal act?
  - how long they rent the place for? when? where?
  - anomalies in the dataset that might point somewhere
  - Do we need other data to examine with?
- If you want to travel on a budget, which times of the year/and regions are most affordable?
  - extrapolate to cities later? 
- What is the most attractive listing type?
  - what/where/when/how much
- Seasonal trends in pricing?
  - in off-seasons (e.g. march) do prices go down at all?
- Per-neighbourhood stats:
  - descriptive stats on properties
- Examine Airbnb listings versus neighbourhood income
  - hypothesis: more income more listings?
  - supporting data sources ??
- look for how a major event (concert, sports, whatever) affects the occupancy rates and prices
  - pick interesting/big events

**Tasks:**
Data loading:
    - read csv's to pandas dataframes
    - clean dataframes and remove NaN/NULLS/etc
      - document any other cleaning steps made

geospatial (geopandas?):
    - compute listing densities by neighbourhood
      -   by total listing #
      -   by total bedroom #
      -   by total guest capacity

Temporal:
- datestamps cleaned and uniform
- f(x) timedelta between given datestamps

Analysis/Modelling:
- population/listing density vs price
- predict christmas holiday pricing for a given scenario

Visualization:
Dashboard that contains:
  - geomap box
    - show/toggle the neighbourhoods as polygons
    - show/toggle the listings as dots
    - show/toggle landmarks?
    - show/toggle a density heatmap