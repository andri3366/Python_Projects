# London Bikes Analysis
## Purpose
This project was designed to explore bike usage patterns in London, UK using the London Bike Sharing Dataset from [Kaggle](https://www.kaggle.com/datasets/hmavrodiev/london-bike-sharing-dataset). The original project, found on [Youtube](https://www.youtube.com/watch?v=nl9eZl1IOKI), explored key indicators such as total bike counts, moving average trend line, and a heatmap comparing tempurature and wind speed. I extended the project by analysing the average humidity and seasonal bike usage to provide a deeper understanding of how weather conditions influence activity.

## Techniques
- VS code
- Jupyter notebooks
- Python Library: Pandas
- Tableau Public

## Data Cleaning
In order to properly analyze the data, a [Jupyter notebook](london_bikes.ipynb) in VS code was used to import pandas libraries and read the csv file from [Kaggle](https://www.kaggle.com/datasets/hmavrodiev/london-bike-sharing-dataset). <br>
Key steps include:
- Renaming the column to more readable names, by using a dictionary and ```.rename()```
- Change the humidity column to a percentage
- Get distinct counts for both the season and weather columns to better understand how to alter naming conventions
  - Used a season and weather distionary to change the column from float to string
  ```
  .astype('str')
  ```
  - Map each assigned value from the season and weather disctionary
  ```
  .map(weather_dict)
  ```
- Write the final dataframe to an Excel file
## Dashboard
The final dahsboard is found on [Tableau](https://public.tableau.com/app/profile/andrianna.wardill/viz/LondonBikeAnalysis_17599482187410/LondonBikeAnalysis?publish=yes) public.

### Moving Average
1. Create a string parameter for Moving Average Period and an integer param for Moving Average Duration
2. Converted the Time table to Date & Time
3. Create a Moving Average Period measure
   ```
   datetrunc([Parameters].[Moving Average Period],[Time])
   ```
   - Change the measure to data type 'Date'
4. Chart:
   - Columns: Moving Average Period measure
   - Rows: Count
5. Create a set from the Moving Average Period
6. Create min & max month calculated fields <br>
  a) ```{ MIN(IF [Moving Average Period Set] THEN [Moving Average Period]END) } ```
    - The ```{}``` are used to ensure all marks are returned
  b) Add min and max month fields into the 'Detail' shelf and select continuous
7. Add worksheet action
   - Select the change set values options
   - Set the target set to Moving Average Period Set
   - Clearing the selection will should be highlighted as 'Keep set values'
   - **Note:** When adding all the worksheets into the dashboard edit the action so the source sheet is set to the dashbord
8. Create a reference band
   - Drag and drop the reference band into Table -> Moving Average Period
   - Set the band from Min Month to Max Month
9. Create an In Range field for highlighting selected data points
    ```
    [Moving Average Period] >= [Min Month] AND [Moving Average Period] <= [Max Month] 
    ```
    - Drag the field into the 'Color' shelf
      - Select the In Range drop down and select Attribute
10. Change Rows from total number of bike rides to Moving Average
    - Perform a Quick Table Calculation for Moving Average on the SUM(Count)
    - Drag the Sum(Count) to the tables and rename to Moving Average Rides
    - Edit the field
    ```
    WINDOW_AVG(SUM([Count]), -[Moving Average Duration]+1, 0)
    ```
11. Drag the Moving Average Period to the Filters
    - Edit the Filter to be for a Range of Dates
### Ride Total
1. Create a In Range Rides field
   ```
   { SUM(INT([In Range]) * [Count]) }
   ```
2. Drag the In Range table into the filter and select True
3. Drag the min and max month tables into the 'Detail' shelf and select Continuous
4. Drage the In Range Rides into the 'Label' shelf

### Heatmap
1. Create bins for temp real c
   - Name the field to Temp C
   - Drag the Temp C table into the rows
2. Create bins for Wind Speed Kph
   - Name the field to Wind Speed (Kph)
   - Drag the Wind Speed (Kph) table into the rows
3. Drag count into the 'Label' and 'Color' shelves
4. Change the marks to 'Square'

### Weather Bar Chart
1. Drag the Weather table into rows
2. Drag the Count into columns
3. Sort the values in descending order
4. Drag the Weather table into the 'Color' shelf

### Hourly Bar Chart
1. Drag the Time table into rows
   - Select Discrete and Hour
2. Drag the Count into columns
3. Change the marks to 'Bar'

### Seasonal Clusters
1. Create an Average Humidity % calculated field
   ```
   { FIXED [Season] : AVG([Humidity Percent])}
   ```
2. Create a Dynamic Humidity calculated field
   ```
   { FIXED [Season] : AVG( IF [In Range] THEN [Humidity Percent] END) }
   ```
   - Drag the calculated filed into columns
3. Create a Dynamic Rides calculated field
   ```
   { FIXED [Season] : Avg( IF [In Range] THEN [Count] END) }
   ```
   - Drag the calculated filed into columns
4. Create clusters
   - Go to Analytics and select the Cluster model
   - Make sure the variable are AVG(Dynamic Humidity) and SUM(Dynamic Rides)
   - Set the Number of Clusters to 2
   - Drag the 'Clusters' into the 'Color' shelf
5. Drag the Season table into the 'Label' shelf
## Future Additions
- Add a forecasting model to preduct future bike demand
- Apply clustering to identify groups of similar days or weather patterns
