## Goal
Use Python, SQLAlchemy, Pandas, and Matplotlib to do basic climate analysis and data exploration. Then design a Flask API based on those queries. 

## Process
To start the analysis, I first had to access the data by creating an engine with `create_engine`, reflecting the database with `automap_base()`, reflecting the tables with `Base.prepare(engine, reflect=True)`, and then creating a session with `Session(engine)`.

<img align="right" width="450" height="280" src="https://github.com/lorijta92/sql-alchemy-climate-analysis/blob/master/Images/precipitation.png?raw=true">
After the data was accessed, I moved onto the precipitation analysis: plotting the precipitation data from the last 12 months. I first queried the precipitation data for the most recent date with `session.query()` and sorted the results in descending before grabbing the first result. I then converted that result into a datetime object named `entered_date`. Using `entered_date`, I calculated the date from one year ago using `dt.timedelta()`. With these two date endpoints as filters, I was able to retrieve a year’s worth of data. The results were stored in a variable `one_year_prcp`, which I used to make a data frame with `pd.DataFrame()`. From that data frame, I plotted the precipitation data.  
