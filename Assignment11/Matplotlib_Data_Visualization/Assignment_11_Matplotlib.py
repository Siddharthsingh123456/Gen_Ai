import csv
import matplotlib.pyplot as plt


# Assignment 11 - Matplotlib
# Dataset: SuperStore Dataset from Kaggle
# I used simple lists, loops and dictionaries for this assignment.


# ==========================================================
# Load the CSV file
# ==========================================================

file = open("Superstore.csv", "r", encoding="utf-8")
data = csv.DictReader(file)

rows = []

for row in data:
    rows.append(row)

file.close()

print("Number of rows:", len(rows))
print("Columns:", rows[0].keys())


# ==========================================================
# Task 1 - Line Plot
# Sales trend over months
# ==========================================================

month_sales = {}

for row in rows:
    date = row["Order Date"]

    # Skip a row if the required values are empty.
    if date == "" or row["Sales"] == "":
        continue

    # The date is in month/day/year format.
    month = date.split("/")[0]
    year = date.split("/")[-1]

    # Make a simple key such as 2015-01.
    key = year + "-" + month

    sales = float(row["Sales"])

    if key in month_sales:
        month_sales[key] = month_sales[key] + sales
    else:
        month_sales[key] = sales

months = sorted(month_sales.keys())
sales_values = []

for month in months:
    sales_values.append(month_sales[month])

plt.figure()
plt.plot(months, sales_values)
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


# ==========================================================
# Task 2 - Scatter Plot
# Quantity Sold vs Sales
# ==========================================================

quantity = []
sales = []

for row in rows:
    if row["Quantity"] != "" and row["Sales"] != "":
        quantity.append(float(row["Quantity"]))
        sales.append(float(row["Sales"]))

plt.figure()
plt.scatter(quantity, sales)
plt.title("Quantity Sold vs Sales")
plt.xlabel("Quantity")
plt.ylabel("Sales")
plt.show()


# ==========================================================
# Task 3 - Bar Plot
# Vertical and horizontal bar charts
# ==========================================================

region_sales = {}

for row in rows:
    region = row["Region"]

    if region == "" or row["Sales"] == "":
        continue

    value = float(row["Sales"])

    if region in region_sales:
        region_sales[region] = region_sales[region] + value
    else:
        region_sales[region] = value

regions = list(region_sales.keys())
values = []

for region in regions:
    values.append(region_sales[region])


# Vertical bar
plt.figure()
plt.bar(regions, values)
plt.title("Sales by Region")
plt.xlabel("Region")
plt.ylabel("Sales")
plt.show()


# Horizontal bar
plt.figure()
plt.barh(regions, values)
plt.title("Sales by Region - Horizontal Bar")
plt.xlabel("Sales")
plt.ylabel("Region")
plt.show()


# ==========================================================
# Task 4 - Multiple Bar Plot
# Compare sales of different years
# ==========================================================

years = ["2015", "2016", "2017", "2018"]
month_names = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

year_month_sales = {}

for year in years:
    year_month_sales[year] = {}

    for month in range(1, 13):
        year_month_sales[year][str(month)] = 0


for row in rows:
    date = row["Order Date"]

    if date == "" or row["Sales"] == "":
        continue

    month = date.split("/")[0]
    year = date.split("/")[-1]

    if year in year_month_sales:
        year_month_sales[year][month] = (
            year_month_sales[year][month]
            + float(row["Sales"])
        )


# This chart compares the four years month by month.
x = list(range(12))
width = 0.2

plt.figure()

for i in range(4):
    values = []

    for month in range(1, 13):
        values.append(
            year_month_sales[years[i]][str(month)]
        )

    positions = []

    for number in x:
        positions.append(number + (i - 1.5) * width)

    plt.bar(
        positions,
        values,
        width=width,
        label=years[i]
    )

plt.title("Monthly Sales Comparison by Year")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(x, month_names)
plt.legend()
plt.show()


# ==========================================================
# Task 5 - Stacked Bar Chart
# Sales by region and category
# ==========================================================

categories = [
    "Furniture",
    "Office Supplies",
    "Technology"
]

stacked_sales = {}

for region in regions:
    stacked_sales[region] = {}

    for category in categories:
        stacked_sales[region][category] = 0


for row in rows:
    region = row["Region"]
    category = row["Category"]

    if region == "" or category == "" or row["Sales"] == "":
        continue

    if category in categories:
        stacked_sales[region][category] = (
            stacked_sales[region][category]
            + float(row["Sales"])
        )


bottom = [0, 0, 0, 0]

plt.figure()

for category in categories:
    values = []

    for region in regions:
        values.append(
            stacked_sales[region][category]
        )

    plt.bar(
        regions,
        values,
        bottom=bottom,
        label=category
    )

    for i in range(len(bottom)):
        bottom[i] = bottom[i] + values[i]

plt.title("Sales by Region and Category")
plt.xlabel("Region")
plt.ylabel("Sales")
plt.legend()
plt.show()


# ==========================================================
# Task 6 - Histogram
# Distribution of Sales
# ==========================================================

sales_values = []

for row in rows:
    if row["Sales"] != "":
        sales_values.append(float(row["Sales"]))

plt.figure()
plt.hist(sales_values, bins=10)
plt.title("Distribution of Sales")
plt.xlabel("Sales")
plt.ylabel("Frequency")
plt.show()


# ==========================================================
# Task 7 - Pie Chart
# Market share by category
# ==========================================================

category_sales = {}

for row in rows:
    category = row["Category"]

    if category == "" or row["Sales"] == "":
        continue

    value = float(row["Sales"])

    if category in category_sales:
        category_sales[category] = category_sales[category] + value
    else:
        category_sales[category] = value

labels = list(category_sales.keys())
values = []

for category in labels:
    values.append(category_sales[category])

plt.figure()
plt.pie(values, labels=labels, autopct="%1.1f%%")
plt.title("Sales Share by Category")
plt.show()
