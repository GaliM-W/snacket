import polars as pl
from plotnine import *
from json import load
from subprocess import run

# run(["pypy3", "-m", "Data.py"])
with open("./data.json") as f:
    data = pl.DataFrame(load(f))

# calculate some new columns
data = data.with_columns(
    food_threshold=pl.col("food_threshold").cast(str), # convert to string so that it can be used as discrete rather than continuous plot variable
    total=pl.col("left") + pl.col("right") + pl.col("straight"),
).with_columns(
    left_prop=pl.col("left") / pl.col("total"),
    straight_prop=pl.col("straight") / pl.col("total"),
    right_prop=pl.col("right") / pl.col("total"),
)

# (
#     ggplot(data)
#     + geom_point(aes(x="walls", y="avg_score", colour="food_threshold"))
#     + scale_colour_discrete() # discrete rather than continuous colour palette
#     + labs(title="Average score by amount of walls")
# ).show()

# + geom_line() adds a line graph (+ geom_point() adds a scatterplot)
# anything that depends on data goes in aes(), e.g. x and y come from dataframe cols
# anything outside the aes doesn't come from the data points, (colours are set manually)

filtered_data = data.filter(pl.col("food_threshold") == "150")

(
    ggplot(filtered_data)
    + geom_line(aes(x="avg_score", y="left_prop"), colour="red")
    + geom_line(aes(x="avg_score", y="right_prop"), colour="blue")
    + geom_line(aes(x="avg_score", y="straight_prop"), colour="green")
    + labs(title="Turning directions for evolution by score", x="Average Score", y="Average Number of Turns") # axis labels
).show()
