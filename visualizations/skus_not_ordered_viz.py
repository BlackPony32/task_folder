import plotly.express as px
import pandas as pd
import streamlit as st
import numpy as np
from plotly.colors import sequential
from plotly.colors import qualitative
#Data preprocess
def preprocess_data(data):
    """
    Data preprocessing: data type conversion and cleaning.

    Args:
        data: A Pandas DataFrame with the source data.

    Returns:
        Pandas DataFrame with the processed data.
    """

    # Identify numeric columns automatically
    numeric_cols = data.select_dtypes(include=np.number).columns

    # Process numeric columns
    for col in numeric_cols:
        # Check for missing values (NaN)
        if np.isnan(data[col]).any():
            print(f"Warning: Column '{col}' contains missing values (NaN).")

    # Remove currency symbols and thousands separators
    data[numeric_cols] = data[numeric_cols].replace('[$,]', '', regex=True).astype(float)

    return data

#Distribution of unordered products across different categories
def create_unordered_products_by_category_plot(df):
    category_counts = df['Category name'].value_counts()

    fig = px.bar(x=category_counts.index, y=category_counts.values,
                 title="Number of Unordered Products per Category")
    fig.update_layout(xaxis_title="Category", yaxis_title="Number of Unordered Products", xaxis_tickangle=45)
    st.plotly_chart(fig)

#Visualizes the distribution of available cases for unordered products using a histogram
def create_available_cases_distribution_plot(df):
    stock_levels = {
        "Low Stock": (0, 10),
        "Medium Stock": (11, 50),
        "High Stock": (51, float('inf'))
    }

    def assign_stock_level(stock):
        for level, (min_val, max_val) in stock_levels.items():
            if min_val <= stock <= max_val:
                return level

    df["Stock Level"] = df['Available cases (QTY)'].apply(assign_stock_level)
    stock_level_counts = df["Stock Level"].value_counts()

    fig = px.bar(x=stock_level_counts.index, y=stock_level_counts.values,
                 title="Distribution of Unordered Products by Stock Level")
    fig.update_layout(xaxis_title="Stock Level", yaxis_title="Number of Products")
    fig.update_traces(marker_line_color='black', marker_line_width=1)  # Add black border to bars
    fig.update_traces(marker_color=qualitative.Pastel) 
    st.plotly_chart(fig)


def price_vs_available_cases_app(df):
    st.title("Average Available Cases by Price Range and Category")

    category_options = df['Category name'].unique()
    selected_category = st.selectbox("Select a Category", category_options)

    df['Price Range'] = pd.cut(df['Retail price'], bins=3, labels=["Low", "Medium", "High"])
    average_cases_data = df[df['Category name'] == selected_category].groupby(['Price Range'])['Available cases (QTY)'].mean()

    fig = px.bar(average_cases_data, x=average_cases_data.index, y=average_cases_data.values,
                 title=f"Average Available Cases for {selected_category}")
    fig.update_layout(xaxis_title="Retail Price Range", yaxis_title="Average Available Cases")
    fig.update_traces(marker_line_color='black', marker_line_width=1)  # Add black border to bars
    st.plotly_chart(fig, use_container_width=True)

#Visualizes the relationship between wholesale and retail prices for unordered products
def create_wholesale_vs_retail_price_scatter(df):
    tab1, tab2 = st.tabs(["Available Cases vs Profit Margin", "Wholesale vs Retail Price"])

    with tab1:
        df["Profit Margin %"] = (df['Retail price'] - df['Wholesale price']) / df['Wholesale price'] * 100
        fig1 = px.scatter(
            df, 
            x='Available cases (QTY)', 
            y="Profit Margin %", 
            color='Category name',
            hover_data=['Category name', 'Retail price', 'Wholesale price'],
            title="Available Cases vs. Profit Margin % for Unordered Products",
            labels={
                "Available cases (QTY)": "Available Cases",
                "Profit Margin %": "Profit Margin (%)"
            }
        )
        fig1.update_layout(
            xaxis_title="Available Cases",
            yaxis_title="Profit Margin (%)",
            font=dict(size=12),
            title_font_size=14,
            showlegend=True
        )
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        fig2 = px.scatter(df, x='Wholesale price', y='Retail price', 
                         title="Wholesale Price vs. Retail Price for Unordered Products")
        fig2.update_layout(xaxis_title="Wholesale Price", yaxis_title="Retail Price")
        st.plotly_chart(fig2, use_container_width=True)

def df_unordered_products_per_category_and_price_range(df, category_col='Category name', retail_price_col='Retail price'):
    price_ranges = [0, 20, 40, 60, 80, 100]
    price_labels = ["0-20", "20-40", "40-60", "60-80", "80-100"]
    df['Price Range'] = pd.cut(df[retail_price_col], bins=price_ranges, labels=price_labels)
    result = df.groupby([category_col, 'Price Range']).size().unstack(fill_value=0)
    fig = px.imshow(result,
                    labels=dict(x="Price Range", y="Category", color="Number of Products"),
                    title="Number of Unordered Products by Category and Price Range")
    fig.update_xaxes(side="top")
    st.plotly_chart(fig, use_container_width=True)