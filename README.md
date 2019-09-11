# Goal
Use Python, SQLAlchemy, Pandas, and Matplotlib to do basic climate analysis and data exploration. Then design a Flask API based on those queries. 

# Process
## Analysis with SQLAlchemy
To start the analysis, I first had to access the data by creating an engine with `create_engine`, reflecting the database with `automap_base()`, reflecting the tables with `Base.prepare(engine, reflect=True)`, and then creating a session with `Session(engine)`.

**Precipitation**

After the data was accessed, I moved onto the precipitation analysis: plotting the precipitation data from the last 12 months. I first queried the precipitation data for the most recent date with `session.query()` and sorted the results in descending before grabbing the first result. I then converted that result into a datetime object named `entered_date`. Using `entered_date`, I calculated the date from one year ago using `dt.timedelta()`. With these two date endpoints as filters, I was able to retrieve a year’s worth of data. The results were stored in a variable `one_year_prcp`, which I used to make a data frame with `pd.DataFrame()`. From that data frame, I plotted the precipitation data.

![precipitation](https://github.com/lorijta92/sql-alchemy-climate-analysis/blob/master/Images/precipitation.png?raw=true)

**Station**

Next was the station analysis in which I wanted to retrieve the total number of weather stations, rank them by activity level, and find the minimum, average, and maximum temperatures of the most active station. To find the total number of weather stations, I queried all stations and then used `.distinct()` and `.count()` to count the number of unique stations found in the data set.

For the most active stations, I defined “active” as the stations with the most rows of data. I therefore had to count how many rows of data were associated with each station by using `func.count()`  in my query, grouping by stations with `.group_by()`, and then sorting in descending order with `.order_by`. These results were then displayed in a data frame.

To find the minimum, average, and maximum temperatures of the most active station, I used `func.min()`, `func.avg()`, and `func.max()` in my session query. 

As a visual, I also wanted to display a histogram of the temperature observations for one year from the most active station. Using the two date endpoints from the precipitation analysis, I queried one year’s worth of temperature observations and filtered for the most active station. I then had to convert the results into a series by using `np.ravel` and `pd.Series`. Using this series, I used `.plot.hist()` to plot a histogram. 

![histogram](https://github.com/lorijta92/sql-alchemy-climate-analysis/blob/master/Images/station-histogram.png?raw=true)

**Comparative Dates**

For this analysis, I wanted to retrieve and plot the minimum, average, and maximum temperatures for a selected two week period. A function was created to calculate those temperatures based on two parameters: the start and end dates. A bar chart was then created to display the average temperature, with an error bar based on the maximum and minimum temperature difference. 

![calc-temps]( https://github.com/lorijta92/sql-alchemy-climate-analysis/blob/master/Images/calc-temps.png?raw=true)

Next, I gathered the total amount of rainfall for each station and displayed that alongside other key facts (station name, latitude, longitude, and elevation) for each station. Because this data was stored in two separate tables, I merged the tables on “station” using `.filter(Measurement.station == Station.station)`. 
