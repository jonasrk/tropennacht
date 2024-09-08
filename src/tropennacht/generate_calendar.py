from meteostat import Point, Hourly
from datetime import datetime, timedelta

import pandas as pd
import plotly_calplot


# Define the location for Berlin
berlin = Point(52.52, 13.405)  # Latitude and Longitude for Berlin

# Define the date range for the past year
start = datetime(
    datetime.now().year - 5, datetime.now().month, datetime.now().day
)  # Start date (one year ago)
end = datetime(
    datetime.now().year, datetime.now().month, datetime.now().day
)  # End date (today)

# Retrieve hourly temperature data
data = Hourly(berlin, start, end)
data = data.fetch()


# Function to determine if a day is a tropical night
def is_tropical_night(df, date):
    """Check if the given date is a tropical night (temperature never drops below 20°C)."""
    day_data = df.loc[date]
    return day_data["temp"].min() >= 20


# Create a DataFrame to store the results
results = []

# Generate a list of dates for the past year
date_range = pd.date_range(start=start, end=end, freq="D")

# Check each day in the date range
for date in date_range:
    # Convert date to the start and end of the day
    start_of_day = date
    end_of_day = date + timedelta(days=1)

    # Filter data for the specific day
    daily_data = data.loc[start_of_day:end_of_day]

    # Determine if the day is a tropical night
    tropical_night = is_tropical_night(daily_data, start_of_day)

    # Append the result
    results.append({"date": start_of_day, "tropical_night": tropical_night})

# Convert results to a DataFrame for easier manipulation
results_df = pd.DataFrame(results)

# Prepare the data for plotting
# Map tropical nights to numeric values: 1 for True, 0 for False
results_df["value"] = results_df["tropical_night"].astype(int)

# Generate sample data
data = pd.DataFrame({"date": results_df["date"], "value": results_df["value"]})

# Create a calendar heatmap
fig = plotly_calplot.calplot(data, x="date", y="value")

# Customize the color scale to match the 0 and 1 values
# 0 will be grey, 1 will be red
fig.update_layout(
    coloraxis=dict(
        colorscale=[[0, "grey"], [1, "red"]],
        colorbar=dict(title="Tropical Night"),
    )
)

# Save the figure as an HTML file
fig.write_html("index.html")
