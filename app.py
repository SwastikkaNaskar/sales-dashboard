import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")
st.title("📊 Sales Analytics Dashboard")

@st.cache_data
def load_data():
    sales_data = pd.read_csv('sales_data.csv', parse_dates=['Month'])
    local_sales_data = pd.read_csv('local_sales_data.csv', parse_dates=['Date'])
    return sales_data, local_sales_data

sales_data, local_sales_data = load_data()

st.sidebar.markdown("## 🎯 Filters")
date_range = st.sidebar.date_input("Date Range", (sales_data['Month'].min(), sales_data['Month'].max()))
product_list = ['All'] + sales_data['Product'].unique().tolist()
selected_product = st.sidebar.selectbox("Product", product_list)
city_list = ['All'] + local_sales_data['City'].unique().tolist()
selected_city = st.sidebar.selectbox("City", city_list)

filtered_sales = sales_data[(sales_data['Month'] >= pd.Timestamp(date_range[0])) & (sales_data['Month'] <= pd.Timestamp(date_range[1]))]
if selected_product != 'All':
    filtered_sales = filtered_sales[filtered_sales['Product'] == selected_product]

filtered_local = local_sales_data[(local_sales_data['Date'] >= pd.Timestamp(date_range[0])) & (local_sales_data['Date'] <= pd.Timestamp(date_range[1]))]
if selected_city != 'All':
    filtered_local = filtered_local[filtered_local['City'] == selected_city]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Sales", f"₹{filtered_sales['Sales'].sum():,.0f}")
c2.metric("Avg Sale", f"₹{filtered_sales['Sales'].mean():,.0f}")
c3.metric("Peak Sale", f"₹{filtered_sales['Sales'].max():,.0f}")
c4.metric("Products", filtered_sales['Product'].nunique())
c5.metric("Cities", filtered_local['City'].nunique())

st.divider()

c1, c2 = st.columns(2)
with c1:
    monthly = filtered_sales.groupby('Month')['Sales'].sum().reset_index()
    fig1 = px.line(monthly, x='Month', y='Sales', title='Monthly Sales Trend', markers=True)
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    products = filtered_sales.groupby('Product')['Sales'].sum().sort_values(ascending=False).reset_index()
    fig2 = px.bar(products, x='Product', y='Sales', title='Sales by Product', color='Sales', color_continuous_scale='Viridis')
    st.plotly_chart(fig2, use_container_width=True)

c1, c2 = st.columns(2)
with c1:
    cities = filtered_local.groupby('City')['Local_Sales'].sum().reset_index()
    fig3 = px.pie(cities, names='City', values='Local_Sales', title='Sales Distribution by City')
    st.plotly_chart(fig3, use_container_width=True)

with c2:
    monthly_cum = filtered_sales.groupby('Month')['Sales'].sum().reset_index()
    monthly_cum['Cumulative'] = monthly_cum['Sales'].cumsum()
    fig4 = px.line(monthly_cum, x='Month', y='Cumulative', title='Cumulative Sales', markers=True)
    st.plotly_chart(fig4, use_container_width=True)

st.divider()
st.markdown("## 📋 Data Tables")
tab1, tab2, tab3 = st.tabs(["Sales Data", "Local Sales", "Summary"])
with tab1:
    st.dataframe(filtered_sales, use_container_width=True, height=300)
    st.download_button("📥 Download", filtered_sales.to_csv(index=False), f"sales_{datetime.now().strftime('%Y%m%d')}.csv")
with tab2:
    st.dataframe(filtered_local, use_container_width=True, height=300)
    st.download_button("📥 Download", filtered_local.to_csv(index=False), f"local_{datetime.now().strftime('%Y%m%d')}.csv")
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Sales Stats**")
        st.dataframe(filtered_sales['Sales'].describe())
    with col2:
        st.write("**Local Sales Stats**")
        st.dataframe(filtered_local['Local_Sales'].describe())

st.divider()
st.markdown("📊 Interactive Dashboard | Filters • Charts • Data Export")
