import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="US Credit Trends Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for compact layout
st.markdown("""
<style>
    .main > div {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        height: 80px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #262730;
        margin: 0;
    }
    .metric-label {
        font-size: 12px;
        color: #6c757d;
        margin: 0;
    }
    .chart-container {
        height: 250px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Load and clean data
@st.cache_data
def load_data():
    df = pd.read_csv("data/24Q4-CreditCardBalances.csv")
    
    # Clean monetary and percentage values
    def clean(value):
        if isinstance(value, str):
            return float(value.replace('$', '').replace('%', '').replace(',', '').strip())
        return value
    
    for col in df.columns:
        if col != 'YRQTR':
            df[col] = df[col].apply(clean)
    
    # Remove rows where YRQTR is NaN and convert to date
    df = df.dropna(subset=['YRQTR'])
    df = df[df['YRQTR'].str.match(r'\d{4}Q[1-4]')]
    df['date'] = pd.PeriodIndex(df['YRQTR'], freq='Q').to_timestamp()
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)
    
    return df

df = load_data()

# Header
st.markdown("""
<h1 style='text-align: center; color: #262730; margin-bottom: 20px; font-size: 28px;'>
📊 U.S. Credit Trends Dashboard (2012–2024)
</h1>
""", unsafe_allow_html=True)

# Top row - KPIs
st.markdown("### 🔍 Key Metrics")
kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5, kpi_col6 = st.columns(6)

with kpi_col1:
    latest_balance = df['Total Balances ($Billions)'].iloc[-1]
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-value">${latest_balance:,.0f}B</div>
        <div class="metric-label">Total Balances</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    util = df['Utilization (Active Accounts Only) (50th percentile)'].iloc[-1]
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-value">{util:.1f}%</div>
        <div class="metric-label">Utilization (P50)</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    score = df['Current Credit Score (50th percentile)'].iloc[-1]
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-value">{score:.0f}</div>
        <div class="metric-label">Credit Score (P50)</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col4:
    delinq_30 = df['30+ Days Past Due Rates: Accounts Based'].iloc[-1]
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-value">{delinq_30:.1f}%</div>
        <div class="metric-label">30+ Days Late</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col5:
    full_payment = df['Share of Accounts Making Full Balance Payment'].iloc[-1]
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-value">{full_payment:.1f}%</div>
        <div class="metric-label">Full Payments</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col6:
    min_payment = df['Share of Accounts Making the Minimum Payment'].iloc[-1]
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-value">{min_payment:.1f}%</div>
        <div class="metric-label">Min Payments</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Main dashboard - 2x3 grid
row1_col1, row1_col2, row1_col3 = st.columns(3)
row2_col1, row2_col2, row2_col3 = st.columns(3)

# Chart 1: Total Balances (compact)
with row1_col1:
    st.markdown("**💰 Total Balances ($B)**")
    fig1 = px.line(df, x=df.index, y='Total Balances ($Billions)')
    fig1.update_layout(
        height=250,
        margin=dict(l=30, r=10, t=20, b=30),
        showlegend=False,
        xaxis_title="",
        yaxis_title="",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    fig1.update_traces(line_color='#1f77b4', line_width=2)
    st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Credit Utilization
with row1_col2:
    st.markdown("**📊 Credit Utilization**")
    fig2 = px.line(
        df, x=df.index,
        y=['Utilization (Active Accounts Only) (50th percentile)',
           'Utilization (Active Accounts Only) (75th percentile)',
           'Utilization (Active Accounts Only) (90th percentile)']
    )
    fig2.update_layout(
        height=250,
        margin=dict(l=30, r=10, t=20, b=30),
        legend=dict(x=0, y=1, bgcolor='rgba(0,0,0,0)'),
        xaxis_title="",
        yaxis_title="",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    fig2.update_traces(line_width=2)
    st.plotly_chart(fig2, use_container_width=True)

# Chart 3: Credit Score Trend
with row1_col3:
    st.markdown("**🎯 Credit Score Trend**")
    fig3 = px.line(df, x=df.index, y='Current Credit Score (50th percentile)')
    fig3.update_layout(
        height=250,
        margin=dict(l=30, r=10, t=20, b=30),
        showlegend=False,
        xaxis_title="",
        yaxis_title="",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    fig3.update_traces(line_color='#2ca02c', line_width=2)
    st.plotly_chart(fig3, use_container_width=True)

# Chart 4: Delinquency Rates
with row2_col1:
    st.markdown("**⚠️ Delinquency Rates**")
    fig4 = px.line(
        df, x=df.index,
        y=['30+ Days Past Due Rates: Accounts Based',
           '60+ Days Past Due Rates: Accounts Based',
           '90+ Days Past Due Rates: Accounts Based']
    )
    fig4.update_layout(
        height=250,
        margin=dict(l=30, r=10, t=20, b=30),
        legend=dict(x=0, y=1, bgcolor='rgba(0,0,0,0)'),
        xaxis_title="",
        yaxis_title="",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    fig4.update_traces(line_width=2)
    st.plotly_chart(fig4, use_container_width=True)

# Chart 5: Payment Behavior
with row2_col2:
    st.markdown("**💳 Payment Behavior**")
    fig5 = px.line(
        df, x=df.index,
        y=['Share of Accounts Making the Minimum Payment',
           'Share of Accounts Making Greater Than the Minimum Payment but Less Than the Full Balance',
           'Share of Accounts Making Full Balance Payment']
    )
    fig5.update_layout(
        height=250,
        margin=dict(l=30, r=10, t=20, b=30),
        legend=dict(x=0, y=1, bgcolor='rgba(0,0,0,0)'),
        xaxis_title="",
        yaxis_title="",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    fig5.update_traces(line_width=2)
    st.plotly_chart(fig5, use_container_width=True)

# Chart 6: Combined Health Score (custom metric)
with row2_col3:
    st.markdown("**📈 Credit Health Overview**")
    
    # Create a combined view with key metrics
    fig6 = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add credit score on primary y-axis
    fig6.add_trace(
        go.Scatter(x=df.index, y=df['Current Credit Score (50th percentile)'], 
                  name="Credit Score", line=dict(color='#2ca02c', width=2)),
        secondary_y=False,
    )
    
    # Add delinquency rate on secondary y-axis
    fig6.add_trace(
        go.Scatter(x=df.index, y=df['30+ Days Past Due Rates: Accounts Based'], 
                  name="30+ Days Late (%)", line=dict(color='#d62728', width=2)),
        secondary_y=True,
    )
    
    fig6.update_layout(
        height=250,
        margin=dict(l=30, r=30, t=20, b=30),
        legend=dict(x=0, y=1, bgcolor='rgba(0,0,0,0)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    fig6.update_xaxes(title_text="")
    fig6.update_yaxes(title_text="Credit Score", secondary_y=False)
    fig6.update_yaxes(title_text="Delinquency %", secondary_y=True)
    
    st.plotly_chart(fig6, use_container_width=True)

# Footer with latest data info
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #6c757d; font-size: 12px;'>
📅 Latest Data: {df.index[-1].strftime('%Y Q%q')} | 
📊 Source: Federal Reserve Bank of Philadelphia | 
🔄 Updated: {pd.Timestamp.now().strftime('%Y-%m-%d')}
</div>
""", unsafe_allow_html=True)