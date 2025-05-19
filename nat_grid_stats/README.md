# National Grid Substation Data – Statistics and Cleaning

This folder contains scripts to clean and summarize the substation and feeder data obtained from the National Grid website.

## Data Cleaning and Preparation

1. **`sub_coord.py`**  
   - Loads `Substations.csv`  
   - Cleans and saves the result as `coordinates.csv`

2. **`column_names.py`**  
   - Standardizes column names  
   - Saves unified data as `column_names.csv`

3. **`summary_sub_NYS.py`**  
   - Processes underground (UG) and overhead (OH) feeder files  
   - Provides summary statistics:
     - Number of feeders per substation
     - Total amps
     - Amperage bins
   - Outputs standardized feeder files
