import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

def preprocess_data(data):
    """
    Data preprocessing: data type conversion and cleaning.

    Args:
        data: A Pandas DataFrame with the source data.

    Returns:
        Pandas DataFrame with the processed data.
    """

    # Convert creation date to datetime type
    data['Created at'] = pd.to_datetime(data['Created at'])

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

#@title Total sales
def visualize_product_analysis(data, product_col='Product name', grand_total_col='Grand total'):
    product_data = data.groupby(product_col)[grand_total_col].agg(['sum', 'count']).sort_values(by='sum', ascending=False)

    # Create two tabs for the visualizations
    tab1, tab2 = st.tabs(["Total Sales", "Order Distribution"])

    with tab1:
        fig = px.bar(product_data, x=product_data.index, y='sum', title="Total Sales by Product",
                     color='sum', color_continuous_scale='Viridis')
        fig.update_layout(xaxis_tickangle=45, yaxis_title="Sales Amount", xaxis_title="Product")
        st.plotly_chart(fig)

    with tab2:
        fig = px.bar(product_data, x=product_data.index, y='count', title="Distribution of Orders by Product",
                     color='count', color_continuous_scale='Cividis') 
        fig.update_layout(xaxis_tickangle=45, yaxis_title="Number of Orders", xaxis_title="Product")
        st.plotly_chart(fig)

#@title Sales amount for each client (top 10)
def visualize_sales_trends(data, customer_col='Customer', product_col='Product name',
                           grand_total_col='Grand total', qty_col='QTY'):
    # Create tabs for better organization
    tab1, tab2 = st.tabs(["Top Customers", "Monthly Trend"])

    with tab1:
        st.subheader("Total Sales by Customer (Top 10)")
        top_customers = data.groupby(customer_col)[grand_total_col].sum().nlargest(10)
        fig = px.bar(top_customers, x=top_customers.index, y=top_customers.values,
                     title="Top 10 Customers by Sales Amount", color=top_customers.values,
                     color_continuous_scale='Bluyl')
        fig.update_layout(xaxis_tickangle=45, yaxis_title="Sales Amount", xaxis_title="Customer")
        st.plotly_chart(fig)

    with tab2:
        st.subheader("Monthly Sales Trend")
        monthly_sales = data.groupby(pd.Grouper(key='Created at', freq='M'))[grand_total_col].sum()
        fig = px.line(monthly_sales, x=monthly_sales.index, y=monthly_sales.values, 
                     title="Monthly Sales Trend", markers=True)
        fig.update_layout(xaxis_title="Month", yaxis_title="Sales Amount")
        st.plotly_chart(fig)

#@title Analysis of discounts
def visualize_discount_analysis(data, discount_type_col='Discount type',
                                grand_total_col='Grand total',
                                total_discount_col='Total invoice discount'):
    # Create tabs for different discount visualizations
    tab1, tab2, tab3 = st.tabs(["By Type", "Top Customers", "Distribution"])

    with tab1:
        st.subheader("Discount Amount by Type")
        discount_amounts = data.groupby(discount_type_col)[total_discount_col].sum().sort_values(ascending=False)
        fig = px.bar(discount_amounts, x=discount_amounts.index, y=discount_amounts.values,
                     title="Discount Amount by Type", color=discount_amounts.values,
                     color_continuous_scale='Aggrnyl')
        fig.update_layout(xaxis_tickangle=45, yaxis_title="Discount Amount", xaxis_title="Discount Type")
        st.plotly_chart(fig)

    with tab2:
        st.subheader("Discount Amount by Customer (Top 10)")
        top_customers_discount = data.groupby('Customer')[total_discount_col].sum().nlargest(10)
        fig = px.bar(top_customers_discount, x=top_customers_discount.index, y=top_customers_discount.values,
                     title="Discount Amount by Customer (Top 10)", color=top_customers_discount.values,
                     color_continuous_scale='Pinkyl')
        fig.update_layout(xaxis_tickangle=45, yaxis_title="Discount Amount", xaxis_title="Customer")
        st.plotly_chart(fig)

    with tab3:
        st.subheader("Distribution of Discount Amount by Type")
        fig = px.box(data, x=discount_type_col, y=total_discount_col, title="Distribution of Discount Amount by Type")
        fig.update_layout(xaxis_tickangle=45, yaxis_title="Discount Amount", xaxis_title="Discount Type")
        st.plotly_chart(fig)

#@title Plot with coloring of points by product type
def visualize_combined_analysis(data, product_col='Product name',
                               grand_total_col='Grand total', qty_col='QTY',
                               delivery_status_col='Delivery status'):
    fig = px.scatter(data, x=qty_col, y=grand_total_col, color=product_col,
                     title="Dependence between Quantity and Amount (by Product)", 
                     labels={"x": "Quantity", "y": "Sales Amount"})
    fig.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig)

#@title Analyzes discounts
def analyze_discounts(data):
    discount_counts = data["Discount type"].value_counts()

    fig = px.bar(discount_counts, x=discount_counts.index, y=discount_counts.values,
                 title="Distribution of Discount Types", text_auto='.2s')
    fig.update_layout(xaxis_title="Discount Type", yaxis_title="Number of Occurrences")
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig)
