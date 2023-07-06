#############################################
# Rule-Based Classification for Potential Customer Revenue Calculation
#############################################

#############################################
# Business Problem
#############################################
# Gezinomi wants to create new sales definitions based on some characteristics of its sales and estimate
# how much potential customers can contribute to the company on average according to these new sales definitions.
# For example: It is desired to determine how much an average customer who wants to go to an all-inclusive hotel
# in Antalya during a busy period can contribute.
#############################################


# PROJECT TASKS


#############################################
# TASK 1: Answer the following questions.
#############################################
# Question 1: Read the file gezinomi.xlsx and show general information about the dataset.


import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

# Load the dataset
df = pd.read_excel('gezinomi.xlsx')


def check_df(dataframe, head=5):
    print("########### Shape ###########")
    print(dataframe.shape)
    print("########### Types ###########")
    print(dataframe.dtypes)
    print("########### Head ###########")
    print(dataframe.head(head))
    print("########### Tail ###########")
    print(dataframe.tail(head))
    print("########### NA ###########")
    print(dataframe.isnull().sum())
    print("########### DS ###########")
    print(dataframe.duplicated().sum())
    print("########### Quantiles ###########")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)


check_df(df)

# Question 2: How many unique cities are there? What are their frequencies?
df["SaleCityName"].nunique()
# 6

df["SaleCityName"].value_counts()
# Antalya    31649
# Muğla      10662
# Aydın      10646
# Diğer       3245
# İzmir       2507
# Girne        455

sns.countplot(x=df["SaleCityName"], data=df)
plt.show(block=True)

# Question 3: How many unique Concepts are there?
df["ConceptName"].nunique()
# 3

sns.countplot(x=df["ConceptName"], data=df)
plt.show(block=True)

# Question 4: How many sales were made for each Concept?
df["ConceptName"].value_counts()

# Herşey Dahil      53186
# Yarım Pansiyon     3559
# Oda + Kahvaltı     2419

df["ConceptName"].value_counts().plot(kind="bar")
plt.show(block=True)

# Question 5: How much revenue was earned for each city?
df.groupby("SaleCityName").agg({"Price": "sum"})

df.groupby("SaleCityName").agg(price_sum=("Price", "sum")).reset_index(). \
    pipe((sns.barplot, "data"), x="SaleCityName", y="price_sum")
plt.show(block=True)

# Question 6: How much revenue was earned for each Concept?
df.groupby("ConceptName").agg({"Price": "sum"})

df.groupby("ConceptName").agg(price_sum=("Price", "sum")).reset_index(). \
    pipe((sns.barplot, "data"), x="ConceptName", y="price_sum")
plt.show(block=True)

# Question 7: What are the average prices by city?
df.groupby("SaleCityName").agg({"Price": "mean"})

df.groupby("SaleCityName").agg(price_mean=("Price", "mean")).reset_index(). \
    pipe((sns.barplot, "data"), x="SaleCityName", y="price_mean")
plt.show(block=True)

# Question 8: What are the average prices by Concept?
df.groupby("ConceptName").agg({"Price": "mean"})

df.groupby("ConceptName").agg(price_mean=("Price", "mean")).reset_index(). \
    pipe((sns.barplot, "data"), x="ConceptName", y="price_mean")
plt.show(block=True)

# Question 9: What are the average prices by city and Concept?
df.groupby(["SaleCityName", 'ConceptName']).agg({"Price": "mean"})

sns.catplot(x="ConceptName", y="Price", col="SaleCityName", data=df, kind="bar", estimator=np.mean)
plt.show(block=True)

#############################################
# TASK 2: Convert the satis_checkin_day_diff variable to a new categorical variable called EB_Score.
#############################################
bins = [-1, 7, 30, 90, df["SaleCheckInDayDiff"].max()]
labels = ["Last Minuters", "Potential Planners", "Planners", "Early Bookers"]

df["EB_Score"] = pd.cut(df["SaleCheckInDayDiff"], bins, labels=labels)
df.head()

#############################################
# TASK 3: Examine the average prices and frequencies by City, Concept, [EB_Score, Seasons, CInDay] breakdown.
#############################################
# Average prices by City-Concept-EB Score
df.groupby(["SaleCityName", 'ConceptName', "EB_Score"]).agg({"Price": ["mean", "count"]})

# Average prices by City-Concept-Season
df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": ["mean", "count"]})

# Average prices by City-Concept-CInDay
df.groupby(["SaleCityName", "ConceptName", "CInDay"]).agg({"Price": ["mean", "count"]})

#############################################
# TASK 4: Sort the output of the City-Concept-Season breakdown according to PRICE.
#############################################
# Apply sort_values method to PRICE in descending order for a better view of the output of the previous question.
# Save the output as agg_df.
agg_df = df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": "mean"}).sort_values("Price",
                                                                                                   ascending=False)
agg_df.head(10)

#############################################
# TASK 5: Convert the names in the index to variable names.
#############################################
# All variables in the output of the third question except PRICE are index names.
# Convert these names to variable names.

agg_df.reset_index(inplace=True)
agg_df.head()

#############################################
# TASK 6: Define new level-based sales and add them as variables to the dataset.
#############################################
# Define a new variable called sales_level_based and add it to the dataset.
agg_df['sales_level_based'] = agg_df[["SaleCityName", "ConceptName", "Seasons"]] \
    .agg(lambda x: '_'.join(x).upper(), axis=1)
#############################################
# TASK 7: Segment the customers.
#############################################
# Segment the customers based on PRICE,
# add the segments to agg_df with the name "SEGMENT",
# and describe the segments.
agg_df["SEGMENT"] = pd.qcut(agg_df["Price"], 4, labels=["D", "C", "B", "A"])
agg_df.head(30)
agg_df.groupby("SEGMENT").agg({"Price": ["mean", "max", "sum"]})

#############################################
# TASK 8: Sort the final df according to the price variable.
# In which segment is "ANTALYA_HERŞEY DAHIL_HIGH" and what is the expected price?
#############################################
agg_df.sort_values(by="Price")


def get_segment_and_expected_price(user):
    user_row = agg_df[agg_df["sales_level_based"] == user]
    segment = user_row["SEGMENT"].values[0]
    expected_price = user_row["Price"].values[0]
    return segment, expected_price


get_segment_and_expected_price("ANTALYA_HERŞEY DAHIL_HIGH")

# ('B', 64.92006453392972)
