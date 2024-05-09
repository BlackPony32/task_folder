import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import calendar
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

#Visualize the relationships between Orders/Cases Sold and Revenue
def plot_sales_relationships(df):
    tab1, tab2 = st.tabs(["Orders vs. Revenue", "Cases Sold vs. Revenue"])

    with tab1:
        st.subheader("Orders vs. Revenue")
        fig = px.scatter(df, x="Orders", y="Total revenue", trendline="ols", opacity=0.7)
        fig.update_layout(xaxis_title="Orders", yaxis_title="Total Revenue")
        st.plotly_chart(fig)

    with tab2:
        st.subheader("Cases Sold vs. Revenue")
        fig = px.scatter(df, x="Cases sold", y="Total revenue", trendline="ols", opacity=0.7)
        fig.update_layout(xaxis_title="Cases Sold", yaxis_title="Total Revenue")
        st.plotly_chart(fig)

#Revenue by Month and Role
def plot_revenue_by_month_and_role(df):
    df['Month'] = pd.to_datetime(df['Date']).dt.month
    df['Total revenue'] = df['Total revenue']
    grouped_data = df.groupby(['Month', 'Role'])['Total revenue'].sum().unstack(fill_value=0)

    fig = px.bar(grouped_data, x=grouped_data.index, y=grouped_data.columns, 
                 title="Revenue by Month and Role", text_auto='.2s')
    fig.update_layout(xaxis_title="Month", yaxis_title="Total Revenue")
    fig.update_xaxes(tickmode='array', tickvals=grouped_data.index, 
                     ticktext=[calendar.month_name[m] for m in grouped_data.index])
    st.plotly_chart(fig)

#Visualize visits and travel distance for each name
def plot_visits_and_travel_distance_by_name(df):
    # Calculate sums BEFORE grouping
    df['Travel distance'] = pd.to_numeric(df['Travel distance'].str.replace(' mi', ''))
    grouped_data = df.groupby('Name')[['Visits', 'Travel distance']].sum()

    fig = px.bar(grouped_data, x=grouped_data.index, y=grouped_data.columns, barmode='group',
                 title="Visits and Travel Distance by Rep", text_auto='.2s')
    fig.update_layout(xaxis_title="Name", yaxis_title="Count / Distance")
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig)

#Visualize the number of cases sold for each day of the week
def plot_cases_sold_by_day_of_week(df):
    df['Day of Week'] = pd.to_datetime(df['Date']).dt.dayofweek
    weekday_counts = df['Day of Week'].value_counts().sort_index()

    fig = px.bar(weekday_counts, x=weekday_counts.index, y=weekday_counts.values,
                 title="Cases Sold by Day of the Week", text_auto='.2s')
    fig.update_layout(xaxis_title="Day of the Week", yaxis_title="Cases Sold")
    fig.update_xaxes(tickmode='array', tickvals=weekday_counts.index, 
                     ticktext=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    st.plotly_chart(fig)

#Visualizing Revenue Trends over Time for Each Role
def plot_revenue_trend_by_month_and_role(df):
    df['Month'] = pd.to_datetime(df['Date']).dt.month
    monthly_revenue = df.groupby(['Month', 'Role'])['Total revenue'].sum().unstack(fill_value=0)

    fig = px.line(monthly_revenue, x=monthly_revenue.index, y=monthly_revenue.columns,
                  markers=True, title="Revenue Trend by Month and Role")
    fig.update_layout(xaxis_title="Month", yaxis_title="Total Revenue")
    fig.update_xaxes(tickmode='array', tickvals=monthly_revenue.index, 
                     ticktext=[calendar.month_abbr[m] for m in monthly_revenue.index])
    st.plotly_chart(fig)

#Exploring the Relationship Between Visits and Orders
def plot_orders_vs_visits_with_regression(df):
    fig = px.scatter(df, x="Visits", y="Orders", trendline="ols", 
                     title="Relationship Between Visits and Orders")
    fig.update_layout(xaxis_title="Visits", yaxis_title="Orders")
    st.plotly_chart(fig)

#Comparing Performance Metrics for Different Roles
def plot_multiple_metrics_by_role(df):
    grouped_data = df.groupby('Role')[['Visits', 'Orders', 'Cases sold']].sum()

    fig = px.bar(grouped_data, x=grouped_data.index, y=grouped_data.columns, barmode='group',
                 title="Comparison of Performance Metrics by Role", text_auto='.2s')
    fig.update_layout(xaxis_title="Role", yaxis_title="Count")
    st.plotly_chart(fig)

#Identifying Potential High-Value Clients
def plot_revenue_vs_cases_sold_with_size_and_color(df):
    fig = px.scatter(df, x="Cases sold", y="Total revenue", size="Visits", color="Travel distance",
                    title="Revenue vs. Cases Sold with Visit Frequency and Travel Distance", 
                     hover_data=df.columns, opacity=0.7)
    fig.update_layout(xaxis_title="Cases Sold", yaxis_title="Total Revenue")
    fig.update_traces(marker=dict(sizemode='area', sizeref=2.*max(df['Visits'])/(40.**2)))  # Adjust marker size
    st.plotly_chart(fig)
