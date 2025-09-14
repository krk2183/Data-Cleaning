import kagglehub

# Download latest version
path = kagglehub.dataset_download("ahmedmohamed2003/retail-store-sales-dirty-for-data-cleaning")

print("Path to dataset files:", path)

import os
import pandas as pd
import matplotlib.pyplot as plt
for x in os.walk(path):
  print(x)

data = os.path.join(path,"retail_store_sales.csv")
dataset = pd.read_csv(open(data,"r"))

import numpy as np

# Calculate total quantity for each item and find the most bought per category
popular_items_per_category = dataset.groupby('Category')['Item'].apply(lambda x: x.mode()[0] if not x.mode().empty else np.nan)
print("Most popular item per category:")
print(popular_items_per_category)

"""Method 1:
Create a price lookup table for each table to fill in the missing item prices

Secondly it fills in the missing item anme from category with the most popular item from that category to maintain logicality and consistency

And then it checks if the discount is applied by checking if the sum of the customer's purchase matches their payment. If it does then they didn't get a discount but if it doesn't then they did.

This keeps the data highly accurate and
"""


mask = dataset['Item'].isnull()

# Here we use map to fill the missing values
dataset.loc[mask, 'Item'] = dataset.loc[mask, 'Category'].map(popular_items_per_category)


numerical_cols = ['Price Per Unit', 'Quantity', 'Total Spent']
for col in numerical_cols:
    dataset[col] = dataset[col].fillna(dataset[col].mean())

dataset['Calculated_Total'] = dataset['Quantity'] * dataset['Price Per Unit']
dataset['Discount Applied'] = dataset['Calculated_Total'] != dataset['Total Spent']
dataset = dataset.drop('Calculated_Total',axis=1)

print("\nDataFrame after filling missing items:")
print(dataset)

missing_values = dataset.isnull().sum()
display(missing_values)

missing_values.plot(kind='bar')
plt.title("Number of Missing Values Per Column")
plt.ylabel("Number of Missing Values")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()









"""# Method 2 filling both numerical and categorical columns with the mean"""

dataset['Calculated_Total'] = dataset['Quantity'] * dataset['Price Per Unit']
dataset['Discount Applied'] = dataset['Calculated_Total'] != dataset['Total Spent']
dataset = dataset.drop('Calculated_Total',axis=1)
display(dataset.head())

numerical_cols = ['Price Per Unit', 'Quantity', 'Total Spent']
for col in numerical_cols:
    dataset[col] = dataset[col].fillna(dataset[col].mean())


categorical_cols = ['Item']
for col in categorical_cols:
    dataset[col] = dataset[col].fillna(dataset[col].mode()[0])

display(dataset.isnull().sum())

missing_values.plot(kind='bar')
plt.title("Number of Missing Values Per Column After Processing")
plt.ylabel("Number of Missing Values")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()



