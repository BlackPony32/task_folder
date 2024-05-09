import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

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

  # Remove currency symbols and thousands separators from numeric columns
  numeric_cols = ['Grand total', 'Balance', 'Paid', 'Item specific discount',
                  'Manufacturer specific discount', 'Total invoice discount',
                  'Customer discount']
  for col in numeric_cols:
    # Check if the column contains text values
    if data[col].dtype == 'object':
      # Replace missing values with an empty string to avoid errors
      data[col] = data[col].fillna('')
      # Remove characters and convert to numbers
      data[col] = data[col].str.replace('[$,]', '', regex=True).astype(float)
    else:
      # If the column is already numeric, check for missing values
      if np.isnan(data[col]).any():
        print(f"Warning: Column '{col}'contains missing values (NaN). ")

  return data

#_________________Sales Trends Function  (with Plotly)_______________________________
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
                     title="Monthly Sales Trend", markers=True)  # Add markers for better data point visibility
        fig.update_layout(xaxis_title="Month", yaxis_title="Sales Amount")
        st.plotly_chart(fig)

#_________________Product Analysis Function (with Plotly)___________________________
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
                     color='count', color_continuous_scale='Cividis')  # Different color scale for visual distinction
        fig.update_layout(xaxis_tickangle=45, yaxis_title="Number of Orders", xaxis_title="Product")
        st.plotly_chart(fig)

#_________________Discount Analysis Function (with Plotly)__________________________
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

# _________________Delivery Analysis Function (with Plotly)___________________________
def visualize_delivery_analysis(data, delivery_status_col='Delivery status',
                               delivery_method_col='Delivery methods'):
    tab1, tab2, tab3 = st.tabs(["By Status", "By Method", "Distribution"])

    with tab1:
        st.subheader("Number of Orders by Delivery Status")
        delivery_status_counts = data[delivery_status_col].value_counts()
        fig = px.bar(delivery_status_counts, x=delivery_status_counts.index, y=delivery_status_counts.values,
                     title="Number of Orders by Delivery Status", color=delivery_status_counts.values,
                     color_continuous_scale='Blugrn')
        fig.update_layout(xaxis_tickangle=45, yaxis_title="Number of Orders", xaxis_title="Delivery Status")
        st.plotly_chart(fig)

    with tab2:
        st.subheader("Number of Orders by Delivery Method")
        delivery_method_counts = data[delivery_method_col].value_counts()
        fig = px.bar(delivery_method_counts, x=delivery_method_counts.index, y=delivery_method_counts.values,
                     title="Number of Orders by Delivery Method", color=delivery_method_counts.values,
                     color_continuous_scale='Emrld')
        fig.update_layout(xaxis_tickangle=45, yaxis_title="Number of Orders", xaxis_title="Delivery Method")
        st.plotly_chart(fig)

    with tab3:
        st.subheader("Distribution of Orders by Delivery Status")
        fig = px.pie(delivery_status_counts, values=delivery_status_counts.values, names=delivery_status_counts.index,
                     title="Distribution of Orders by Delivery Status")
        st.plotly_chart(fig)

# _________________Payment Analysis Function (with Plotly)___________________________
def visualize_payment_analysis(data, payment_status_col='Payment status'):
    # Number of orders for each payment status
    payment_status_counts = data[payment_status_col].value_counts()
    fig = px.bar(payment_status_counts, x=payment_status_counts.index, y=payment_status_counts.values,
                 title="Number of Orders by Payment Status", color=payment_status_counts.values,
                 color_continuous_scale='Sunset')
    fig.update_layout(xaxis_tickangle=45, yaxis_title="Number of Orders", xaxis_title="Payment Status")
    st.plotly_chart(fig)

# _________________Combined Analysis Function (with Plotly)___________________________
def visualize_combined_analysis(data, product_col='Product name',
                               grand_total_col='Grand total', qty_col='QTY',
                               delivery_status_col='Delivery status'):
    tab1, tab2 = st.tabs(["Quantity vs. Amount", "Orders by Product & Status"])

    with tab1:
        st.subheader("Relationship between Quantity and Amount (by Product)")
        fig = px.scatter(data, x=qty_col, y=grand_total_col, color=product_col,
                         title="Relationship between Quantity and Amount (by Product)",
                         labels={"x": "Quantity", "y": "Sales Amount"})
        fig.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig)

    with tab2:
        st.subheader("Number of Orders by Product and Delivery Status")
        fig = px.histogram(data, x=product_col, color=delivery_status_col,
                         title="Number of Orders by Product and Delivery Status",
                         labels={"x": "Product", "color": "Delivery Status"})
        fig.update_layout(xaxis_tickangle=45, yaxis_title="Number of Orders", barmode='group')
        st.plotly_chart(fig)