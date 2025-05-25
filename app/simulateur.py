import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="US Credit Trends Dashboard",
    layout="wide"
)

st.title("📊 U.S. Credit Trends Dashboard (2012–2024)")
st.markdown("Built with data from the Federal Reserve Bank of Philadelphia – Aggregated quarterly credit card metrics.")

# Load and clean data
df = pd.read_csv("/mount/src/credit-scoring-federal-reserve/data/24Q4-CreditCardBalances.csv")

# Clean monetary and percentage values
def clean(value):
    if isinstance(value, str):
        return float(value.replace('$', '').replace('%', '').replace(',', '').strip())
    return value

for col in df.columns:
    if col != 'YRQTR':
        df[col] = df[col].apply(clean)

# Remove rows where YRQTR is NaN
df = df.dropna(subset=['YRQTR'])

# Convert YRQTR to date
df = df[df['YRQTR'].str.match(r'\d{4}Q[1-4]')]
df['date'] = pd.PeriodIndex(df['YRQTR'], freq='Q').to_timestamp()
df.set_index('date', inplace=True)
df.sort_index(inplace=True)

# ---------- KPIs section ----------
st.markdown("### 🔍 Key Credit Indicators")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Latest Total Balances ($B)", f"${df['Total Balances ($Billions)'].iloc[-1]:,.2f}")

with col2:
    util = df['Utilization (Active Accounts Only) (50th percentile)']
    delta_util = util.iloc[-1] - util.iloc[-2]
    st.metric("Utilization Rate (P50)", f"{util.iloc[-1]:.2f}%", delta=f"{delta_util:.2f}%")

with col3:
    score = df['Current Credit Score (50th percentile)']
    st.metric("Median Credit Score", f"{score.iloc[-1]:.0f}")

st.markdown("---")

# ---------- Layout with full-width charts ----------
# Chart 1: Total Balances
fig1 = px.line(df, x=df.index, y='Total Balances ($Billions)', title="Total Credit Card Balances Over Time")
fig1.update_layout(margin=dict(t=40, b=10), height=400)
st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Utilization
st.markdown("### 🧮 Credit Utilization Rates (P50, P75, P90)")
fig2 = px.line(
    df,
    x=df.index,
    y=[
        'Utilization (Active Accounts Only) (50th percentile)',
        'Utilization (Active Accounts Only) (75th percentile)',
        'Utilization (Active Accounts Only) (90th percentile)'
    ],
    labels={'value': 'Utilization (%)', 'variable': 'Percentile'},
    title="Credit Utilization Rates Over Time"
)
fig2.update_layout(margin=dict(t=40, b=10), height=400)
st.plotly_chart(fig2, use_container_width=True)

# Chart 3: Credit Score
st.markdown("### 🧠 Median Credit Score")
fig3 = px.line(df, x=df.index, y='Current Credit Score (50th percentile)', title="Median Credit Score Over Time")
fig3.update_layout(margin=dict(t=40, b=10), height=400)
st.plotly_chart(fig3, use_container_width=True)

# Chart 4: Delinquency
st.markdown("### ⚠️ Delinquency Rates (30+, 60+, 90+ Days)")
fig4 = px.line(
    df,
    x=df.index,
    y=[
        '30+ Days Past Due Rates: Accounts Based',
        '60+ Days Past Due Rates: Accounts Based',
        '90+ Days Past Due Rates: Accounts Based'
    ],
    labels={'value': 'Delinquency Rate (%)', 'variable': 'Days Late'},
    title="Delinquency Rates Over Time"
)
fig4.update_layout(margin=dict(t=40, b=10), height=400)
st.plotly_chart(fig4, use_container_width=True)

# Chart 5: Payment Behavior
st.markdown("### 💵 Payment Behavior")
fig5 = px.line(
    df,
    x=df.index,
    y=[
        'Share of Accounts Making the Minimum Payment',
        'Share of Accounts Making Greater Than the Minimum Payment but Less Than the Full Balance',
        'Share of Accounts Making Full Balance Payment'
    ],
    labels={'value': 'Share of Accounts (%)', 'variable': 'Payment Behavior'},
    title="Trends in Payment Behavior"
)
fig5.update_layout(margin=dict(t=40, b=10), height=400)
st.plotly_chart(fig5, use_container_width=True)
