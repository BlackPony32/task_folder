import plotly.express as px
import pandas as pd
import streamlit as st
#Visualization of Customer_details
def customer_analysis_app(df):
    """Creates a Streamlit app with tabs for analyzing customer data using plots."""

    st.title("Customer Sales Analysis")

    tab1, tab2, tab3 = st.tabs(["Top Customers", "Territory Analysis", "Payment Terms Analysis"])

    with tab1:
        st.header("Top 10 Customers by Total Sales")
        top_10_customers = df.groupby('Name')['Total sales'].sum().nlargest(10)
        fig = px.bar(top_10_customers, x=top_10_customers.index, y=top_10_customers.values, title="Top 10 Customers")
        st.plotly_chart(fig)

    with tab2:
        st.header("Total Sales by Territory")
        territory_sales = df.groupby('Territory')['Total sales'].sum()
        fig = px.pie(territory_sales, values=territory_sales.values, names=territory_sales.index, title="Sales by Territory")
        st.plotly_chart(fig)

    with tab3:
        st.header("Total Sales by Payment Terms")
        payment_terms_sales = df.groupby('Payment terms')['Total sales'].sum()
        fig = px.bar(payment_terms_sales, x=payment_terms_sales.index, y=payment_terms_sales.values, title="Sales by Payment Terms")
        st.plotly_chart(fig)

#--------------------------bar_plot_with_percentages--------------------------------------
def create_bar_plot_with_percentages(df, col):
    counts = df[col].value_counts().sort_values(ascending=False)
    percentages = (counts / len(df)) * 100
    df_plot = pd.DataFrame({'Category': counts.index, 'Count': counts.values, 'Percentage': percentages})

    fig = px.bar(df_plot, x='Category', y='Count', text='Percentage', title=f"Distribution of clients by {col}")
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', title_x=0.5)
    return fig
def interactive_bar_plot_app(df):
    st.title("Interactive Bar Chart with Percentages")

    column_options = df.select_dtypes(include='object').columns
    selected_column = st.selectbox("Select a Categorical Column", column_options)

    fig = create_bar_plot_with_percentages(df, selected_column)
    st.plotly_chart(fig)

#Data distribution visualization
def create_non_zero_sales_grouped_plot(df, sales_col='Total sales', threshold=500):
    df_filtered = df[df[sales_col] > 0]
    df_below_threshold = df_filtered[df_filtered[sales_col] <= threshold]
    df_above_threshold = df_filtered[df_filtered[sales_col] > threshold]
    counts_below = df_below_threshold[sales_col].value_counts().sort_index()
    count_above = df_above_threshold[sales_col].count()
    values = counts_below.index.tolist() + [f"{threshold}+"]
    counts = counts_below.values.tolist() + [count_above]
    df_plot = pd.DataFrame({'Sales Value': values, 'Count': counts})

    fig = px.line(df_plot, x='Sales Value', y='Count', markers=True, 
                  title="Distribution of non-zero total sales")
    fig.update_layout(title_x=0.5, xaxis_title="Value of total sales", 
                      yaxis_title="Number of entries")
    # Use a valid color string instead of 'tab:blue'
    fig.update_traces()
    st.plotly_chart(fig)

#Distribution of customer groups by city
def interactive_group_distribution_app(df, group_col='Group' , city_col= 'Billing city'):
    st.title("Customer Group Distribution by City")

    most_frequent_city = df[city_col].value_counts().index[0]

    data_all_cities = df.copy()
    data_without_frequent_city = df[df[city_col] != most_frequent_city]

    # Create figures directly within tabs
    tab1, tab2 = st.tabs(["All Cities", f"Without Most Frequent City"])

    with tab1:
        fig1 = px.bar(data_all_cities, x=city_col, color=group_col, barmode='group', title="Distribution of Client Groups by City")
        fig1.update_layout(xaxis_title="City", yaxis_title="Number of Clients", legend_title_text="Group")
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        fig2 = px.bar(data_without_frequent_city, x=city_col, color=group_col, barmode='group', 
                       title=f"Distribution of Client Groups (without {most_frequent_city})")
        fig2.update_layout(xaxis_title="City", yaxis_title="Number of Clients", legend_title_text="Group")
        st.plotly_chart(fig2, use_container_width=True)
