# Imports
import pandas
import numpy
from datetime import datetime
import matplotlib.pyplot as plt

# Import the CSV into df
df=pandas.read_csv('data.csv', sep=',',header=0)
df = df[:-1]

# Read birth date
df["year_of_birth"] = pandas.DatetimeIndex(df["BIRTH DATE"]).year.astype(int)

# Change all unknown locations of death to "Living"
df["LOCATION OF DEATH"].fillna('Alive', inplace=True)

# Creating variable "last_known_alive_date" to calculate lived_dates, months_lived and years_lived.
# This was done to include currently living Presidents as well, since their death dates come as NaN in the dataset.
today_date = datetime.now().strftime("%b %d, %Y")
df["last_known_alive_date"] = df["DEATH DATE"]
df["last_known_alive_date"].fillna(today_date, inplace=True)

# Calculating lived_dates, months_lived and years_lived
date_diff = pandas.DatetimeIndex(df["last_known_alive_date"]) - pandas.DatetimeIndex(df["BIRTH DATE"])
df["days_lived"] = (date_diff/ numpy.timedelta64(1, "D"))
df["months_lived"] = date_diff / numpy.timedelta64(1, "M")
df["years_lived"] = date_diff / numpy.timedelta64(1, "Y")

# replace death date as living for death date is unknown.
df["DEATH DATE"].fillna('Alive', inplace=True)

# helper function to style the living president
def show_alive(s):
    if s['DEATH DATE'] == 'Alive':
        return ['background-color: #FFDADA'] * len(s)
    else:
        return ['background-color: transparent'] * len(s)

# sorting dataframe in desending order of days_lived and selecting top ten presidents
oldest_df = df.sort_values("days_lived", ascending=False).head(10)
oldest_df["years_lived"] = oldest_df["years_lived"].astype(int)
oldest_df.rename(columns={"years_lived": "AGE"}, inplace=True)

oldest_presidents = oldest_df.style
oldest_presidents.hide(axis="index")
oldest_presidents.hide(axis="columns",subset=["last_known_alive_date","year_of_birth", "days_lived", "months_lived"])
oldest_presidents.apply(show_alive, axis=1)
oldest_presidents.set_caption("Top 10 Presidents of the United States by age lived, oldest first")
oldest_presidents

# sorting dataframe in ascending order of days_lived and selecting top ten presidents
youngest_presidents_df = df.sort_values("days_lived", ascending=True).head(10)
youngest_presidents_df["years_lived"] = youngest_presidents_df["years_lived"].astype(int)
youngest_presidents_df.rename(columns={"years_lived": "AGE"}, inplace=True)

youngest_presidents = youngest_presidents_df.style
youngest_presidents.hide(axis="index")
youngest_presidents.hide(axis="columns",subset=["last_known_alive_date", "year_of_birth", "months_lived", "days_lived"])
youngest_presidents.apply(show_alive, axis=1)
youngest_presidents.set_caption("Top 10 Presidents of the United States by age lived, youngest first")
youngest_presidents

# Extracting necessary cols
days_lived_col = df["days_lived"]
years_lived_col = df["years_lived"].astype(int)
value_counts = years_lived_col.value_counts()

# Calculating weights
weights = []
for i in range(len(years_lived_col)):
    year = years_lived_col[i]
    # Using the frequency of a year as the weight
    weights.append(value_counts[year])
weights = numpy.array(weights)
# Getting weighted values
weighted_values = weights * days_lived_col

# Calculating the statistics
mean = days_lived_col.mean()
weighted_mean = weighted_values.sum() / weights.sum()
median = days_lived_col.median()
mode = years_lived_col.mode() * 365
max = days_lived_col.max()
min = days_lived_col.min()
std = days_lived_col.std()

# Tabularizing by appending everything to a dictionary
data = {
    "Statistic": ["Mean Age", "Weighted Mean Age", "Median Age", "Mode Age", "Maximum Age", "Minimum Age", "Standard Deviation"],
    "Age (Days)": [mean, weighted_mean, median, list(mode), max, min, std],
    "Age (Years)": [mean / 365, weighted_mean / 365, median / 365, [x / 365 for x in list(mode)], max / 365, min / 365, std / 365]
}

# Creating df from the dictionary
df_stats = pandas.DataFrame.from_dict(data)
df_stats.style.hide(axis="index")

x_axis = ["Mean", "Weighted Mean", "Median", "Maximum", "Minimum"]
x_axis_positions = range(len(x_axis))
y_axis = [mean, weighted_mean, median, max, min]
plt.figure(figsize=(8, 6))
plt.stem(x_axis_positions, y_axis)
plt.ylabel("Age (in Days)")
plt.title("Statistics of Presidential Ages")

plt.axhline(y = mean + std, color = 'r', linestyle = '--', label='Standard Deviation')
plt.axhline(y = mean, color = 'gray', linestyle = '-.', label='Mean')
plt.axhline(y = mean - std, color = 'r', linestyle = '--')

plt.legend(labels=['Standard Deviation', 'Mean'])

plt.xticks(x_axis_positions, x_axis)
plt.show()

x_axis_positions = [i for i in range(len(value_counts))]
plt.figure(figsize=(15, 4))
plt.stem(x_axis_positions, value_counts)
plt.xlabel("Age (years)")
plt.ylabel("Number of Presidents")
plt.title("Frequency of Presidential Ages")

plt.xticks(x_axis_positions, value_counts.keys())
plt.yticks(range(value_counts.max() + 1))
plt.show()