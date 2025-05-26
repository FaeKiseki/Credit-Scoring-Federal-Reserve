import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(page_title="US Credit Trends Dashboard", layout="wide")

# Custom CSS combining both styles
st.markdown("""
    <style>
    /* Power BI inspired cards */
    .pbi-card {
        padding: 1rem;
        background-color: white;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #0078d4;
    }
    .pbi-title {
        font-size: 1rem;
        color: #333;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .pbi-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #000;
    }
    .pbi-subtext {
        font-size: 0.9rem;
        color: #666;
    }
    
    /* Your original KPI styles */
    .kpi-card {
        padding: 1.5rem;
        background-color: #f9f9f9;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .kpi-title {
        font-size: 1.1rem;
        color: #555;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
        color: #111;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🔍 U.S. Credit Trends Dashboard (2012-2024)")
st.markdown("Data: [Federal Reserve Bank of Philadelphia](https://www.philadelphiafed.org/surveys-and-data/large-bank-credit-card-and-mortgage-data)")

# Load data function with caching
@st.cache_data
def load_data():
    df = pd.read_csv("data/24Q4-CreditCardBalances.csv")
    
    def clean(value):
        if isinstance(value, str):
            return float(value.replace('$', '').replace('%', '').replace(',', '').strip())
        return value

    for col in df.columns:
        if col != 'YRQTR':
            df[col] = df[col].apply(clean)

    df = df.dropna(subset=['YRQTR'])
    df = df[df['YRQTR'].str.match(r'\d{4}Q[1-4]')]
    df['date'] = pd.PeriodIndex(df['YRQTR'], freq='Q').to_timestamp()
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)
    return df

df = load_data()

# ======================================================================
# Power BI Style Section - Opportunity Court Cards
# ======================================================================
st.markdown("## Opportunity Court Metrics")

# Create columns for the cards
col1, col2, col3 = st.columns(3)

# Opportunity Court Cards
with col1:
    st.markdown("""
        <div class="pbi-card">
            <div class="pbi-title">Opportunity Court</div>
            <div class="pbi-value">Government seat</div>
            <div class="pbi-subtext">State: Special Services design</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="pbi-card">
            <div class="pbi-title">Opportunity Court</div>
            <div class="pbi-value">Government seat</div>
            <div class="pbi-subtext">State: Special Security Solutions</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="pbi-card">
            <div class="pbi-title">Opportunity Court</div>
            <div class="pbi-value">Government seat</div>
            <div class="pbi-subtext">State: Special Security Solutions</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="pbi-card">
            <div class="pbi-title">Opportunity Court</div>
            <div class="pbi-subtext">Low Rate: Senior Security Solutions Provided of State</div>
        </div>
    """, unsafe_allow_html=True)

# Revenue Cards (using actual data)
with col3:
    # Example revenues - replace with your actual data
    sample_revenues = [287, 250, 300, 200, 100] + [x*0.1 for x in range(1, 6)]
    
    for rev in sample_revenues[:5]:  # Show first 5 revenue cards
        st.markdown(f"""
            <div class="pbi-card">
                <div class="pbi-title">Revenue</div>
                <div class="pbi-value">${rev:,.1f}</div>
            </div>
        """, unsafe_allow_html=True)

st.divider()

# ======================================================================
# Your Original Analytics Dashboard (Fully Functional)
# ======================================================================
st.markdown("## Credit Trends Analytics")

# KPI Cards (your original functional KPIs)
st.markdown("### 🔍 Key Indicators")
kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Balances</div>
            <div class="kpi-value">${df['Total Balances ($Billions)'].iloc[-1]:,.0f}B</div>
        </div>
    """, unsafe_allow_html=True)

with kpi2:
    util = df['Utilization (Active Accounts Only) (90th percentile)']
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Utilization (P90)</div>
            <div class="kpi-value">{util.iloc[-1]:.2f}%</div>
        </div>
    """, unsafe_allow_html=True)

with kpi3:
    score = df['Current Credit Score (50th percentile)']
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Median Credit Score</div>
            <div class="kpi-value">{score.iloc[-1]:.0f}</div>
        </div>
    """, unsafe_allow_html=True)

# Charts row 1
col1, col2 = st.columns(2)

with col1:
    fig1 = px.line(df, x=df.index, y='Total Balances ($Billions)', 
                  title="📈 Total Credit Card Balances Over Time")
    fig1.update_layout(height=400, margin=dict(t=50, l=20, r=20, b=30))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.line(
        df, x=df.index,
        y=[
            'Utilization (Active Accounts Only) (50th percentile)',
            'Utilization (Active Accounts Only) (75th percentile)',
            'Utilization (Active Accounts Only) (90th percentile)'
        ],
        labels={'value': 'Utilization (%)', 'variable': 'Percentile'},
        title="📊 Credit Utilization Rates (P50, P75, P90)"
    )
    fig2.update_layout(height=400, margin=dict(t=50, l=20, r=20, b=30))
    st.plotly_chart(fig2, use_container_width=True)

# Charts row 2
col3, col4 = st.columns(2)

with col3:
    fig3 = px.line(df, x=df.index, y='Current Credit Score (50th percentile)', 
                  title="🧠 Median Credit Score Over Time")
    fig3.update_layout(height=400, margin=dict(t=50, l=20, r=20, b=30))
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.line(
        df, x=df.index,
        y=[
            '30+ Days Past Due Rates: Accounts Based',
            '60+ Days Past Due Rates: Accounts Based',
            '90+ Days Past Due Rates: Accounts Based'
        ],
        labels={'value': 'Delinquency Rate (%)', 'variable': 'Days Late'},
        title="⚠️ Delinquency Rates Over Time"
    )
    fig4.update_layout(height=400, margin=dict(t=50, l=20, r=20, b=30))
    st.plotly_chart(fig4, use_container_width=True)

# Payment Behavior
st.markdown("### 💳 Payment Behavior Over Time")
fig5 = px.line(
    df, x=df.index,
    y=[
        'Share of Accounts Making the Minimum Payment',
        'Share of Accounts Making Greater Than the Minimum Payment but Less Than the Full Balance',
        'Share of Accounts Making Full Balance Payment'
    ],
    labels={'value': 'Share of Accounts (%)', 'variable': 'Payment Behavior'},
    title="Trends in Credit Card Repayment"
)
fig5.update_layout(height=500, margin=dict(t=50, l=20, r=20, b=30))
st.plotly_chart(fig5, use_container_width=True)