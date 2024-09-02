#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


data=pd.read_csv("C:\\Users\\karth\\Downloads\\archive\\supermarket_sales - Sheet1.csv")
data


# In[3]:


data.head(5)


# In[4]:


data.shape


# In[5]:


data.info()


# In[6]:


data.describe()


# In[7]:


data.isna().sum()


# In[8]:


data.duplicated().sum()


# In[9]:


data.columns


# In[10]:


data.dtypes


# In[12]:


def display_pie_chart(values, labels, title, chart_type = 'pie'):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot()
    if chart_type == 'doughnat':
        explode = np.full(len(labels), 0.05)
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, explode = explode, pctdistance=0.85)
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
    else:
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  
    ax.set_title(title)
    
    
    plt.savefig(f'{labels[0]}', bbox_inches='tight')
    plt.show()


# In[13]:


def group_by_column(df, col, function):
    grouped_df = df.groupby(col).agg(function).reset_index()
    grouped_df = grouped_df.set_index(col)

    return grouped_df


# # 1- What is the gender with the most purchases?

# In[14]:


gender_and_total = data[['Gender', 'Total']]

grouped_by_gender_df = group_by_column(gender_and_total, 'Gender', 'sum')

print(grouped_by_gender_df)

labels = grouped_by_gender_df.index
values = grouped_by_gender_df['Total']

display_pie_chart(values, labels, 'Total Sales by Gender')


# # 2- Is there a difference in purchases between a customer with a membership card and a normal customer?

# In[15]:


group_by_type = data[['Customer type', 'Total']]

group_by_type_df = group_by_column(group_by_type, 'Customer type', 'sum')

print(group_by_type_df)

labels = group_by_type_df.index
values = group_by_type_df['Total']

display_pie_chart(values, labels, 'Total Sales by Customer type', chart_type = 'doughnat')


# # 3- What type of products do both genders buy the most?

# In[16]:


group = data.groupby(['Product line', 'Gender']).size().reset_index()
group.columns = ['Product line', 'Gender', 'Count']

group.head(5)


# In[17]:


plt.figure(figsize=(15, 10))


sns.barplot(data=group, x="Product line", y="Count", hue="Gender")
plt.title('Count of Product Line by Gender')
plt.xlabel('Product Line')
plt.ylabel('Count')
plt.savefig('count_by_gender')
plt.show()


# # 1- Which cities and branches are top performers in sales and revenue?

# In[18]:


data.City.unique()


# In[19]:


branches_sales = data.groupby('Branch')['Total'].sum()

for branch, sales in branches_sales.items():
    print(f'Branch {branch} : {sales}')
    
print('-' * 50)

most_selling_branch = branches_sales.idxmax()

print(f'The most selling branch is {most_selling_branch}')


# plt.figure(figsize=(10, 6))
# 
# branches_sales.plot(kind='bar', color='grey')
# plt.title('Total Sales by City')
# plt.xlabel('City')
# plt.ylabel('Total Sales')
# plt.show()
# 

# # 2- Are there differences in customer satisfaction among cities and branches?

# In[20]:


customer_rate = data.groupby('City')['Rating'].mean()

cities = customer_rate.index
rates = customer_rate

print(customer_rate)

display_pie_chart(rates, cities, 'Avarage Customers Rate by City')


# # 3- Most sold product?

# In[21]:


product_sales = data.groupby('Product line')['Quantity'].sum()

highest_selling_product = product_sales.idxmax()

print("Highest selling product:", highest_selling_product)


# In[22]:


plt.figure(figsize=(12, 8))

product_sales.plot(kind='bar')
plt.title('Product Sales by Quantity')
plt.xlabel('Product Category',  rotation=0)
plt.ylabel('Quantity')
plt.show()


# # 4- How do product lines impact revenue and gross income?

# In[23]:


grouped_products = data.groupby('Product line')['gross income'].sum()

products = grouped_products.index
income = grouped_products

display_pie_chart(income, products, '', chart_type='doughnat')


# In[24]:


dates = pd.DataFrame()

# Convert Date values in dataset to pd.datetime object
dates['Date'] = pd.to_datetime(data['Date'])

# separate year value form datetime object
dates['Year'] = dates['Date'].dt.year

# separate month value form datetime object
dates['Month'] = dates['Date'].dt.month

# separate day value form datetime object
dates['Day'] = dates['Date'].dt.day

# Get Total column values from the original datafram 
dates['Total'] = data['Total']

dates


# In[25]:


monthly_sales = dates.groupby(['Month', 'Day'])['Total'].sum()

monthly_sales


# In[26]:


for month in range(1, 4):
    plt.figure(figsize=(8, 6))
    month_data = monthly_sales.loc[month]
    plt.plot(month_data.index.get_level_values('Day'), month_data.values)
    plt.title(f'Monthly Sales for Month {month}')
    plt.xlabel('Day')
    plt.ylabel('Total Sales')
    plt.grid(True)
    plt.savefig(f'{month}')
    plt.show()


# In[ ]:




