import polars as pl
from plotnine import *
from json import load
from subprocess import run

# run(["pypy3", "-m", "Data.py"])
with open("./data.json") as f:
    data = pl.DataFrame(load(f))

# calculate some new columns
data = data.with_columns(
    # food_threshold=pl.col("food_threshold").cast(str), # convert to string so that it can be used as discrete rather than continuous plot variable
    total=pl.col("left") + pl.col("right") + pl.col("straight"),
    scaled_kills=pl.col("avg_kills") / pl.col("avg_score"),
).with_columns(
    left_prop=pl.col("left") / pl.col("total"),
    straight_prop=pl.col("straight") / pl.col("total"),
    right_prop=pl.col("right") / pl.col("total"),
)

(
    ggplot(data)
    + geom_line(
        aes(x="food_threshold", y="avg_score", colour="size", group="size"),
        # position=position_jitter(width=10),
    )
    # + scale_colour_discrete() # discrete rather than continuous colour palette
    + labs(
        title="Average score by amount of food",
        x="Food Threshold",
        y="Average Cannibalism Incidence",
        colour="Board Size",
    )
).show()

(
    ggplot(data)
    + geom_line(
        aes(x="food_threshold", y="avg_kills", colour="size", group="size"),
        # position=position_jitter(width=5, height=5),
    )
    # + scale_colour_discrete() # discrete rather than continuous colour palette
    + labs(
        title="Average number of snakes eaten by amount of food",
        x="Food Threshold",
        y="Average Snake Score",
        colour="Board Size",
    )
).show()

(
    ggplot(data)
    + geom_line(
        aes(x="food_threshold", y="scaled_kills", colour="size", group="size"),
        # position=position_jitter(width=5, height=5),
    )
    # + scale_colour_discrete() # discrete rather than continuous colour palette
    + labs(
        title="Average number of snakes eaten per score, by amount of food",
        x="Food Threshold",
        y="Average Cannibalism Incidence per Average Score",
        colour="Board Size",
    )
).show()

# (
#     ggplot(data)
#     + geom_line(aes(x="food_threshold", y="avg_kills", colour="size"))
#     # + scale_colour_discrete() # discrete rather than continuous colour palette
#     + labs(title="Average number of snakes eaten by amount of food")
# ).show()

# + geom_line() adds a line graph (+ geom_point() adds a scatterplot)
# anything that depends on data goes in aes(), e.g. x and y come from dataframe cols
# anything outside the aes doesn't come from the data points, (colours are set manually)

# filtered_data = data.filter(pl.col("food_threshold") == "150")

# (
#     ggplot(
#         data,
#         aes(x="size", fill="food_threshold"),
#     )
#     + geom_col(aes(y="straight_prop"), position=position_dodge())
#     + labs(
#         title="Turning directions for evolution by score",
#         x="Average Score",
#         y="Inverse Average Number of Turns",
#         fill = "Food threshold",
#     )  # axis labels
# ).show()
