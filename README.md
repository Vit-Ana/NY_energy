# Evaluating Substation Capacity in the United States

## 1. Purpose of the Analysis
This project evaluates the capacity of electric substations using New York and California as case studies. It also estimates the population served by each substation, providing insight into the spatial distribution of electrical infrastructure relative to population density.

### 2. Data
#### 1. Substations and National Grid Feeders
- Files: Substations.csv, National Grid Feeders By Phase.csv
- Source: National Grid System Data Portal – New York
- Description: These datasets contain geolocated information about electrical substations and feeder lines across New York State. The data includes attributes such as substation IDs, rated capacity, phase information, and associated geographic coordinates.

#### 2. List of Electric Substations Feeding the Distribution System
- File: Electric_Substations_List_2013.pdf
- Source: New York State Department of Public Service (2013)
- Description: A government-issued document listing substations connected to the distribution system as of 2013. It provides official naming, utility affiliations, and operational context.

#### 3. Census and Geographic Data
- Files: ZIP code shapefiles, population statistics, city boundary shapefiles for Buffalo and Syracuse
- Source: U.S. Census Bureau and local government GIS portals
- Description: Used to spatially associate populations and urban areas with substations and feeders. These datasets are essential for calculating service coverage (e.g., estimated people served per substation) and for visualizing energy infrastructure in urban contexts.

### 3. Folder Structure and Workflow
```nat_grid_stats/```: Initial analysis of New York substations and feeders using data from the National Grid website.

```nat_grid_maps/```: Calculates estimated service coverage and visualizes substations on a map. Run this after completing ```nat_grid_stats/```.

```city_substations/```: Focuses on service coverage for individual cities (Buffalo, Syracuse). Depends on outputs from ```nat_grid_maps/```.

```data_from_state_gov/```: Analyzes historical data from the New York State Department of Public Service (2013) and maps those substations. Depends on outputs from ```nat_grid_stats/```.

```California/```: Evaluates substations in California. To run this analysis, first execute ```pop_data.py``` and ```state_maps.py``` from ```nat_grid_maps/```.

**The New York State Map with Substations**\
color-coded by number of feeders (created with QGIS)
![New York State Map with Substations]( gov_file_substations.png)
