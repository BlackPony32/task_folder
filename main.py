import streamlit as st
import pandas as pd
import os
from visualizations import order_sales_summary_viz, reps_details_viz, reps_summary_viz, third_party_sales_viz, top_customers_viz, customer_details_viz, low_stock_inventory_viz, best_sellers_viz, skus_not_ordered_viz, current_inventory_viz
#test
def identify_file(uploaded_file):
  try:
    df = pd.read_csv(uploaded_file, encoding='utf-8') 
    columns = set(df.columns)
    file_size = uploaded_file.size
    file_name = uploaded_file.name

    if columns == {'Role', 'Id', 'Status', 'Name', 'Email', 'Phone number', 'Assigned customers', 
                    'Active customers', 'Inactive customers', 'Total visits', 'Total photos', 
                    'Total notes', 'Total working hours', 'Total break hours', 'Total travel distance'}:
      return "Representative Details report"

    elif columns == {'Id', 'Created at', 'Created by', 'Customer', 'Representative', 'Grand total', 
                      'Balance', 'Paid', 'Delivery status', 'Payment status', 'Order Status', 
                      'Delivery methods', 'Manufacturer name', 'Product name', 'QTY', 'Delivered', 
                      'Item specific discount', 'Manufacturer specific discount', 'Total invoice discount', 
                      'Discount type', 'Customer discount', 'Free cases'}:
      return "Order Sales Summary report"

    elif columns == {'Role', 'Id', 'Name', 'Date', 'Start day', 'End day', 'Total time', 'Break', 
                      'Travel distance', 'Visits', 'Photos', 'Notes', 'Orders', 'New clients', 
                      'Cases sold', 'Total revenue'}:
      return "Reps Summary report"

    elif columns == {'Product name', 'Manufacturer name', 'Category name', 'SKU', 'Available cases (QTY)',
                      'Wholesale price', 'Retail price', 'Cases sold', 'Total revenue'}:
      if df['Cases sold'].any():
        return "Best Sellers report"
      elif "SKU" in file_name: 
        return "SKU's Not Ordered report"
      else:
        return "Unknown (similar columns to Best Sellers and SKU's Not Ordered)"

    elif columns == {'Product name', 'Manufacturer name', 'Category name', 'SKU', 'Available cases (QTY)',
                    'Wholesale price', 'Retail price'}:
      low_stock_threshold = 50
      if "Low" in file_name:
        return "Low Stock Inventory report"
      elif "Current" in file_name:
        return "Current Inventory report"
      else:
        return "Unknown (similar columns to Low Stock and Current Inventory)"

    elif columns == {'Id', 'Created at', 'Created by', 'Customer', 'Representative', 'Grand total', 
                      'Manufacturer name', 'Product name', 'QTY', 'Item specific discount', 
                      'Manufacturer specific discount', 'Total invoice discount', 'Discount type', 
                      'Customer discount', 'Free cases'}:
      return "3rd Party Sales Summary report"

    elif columns == {'Name', 'Group', 'Billing address', 'Billing city', 'Billing state', 
                      'Billing zip', 'Shipping address', 'Shipping city', 'Shipping state', 
                      'Shipping zip', 'Phone', 'Payment terms', 'Customer discount', 'Territory', 
                      'Website', 'Tags', 'Contact name', 'Contact role', 'Contact phone', 
                      'Contact email', 'Order direct access', 'Total orders', 'Total sales', 
                      'Business Fax', 'Primary payment method', 'Licenses & certifications'} and "Top" in file_name:
      return "Top Customers report"

    elif columns == {'Name', 'Group', 'Billing address', 'Billing city', 'Billing state', 
                      'Billing zip', 'Shipping address', 'Shipping city', 'Shipping state', 
                      'Shipping zip', 'Phone', 'Payment terms', 'Customer discount', 'Territory', 
                      'Website', 'Tags', 'Contact name', 'Contact role', 'Contact phone', 
                      'Contact email', 'Order direct access', 'Total orders', 'Total sales', 
                      'Business Fax', 'Primary payment method', 'Licenses & certifications'}:
      return "Customer Details report"

    else:
      return "Unknown"

  except:
    return "Invalid File"

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    file_type = identify_file(uploaded_file)
    st.write(f"**File type:** {file_type}")
    path_to_save = 'filename.csv'
    with open(path_to_save, "wb") as f:
      f.write(uploaded_file.getvalue())

    st.dataframe(pd.read_csv(path_to_save), height=500)
    df = pd.read_csv(path_to_save)

    identify  = identify_file(uploaded_file)
    if file_type == "Order Sales Summary report":
      processed_data = order_sales_summary_viz.preprocess_data(df)
      # Product Analysis
      order_sales_summary_viz.visualize_product_analysis(processed_data)
      st.markdown("""
    **Insights:**

    * **Direct Comparison:** The side-by-side placement enables immediate visual comparison between two related metrics, such as sales amount and number of orders. This allows for a quick understanding of how products perform across different dimensions.
    * **Identifying Trends and Discrepancies:** By observing the relative heights of the bars in each chart, businesses can easily identify products that are performing well in both areas, those that excel in one metric but lag in another, and those that underperform across the board. This helps pinpoint areas for further investigation and potential optimization.
    * **Comprehensive Insights:** Analyzing sales amount alone might highlight high-revenue products, but it wouldn't reveal the volume of sales or the popularity of a product. Conversely, focusing solely on the number of orders might overlook the revenue generated. Comparing both metrics provides a more holistic understanding of product performance and market dynamics.
    * **Data-Driven Decision Making:** The insights gleaned from this visualization can inform various business decisions, such as product development, pricing strategies, marketing campaigns, inventory management, and resource allocation. 
    """)

      # Sales Trends
      order_sales_summary_viz.visualize_sales_trends(processed_data)
      st.markdown("""
    **Insights:**

    * **Identifying High-Value Customers:** The chart instantly highlights the customers who contribute the most to overall revenue. This allows businesses to focus their attention and resources on nurturing relationships with these key clients.
    * **Sales Performance Evaluation:** The visualization offers a quick snapshot of sales performance across the top customer segment. Businesses can easily compare the relative contribution of each customer and identify any significant gaps or disparities.
    * **Segmentation and Targeting:** The chart can serve as a starting point for further customer segmentation analysis. By grouping customers based on similar sales amounts or other characteristics, businesses can develop targeted marketing campaigns and tailor their offerings to specific customer needs.
    * **Tracking Changes Over Time:** Monitoring this chart over different periods can reveal trends in customer behavior, such as changes in purchasing patterns or the emergence of new high-value clients. This information is crucial for adapting sales strategies and maintaining strong customer relationships.
    * **Sales Goal Setting:** The visualization can aid in setting realistic sales goals and targets based on the performance of top customers.
    * **Identifying and Patterns:** The line clearly shows the overall trajectory of sales, whether it's increasing, decreasing, or remaining stable. This allows businesses to quickly identify periods of growth, decline, or seasonality.
    * **Specific Data Points:** The plotted points on the line correspond to the sales amount for each month. This enables easy identification of months with exceptionally high or low sales, prompting further investigation into the factors influencing those results.
    * **Performance Monitoring:** Businesses can use this chart to track sales performance over time and evaluate the effectiveness of sales strategies, marketing campaigns, or other initiatives.
    * **Forecasting and Planning:** By analyzing the trend and seasonality observed in the line chart, businesses can make more informed forecasts about future sales and plan their inventory, production, and resource allocation accordingly.
    """)

      # Discount Analysis, б Discount by Customer (Top 10)
      order_sales_summary_viz.visualize_discount_analysis(processed_data)
      st.markdown("""
    **Insights:**

    * **Identifying Dominant Discount Type:** The chart clearly shows which type of discount is most frequently applied. In this case, it highlights the prevalence of "Invoice Total Discount" compared to other options.
    * **Evaluating Discount Strategy:** Businesses can assess the effectiveness of their current discount strategy based on the distribution of discounts. This may prompt further analysis into the impact of different discount types on sales, profitability, and customer behavior.
    * **Cost Analysis:** The chart provides insights into the overall cost of discounts, which can be valuable for budgeting and financial planning.
    * **Comparing Discount Options:** Businesses can use this visualization to compare the usage and impact of various discount types and identify potential areas for optimization or experimentation.
    * **Identifying Top Discount Recipients:** The chart clearly shows which customers receive the most discounts, allowing businesses to assess if these discounts align with their customer relationship strategies or if any adjustments are needed.
    * **Discount Distribution Analysis:** Businesses can evaluate how discounts are distributed among their top customers and identify any significant disparities or patterns. This may lead to insights about specific customer negotiations, pricing agreements, or potential customer segmentation based on discount utilization.
    * **Customer Relationship Management:** The information can be used to inform customer relationship management strategies. Businesses may choose to offer loyalty programs or targeted discounts to specific customers based on their past discount usage or value to the company.
    * **Sales and Pricing Strategies:** Analyzing discount distribution can help refine sales and pricing strategies. Businesses might consider adjusting pricing structures, negotiating bulk discounts, or exploring alternative promotional offers based on the observed patterns.
    """)

      # Delivery Analysis # Delivery Method Analysis
      order_sales_summary_viz.visualize_delivery_analysis(processed_data)
      st.markdown(""" 
    **Insights:**

    * **Identifying Fulfillment Issues:** The chart quickly reveals any potential problems with order fulfillment. A high number of unfulfilled orders could indicate bottlenecks in the delivery process, inventory management issues, or other logistical challenges that require attention.
    * **Performance Monitoring:** Businesses can track the rate of order fulfillment over time and identify any trends or patterns. This information can be used to evaluate the efficiency of the delivery process and identify areas for improvement. 
    * **Customer Service Insights:** Understanding the number of unfulfilled orders can inform customer service strategies. Businesses may need to proactively communicate with customers about delays, offer alternative solutions, or adjust delivery expectations. 
    * **Operational Efficiency:** The chart highlights the importance of optimizing the order fulfillment process to ensure timely deliveries and customer satisfaction. This may involve streamlining logistics, improving inventory management, or investing in delivery technology. 
    * **Identifying Popular Delivery Options:** The chart clearly shows which delivery methods are preferred by customers. This information can inform business decisions regarding logistics, partnerships with delivery providers, and pricing strategies for different delivery options. 
    * **Resource Allocation:** Businesses can allocate resources effectively based on the demand for each delivery method. For instance, if local delivery is the dominant choice, optimizing local delivery routes and investing in local delivery infrastructure may be a priority. 
    * **Customer Segmentation:** Analyzing delivery preferences can reveal insights into customer demographics or behaviors. This information can be used to create targeted marketing campaigns or develop specialized delivery options for specific customer segments.
    * **Service Expansion:** Businesses can evaluate the potential for expanding their delivery services based on customer demand and market trends. For example, if there's a growing preference for a particular delivery method that's not currently offered, it may be worth considering adding it to the service portfolio. 
    """)

      # Payment Analysis
      order_sales_summary_viz.visualize_payment_analysis(processed_data)
      st.markdown("""
    **Insights:**

    * **Identifying Payment Issues:** The chart instantly reveals potential problems with payment processing or collection. A high number of unpaid orders may indicate issues with the payment gateway, customer billing errors, or a need for more efficient payment collection procedures.
    * **Monitoring Payment Trends:** Businesses can track the proportion of paid and unpaid orders over time to identify any trends or patterns. This information can be used to assess the effectiveness of payment collection efforts and identify areas for improvement. 
    * **Refund Analysis:** The chart provides insights into the frequency of refunds. This may prompt further investigation into the reasons behind refunds, such as product quality issues, customer dissatisfaction, or errors in order processing. 
    * **Financial Management:** Understanding the distribution of payment statuses is crucial for effective financial management. Businesses can use this information to forecast cash flow, manage outstanding payments, and ensure accurate financial reporting. 
    """)

      # Combined Analysis
      order_sales_summary_viz.visualize_combined_analysis(processed_data)
      st.markdown("""
    **Insights (Scatter Plot):**

    * **Identifying Trends:** The scatter plot helps identify any potential trends or correlations between quantity and sales amount. For instance, it can reveal whether higher quantities generally lead to higher sales amounts, or if the relationship is more complex.
    * **Outlier Detection:** The visualization makes it easy to spot outliers, which are data points that deviate significantly from the general pattern. This could indicate unusual sales events, bulk purchases, or potential data entry errors that require further investigation.
    * **Product Performance Comparison:** Businesses can compare the performance of different products by observing their distribution on the plot. This can reveal insights into pricing strategies, product popularity, and potential areas for improvement. 
    * **Sales Analysis:** The scatter plot helps analyze the distribution of sales across different quantity levels. This can inform inventory management, pricing strategies, and sales forecasting. 
    * **Comparison Across Products:** Businesses can directly compare the number of orders and fulfillment rates for different products. This allows for identifying products with potential fulfillment issues, such as a higher proportion of unfulfilled orders compared to others.
    * **Identifying Bottlenecks:** If a specific product consistently shows a higher number of unfulfilled orders, it may indicate bottlenecks or challenges in the production, inventory, or delivery process related to that particular item. 
    * **Inventory Management:** The insights gained can inform inventory management strategies. Businesses can ensure sufficient stock for products with high order volumes and prioritize fulfillment for products with a backlog of unfulfilled orders.
    * **Customer Service and Communication:** Understanding the fulfillment status for each product allows for proactive customer service. Businesses can communicate with customers about potential delays or provide updates on the status of their orders.
    * **Product Performance Analysis:** The chart offers insights into the overall demand and popularity of different products based on the number of orders received. This information can be valuable for product development, marketing, and sales strategies. 
    """)
    elif file_type == "Representative Details report":
      reps_details_viz.analyze_sales_rep_efficiency(df)
      st.markdown("""
## Efficiency Comparison Across Roles Based on Visits and Customers per Visit

The bar chart effectively visualizes the median efficiency metrics for different roles, providing insights into performance and potential areas for improvement:

*   **Comparing Efficiency Across Roles:** The chart allows for a direct visual comparison of efficiency between different roles based on the chosen metrics ("Visits per Working Hour" and "Customers per Visit"). This helps identify which roles are performing better in terms of visit frequency and customer engagement per visit.
*   **Identifying Performance Gaps:** Businesses can quickly spot any significant performance gaps between roles by visualizing the median values. For instance, if one role has a substantially lower number of visits per working hour, it might indicate a need for further investigation and potential process improvements.
*   **Resource Allocation and Training:** The insights from this plot can guide decisions related to resource allocation and training programs. Roles with lower efficiency metrics might benefit from additional training, support, or adjustments in workload distribution to improve their performance.
*   **Tracking Performance Over Time:** Creating similar bar charts for different time periods allows businesses to track changes in efficiency metrics over time. This helps assess the effectiveness of implemented strategies and identify areas for continuous improvement.
""")
      reps_details_viz.plot_active_customers_vs_visits(df)
      st.markdown("""
## Analyzing Customer Engagement: Active Customers vs. Total Visits

The scatter plot visualizes the relationship between the number of active customers a sales rep handles and the total number of visits they make, providing insights into individual performance and potential areas for improvement:

*   **Relationship Visualization:** The plot allows us to explore the relationship between active customers and total visits, potentially revealing correlations or patterns that can inform sales strategies and resource allocation.
*   **Individual Performance Comparison:**  By plotting each sales rep's data as separate points and using different colors, we can easily compare their individual performance and identify areas for improvement or potential training needs.
*   **Trend Line Insights:** The inclusion of a trend line provides a general overview of the relationship between active customers and total visits, offering insights into whether there is a correlation between the two variables.
*   **Resource Allocation and Goal Setting:**  Businesses can use this information to make informed decisions about resource allocation, sales territories, and individual goals for sales reps, optimizing workload distribution and improving sales performance. 
""")
      reps_details_viz.plot_travel_efficiency_line(df)
      st.markdown("""
## Travel Efficiency Analysis: Travel Distance vs. Number of Visits

The plot visualizes the relationship between travel distance and the number of visits conducted by individuals in different roles, offering insights for optimizing travel routes and schedules: 

*   **Travel Efficiency Analysis:** The plot allows us to analyze the relationship between travel distance and the number of visits, helping assess the efficiency of travel routes and identify potential areas for optimization.
*   **Role Comparison:** By plotting data for each role using different line styles, we can easily compare their travel patterns and identify potential differences in territory size, visit frequency, or scheduling efficiency.
*   **Identifying Outliers:** The plot helps identify outliers or data points that deviate significantly from the general trend, potentially indicating inefficient travel routes, scheduling issues, or other factors affecting the relationship between travel distance and the number of visits. 
*   **Optimizing Travel Routes:** Businesses can use this information to optimize travel routes and schedules for their sales and merchandising teams, exploring ways to reduce travel time and costs and increase efficiency and productivity.
""") 
      reps_details_viz.analyze_work_hours_and_distance(df)
      st.markdown("""

Effectively visualizes two key metrics per employee: "Pure Work Hours" and "Total Travel Distance."

*Comparing Workload Distribution:* The "Pure Work Hours" chart provides a clear comparison of workload distribution among employees. It helps identify individuals with significantly higher or lower work hours, potentially indicating imbalances in task allocation or scheduling.

*Analyzing Travel Patterns:* The "Total Travel Distance" chart reveals the travel patterns of each employee. This helps identify individuals who travel more extensively, which could be due to larger territories, specific roles requiring more travel, or inefficient route planning.

*Identifying Potential Issues:* By comparing the two charts, businesses can identify potential issues or areas for improvement. For instance, an employee with high work hours and extensive travel distance might be at risk of burnout, suggesting a need for workload adjustments or travel optimization.

*Resource Allocation and Planning:* This information can guide decisions related to resource allocation, territory assignments, and travel planning. Businesses can optimize travel routes, adjust workloads to ensure balance, and implement strategies to improve employee well-being and overall productivity.

""")
      reps_details_viz.plot_visits_vs_photos_separate(df)
      st.markdown("""
## Relationship Between Visits and Photos Taken for Sales Reps

This visualization explores the activity of sales representatives by correlating the number of photos taken with the total number of visits made. Analyzing this relationship provides valuable insights:

* **Understanding Engagement:** By identifying a potential correlation between visit frequency and photo-taking activity, we can gain a sense of engagement levels during visits. A higher number of photos might indicate a more thorough approach to documenting client interactions.
* **Identifying Patterns:** The plot can reveal trends in photo-taking behavior. For instance, a plateau in photos taken despite increasing visits could suggest a limit to photo-taking activity, regardless of visit frequency. This might warrant further investigation into the reasons behind this behavior.
* **Performance Evaluation:** This information can be used to assess the performance and engagement of sales representatives. It helps identify individuals who consistently document their visits through photos and those who might require additional training or motivation to capture relevant information. 
* **Data Collection Analysis:** The plot can be a valuable tool for evaluating the effectiveness of data collection processes. A consistently low number of photos taken despite high visit counts could indicate issues with the photo capture process itself or a lack of clarity on when and how to take photos. Addressing these issues can improve data collection efficiency.

""")
      reps_details_viz.analyze_customer_distribution(df)
      st.markdown("""
## Distribution of Assigned Customers per Sales Representative

This chart visualizes the distribution of assigned customers across your sales team. It reveals some interesting insights about workload allocation:

* **Varied Customer Distribution:** The graph highlights that the number of assigned customers per sales representative varies. There's a spread, indicating some reps manage more customers than others. 
* **Potential Imbalances:** The distribution appears skewed towards a higher number of reps with fewer assigned customers. This might suggest potential imbalances in workload allocation across the sales team. 

Further investigation into the underlying reasons behind this distribution is recommended. It could be due to factors like territory size, customer complexity, or sales rep experience. 
""")
    elif file_type == "Reps Summary report":
      df = reps_summary_viz.preprocess_data(df)
      reps_summary_viz.plot_sales_relationships(df)
      st.markdown("""
## Unveiling Revenue Drivers: Orders vs. Cases Sold

This visualization explores the relationship between revenue and two key sales metrics: orders placed and cases sold. By analyzing these connections, we gain valuable insights into what drives your business's revenue generation:

* **Identifying Revenue Drivers:** The plots shed light on which metric, orders or cases sold, has a stronger correlation with revenue. This knowledge helps understand the core dynamics of your sales and which aspect deserves more focus for revenue growth.
* **Understanding Order Impact vs. Volume Impact:** Presenting separate plots allows for a clear comparison of how order volume and sales volume (cases sold) individually influence revenue. This reveals if increasing order frequency or overall sales quantity has a greater impact on your bottom line.
* **Uncovering Revenue Trends:** The plots can expose patterns or trends in the data. For instance, we might observe a steady rise in revenue with increasing case sales, while the relationship with order volume might be less pronounced or more variable.
* **Optimizing Sales Strategies:** These insights empower businesses to optimize their sales strategies.  If case sales are the stronger revenue driver, strategies like upselling or cross-selling to increase the number of cases per order become more valuable.  Conversely, if order volume reigns supreme, acquiring new customers or promoting repeat purchases might be more impactful.

By understanding the relationship between revenue, orders, and cases sold, businesses can make informed decisions to maximize their sales success.

""")
      reps_summary_viz.plot_revenue_by_month_and_role(df)
      st.markdown("""
## Revenue Generated by Month and Role (MERCHANDISER and SALES)

**Revenue Trend Analysis:** The chart allows us to analyze revenue trends over time for each role (MERCHANDISER and SALES). This helps identify periods of high and low revenue generation, potentially revealing seasonal fluctuations, the impact of marketing campaigns, or changes in sales performance.

**Role Comparison:** By presenting the data for each role side-by-side, we can easily compare their revenue contributions over different months. This helps identify which role generates more revenue and if there are any significant differences in their performance patterns.

**Identifying Performance Gaps:** Businesses can use this information to identify potential performance gaps between roles or periods of underperformance. For instance, a significant drop in revenue for a particular role might indicate a need for further investigation and potential interventions to improve sales or address underlying issues.

**Sales Strategy and Goal Setting:** The insights from this plot can guide decisions related to sales strategies, resource allocation, and goal setting. Businesses can identify months or roles that require additional support, adjust sales targets based on historical trends, and develop targeted strategies to boost revenue during periods of lower performance.
""")
      reps_summary_viz.plot_visits_and_travel_distance_by_name(df)
      reps_summary_viz.plot_cases_sold_by_day_of_week(df)
      st.markdown("""
## Number of Cases Sold for Each Day of the Week

**Identifying Sales Patterns:** The chart allows us to quickly identify any patterns or trends in sales volume throughout the week. We can see which days have higher or lower sales, potentially revealing days with peak demand or slower periods.

**Resource Allocation:** Businesses can use this information to optimize resource allocation, such as staffing levels or marketing efforts, based on the expected sales volume for each day. This ensures you have the right amount of staff and marketing focus on days with higher customer traffic.

**Sales Strategy Planning:** Understanding the daily sales patterns can help businesses develop targeted sales strategies. For instance, they might consider running promotions or offering special deals on slower days to boost sales and even out the weekly sales volume.

**Customer Behavior Insights:** The plot can provide insights into customer behavior and preferences. For example, if sales are significantly higher on weekends compared to weekdays, it might suggest that customers have more time for shopping during those days. This knowledge can be used to tailor marketing campaigns and store hours to better cater to customer buying habits.
""")
      reps_summary_viz.plot_revenue_trend_by_month_and_role(df)
      st.markdown("""
## Revenue Trend by Month and Role

This chart visualizes the revenue generated by both Merchandisers and Sales Representatives on a monthly basis. 

* **Revenue Fluctuations:**  We can observe that revenue fluctuates throughout the months displayed ("Jan" to "May") for both roles. There isn't a clear upward or downward trend for either Merchandisers or Sales Representatives during this period.

* **Comparing Roles:** In the month of "May", the revenue generated by Merchandisers appears to be slightly higher compared to Sales Representatives. However, it's important to analyze data over a longer timeframe to draw more definitive conclusions about performance differences between the roles.

Further analysis considering a larger time frame can provide more insights into seasonal trends, the impact of marketing campaigns, or potential changes in sales strategies that might influence revenue generation for each role.
""")
      reps_summary_viz.plot_orders_vs_visits_with_regression(df)
      reps_summary_viz.plot_multiple_metrics_by_role(df)
      reps_summary_viz.plot_revenue_vs_cases_sold_with_size_and_color(df)
      st.markdown("""
## Sales Performance Insights by Representative

This chart offers insights into potential sales performance variations between your sales representatives. While the specific metrics are labeled "Average [Metric 1]" and "Average [Metric 2]," let's assume they represent:

* **Average Revenue per Visit (ARPV):** This reflects the average amount of revenue generated per sales visit.
* **Average Visits per Week:** This indicates the average number of visits completed by a sales representative in a week.

**Observations and Recommendations:**

* **Identify High Performers:** Sales representatives with a higher ARPV might require less oversight and could potentially mentor colleagues on effective sales techniques that contribute to higher revenue per visit. 
* **Optimize Visit Frequency:**  Analyze if there's a correlation between ARPV and number of visits. If high ARPV coincides with fewer visits, it might suggest these representatives are highly efficient in their visits, focusing on quality interactions over quantity. 
* **Targeted Training:**  For representatives with a lower ARPV, consider targeted training programs to improve their sales skills and negotiation techniques to increase revenue per visit. 
* **Balanced Approach:**  While a higher ARPV is generally desirable, ensure it's not achieved by neglecting visit frequency. A balanced approach that considers both metrics is crucial for overall sales success.
""")
    elif file_type == "3rd Party Sales Summary report":
      df = third_party_sales_viz.preprocess_data(df)
      third_party_sales_viz.visualize_product_analysis(df)
      st.markdown("""
## Total Sales by Product Category

This stacked bar chart provides a breakdown of total sales across three product categories: Beverages, Snacks, and Personal Care. It allows us to visualize sales performance for each category over different time periods (likely months).

* **Total Sales and Category Contribution:** 
    * The height of each bar represents the total sales figure for a specific time period.
    * The colors within each bar represent the contribution of each product category to the overall sales. 
    * By analyzing the color segments, we can identify which categories are driving sales in each period. 

""")
      third_party_sales_viz.visualize_sales_trends(df)
      st.markdown("""
## Sales Insights and Actionable Recommendations

This product sales analysis offers valuable insights to guide strategic business decisions and maximize revenue potential.

**Product Focus and Sales Strategy:**

* **Prioritizing Top Performers:** By identifying the top-performing product variants, like "Ginger Shots / Digestive Aid / Immunity Booster" in this example, businesses can prioritize marketing and sales efforts for these products. Capitalizing on their current popularity can significantly boost revenue generation. 

**Inventory Management:**

* **Data-Driven Decisions:** Sales and order distribution data empower businesses to make informed inventory management decisions. This ensures adequate stock levels for high-demand products while optimizing inventory for slower-moving items. This approach minimizes storage costs and ensures availability for customers. 

**Pricing and Promotions:**

* **Strategic Pricing:** Analyzing the pricing and promotional strategies for different products, considering their sales performance and contribution to overall revenue, is crucial. Businesses might adjust prices for specific products to optimize profitability or develop targeted promotions to stimulate sales of less popular items.

**Product Development and Innovation:**

* **Evaluating Performance:** Continuously evaluating the performance of less popular products allows for identifying areas for improvement or potential discontinuation. Exploring reformulations, new product development initiatives, or new markets can help cater to unmet customer needs and strategically expand the product line.

By implementing these recommendations and leveraging data-driven insights, businesses can optimize their product offerings, inventory management, pricing strategies, and ultimately achieve long-term sales success.
""")
      third_party_sales_viz.visualize_discount_analysis(df)
      st.markdown("""

**Additional Considerations:**

* **Data Verification:** Before drawing conclusions, it's important to verify the accuracy of the data and ensure the discount amounts are correctly represented. Inconsistencies in the data can lead to misleading insights.

* **Discount Types:** This analysis might not capture all types of discounts or incentives offered to customers. Consider exploring if there are other programs like rebates, loyalty programs, or free shipping that could be influencing customer purchasing behavior.

* **Impact of Discounts:** Implementing a discount policy requires careful analysis. Businesses should assess the potential impact on profit margins and overall profitability before making pricing adjustments. Striking a balance between attracting customers and maintaining healthy profit margins is crucial.

By considering these additional factors alongside the initial analysis, businesses can gain a more comprehensive understanding of their pricing strategy and make data-driven decisions to optimize sales and profitability.
""")
      third_party_sales_viz.visualize_combined_analysis(df)
      st.markdown("""

**Product Performance and Strategy:**

* **Product Performance Analysis:** Analyze the individual relationships between quantity and amount for each product. This can help identify:
    * Products with higher price points
    * Products sold in larger quantities
    * Products with potentially higher profit margins

By understanding these relationships, businesses can develop targeted pricing and sales strategies.

* **Pricing Strategies:** Evaluate pricing strategies for different products based on their sales volume and revenue generated. Consider:
    * Adjusting prices to optimize profitability
    * Offering bulk discounts to incentivize larger purchases for specific products

Data-driven pricing strategies can lead to increased revenue and improved profit margins.

* **Sales and Marketing Efforts:** Allocate sales and marketing resources effectively by focusing on products with the potential to generate higher revenue or profit based on their quantity-amount relationship. This ensures your marketing efforts target the most impactful products.

**Inventory Optimization:**

* **Inventory Management:** Understanding the quantity and sales amount for different products informs inventory management decisions. This ensures:
    * Optimal stock levels to meet demand
    * Avoiding stockouts or overstocking

By optimizing inventory levels, businesses can minimize storage costs and ensure product availability for customers.

By implementing these recommendations, businesses can leverage data insights to optimize product performance, pricing strategies, sales & marketing efforts, and ultimately achieve efficient inventory management.
""")
      third_party_sales_viz.analyze_discounts(df)
    elif file_type == "Top Customers report":
      top_customers_viz.customer_analysis_app(df)
      st.markdown("""
## Distribution of Clients by Payment Terms

Understanding the distribution of clients by their preferred payment terms is crucial for effective cash flow management, customer segmentation, and overall business strategy:

**1. Cash Flow Management:**

*   The prevalence of "Net 15" terms necessitates effective cash flow management strategies. Businesses must anticipate a delay in receiving payments and plan accordingly to ensure sufficient working capital.
*   Offering early payment discounts could incentivize faster payments and improve cash flow.

**2. Customer Segmentation and Targeting:**

*   Analyze the characteristics of clients who prefer different payment terms to identify potential customer segments. 
*   This information can be used to tailor marketing campaigns, credit policies, and collection strategies.
*   Consider offering more flexible payment options for specific customer segments, such as longer terms for larger businesses or shorter terms for smaller clients.

**3. Competitive Analysis and Pricing Strategies:**

*   Evaluate industry benchmarks and competitor offerings regarding payment terms to ensure competitiveness. 
*   Businesses may need to adjust their policies to remain attractive to clients while balancing cash flow considerations.
*   Explore the possibility of offering more favorable payment terms for high-value clients or strategic partnerships.

**4. Operational Efficiency and Technology:**

*   Streamline invoicing and payment processing systems to ensure efficiency and accuracy.
*   Invest in technology solutions that automate payment reminders, collections, and reporting processes. 
""")
      st.markdown("""
## Distribution of Clients by Groups

A bar chart visualizing the distribution of clients by groups provides a clear understanding of the composition of the customer base:

**Easy Comparison:**

*   The varying heights of the bars enable immediate visual comparison between the sizes of different customer groups. 
*   This allows businesses to quickly identify the most prominent segments and those that represent a smaller portion of their clientele.

**Proportion Visualization:**

*   Including percentages alongside the quantities further enhances understanding. 
*   It provides a clear picture of each group's relative contribution to the total customer base.

**Identifying Key Segments:**

*   This visualization aids in pinpointing the groups that require the most attention, whether due to their size, potential value, or unique needs. 
*   For instance, a large bar might signify a core customer group deserving focused marketing efforts, while a smaller bar could represent a niche segment with high-value potential.

**Data-Driven Decision Making:**

*   By understanding the composition of their customer base, businesses can make informed decisions regarding resource allocation, marketing strategies, product development, and customer relationship management.

**Monitoring Trends:**

*   Tracking changes in the distribution over time can reveal shifts in customer demographics, preferences, or market trends. 
""")
      top_customers_viz.interactive_bar_plot_app(df)
      top_customers_viz.create_non_zero_sales_grouped_plot(df)
      st.markdown("""
## Analysis of Skewed Distribution of Total Sales

The skewed distribution of total sales, with a long tail, reveals important insights about customer behavior and potential areas of focus for businesses:

**Skewed Distribution:**

*   The distribution is heavily skewed to the right, indicating that a significant number of entities have very few total sales (categories 1 and 2).

**Long Tail:**

*   There is a long tail in the distribution, suggesting the presence of a few entities with a high number of total sales.

**Distinct Categories:**

*   The x-axis labels imply that the data has been categorized into distinct groups based on the number of total sales.

**Customer Segmentation:**

*   The skewed distribution suggests the presence of distinct customer segments with varying purchasing behaviors. 
*   Businesses should further analyze the characteristics of customers within each segment to understand their behavior and needs.

**Focus on High-Value Customers:**

*   While many customers contribute to low total sales, the long tail indicates the presence of high-value customers who significantly impact overall sales revenue. 
*   Businesses should prioritize identifying and nurturing these high-value customers through targeted strategies and relationship management.
""")
      top_customers_viz.create_non_zero_sales_grouped_plot(df,sales_col='Total orders')
      top_customers_viz.interactive_group_distribution_app(df)
      st.markdown("""
## Insights from Geographic Distribution of Client Groups

Analyzing the geographic distribution of client groups can provide valuable insights for strategic decision-making:

**Market Focus:**

*   The business seems to have a strong focus on the New York City market, particularly with the "Doras Naturals" group. 
*   It's crucial to understand the factors driving this concentration, including potential advantages and disadvantages.
*   Consider the risks associated with dependence on a single market and explore opportunities for diversification.

**Geographic Expansion:**

*   The business might evaluate expanding into cities with lower representation of client groups.
*   Alternatively, focus on targeting specific customer segments for growth within those cities.

**Client Relationship Management:**

*   Understanding the geographic distribution of client groups can help tailor marketing and sales strategies to specific regions and customer segments.
*   Develop targeted campaigns and initiatives based on regional preferences and customer needs.

**Distribution and Logistics:**

*   The geographic concentration of client groups may influence distribution and logistics strategies.
*   Analyze the efficiency and cost-effectiveness of current operations and explore potential optimizations based on the geographic distribution of clients.
""")
    elif file_type == "Customer Details report":
      customer_details_viz.plot_orders_and_sales_plotly(df)
      st.markdown("""
## Comparison of Total Orders and Sales by Customer Group

Visualizations comparing total orders and sales by customer group provide valuable insights for businesses, including:

**1. Identifying High-Value Customers:**

*   Visualizations quickly pinpoint customer segments that contribute significantly to order volume or sales revenue. 
*   This allows businesses to focus their efforts on nurturing relationships with these valuable customers through targeted marketing, loyalty programs, or personalized offers.

**2. Understanding Customer Behavior:**

*   By comparing order volume and sales across different groups, businesses can uncover distinct purchasing patterns. 
*   This knowledge helps tailor strategies for each segment. 
*   For instance, high-volume, low-value customers might benefit from upselling or cross-selling initiatives, while low-volume, high-value customers might require a more personalized approach.

**3. Optimizing Marketing and Sales Efforts:**

*   Visualizations reveal which customer groups or regions have the most potential for growth. 
*   Businesses can then allocate marketing and sales resources effectively, targeting specific segments with tailored campaigns or promotions.

**4. Data-Driven Decision Making:**

*   Instead of relying on intuition or guesswork, visualizations provide concrete evidence for making informed decisions about pricing strategies, product development, inventory management, and overall business growth.

**5. Monitoring Performance and Trends:**

*   Regularly updating and reviewing visualizations helps track changes in customer behavior over time, identify emerging trends, and adapt strategies accordingly to stay ahead of the competition.
""")
      customer_details_viz.bar_plot_sorted_with_percentages(df)
      st.markdown("""
## Distribution of Clients by 'Payment Terms'

Analyzing the distribution of clients by their preferred payment terms offers several key insights:

**1. Cash Flow Management:**

*   Knowing the dominant payment terms helps businesses optimize their cash flow. 
*   For example, if most clients prefer "Net 30" terms, the company can anticipate a delay in receiving payments and plan accordingly to ensure sufficient working capital.

**2. Customer Segmentation:**

*   Different payment term preferences may reflect distinct customer segments or industries. 
*   Businesses can use this information to tailor their marketing or service offerings. 
*   For example, offering extended payment terms might be more attractive to larger businesses, while smaller clients might prefer shorter terms or upfront payments.

**3. Negotiation and Flexibility:**

*   Understanding the prevalence of various payment terms provides a basis for negotiation with clients. 
*   While a standard term might be preferred, businesses can evaluate offering more flexible options on a case-by-case basis to secure deals or accommodate specific customer needs.

**4. Risk Assessment:**

*   The distribution of payment terms can be an indicator of potential credit risk. 
*   A higher concentration of clients using longer payment terms might necessitate stricter credit checks or more proactive collection efforts to mitigate the risk of late or non-payment.
""")
      customer_details_viz.create_interactive_non_zero_sales_plot(df)
      st.markdown("""
## Distribution of Non-Zero Total Sales

Analyzing the distribution of non-zero total sales values provides valuable insights for businesses to optimize their operations and strategies:

**1. Pricing and Promotion Strategies:**

*   Evaluate the distribution of sales values to assess the effectiveness of current pricing strategies. 
*   This may involve analyzing price points, discounts, and promotional offers to optimize revenue and profitability.
*   Consider developing targeted promotions or pricing tiers based on identified customer segments and their spending patterns.

**2. Sales Performance and Forecasting:**

*   Analyze historical trends in the distribution of sales values to identify seasonality, cyclical patterns, or other factors influencing sales performance.
*   Utilize the insights to improve sales forecasting and inventory management, ensuring adequate stock availability for products with high demand or frequent purchases.

**3. Product Management and Development:**

*   Investigate the relationship between sales value and product categories or features. 
*   This can inform product development decisions, pricing strategies, and marketing efforts. 
*   Consider developing new products or bundles targeted towards specific customer segments based on their purchasing power and preferences.

**4. Risk Management:**

*   Analyze the distribution of sales values to assess potential risks associated with concentrated sales within specific customer segments or product categories.
*   Develop strategies to diversify the customer base and product portfolio to mitigate risks and ensure business stability.
""")
      customer_details_viz.create_interactive_average_sales_heatmap(df)
      st.markdown("""
## Average Total Sales by Customer Group and Billing State

The heatmap provides valuable insights into the distribution of average total sales across different customer groups and states. Here's how a business can leverage this information:

**1. Identifying Key Customer Groups and Geographic Areas:**

*   **Focus on "Potential Customers":** Understanding their characteristics and needs is crucial for further growth.
*   **Analyze High-Performing States:** NY and CA demonstrate higher average sales across multiple customer groups. Investigating the factors driving these sales can help replicate success in other states.
*   **Evaluate Underperforming Segments:** Several cells show minimal or no sales. Analyze the reasons behind this (e.g., lack of market penetration, competition) and consider strategies for improvement or resource reallocation.

**2. Sales and Marketing Strategies:**

*   **Targeted Marketing:** Tailor marketing campaigns based on the performance of customer groups and states. Allocate more resources towards high-performing segments like "Potential Customers" in NY.
*   **Expansion Opportunities:** Explore potential expansion into states with high average sales like NY and CA, focusing on successful customer groups.
*   **Customer Acquisition and Retention:** Develop targeted strategies to acquire new customers in underperforming states and customer groups. Implement retention programs to maintain strong relationships with existing high-value customers.

**3. Resource Allocation and Operations:**

*   **Optimize Sales Team Structure:** Align sales teams based on the geographic distribution of sales and customer groups. Consider dedicated teams or specialists for high-performing segments.
*   **Inventory Management:** Analyze the sales distribution to optimize inventory management and distribution strategies. Ensure sufficient stock availability in high-demand states and for key customer groups.
*   **Pricing and Promotions:** Evaluate the effectiveness of current pricing strategies and promotional activities based on their impact on sales in different segments. Consider tailored pricing or promotions for specific customer groups or regions.
""") 
    elif file_type == "Low Stock Inventory report":
      low_stock_inventory_viz.low_stock_analysis_app(df)
      st.markdown("""
## Distribution of Low Stock Items by Category

Visualizing the distribution of low stock items by category helps businesses proactively manage inventory and prevent stockouts:

**Identifying Inventory Issues:**

*   The chart quickly reveals which categories have the most items with low stock levels.
*   This allows businesses to prioritize inventory replenishment for those categories to avoid stockouts and potential lost sales.

**Category Management:**

*   Businesses can evaluate the effectiveness of their category management strategies based on the distribution of low-stock items. 
*   This may prompt further analysis into demand forecasting, supplier relationships, or product assortment within specific categories.

**Inventory Optimization:**

*   The insights from the chart can guide inventory optimization efforts. 
*   Businesses may consider adjusting reorder points, safety stock levels, or supplier lead times for categories prone to frequent low-stock issues.

**Preventing Stockouts:**

*   By proactively identifying low-stock items, businesses can take steps to prevent stockouts, which can lead to lost sales, customer dissatisfaction, and potential damage to brand reputation. 
""")
      st.markdown("""
## Analysis of Wholesale Price vs. Available Quantity

A scatter plot visualizing the relationship between wholesale price and available quantity provides insights into inventory management and pricing strategies:

**Identifying Pricing Trends:**

*   The plot helps reveal potential correlations or patterns between wholesale price and available quantity. 
*   For example, it may show whether higher-priced items tend to have lower stock levels or if there's no clear relationship between the two variables.

**Inventory Management:**

*   Businesses can use the insights to inform inventory management decisions. 
*   For instance, if high-value items have low stock, it might be necessary to prioritize their replenishment to avoid stockouts and potential lost sales.

**Pricing Strategy Evaluation:**

*   The scatter plot can help assess the effectiveness of pricing strategies in relation to inventory levels. 
*   Businesses may consider adjusting prices or exploring promotional offers for items with high stock levels to stimulate demand and optimize inventory turnover.

**Category Analysis:**

*   By incorporating color-coding or other visual cues to represent different categories, businesses can analyze how pricing and inventory levels vary across different product groups. 
""") 
      low_stock_inventory_viz.create_profit_margin_analysis_plot(df)
      st.markdown("""
## Profit Margins of Low Stock Items

Analyzing the profit margins of low-stock items provides valuable insights for inventory management and pricing strategies:

**Prioritizing Inventory Replenishment:**

*   The chart highlights which low-stock items have the highest profit margins.
*   Businesses can prioritize inventory replenishment for these items to maximize profitability and avoid potential lost revenue.

**Pricing Strategy Evaluation:**

*   Businesses can assess the pricing strategies of low-stock items in relation to their profit margins. 
*   This may lead to insights on potential price adjustments or promotional offers to optimize profitability while managing inventory levels.

**Product Performance Analysis:**

*   The chart helps identify low-stock items that are high-performing in terms of profitability. 
*   This information can inform decisions related to product development, marketing, and sales strategies. 

**Inventory Management:**

*   The insights gleaned from the chart can inform inventory management practices. 
*   Businesses may consider adjusting reorder points or safety stock levels for high-margin items with low stock to prevent stockouts and ensure availability for customers. 
""")
      low_stock_inventory_viz.create_low_stock_by_manufacturer_bar_plot(df)
      st.markdown("""
## Distribution of Wholesale Prices for Low-Stock Items

Analyzing the distribution of wholesale prices for low-stock items offers valuable insights for inventory management and pricing strategies:

**Identifying Price Ranges:**

*   The histogram clearly displays the range of wholesale prices for low-stock items and the frequency of items within different price ranges.
*   This helps businesses understand the overall pricing structure of their low-stock inventory.

**Inventory Valuation:**

*   The visualization provides insights into the value of low-stock inventory based on the distribution of wholesale prices.
*   This information can be valuable for financial planning and analysis.

**Pricing Strategy Evaluation:**

*   Businesses can assess the pricing strategies of low-stock items in relation to their frequency within different price ranges. 
*   This may lead to insights on potential price adjustments, promotions, or inventory management decisions based on the price distribution.

**Category Analysis:**

*   By comparing histograms for different categories, businesses can identify how the distribution of wholesale prices varies across different product groups. 
*   This information can inform category management and pricing strategies. 
""")
      #low_stock_inventory_viz.create_price_distribution_plot(df)
      low_stock_inventory_viz.create_interactive_price_vs_quantity_plot(df)
      st.markdown("""
## Wholesale Price vs. Available Quantity for Low-Stock Items

A scatter plot with a trendline visualizing the relationship between wholesale price and available quantity for low-stock items offers valuable insights:

**Identifying Trends and Correlations:**

*   The scatter plot helps reveal potential trends or correlations between wholesale price and available quantity for low-stock items.
*   The trendline summarizes the overall direction of the relationship, indicating whether there's a positive, negative, or no clear association between the variables.

**Inventory Management Insights:**

*   Businesses can gain insights into how pricing might influence the availability of low-stock items.
*   This information can inform inventory management decisions, such as prioritizing replenishment for specific price ranges or adjusting pricing strategies to manage stock levels.

**Pricing Strategy Evaluation:**

*   The visualization helps assess the effectiveness of pricing strategies for low-stock items.
*   Businesses may consider adjusting prices or exploring promotional offers for certain price ranges based on the observed trends and available quantities.

**Predictive Potential:**

*   The trendline provides a potential basis for predicting available quantity based on wholesale price.
*   This allows businesses to anticipate inventory needs and proactively manage stock levels. 
""")
      low_stock_inventory_viz.create_quantity_price_ratio_plot(df)
      st.markdown("""
## Ratio of Available Quantity to Retail Price for Low-Stock Items

Visualizing the ratio of available quantity to retail price for low-stock items provides insights into potential inventory and pricing issues:

**Identifying Potential Issues:**

*   The plot highlights items where the ratio of available quantity to price deviates significantly from the majority.
*   For instance, an item with a high ratio (e.g., Ginger Shots) might indicate overstocking or pricing issues, while items with very low ratios may suggest potential stockouts or high demand.

**Visual Comparison:**

*   Presenting the information visually makes it easier to compare ratios across different products than examining a table of numbers. 
*   This allows for quick identification of outliers and patterns.

**Decision Making:**

*   This type of plot can be instrumental in making informed decisions about inventory management, pricing strategies, and marketing efforts. 
*   It helps prioritize which products require attention and action.
""")
    elif file_type == "Best Sellers report":
      df = best_sellers_viz.preprocess_data(df)
      best_sellers_viz.create_available_cases_plot(df)
      st.markdown("""
## Inventory Levels of Products Over Time

Visualizing the inventory levels of products over time provides insights into stock fluctuations and potential inventory management issues:

**Visualizing Trends:**

*   The plot allows for quick understanding of the overall trend of available cases for each product.
*   We can easily identify periods of high and low inventory, as well as any sudden changes or fluctuations. 

**Comparing Products:**

*   With all products displayed on a single chart, it's simple to compare their inventory levels and identify any significant differences or similarities in their stock patterns.

**Identifying Potential Issues:**

*   Products with consistently low or negative inventory levels (like "Ginger Shots" in this example) may indicate potential stockouts or supply chain problems that require attention.

**Decision Making:**

*   For businesses, this plot can be a crucial tool for making informed decisions about inventory management, production planning, and sales strategies.
*   It provides insights into which products need restocking, potential overstock situations, and overall inventory health.
""")
      best_sellers_viz.product_analysis_app(df)
      st.markdown("""
## Comparison of Total Cases Sold and Total Revenue by Product

Placing "Total Revenue" and "Total Cases Sold" charts side-by-side provides valuable insights into product performance:

**Comparison of Key Metrics:**

*   The side-by-side bar charts allow for easy comparison of sales volume and revenue generation for each product.
*   This helps understand the relationship between these two crucial metrics and identify products that excel in one or both areas.

**Identifying Top Performers:**

*   The charts quickly reveal which products are generating the most revenue and selling the most cases.
*   In this example, "Ginger Shots" clearly stands out as the top performer in both categories.

**Assessing Product Contribution:**

*   The percentages on each bar provide context by showing each product's contribution to total revenue and sales volume.
*   This helps understand the relative importance of each product to the business.

**Decision Making:**

*   Businesses can utilize this information to make informed decisions about product focus, marketing strategies, and resource allocation. 
*   For instance, they might invest more in promoting "Ginger Shots" or explore ways to improve the performance of products with lower sales or revenue.
""")
      best_sellers_viz.create_cases_revenue_relationship_plot(df)
      st.markdown("""
## Relationship between Cases Sold and Total Revenue

Visualizing the relationship between cases sold and total revenue provides insights into sales performance and potential trends:

**Visualizing Correlation:**

*   The chart allows for visual assessment of any correlation between the number of cases sold and total revenue generated.
*   In this example, we observe a general trend where higher case sales tend to correspond with higher revenue, although some variations exist.

**Identifying Outliers:**

*   The plot helps pinpoint data points that deviate significantly from the overall trend.
*   For instance, the bar representing 240 cases sold with 4050 in revenue appears lower than what the general trend might suggest, prompting further investigation.

**Understanding Sales Performance:**

*   Businesses can utilize this chart to gain insights into their sales performance and identify areas for improvement.
*   They can analyze which sales volumes contribute the most to overall revenue and strategize accordingly. 

**Predictive Potential:**

*   While this chart uses historical data, it can also provide a basis for predicting future revenue based on projected sales volumes.
*   This can be helpful for budgeting, forecasting, and setting sales targets.
""")
      best_sellers_viz.price_comparison_app(df)
      st.markdown("""
## Average Wholesale Price by Category

Analyzing the average wholesale price per category provides insights into pricing structures and potential profitability:

**Comparing Averages:**

*   The chart enables direct visual comparison of average wholesale prices between different categories.
*   This makes it easy to identify which categories have higher or lower average prices.

**Category Analysis:**

*   Businesses can use this chart to analyze the pricing structure of their products across different categories.
*   It helps identify potential areas where pricing adjustments might be necessary.

**Profitability Insights:**

*   Understanding the average wholesale price per category provides insights into potential profitability and margins for each category.
*   This information can guide decisions related to product sourcing, pricing strategies, and inventory management. 

**Identifying Discrepancies:**

*   In cases where certain categories show significantly higher or lower average prices, further investigation can be conducted to understand the underlying reasons. 
*   This could reveal opportunities for cost optimization or pricing adjustments.
""")
      best_sellers_viz.create_revenue_vs_profit_plot(df)
      #markdown call in the function
    elif file_type == "SKU's Not Ordered report":
      df = skus_not_ordered_viz.preprocess_data(df)
      skus_not_ordered_viz.create_unordered_products_by_category_plot(df)
      st.markdown("""
## Analysis of Unordered Products by Category

The bar chart effectively visualizes the number of unordered products across different categories, providing insights for inventory management and demand forecasting:

*   **Identifying Stock Issues:** The chart immediately draws attention to categories with a higher number of unordered products, signaling potential stockouts or supply chain issues that need to be addressed.
*   **Category Comparison:** The side-by-side presentation allows for easy comparison of categories in terms of maintaining sufficient stock levels, highlighting areas needing more attention or adjustments in ordering processes. 
*   **Inventory Management Insights:** Businesses can utilize this information to gain insights into their inventory management practices and identify areas for improvement, helping prioritize reordering and preventing stockouts of popular or essential items.
*   **Demand Forecasting:** The data on unordered products can be used in conjunction with sales data to improve demand forecasting and ensure sufficient inventory availability to meet customer demand. 
""")
      skus_not_ordered_viz.create_available_cases_distribution_plot(df)
      st.markdown("""
## Distribution of Unordered Products by Stock Level

The bar chart provides a clear overview of the distribution of unordered products based on their stock levels:

*   **Inventory Insights:** The majority of unordered products fall into the "Medium Stock" category, suggesting that most items without open orders have adequate stock levels.
*   **Potential Stock Issues:** While the number is smaller, there are still products in the "Low Stock" and "High Stock" categories that require attention.
*   **Low Stock Concerns:** Businesses should investigate the "Low Stock" items to prevent potential stockouts and ensure timely replenishment.
*   **High Stock Analysis:** The "High Stock" category might indicate overstocking or slower-moving items, prompting analysis of demand forecasting and potential adjustments in ordering quantities. 
""")
      skus_not_ordered_viz.price_vs_available_cases_app(df)
      st.markdown("""
## Average Available Cases by Retail Price Range and Category

The charts effectively visualize the average available cases for products within different retail price ranges for each category, providing insights for inventory management and pricing strategies:

*   **Inventory Analysis by Price Range:** The charts enable analysis of inventory levels for different price ranges within each category, helping identify potential stock imbalances and areas for optimization.
*   **Category Comparison:** The separate presentation of data for each category allows for easy comparison of inventory distribution across price ranges, revealing potential differences in stocking patterns and demand across categories.
*   **Pricing Strategy Insights:** The plots can offer insights into the effectiveness of pricing strategies and guide potential adjustments in pricing or product assortment within categories to optimize inventory levels and sales.
*   **Demand and Supply Alignment:** Businesses can use this information to ensure that inventory levels are aligned with customer demand across different price points within each category, optimizing stock levels, reducing carrying costs, and avoiding stockouts or overstocks.
""")
      skus_not_ordered_viz.create_wholesale_vs_retail_price_scatter(df)
      st.markdown("""
## Insights from Available Cases vs. Profit Margin

The scatter plot visualizes the relationship between available cases and profit margin for unordered products, offering insights into inventory and pricing strategies:

*   **Limited Data:** The plot shows a limited number of data points, making it difficult to identify clear trends or patterns. More data would be needed for a comprehensive analysis. 
*   **Category Comparison:** The color-coding allows for comparison between the "Uncategorized" and "Drinks" categories. However, with limited data, it's difficult to draw definitive conclusions about category-specific trends.
*   **Potential Outliers:** A few data points appear to deviate from the general distribution, particularly those with higher profit margins and low available cases. These could warrant further investigation to understand the reasons behind their profitability and inventory levels.
*   **Further Analysis Needed:**  A more extensive dataset would allow for a more robust analysis of the relationship between available cases and profit margin, potentially revealing valuable insights for inventory management, pricing strategies, and product assortment decisions.
""")
      skus_not_ordered_viz.df_unordered_products_per_category_and_price_range(df)
      st.markdown("""
## Analysis of Unordered Products by Category and Price Range

The heatmap effectively visualizes the number of unordered products within different price ranges for each category, providing insights for inventory management and demand forecasting:

*   **Identifying Problem Areas:** The heatmap quickly reveals areas with a higher concentration of unordered products through color intensity, allowing businesses to pinpoint specific categories and price ranges that require immediate attention.
*   **Category and Price Analysis:** The combination of category and price range on a single plot enables comprehensive analysis of inventory issues, helping identify whether certain categories are more prone to stockouts within specific price ranges. 
*   **Visualizing Trends:** A heatmap with more data can reveal trends or patterns in unordered products, highlighting seasonal fluctuations, shifts in customer preferences, or the impact of marketing campaigns on product demand. 
*   **Inventory Management Optimization:** Businesses can utilize this information to optimize inventory management practices by focusing on categories and price ranges with a higher number of unordered products, prioritizing reordering, adjusting stock levels, and implementing strategies to prevent future stockouts. 
""")
    elif file_type == "Current Inventory report":
      current_inventory_viz.df_analyze_inventory_value_by_category(df)
      st.markdown("""
## Distribution of Low Stock Items by Category

Visualizing the distribution of low stock items by category helps businesses proactively manage inventory and prevent stockouts:

**Identifying Inventory Issues:**

*   The chart quickly reveals which categories have the most items with low stock levels.
*   This allows businesses to prioritize inventory replenishment for those categories to avoid stockouts and potential lost sales.

**Category Management:**

*   Businesses can evaluate the effectiveness of their category management strategies based on the distribution of low-stock items. 
*   This may prompt further analysis into demand forecasting, supplier relationships, or product assortment within specific categories.

**Inventory Optimization:**

*   The insights from the chart can guide inventory optimization efforts. 
*   Businesses may consider adjusting reorder points, safety stock levels, or supplier lead times for categories prone to frequent low-stock issues.

**Preventing Stockouts:**

*   By proactively identifying low-stock items, businesses can take steps to prevent stockouts, which can lead to lost sales, customer dissatisfaction, and potential damage to brand reputation.
""")
      current_inventory_viz.df_analyze_quantity_vs_retail_price(df)
      st.markdown("""
## Comprehensive Analysis of Available Quantity, Retail Price, Category, and Wholesale Price

A scatter plot with color-coding and size variations provides a comprehensive view of the relationships between multiple variables:

**Multiple Variable Analysis:**

*   This plot allows us to analyze the interplay of several variables simultaneously.
*   We can observe how available quantity relates to retail price, while also considering the influence of category and wholesale price. 

**Color-Coding for Insights:**

*   The use of color to differentiate categories helps identify any potential patterns or trends within each category.
*   For instance, we might observe that one category tends to have higher retail prices or larger available quantities compared to others.

**Size as an Indicator:**

*   Varying the size of the points based on wholesale price adds another layer of information.
*   This allows us to assess whether there's a relationship between wholesale price and the other variables. 
*   For example, we might observe if products with higher wholesale prices also tend to have higher retail prices or larger available quantities.

**Identifying Outliers:**

*   The plot makes it easy to spot any outliers or data points that deviate significantly from the general patterns.
*   This could prompt further investigation to understand the reasons behind such deviations and potentially uncover valuable insights.

**Decision Making Support:**

*   Businesses can utilize this information to make informed decisions about pricing strategies, inventory management, and product assortment. 
*   It helps identify potential areas for optimization, such as adjusting pricing for certain products or categories, managing stock levels based on demand and wholesale costs, and understanding the profitability of different products. 
""")
      current_inventory_viz.df_analyze_inventory_value_by_manufacturer(df)
      current_inventory_viz.df_analyze_inventory_value_per_unit(df)
      st.markdown("""
## Analysis of Average Inventory Value per Unit

The bar chart effectively visualizes the average inventory value per unit for each product, providing valuable insights for inventory management and financial planning:

*   **Product Comparison:** The chart allows for immediate comparison of the average inventory value between "Ginger Shots" and "Test T". It clearly highlights the significant difference in value, with "Ginger Shots" having a substantially higher average inventory value per unit. 
*   **Inventory Valuation:** Businesses can use this information to estimate the overall value of their inventory based on the quantity of each product in stock. This is crucial for financial reporting, budgeting, and understanding the financial impact of inventory levels.
*   **Resource Allocation:** The chart can inform decisions regarding resource allocation and investment. Given the higher value of "Ginger Shots," businesses might prioritize its production, marketing, or inventory management to maximize returns.
*   **Pricing Strategies:** Understanding the inventory value per unit can be helpful in setting appropriate pricing strategies. Products with higher inventory value might require different pricing considerations compared to those with lower value. 
""")
      current_inventory_viz.df_compare_average_retail_prices(df)
      st.markdown("""
## Insights from Average Retail Price by Category

The bar chart provides a clear comparison of average retail prices between the "Drinks" and "Uncategorized" categories:

*   **Price Discrepancy:** The "Drinks" category has a significantly higher average retail price compared to the "Uncategorized" category. This indicates a potential difference in the types of products or pricing strategies within these categories.
*   **Category Analysis:**  Businesses can investigate the factors contributing to the price difference, such as product quality, brand positioning, or target customer segments. 
*   **Pricing Strategies:** The insights can inform pricing strategies for each category. For example, businesses might explore premium pricing options for the "Drinks" category or consider competitive pricing for the "Uncategorized" category to increase sales volume.
*   **Product Assortment:** The price difference could also influence product assortment decisions within each category. 
""") 
    else:
      st.write("**Invalid File**")