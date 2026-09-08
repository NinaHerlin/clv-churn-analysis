import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Customer Churn & CLV Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    :root { --ink: #172033; --muted: #667085; --line: #e6eaf0; --teal: #087f8c; }
    * { font-family: 'DM Sans', sans-serif; }
    h1, h2, h3, h4 { font-family: 'Space Grotesk', sans-serif !important; color: var(--ink); }
    .stApp { background: linear-gradient(135deg, #f7fbfc 0%, #ffffff 48%, #fff9f5 100%); }
    [data-testid="stHeader"] { background: rgba(255, 255, 255, 0.86); }
    [data-testid="stSidebar"] { background: #f3f8fa; border-right: 1px solid var(--line); }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] label { color: var(--ink); }
    .block-container { max-width: 1500px; padding-top: 2.2rem; padding-bottom: 3rem; }
    .dashboard-hero { background: linear-gradient(120deg, #0b7285 0%, #12949b 58%, #f4a261 150%); border-radius: 18px; padding: 2rem 2.2rem; margin-bottom: 1.6rem; box-shadow: 0 12px 30px rgba(8, 127, 140, .16); }
    .dashboard-hero h1 { color: white !important; margin: 0 0 .35rem; font-size: 2.15rem; }
    .dashboard-hero p { color: rgba(255,255,255,.9); margin: 0; font-size: 1.02rem; }
    [data-testid="stMetric"] { background: white; border: 1px solid var(--line); border-radius: 14px; padding: 1rem 1.1rem; box-shadow: 0 5px 18px rgba(23, 32, 51, .05); }
    [data-testid="stMetricLabel"] { color: var(--muted); }
    [data-testid="stMetricValue"] { color: var(--teal); font-family: 'Space Grotesk', sans-serif; }
    div[data-baseweb="tab-list"] { background: rgba(255,255,255,.72); border: 1px solid var(--line); border-radius: 13px; padding: .3rem; box-shadow: 0 5px 18px rgba(23, 32, 51, .04); }
    button[data-baseweb="tab"] { color: var(--muted); font-weight: 600; padding: .72rem 1rem; border-radius: 9px; transition: all .2s ease; }
    button[data-baseweb="tab"]:hover { color: var(--teal); background: #eaf7f6; }
    button[data-baseweb="tab"][aria-selected="true"] { color: white; background: var(--teal); border-bottom-color: transparent; }
    .stDownloadButton > button { border: 1px solid var(--teal); border-radius: 9px; color: var(--teal); background: white; font-weight: 600; transition: all .2s ease; }
    .stDownloadButton > button:hover { color: white; background: var(--teal); }
    [data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 12px; overflow: hidden; }
    .section-kicker { color: #d8f3f0; font-size: .76rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
    hr { border-color: var(--line); }
</style>
""", unsafe_allow_html=True)

CHART_LAYOUT = {
    "template": "plotly_white",
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "#ffffff",
    "font": {"family": "DM Sans, sans-serif", "color": "#172033"},
    "margin": {"l": 18, "r": 18, "t": 28, "b": 18},
    "legend": {"orientation": "h", "y": 1.08, "x": 0}
}

def format_compact_currency(value):
    """Format currency values for compact KPI cards."""
    absolute_value = abs(value)
    if absolute_value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    if absolute_value >= 1_000:
        return f"${value / 1_000:.1f}K"
    return f"${value:,.0f}"

# 2. Fungsi Load Data (dengan pengaman dari KeyError)
@st.cache_data
def load_data():
    df_loaded = pd.read_csv("data/churn_clv_predictions.csv")
    df_loaded.columns = df_loaded.columns.str.strip()  # Hapus spasi pada nama kolom
    
    # Proteksi: Buat kolom cadangan jika belum diekspor dari notebook
    if 'Country' not in df_loaded.columns:
        df_loaded['Country'] = 'Unknown'
    if 'Top_Product' not in df_loaded.columns:
        df_loaded['Top_Product'] = 'No Product Data'
        
    return df_loaded

# WAJIB ADA: Panggil fungsi load_data() ke variabel 'df' di sini!
df = load_data()

# 3. Sidebar Filter
st.sidebar.header("Customer Filters")

# Filter Kategori Risiko Churn (sekarang 'df' sudah terdefinisi)
risk_options = df['Churn_Risk'].unique().tolist()
selected_risk = st.sidebar.multiselect(
    "Churn Risk Category",
    options=risk_options,
    default=risk_options
)

# Filter Rentang CLTV 180 Days
clv_min = float(df['CLTV_180_days'].min())
clv_max = float(df['CLTV_180_days'].max())

selected_clv = st.sidebar.slider(
    "Predicted CLTV Range (180 Days)",
    min_value=clv_min,
    max_value=clv_max,
    value=(clv_min, clv_max)
)

# Filter Negara / Area (Fitur Baru)
country_options = sorted(df['Country'].dropna().unique().tolist())
selected_country = st.sidebar.multiselect(
    "Country / Area",
    options=country_options,
    default=country_options
)

# Terapkan Semua Filter ke DataFrame
filtered_df = df[
    (df['Churn_Risk'].isin(selected_risk)) &
    (df['CLTV_180_days'].between(selected_clv[0], selected_clv[1])) &
    (df['Country'].isin(selected_country))
]

# 4. Header Utama
st.markdown("""
<section class="dashboard-hero">
    <div class="section-kicker">CUSTOMER INTELLIGENCE / 180 DAYS</div>
    <h1>Customer Churn &amp; CLV Analytics</h1>
    <p>Prioritize customers, measure revenue at risk, and turn predictions into focused retention actions.</p>
</section>
""", unsafe_allow_html=True)

st.divider()

# 5. Executive Summary (KPI Cards)
col1, col2, col3, col4 = st.columns(4)

total_cust = len(filtered_df)
avg_churn_prob = filtered_df['Churn_Probability'].mean() * 100 if total_cust > 0 else 0
total_clv = filtered_df['CLTV_180_days'].sum()
revenue_at_risk = filtered_df[filtered_df['Churn_Risk'] == 'High Risk']['CLTV_180_days'].sum()

col1.metric("Filtered Customers", f"{total_cust:,}")
col2.metric("Average Churn Probability", f"{avg_churn_prob:.1f}%")
col3.metric("Total Predicted CLTV (180 Days)", format_compact_currency(total_clv))
col4.metric("Revenue at Risk (High Risk)", format_compact_currency(revenue_at_risk))

st.divider()

# 6. Tab Layout
tab1, tab2, tab3, tab4 = st.tabs([
    "CLV vs Churn", 
    "Regions & Products", 
    "Target Customers", 
    "Purchase Forecast"
])

with tab1:
    st.subheader("CLTV vs Churn Probability")
    
    fig = px.scatter(
        filtered_df,
        x="Churn_Probability",
        y="CLTV_180_days",
        color="Churn_Risk",
        hover_data=["Customer ID", "Country", "Top_Product", "predicted_purchases"],
        color_discrete_map={"High Risk": "#EF553B", "Medium Risk": "#FECB52", "Low Risk": "#00CC96"},
        labels={
            "Churn_Probability": "Churn Probability (0 - 1)",
            "CLTV_180_days": "Predicted CLTV (180 Days, $)",
            "Churn_Risk": "Risk Level"
        }
    )
    fig.update_layout(**CHART_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Regional and Product Insights")
    col_geo, col_prod = st.columns(2)
    
    with col_geo:
        st.markdown("#### Top 5 Countries by Revenue at Risk")
        risk_by_country = (
            filtered_df[filtered_df['Churn_Risk'] == 'High Risk']
            .groupby('Country')['CLTV_180_days'].sum()
            .reset_index()
            .sort_values('CLTV_180_days', ascending=True)
            .tail(5)
        )
        
        if not risk_by_country.empty:
            fig_country = px.bar(
                risk_by_country, 
                x="CLTV_180_days", 
                y="Country", 
                orientation='h',
                labels={"CLTV_180_days": "Total Revenue at Risk ($)", "Country": "Country"},
                color_discrete_sequence=['#EF553B']
            )
            fig_country.update_layout(**CHART_LAYOUT)
            st.plotly_chart(fig_country, use_container_width=True)
        else:
            st.info("No high-risk data matches the selected filters.")

    with col_prod:
        st.markdown("#### Top 5 Products among High-Risk Customers")
        top_prod_high_risk = (
            filtered_df[filtered_df['Churn_Risk'] == 'High Risk']['Top_Product']
            .value_counts()
            .reset_index()
            .head(5)
        )
        
        if not top_prod_high_risk.empty:
            top_prod_high_risk.columns = ['Produk', 'Jumlah_Pelanggan']
            top_prod_high_risk = top_prod_high_risk.sort_values('Jumlah_Pelanggan', ascending=True)
            
            fig_prod = px.bar(
                top_prod_high_risk,
                x="Jumlah_Pelanggan",
                y="Produk",
                orientation='h',
                labels={"Jumlah_Pelanggan": "High-Risk Customers", "Produk": "Product"},
                color_discrete_sequence=['#FECB52']
            )
            fig_prod.update_layout(**CHART_LAYOUT)
            st.plotly_chart(fig_prod, use_container_width=True)
        else:
            st.info("No product data matches the selected filters.")

with tab3:
    st.subheader("Retention Campaign Targets")
    st.markdown("Review customer IDs, preferred products, and locations for personalized retention campaigns.")
    
    # Format Tampilan Tabel dengan Kolom Produk dan Negara
    cols_to_show = ['Customer ID', 'Country', 'Top_Product', 'Churn_Risk', 'Churn_Probability', 'CLTV_180_days', 'predicted_purchases']
    available_cols = [c for c in cols_to_show if c in filtered_df.columns]
    
    display_df = filtered_df[available_cols].copy()
    if 'Customer ID' in display_df.columns:
        display_df['Customer ID'] = display_df['Customer ID'].astype(str).str.replace(r'\.0$', '', regex=True)
    
    st.dataframe(display_df, use_container_width=True)
    
    # Tombol Unduh CSV
    csv_data = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Target Customer List (CSV)",
        data=csv_data,
        file_name="target_customers_churn_clv.csv",
        mime="text/csv"
    )

with tab4:
    st.subheader("Purchase Frequency Forecast")
    
    fig_hist = px.histogram(
        filtered_df,
        x="predicted_purchases",
        color="Churn_Risk",
        nbins=20,
        labels={"predicted_purchases": "Predicted Purchase Frequency (180 Days)"},
        color_discrete_map={"High Risk": "#EF553B", "Medium Risk": "#FECB52", "Low Risk": "#00CC96"}
    )
    fig_hist.update_layout(**CHART_LAYOUT)
    st.plotly_chart(fig_hist, use_container_width=True)