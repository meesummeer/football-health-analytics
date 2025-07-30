import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIG & LOGO ---
st.set_page_config(
    page_title="Football Health Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)
# If you have a logo.png, upload to your GitHub repo and uncomment below
# st.sidebar.image("logo.png", width=180)
st.sidebar.markdown("## **CyberHealth Solutions**")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv("football_health_dashboard_data.csv")
    return df

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filters")
position = st.sidebar.selectbox("Select Position", ["All"] + sorted(df["position"].unique().tolist()))
risk_filter = st.sidebar.checkbox("Show only players with Injury Risk > 70%")
compliance_filter = st.sidebar.checkbox("Show only Non-Compliant players")

filtered_df = df.copy()
if position != "All":
    filtered_df = filtered_df[filtered_df["position"] == position]
if risk_filter:
    filtered_df = filtered_df[filtered_df["injury_risk"] > 70]
if compliance_filter:
    filtered_df = filtered_df[filtered_df["compliance_status"] == "Non-Compliant"]

# --- MAIN CONTENT ---
st.markdown(
    """
    <h1 style='text-align: center; color: white;'>⚽ Football Health Analytics Dashboard</h1>
    <h3 style='text-align: center; color: #e06666;'>Visual Insights</h3>
    """, unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Players", len(filtered_df))
with col2:
    st.metric("Avg. Injury Risk (%)", f"{filtered_df['injury_risk'].mean():.2f}" if len(filtered_df) > 0 else "0")
with col3:
    st.metric("% Cleared for Play", f"{100 * (filtered_df['cleared_for_play'] == 'Yes').mean():.1f}" if len(filtered_df) > 0 else "0")
with col4:
    st.metric("% Compliance Rate", f"{100 * (filtered_df['compliance_status'] == 'Compliant').mean():.1f}" if len(filtered_df) > 0 else "0")

st.markdown("---")

# --- Compliance Pie Chart ---
st.subheader("Compliance Status Distribution")
if len(filtered_df) > 0:
    pie = px.pie(filtered_df, names="compliance_status", hole=0.3,
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(pie, use_container_width=True)
else:
    st.info("No data to display.")

# --- Training Load vs Recovery Score ---
st.subheader("Training Load vs Recovery Score")
if len(filtered_df) > 0:
    melt_df = filtered_df.melt(id_vars=["player_name"], value_vars=["training_load", "recovery_score"], var_name="variable", value_name="score")
    bar = px.bar(melt_df, x="player_name", y="score", color="variable", barmode="group", height=400)
    st.plotly_chart(bar, use_container_width=True)
else:
    st.info("No data to display.")

# --- Sorted Injury Risk Heatmap ---
st.subheader("Top 10 Injury Risk Heatmap")
if len(filtered_df) > 0:
    top_risk = filtered_df.sort_values("injury_risk", ascending=False).head(10)
    heatmap = px.density_heatmap(top_risk, x="player_name", y="injury_risk",
                                 color_continuous_scale="Reds", nbinsx=10, height=350)
    st.plotly_chart(heatmap, use_container_width=True)
else:
    st.info("No data to display.")

# --- Summary Table: Sorted by Injury Risk ---
st.markdown("## 📊 Player Data (sorted by Injury Risk)")
if len(filtered_df) > 0:
    st.dataframe(filtered_df.sort_values("injury_risk", ascending=False).reset_index(drop=True))
else:
    st.info("No data to display.")

# --- Download CSV ---
st.download_button(
    label="Download current data as CSV",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name='filtered_players.csv',
    mime='text/csv'
)

# --- Footer ---
st.markdown(
    "<hr><center style='color: gray;'>Built by Meesum Mir · CyberHealth Solutions · FIFA Football Medicine Diploma</center>",
    unsafe_allow_html=True,
)
