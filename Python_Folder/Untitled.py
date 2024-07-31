#!/usr/bin/env python
# coding: utf-8

# In[9]:


# Import necessary libraries
import pandas as pd
from sqlalchemy import create_engine

# Database credentials
user = 'root'
password = 'Siddharth'
host = 'localhost'
port = 3306
database = 'customer_purchase_db'

# Create a connection string
connection_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'

# Create a SQLAlchemy engine
engine = create_engine(connection_string)


# In[10]:


# Load data from the Purchase table
query = "SELECT * FROM Purchase"
purchase_df = pd.read_sql(query, engine)

# Print column names to debug the issue
print("Columns in purchase_df:", purchase_df.columns)


# In[11]:


# Check if 'PurchaseDate' is in the DataFrame
if 'PurchaseDate' in purchase_df.columns:
    # Ensure PurchaseDate is in datetime format
    purchase_df['PurchaseDate'] = pd.to_datetime(purchase_df['PurchaseDate'])
else:
    print("Error: 'PurchaseDate' column not found in purchase_df")


# Calculate Total Purchases, Total Revenue, and Average Purchase Value

# In[12]:


# Calculate total purchases
total_purchases = purchase_df['PurchaseQuantity'].sum()

# Calculate total revenue
total_revenue = (purchase_df['PurchasePrice'] * purchase_df['PurchaseQuantity']).sum()

# Calculate average purchase value
average_purchase_value = total_revenue / total_purchases

print(f"Total Purchases: {total_purchases}")
print(f"Total Revenue: {total_revenue}")
print(f"Average Purchase Value: {average_purchase_value}")


# Identify Top Customers and Their Purchasing Behavior

# In[13]:


# Load customer data
customer_df = pd.read_sql("SELECT * FROM Customer", engine)

# Identify top customers
top_customers = purchase_df.groupby('CustomerID').agg({
    'PurchaseQuantity': 'sum',
    'PurchasePrice': lambda x: (x * purchase_df.loc[x.index, 'PurchaseQuantity']).sum()
}).rename(columns={'PurchaseQuantity': 'TotalQuantity', 'PurchasePrice': 'TotalRevenue'}).sort_values(by='TotalRevenue', ascending=False)

# Merge with customer information
top_customers = top_customers.merge(customer_df, on='CustomerID')

print("Top Customers:")
print(top_customers.head())


# Analyze purchase trends over time (monthly, quarterly, yearly).

# In[14]:


# Analyze purchase trends over time (monthly, quarterly, yearly)
# Set PurchaseDate as index for resampling
purchase_df.set_index('PurchaseDate', inplace=True)

# Monthly trend analysis
monthly_trends = purchase_df.resample('M').agg({
    'PurchaseQuantity': 'sum',
    'PurchasePrice': lambda x: (x * purchase_df.loc[x.index, 'PurchaseQuantity']).sum()
})

print("Monthly Purchase Trends:")
print(monthly_trends)

# Quarterly trend analysis
quarterly_trends = purchase_df.resample('Q').agg({
    'PurchaseQuantity': 'sum',
    'PurchasePrice': lambda x: (x * purchase_df.loc[x.index, 'PurchaseQuantity']).sum()
})

print("Quarterly Purchase Trends:")
print(quarterly_trends)

# Yearly trend analysis
yearly_trends = purchase_df.resample('Y').agg({
    'PurchaseQuantity': 'sum',
    'PurchasePrice': lambda x: (x * purchase_df.loc[x.index, 'PurchaseQuantity']).sum()
})

print("Yearly Purchase Trends:")
print(yearly_trends)


# Identify the top-performing product categories.

# In[15]:


# Load product data
product_df = pd.read_sql("SELECT * FROM Product", engine)

# Merge purchase data with product data
purchase_with_product = purchase_df.reset_index().merge(product_df, on='ProductID')

# Top performing product categories
top_categories = purchase_with_product.groupby('ProductCategory').agg({
    'PurchaseQuantity': 'sum',
    'PurchasePrice': lambda x: (x * purchase_with_product.loc[x.index, 'PurchaseQuantity']).sum()
}).rename(columns={'PurchaseQuantity': 'TotalQuantity', 'PurchasePrice': 'TotalRevenue'}).sort_values(by='TotalRevenue', ascending=False)

print("Top Performing Product Categories:")
print(top_categories)


# generate a summary report with the key insights.

# In[17]:


# Import necessary libraries
import pandas as pd
from sqlalchemy import create_engine

# Database credentials
user = 'root'
password = 'Siddharth'
host = 'localhost'
port = 3306
database = 'customer_purchase_db'

# Create a connection string
connection_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'

# Create a SQLAlchemy engine
engine = create_engine(connection_string)

# Load data from the Purchase table
query = "SELECT * FROM Purchase"
purchase_df = pd.read_sql(query, engine)

# Ensure PurchaseDate is in datetime format
if 'PurchaseDate' in purchase_df.columns:
    purchase_df['PurchaseDate'] = pd.to_datetime(purchase_df['PurchaseDate'])
else:
    raise KeyError("Error: 'PurchaseDate' column not found in purchase_df")

# Calculate total purchases
total_purchases = purchase_df['PurchaseQuantity'].sum()

# Calculate total revenue
total_revenue = (purchase_df['PurchasePrice'] * purchase_df['PurchaseQuantity']).sum()

# Calculate average purchase value
average_purchase_value = total_revenue / total_purchases

# Load customer data
customer_df = pd.read_sql("SELECT * FROM Customer", engine)

# Identify top customers
top_customers = purchase_df.groupby('CustomerID').agg({
    'PurchaseQuantity': 'sum',
    'PurchasePrice': lambda x: (x * purchase_df.loc[x.index, 'PurchaseQuantity']).sum()
}).rename(columns={'PurchaseQuantity': 'TotalQuantity', 'PurchasePrice': 'TotalRevenue'}).sort_values(by='TotalRevenue', ascending=False)

# Merge with customer information
top_customers = top_customers.merge(customer_df, on='CustomerID')

# Analyze purchase trends over time (monthly, quarterly, yearly)
# Set PurchaseDate as index for resampling
purchase_df.set_index('PurchaseDate', inplace=True)

# Monthly trend analysis
monthly_trends = purchase_df.resample('M').agg({
    'PurchaseQuantity': 'sum',
    'PurchasePrice': lambda x: (x * purchase_df.loc[x.index, 'PurchaseQuantity']).sum()
})

# Quarterly trend analysis
quarterly_trends = purchase_df.resample('Q').agg({
    'PurchaseQuantity': 'sum',
    'PurchasePrice': lambda x: (x * purchase_df.loc[x.index, 'PurchaseQuantity']).sum()
})

# Yearly trend analysis
yearly_trends = purchase_df.resample('Y').agg({
    'PurchaseQuantity': 'sum',
    'PurchasePrice': lambda x: (x * purchase_df.loc[x.index, 'PurchaseQuantity']).sum()
})

# Load product data
product_df = pd.read_sql("SELECT * FROM Product", engine)

# Merge purchase data with product data
purchase_with_product = purchase_df.reset_index().merge(product_df, on='ProductID')

# Top performing product categories
top_categories = purchase_with_product.groupby('ProductCategory').agg({
    'PurchaseQuantity': 'sum',
    'PurchasePrice': lambda x: (x * purchase_with_product.loc[x.index, 'PurchaseQuantity']).sum()
}).rename(columns={'PurchaseQuantity': 'TotalQuantity', 'PurchasePrice': 'TotalRevenue'}).sort_values(by='TotalRevenue', ascending=False)

# Generate summary report in tabular format
summary_report = {
    "Metric": ["Total Purchases", "Total Revenue", "Average Purchase Value"],
    "Value": [total_purchases, total_revenue, average_purchase_value]
}

summary_report_df = pd.DataFrame(summary_report)

print("Summary Report:")
print(summary_report_df.to_string(index=False))

print("\nTop Customers:")
print(top_customers[['CustomerID', 'CustomerName', 'TotalQuantity', 'TotalRevenue']].head().to_string(index=False))

print("\nMonthly Purchase Trends:")
print(monthly_trends.to_string(index=True))

print("\nQuarterly Purchase Trends:")
print(quarterly_trends.to_string(index=True))

print("\nYearly Purchase Trends:")
print(yearly_trends.to_string(index=True))

print("\nTop Performing Product Categories:")
print(top_categories[['TotalQuantity', 'TotalRevenue']].head().to_string(index=False))


# In[ ]:




