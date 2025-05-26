import streamlit as st 
import pandas as pd 
import plotly.express as px


# Page configuration

st.set_page_config(page_title="US Credit Trends Dashboard", layout="wide")

# Custom CSS for styled KPI cards

st.markdown(""" <style> .kpi-card { padding: 1.5rem; background-color: #f9f9f9; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1.5rem; } .kpi-title { font-size: 1.1rem; color: #555; } .kpi-value { font-size: 2rem; font-weight: bold; color: #111; } </style> """, unsafe_allow_html=True)

# Title

st.title("\U0001F4CA U.S. Credit Trends Dashboard (2012–2024)") st.markdown("Data: Federal Reserve Bank of Philadelphia")

# Load data

df = pd.read_csv("data/24Q4-CreditCardBalances.csv")
 

def clean(value): if isinstance(value, str): return float(value.replace('$', '').replace('%', '').replace(',', '').strip()) return value

for col in df.columns: if col != 'YRQTR': df[col] = df[col].apply(clean)

df = df.dropna(subset=['YRQTR']) df = df[df['YRQTR'].str.match(r'\d{4}Q[1-4]')] df['date'] = pd.PeriodIndex(df['YRQTR'], freq='Q').to_timestamp() df.set_index('date', inplace=True) df.sort_index(inplace=True)

# KPI Cards

st.markdown("### \U0001F50D Key Indicators") kpi1, kpi2, kpi3 = st.columns(3)

with kpi1: st.markdown(f""" <div class="kpi-card"> <div class="kpi-title">Total Balances</div> <div class="kpi-value">${df['Total Balances ($Billions)'].iloc[-1]:,.0f}B</div> </div> """, unsafe_allow_html=True)

with kpi2: util = df['Utilization (Active Accounts Only) (90th percentile)'] st.markdown(f""" <div class="kpi-card"> <div class="kpi-title">Utilization (P90)</div> <div class="kpi-value">{util.iloc[-1]:.2f}%</div> </div> """, unsafe_allow_html=True)

with kpi3: score = df['Current Credit Score (50th percentile)'] st.markdown(f""" <div class="kpi-card"> <div class="kpi-title">Median Credit Score</div> <div class="kpi-value">{score.iloc[-1]:.0f}</div> </div> """, unsafe_allow_html=True)

st.divider()

# Charts row 1

col1, col2 = st.columns(2)

with col1: fig1 = px.line(df, x=df.index, y='Total Balances ($Billions)', title="\U0001F4C8 Total Credit Card Balances Over Time") fig1.update_layout(height=400, margin=dict(t=50, l=20, r=20, b=30)) st.plotly_chart(fig1, use_container_width=True)

with col2: fig2 = px.line( df, x=df.index, y=[ 'Utilization (Active Accounts Only) (50th percentile)', 'Utilization (Active Accounts Only) (75th percentile)', 'Utilization (Active Accounts Only) (90th percentile)' ], labels={'value': 'Utilization (%)', 'variable': 'Percentile'}, title="\U0001F4CA Credit Utilization Rates (P50, P75, P90)" ) fig2.update_layout(height=400, margin=dict(t=50, l=20, r=20, b=30)) st.plotly_chart(fig2, use_container_width=True)

# Charts row 2

col3, col4 = st.columns(2)

with col3: fig3 = px.line(df, x=df.index, y='Current Credit Score (50th percentile)', title="\U0001F9E0 Median Credit Score Over Time") fig3.update_layout(height=400, margin=dict(t=50, l=20, r=20, b=30)) st.plotly_chart(fig3, use_container_width=True)

with col4: fig4 = px.line( df, x=df.index, y=[ '30+ Days Past Due Rates: Accounts Based', '60+ Days Past Due Rates: Accounts Based', '90+ Days Past Due Rates: Accounts Based' ], labels={'value': 'Delinquency Rate (%)', 'variable': 'Days Late'}, title="\u26A0\uFE0F Delinquency Rates Over Time" ) fig4.update_layout(height=400, margin=dict(t=50, l=20, r=20, b=30)) st.plotly_chart(fig4, use_container_width=True)

# Payment Behavior

st.markdown("### \U0001F4B5 Payment Behavior Over Time") fig5 = px.line( df, x=df.index, y=[ 'Share of Accounts Making the Minimum Payment', 'Share of Accounts Making Greater Than the Minimum Payment but Less Than the Full Balance', 'Share of Accounts Making Full Balance Payment' ], labels={'value': 'Share of Accounts (%)', 'variable': 'Payment Behavior'}, title="Trends in Credit Card Repayment" ) fig5.update_layout(height=500, margin=dict(t=50, l=20, r=20, b=30)) st.plotly_chart(fig5, use_container_width=True)

