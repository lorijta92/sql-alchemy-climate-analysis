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

**Temperature**

This analysis was to answer the question, “Is a statistically significant difference between average temperatures in June and December?” To accomplish this using Pandas, I read in a csv file with the necessary data, extracted the month from the date column, and then filtered for the June and December months. Before performing a t-test on these two samples, I first checked the length of the samples to see if they were equal. Because the June sample (1700) was longer than the December sample (1517), I took a random sampling of 1517 data points in the June sample in order to match sample sizes. I then performed a paired t-test, as both sample sets were from the same “subject” or station. This test returned a p-value less than 0.05, so I can confidently assume that there is a statistically significant difference between the average temperatures in June and December. 

I repeated the calculation using SQLAlchemy as well, and also received a p-value less than 0.05 (though a different value as the June sample was randomly selected). 

**Daily Normals**

Lastly, I wanted to calculate and plot the daily normals (the averages for the minimum, average, and maximum temperatures for all historical data matching a specified month and day) for the same two-week period I used in the comparative dates analysis. 

A function (`daily_normals`) was first created to query the minimum, average, and maximum temperature observations for a given date. Then, I used the start and end date variables from the comparative dates analysis to create a range of dates with `pd.date_range()` and then converted the data to strings and stripped off the year, storing the month and day in a list. I then calculated the daily normals by iterating through that list using a list comprehension, passing each object through the `daily_normals` function and storing the results in another list, `normals`.

To store this information in a data frame, I created empty lists to store the minimum, average, and maximum temperatures, and the daily normals. I appended each value to its respective list using for loops, and use those now populated lists to create a data frame. From that data frame, I plotted the data in a stacked area plot. 

![daily-norms]( https://github.com/lorijta92/sql-alchemy-climate-analysis/blob/master/Images/daily-norms.png?raw=true)
