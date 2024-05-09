import plotly.express as px
import pandas as pd
import streamlit as st
import numpy as np
from plotly.colors import sequential
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

def create_available_cases_plot(df):
    df['Available cases (QTY)'] = df['Available cases (QTY)'].astype(int)

    fig = px.scatter(df, y='Product name', x='Available cases (QTY)', 
                     title='Available Cases (QTY)', text='Available cases (QTY)')
    fig.update_traces(textposition="top center", marker_color='steelblue')  # Set marker color
    fig.update_layout(xaxis_tickangle=45, showlegend=False,  # Remove legend
                      plot_bgcolor='white',  # Set background color to white
                      xaxis={'categoryorder':'total descending'})  # Sort x-axis
    st.plotly_chart(fig)


def product_analysis_app(df):
    st.title("Product Sales Analysis")

    tab1, tab2 = st.tabs(["Total Revenue", "Cases Sold"])

    product_data = df.groupby('Product name')[['Total revenue', 'Cases sold']].sum()

    with tab1:
        fig1 = px.bar(product_data, x=product_data.index, y='Total revenue',
                      title="Total Revenue by Product")
        fig1.update_layout(xaxis_title="Product", yaxis_title="Revenue", xaxis_tickangle=45)
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        fig2 = px.bar(product_data, x=product_data.index, y='Cases sold',
                      title="Total Cases Sold by Product")
        fig2.update_layout(xaxis_title="Product", yaxis_title="Cases Sold", xaxis_tickangle=45)
        st.plotly_chart(fig2, use_container_width=True)


def create_cases_revenue_relationship_plot(df):
    fig = px.bar(df, x='Cases sold', y='Total revenue', color='Total revenue',
                 title="Relationship between Cases Sold and Total Revenue",
                 color_continuous_scale='Greens', text='Total revenue')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside', width=25)  # Adjust bar width
    fig.update_layout(xaxis_title="Cases Sold", yaxis_title="Total Revenue", 
                      plot_bgcolor='white')  # Set background color to white 
    st.plotly_chart(fig)


def price_comparison_app(df):
    st.title("Average Price Comparison by Category")

    tab1, tab2 = st.tabs(["Wholesale Price", "Retail Price"])

    average_prices = df.groupby('Category name')[['Wholesale price', 'Retail price']].mean()

    with tab1:
        fig1 = px.bar(average_prices, x=average_prices.index, y='Wholesale price',
                      title="Average Wholesale Price by Category")
        fig1.update_layout(xaxis_title="Category", yaxis_title="Wholesale Price", xaxis_tickangle=45)
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        fig2 = px.bar(average_prices, x=average_prices.index, y='Retail price',
                      title="Average Retail Price by Category")
        fig2.update_layout(xaxis_title="Category", yaxis_title="Retail Price", xaxis_tickangle=45)
        st.plotly_chart(fig2, use_container_width=True)


def create_revenue_vs_profit_plot(df):
    st.title("Revenue Analysis")

    tab1, tab2 = st.tabs(["Revenue vs. Profit", "Revenue Breakdown by Category"])

    df['Profit'] = (df['Retail price'] - df['Wholesale price']) * df['Cases sold']
    category_revenue = df.groupby('Category name')['Total revenue'].sum()

    with tab1:
        fig1 = px.scatter(df, x='Total revenue', y='Profit', hover_name='Product name',
                         title="Total Revenue vs. Profit per Product")
        fig1.update_layout(xaxis_title="Total Revenue", yaxis_title="Profit")
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("""
## The Relationship Between Total Revenue and Profit for Different Products

Visualizing the relationship between total revenue and profit for different products provides valuable insights into product performance and profitability:

**Profitability Analysis:**

*   The plot allows for quick assessment of each product's profitability by visualizing its profit in relation to its total revenue.
*   This helps identify high-performing products in terms of generating profit and those that might require attention.

**Identifying Trends:**

*   While the provided example mainly focuses on "Ginger Shots," a real-world scenario with diverse products could reveal trends or patterns.
*   For example, it might show a general correlation between total revenue and profit or if certain product categories tend to be more profitable than others.

**Outlier Detection:**

*   The plot helps pinpoint any data points that deviate significantly from the overall trend.
*   This could be a product with high revenue but low profit, indicating potential pricing or cost issues that require further investigation.

**Decision Making Support:**

*   Businesses can utilize this information to make strategic decisions regarding product pricing, cost management, and marketing efforts.
*   It can help identify products with high-profit potential, those requiring adjustments to improve profitability, and areas where resources should be allocated for maximum return. 
""")
    with tab2:
        fig2 = px.pie(category_revenue, values=category_revenue.values, names=category_revenue.index,
                      title="Revenue Breakdown by Category")
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("""
## Distribution of Revenue Across Different Categories

A pie chart visualizing the distribution of revenue across different categories offers insights into the relative contribution of each category:

**Proportion Visualization:**

*   The pie chart effectively showcases the proportion of each category's contribution to total revenue.
*   A quick glance reveals the relative sizes of each slice, highlighting which categories generate the most significant portion of the revenue.

**Category Comparison:**

*   It provides a clear visual comparison between different categories.
*   In this example, we can easily see that the "Drinks" category dominates revenue generation compared to the "Uncategorized" category.

**Identifying Key Drivers:**

*   Businesses can use this information to identify the key drivers of their revenue.
*   This knowledge is essential for strategic decision-making related to product development, marketing, and resource allocation.

**Tracking Changes Over Time:**

*   Creating pie charts for different time periods allows businesses to track how the revenue distribution across categories evolves over time.
*   This can reveal valuable insights into shifts in consumer preferences, market trends, and the effectiveness of sales strategies.
""")
