import plotly.express as px
import pandas as pd
import streamlit as st
import numpy as np
from plotly.colors import sequential
from plotly.colors import qualitative

#Analyzes and visualizes the total inventory value by category
def df_analyze_inventory_value_by_category(df):
    if df['Wholesale price'].dtype == 'object':
        df['Wholesale price'] = pd.to_numeric(df['Wholesale price'].str.replace(',', '').str.replace('$ ', ''))
    df["Inventory Value"] = df["Available cases (QTY)"] * df["Wholesale price"]
    category_value = df.groupby("Category name")["Inventory Value"].sum()
    fig = px.bar(category_value,
                 title="Total Inventory Value by Category",
                 labels={'value': 'Total Inventory Value', 'index': 'Category'})
    st.plotly_chart(fig, use_container_width=True)

#Analyzing the correlation between available quantity and retail price
def df_analyze_quantity_vs_retail_price(df):
    for col in ["Retail price", "Wholesale price"]:
        if df[col].dtype == 'object':
            df[col] = pd.to_numeric(df[col].str.replace(',', '').str.replace('$ ', ''))

    # Handle NaN values in 'Wholesale price'
    df['Wholesale price'] = df['Wholesale price'].fillna(0)  # Replace NaN with 0 or another suitable value

    fig = px.scatter(df, x="Available cases (QTY)", y="Retail price",
                     color="Category name", size="Wholesale price", 
                     hover_data=['Category name', 'Wholesale price'],
                     title="Available Quantity vs. Retail Price",
                     labels={'Available cases (QTY)': 'Available Cases', 
                             'Retail price': 'Retail Price'})
    fig.update_layout(legend_title_text='Category')
    st.plotly_chart(fig, use_container_width=True)

#Analyzing Inventory Value Distribution Across Manufacturers
def df_analyze_inventory_value_by_manufacturer(df):
    if df['Wholesale price'].dtype == 'object':
        df['Wholesale price'] = pd.to_numeric(df['Wholesale price'].str.replace(',', '').str.replace('$ ', ''))
    df["Inventory Value"] = df["Available cases (QTY)"] * df["Wholesale price"]
    manufacturer_value = df.groupby("Manufacturer name")["Inventory Value"].sum()
    fig = px.bar(manufacturer_value,
                 title="Total Inventory Value by Manufacturer",
                 labels={'value': 'Total Inventory Value', 'index': 'Manufacturer'})
    st.plotly_chart(fig, use_container_width=True)

#Analyzes and visualizes the average inventory value per unit for each product
def df_analyze_inventory_value_per_unit(df):
    if df['Wholesale price'].dtype == 'object':
        df['Wholesale price'] = pd.to_numeric(df['Wholesale price'].str.replace(',', '').str.replace('$ ', ''))
    df["Inventory Value per Unit"] = pd.to_numeric(df["Wholesale price"], errors='coerce')
    df = df.dropna(subset=["Inventory Value per Unit"])
    df = df.sort_values(by="Inventory Value per Unit", ascending=False)
    fig = px.bar(df, y="Product name", x="Inventory Value per Unit", orientation='h',
                 title="Average Inventory Value per Unit",
                 labels={'Inventory Value per Unit': 'Inventory Value per Unit', 'Product name': 'Product Name'})
    st.plotly_chart(fig, use_container_width=True)

#Comparing Average Retail Prices Across Categories
def df_compare_average_retail_prices(df):
    if df['Retail price'].dtype == 'object':
        df['Retail price'] = pd.to_numeric(df['Retail price'].str.replace(',', '').str.replace('$ ', ''))
    average_prices = df.groupby("Category name")["Retail price"].mean()
    fig = px.bar(average_prices,
                 title="Average Retail Price by Category",
                 labels={'value': 'Average Retail Price', 'index': 'Category'})
    st.plotly_chart(fig, use_container_width=True)



