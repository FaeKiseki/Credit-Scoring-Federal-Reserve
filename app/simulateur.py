import streamlit as st
import pandas as pd
import plotly.express as px

# --- Config page
st.set_page_config(page_title="US Credit Trends Dashboard", layout="wide")

# --- Title
st.title("📊 U.S. Credit Trends Dashboard (2012–2024)")
st.markdown("Data: [Federal Reserve Bank of Philadelphia](https://www.philadelphiafed.org/surveys-and-data/large-bank-credit-card-and-mortgage-data) | Quarterly aggregated metrics")

# --- Load data
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

# --- KPIs section
st.markdown("### 🔍 Key Indicators")
kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric("💰 Total Balances (latest)", f"${df['Total Balances ($Billions)'].iloc[-1]:,.0f} B")

with kpi2:
    util = df['Utilization (Active Accounts Only) (90th percentile)']
    st.metric("🔥 Utilization P90", f"{util.iloc[-1]:.2f}%", delta=f"{util.iloc[-1] - util.iloc[-2]:.2f}%")

with kpi3:
    score = df['Current Credit Score (50th percentile)']
    st.metric("🧠 Median Credit Score", f"{score.iloc[-1]:.0f}")

st.divider()

# --- Two-column layout for plots
col1, col2 = st.columns(2)

# --- Balances
with col1:
    fig = px.line(df, x=df.index, y='Total Balances ($Billions)', title="📈 Total Credit Card Balances Over Time")
    fig.update_layout(height=400, margin=dict(t=50, l=20, r=20, b=30))
    st.plotly_chart(fig, use_container_width=True)

# --- Utilization
with col2:
    fig = px.line(
        df, x=df.index,
        y=[
            'Utilization (Active Accounts Only) (50th percentile)',
            'Utilization (Active Accounts Only) (75th percentile)',
            'Utilization (Active Accounts Only) (90th percentile)'
        ],
        labels={'value': 'Utilization (%)', 'variable': 'Percentile'},
        title="📊 Credit Utilization Rates (P50, P75, P90)"
    )
    fig.update_layout(height=400, margin=dict(t=50, l=20, r=20, b=30))
    st.plotly_chart(fig, use_container_width=True)

# --- Second row
col3, col4 = st.columns(2)

# --- Credit Score
with col3:
    fig = px.line(df, x=df.index, y='Current Credit Score (50th percentile)', title="🧠 Median Credit Score Over Time")
    fig.update_layout(height=400, margin=dict(t=50, l=20, r=20, b=30))
    st.plotly_chart(fig, use_container_width=True)

# --- Delinquency
with col4:
    fig = px.line(
        df, x=df.index,
        y=[
            '30+ Days Past Due Rates: Accounts Based',
            '60+ Days Past Due Rates: Accounts Based',
            '90+ Days Past Due Rates: Accounts Based'
        ],
        labels={'value': 'Delinquency Rate (%)', 'variable': 'Days Late'},
        title="⚠️ Delinquency Rates (30+, 60+, 90+ Days)"
    )
    fig.update_layout(height=400, margin=dict(t=50, l=20, r=20, b=30))
    st.plotly_chart(fig, use_container_width=True)

# --- Payment behavior
st.markdown("### 💵 Payment Behavior Over Time")
fig = px.line(
    df, x=df.index,
    y=[
        'Share of Accounts Making the Minimum Payment',
        'Share of Accounts Making Greater Than the Minimum Payment but Less Than the Full Balance',
        'Share of Accounts Making Full Balance Payment'
    ],
    labels={'value': 'Share of Accounts (%)', 'variable': 'Payment Behavior'},
    title="Trends in Credit Card Repayment"
)
fig.update_layout(height=500, margin=dict(t=50, l=20, r=20, b=30))
st.plotly_chart(fig, use_container_width=True)