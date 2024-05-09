import plotly.express as px
import pandas as pd
import streamlit as st

def low_stock_analysis_app(df):
    st.title("Low Stock Inventory Analysis")

    tab1, tab2 = st.tabs(["Distribution by Category", "Price vs. Quantity"])

    with tab1:
        fig1 = px.bar(df.groupby("Category name")["Product name"].count().reset_index(), 
                      x="Category name", y="Product name", color="Product name",
                      title="Distribution of Low Stock Items by Category")
        fig1.update_layout(xaxis_title="Category", yaxis_title="Number of Low Stock Items")
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        # Filter out negative quantities before using them for size
        df_positive_qty = df[df['Available cases (QTY)'] > 0]  
        fig2 = px.scatter(df_positive_qty, x="Wholesale price", y="Available cases (QTY)", 
                         color="Category name", size="Available cases (QTY)", 
                         hover_data=['Product name'], title="Wholesale Price vs. Available Quantity")
        fig2.update_layout(xaxis_title="Wholesale Price", yaxis_title="Available Cases (QTY)")
        st.plotly_chart(fig2, use_container_width=True)

#Analyzing Profit Margins of Low Stock Items
def create_profit_margin_analysis_plot(df):
    df["Profit Margin"] = df["Retail price"] - df["Wholesale price"]
    df_sorted = df.sort_values(by="Profit Margin", ascending=False)

    fig = px.bar(df_sorted, x='Product name', y='Profit Margin', color='Profit Margin',
                 title="Profit Margins of Low Stock Items", color_continuous_scale='teal')
    fig.update_layout(xaxis_title="Product Name", yaxis_title="Profit Margin", 
                      xaxis_tickangle=45, xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig)

#Analyzes and visualizes the number of low-stock items by manufacturer
def create_low_stock_by_manufacturer_bar_plot(df):
    from plotly.colors import sequential
    low_stock_counts = df.groupby("Manufacturer name")["Product name"].count().reset_index()

    fig = px.bar(low_stock_counts, x='Manufacturer name', y='Product name', color='Product name',
                 title="Distribution of Low Stock Items by Manufacturer", 
                 color_continuous_scale=sequential.OrRd)  # Use a valid Plotly colorscale
    fig.update_layout(xaxis_title="Manufacturer", yaxis_title="Number of Low Stock Items", 
                      xaxis_tickangle=0, xaxis={'categoryorder': 'total descending'}) 
    st.plotly_chart(fig)

#Analyzing the correlation Between Price and Available Quantity
def create_interactive_price_vs_quantity_plot(df):
    df['Wholesale price'] = pd.to_numeric(df['Wholesale price'], errors='coerce')

    fig = px.scatter(df, x="Wholesale price", y="Available cases (QTY)", trendline="ols",
                     title="Wholesale Price vs. Available Quantity for Low-Stock Items",
                     color_discrete_sequence=['indigo'])
    fig.update_layout(xaxis_title="Wholesale Price", yaxis_title="Available Cases (QTY)")
    st.plotly_chart(fig)

#Analyzing the Relationship Between Price and Available Quantity
def create_quantity_price_ratio_plot(df):
    df['Retail price'] = pd.to_numeric(df['Retail price'], errors='coerce')
    df["QTY/Price Ratio"] = df["Available cases (QTY)"] / df["Retail price"]
    df_sorted = df.sort_values(by="QTY/Price Ratio")

    fig = px.bar(df_sorted, y='Product name', x='QTY/Price Ratio', color='QTY/Price Ratio', orientation='h',
                 title="Ratio of Available Quantity to Retail Price for Low-Stock Items",
                 color_continuous_scale='purples', text='QTY/Price Ratio')  # Add text labels
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(xaxis_title="QTY/Price Ratio", yaxis_title="Product Name")
    st.plotly_chart(fig)
