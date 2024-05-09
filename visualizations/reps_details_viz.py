import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

def analyze_sales_rep_efficiency(df_pd):
    df_pd = df_pd.copy()

    def convert_hours_to_numeric(time_str):
        try:
            hours, minutes = map(int, time_str.split('h '))
            return hours + minutes/60
        except ValueError:
            return pd.NA  # Handle cases where conversion fails

    df_pd['Total working hours'] = df_pd['Total working hours'].apply(convert_hours_to_numeric)
    df_pd["Visits per Working Hour"] = df_pd["Total visits"] / df_pd["Total working hours"]
    df_pd["Customers per Visit"] = df_pd["Assigned customers"] / df_pd["Total visits"]

    # Group by Role and calculate median efficiency metrics
    grouped = df_pd.groupby("Role")[["Visits per Working Hour", "Customers per Visit"]].median()

    # Convert all columns to numeric type
    grouped = grouped.apply(pd.to_numeric, errors='coerce')  # 'coerce' will convert non-numeric values to NaN

    st.subheader("Efficiency Metrics by Role (Median)")
    fig = px.bar(grouped, barmode='group', title="Efficiency Metrics by Role (Median)")
    fig.update_layout(xaxis_title="Role", yaxis_title="Metric Value")
    st.plotly_chart(fig)

#Visualizing Customer Engagement: Active Customers vs. Total Visits
def plot_active_customers_vs_visits(df_pd):
    sales_data = df_pd[df_pd["Role"] == "SALES"]

    fig = px.scatter(sales_data, x="Active customers", y="Total visits", color="Name", 
                     trendline="ols", title="Active Customers vs. Total Visits (Sales Reps)")
    fig.update_layout(xaxis_title="Active Customers", yaxis_title="Total Visits")
    st.plotly_chart(fig)

#Travel Distance vs. Number of Visits
def plot_travel_efficiency_line(df_pd):
    tab1, tab2 = st.tabs(["Sales", "Merchandiser"])

    with tab1:
        st.subheader("Travel Distance vs. Visits (Sales)")
        sales_data = df_pd[df_pd["Role"] == "SALES"]
        fig = px.line(sales_data, x="Total travel distance", y="Total visits", 
                     markers=True, title="Travel Distance vs. Number of Visits (Sales)")
        fig.update_layout(xaxis_title="Total Travel Distance (miles)", yaxis_title="Total Visits")
        st.plotly_chart(fig)

    with tab2:
        st.subheader("Travel Distance vs. Visits (Merchandiser)")
        merch_data = df_pd[df_pd["Role"] == "MERCHANDISER"]
        fig = px.line(merch_data, x="Total travel distance", y="Total visits", 
                     markers=True, title="Travel Distance vs. Number of Visits (Merchandiser)")
        fig.update_layout(xaxis_title="Total Travel Distance (miles)", yaxis_title="Total Visits")
        st.plotly_chart(fig)

#Pure work time per Employee
def analyze_work_hours_and_distance(df_pd):
    """
    Calculates clear work hours and visualizes both clear work hours and
    total travel distance in two separate plots.

    Args:
        df_pd (pd.DataFrame): The DataFrame containing the data.
    """
    df_pd = df_pd.copy()
    def parse_time(time_str):
        if pd.isna(time_str):
            return 0
        import re
        match = re.match(r'(\d+)h\s*(\d+)m', time_str)
        if match:
            h, m = map(int, match.groups())
        else:
            match = re.match(r'(\d+)m', time_str)
            if match:
                m = int(match.group(1))
                h = 0
            else:
                h, m = 0, 0
        return h + m / 60

    df_pd['Total working hours'] = df_pd['Total working hours'].apply(parse_time)
    df_pd['Total break hours'] = df_pd['Total break hours'].apply(parse_time)
    df_pd['Pure Work Hours'] = df_pd['Total working hours'] - df_pd['Total break hours']
    df_pd = df_pd.sort_values(by='Pure Work Hours', ascending=False).head(10)

    # Create two columns for the bar charts
    col1, col2 = st.tabs(["SalesPure Work Hours", "Total Travel Distance"])

    with col1:
        st.subheader("Pure Work Hours per Employee")
        fig = px.bar(df_pd, x='Name', y='Pure Work Hours', title="Pure Work Hours per Employee",
                     text='Pure Work Hours')  # Display values on top of bars
        fig.update_traces(texttemplate='%{text:.1f}h', textposition='outside')  # Format text as hours
        fig.update_layout(xaxis_tickangle=45, yaxis_title="Pure Work Hours (hours)", xaxis_title="Employee")
        st.plotly_chart(fig)

    with col2:
        st.subheader("Total Travel Distance per Employee")
        fig = px.bar(df_pd, x='Name', y='Total travel distance', title="Total Travel Distance per Employee",
                     text='Total travel distance') 
        #fig.update_traces(textposition='outside')  # Format text as miles
        fig.update_layout(xaxis_tickangle=45, yaxis_title="Total Travel Distance (miles)", xaxis_title="Employee")
        st.plotly_chart(fig)

#Total Visits vs. Total Photos Taken
def plot_visits_vs_photos_separate(df_pd):
    roles = df_pd['Role'].unique()

    # Create tabs for each role
    tabs = st.tabs([role for role in roles])  # Create tabs with role names

    for i, role in enumerate(roles):
        with tabs[i]:  # Access each tab using its index
            st.subheader(f"Total Visits vs. Total Photos Taken ({role})")
            role_data = df_pd[df_pd['Role'] == role]
            fig = px.scatter(role_data, x="Total visits", y="Total photos", 
                             title=f"Total Visits vs. Total Photos Taken ({role})")
            fig.update_layout(xaxis_title="Total Visits", yaxis_title="Total Photos")
            st.plotly_chart(fig)

#Exploring Customer Distribution Across Sales Representatives
def analyze_customer_distribution(df_pd):
    sales_data = df_pd[df_pd["Role"] == "SALES"].copy()

    st.subheader("Distribution of Assigned Customers per Sales Rep")
    fig = px.box(sales_data, x="Assigned customers", points="all", title="Distribution of Assigned Customers per Sales Rep")
    fig.update_layout(xaxis_title="Number of Assigned Customers")
    st.plotly_chart(fig)
