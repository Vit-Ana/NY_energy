# National Grid Substation Data – Mapping and Geographic Analysis

This folder generates maps and performs geographic analysis for substations and feeders in New York and downloads input data for California.

## Downloading Shapefiles and Population Data

1. **`pop_data.py`**  
   - Downloads population data by ZIP code for New York and California

2. **`state_maps.py`**  
   - Downloads ZIP code boundary shapefiles for New York and California

## Preparing Geographic Files

3. **`geo_feeders.py`**  
   - Creates:
     - `grid_shape.gpkg`: all substations as geographic points
     - `MW10_shape.gpkg`: substations with feeder loads ≥ 10 MW
   - Generates overview maps

4. **`energy_per_pop.py`**  
   - Produces visualizations and maps showing population served per substation in New York
   
  **Estimated Population Size per Substation by ZIP Code**  
  Visualized from `substation_output.gpkg` using QGIS. ZIP codes are color-coded by equal quantiles of estimated population.
  ![Substations per Populatio in ZIP](output/ny_sub_per_pop_in_zip.png)

