import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------
# Page Title
# --------------------------
st.set_page_config(page_title="Customer Analysis Dashboard", layout="wide")
st.title("📊 Customer Purchase Behavior Analysis")

# --------------------------
# Load Dataset
# --------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("OnlineRetail.csv", encoding='ISO-8859-1')
    return df

df = load_data()

# --------------------------
# Data Cleaning
# --------------------------
df.dropna(subset=['CustomerID'], inplace=True)
df = df[df['Quantity'] > 0]
df = df[df['UnitPrice'] > 0]

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# --------------------------
# Sidebar Filters
# --------------------------
st.sidebar.header("Filters")

countries = df['Country'].unique()
selected_country = st.sidebar.selectbox("Select Country", countries)

filtered_df = df[df['Country'] == selected_country]

# --------------------------
# Metrics
# --------------------------
st.subheader("📌 Key Metrics")

total_revenue = filtered_df['TotalPrice'].sum()
total_orders = filtered_df['InvoiceNo'].nunique()
total_customers = filtered_df['CustomerID'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${round(total_revenue, 2)}")
col2.metric("Total Orders", total_orders)
col3.metric("Total Customers", total_customers)

# --------------------------
# Top Products
# --------------------------
st.subheader("🔥 Top 10 Products")

top_products = (
    filtered_df.groupby('Description')['Quantity']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig1, ax1 = plt.subplots()
top_products.plot(kind='bar', ax=ax1)
ax1.set_ylabel("Quantity Sold")
st.pyplot(fig1)

# --------------------------
# Revenue by Country
# --------------------------
st.subheader("🌍 Top Countries by Revenue")

country_sales = (
    df.groupby('Country')['TotalPrice']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig2, ax2 = plt.subplots()
country_sales.plot(kind='bar', ax=ax2)
ax2.set_ylabel("Revenue")
st.pyplot(fig2)

# --------------------------
# Monthly Sales Trend
# --------------------------
st.subheader("📈 Monthly Sales Trend")

filtered_df['Month'] = filtered_df['InvoiceDate'].dt.to_period('M')
monthly_sales = filtered_df.groupby('Month')['TotalPrice'].sum()

fig3, ax3 = plt.subplots()
monthly_sales.plot(ax=ax3)
ax3.set_ylabel("Revenue")
st.pyplot(fig3)

# --------------------------
# Top Customers
# --------------------------
st.subheader("💎 Top 10 High-Value Customers")

top_customers = (
    filtered_df.groupby('CustomerID')['TotalPrice']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.dataframe(top_customers)

# --------------------------
# Insights Section
# --------------------------
st.subheader("🧠 Key Insights")

st.write("✔ A small number of customers contribute significantly to total revenue.")
st.write("✔ Certain products dominate sales volume.")
st.write("✔ Revenue shows variation across months indicating seasonal trends.")
st.write("✔ Geographic regions have different purchasing behaviors.")
