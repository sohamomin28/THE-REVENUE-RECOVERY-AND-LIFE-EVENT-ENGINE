import streamlit as st
import pandas as pd
import plotly.express as px

# Set Page Config for a professional look
st.set_page_config(page_title="Bank Executive Dashboard", layout="wide")

# Load your fixated data
df = pd.read_csv('bank_priority_hitlist.csv')

# --- THE SUNSET COLOR PALETTE ---
SUNSET_COLORS = ["#FF007F", "#FFD700", "#FF8C00", "#FF1493", "#FFFF00"]

# --- HUMAN LIFE EVENT MAPPING ---
# This maps technical actions to the underlying human life events
event_map = {
    "SALES: Mortgage Pre-Approval": "Home Buying",
    "SALES: FHSA Invite": "First Home Planning",
    "SALES: RESP & Insurance Review": "New Child or Family",
    "UPSELL: Student Credit Bundle": "Graduation or College",
    "RETENTION: Fintech Match Offer": "Fintech Competitor Risk",
    "RETENTION: Loyalty Bonus Offer": "General Churn Risk",
    "PREMIER: Wealth Management Invite": "High Wealth Gain"
}
df['Life_Event'] = df['recommended_action'].map(event_map)

st.title("Executive Strategy and Revenue Dashboard")
st.markdown("### Strategic Intelligence for Retention and Growth")

# --- STEP 2: REVENUE AT RISK GAUGE ---
total_risk_value = len(df[df['recommended_action'].str.contains("RETENTION")]) * 5000 

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Priority Leads", value=len(df))
with col2:
    st.metric(label="Revenue at Risk (Est.)", value=f"${total_risk_value:,}", delta="-12% vs last month")
with col3:
    st.metric(label="Avg Churn Probability", value=f"{df['churn_prob'].mean():.1%}")

st.divider()

# --- NEW: LIFE EVENT PIE CHART SECTION ---
st.subheader("Market Opportunity: Life Event Distribution")

event_counts = df['Life_Event'].value_counts().reset_index()
event_counts.columns = ['Event', 'Count']

# Create the Donut Chart with the Sunset theme
fig_pie = px.pie(
    event_counts, 
    values='Count', 
    names='Event', 
    hole=0.6,
    color_discrete_sequence=SUNSET_COLORS
)

# Clean formatting for a professional look
fig_pie.update_traces(textposition='inside', textinfo='percent+label')
fig_pie.update_layout(showlegend=False, margin=dict(t=20, b=20, l=0, r=0))

col_left, col_right = st.columns([2, 1])
with col_left:
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    st.write("### Strategy Summary")
    top_event = event_counts.iloc[0]['Event']
    st.write(f"The most frequent life event detected is **{top_event}**.")
    st.write("Current lead volume for top categories:")
    for i, row in event_counts.head(3).iterrows():
        st.write(f"- {row['Event']}: {row['Count']} customers")

st.divider()

# --- STEP 1: STRATEGIC DISTRIBUTION ---
st.subheader("Strategic Opportunity Breakdown")
fig = px.bar(df['recommended_action'].value_counts().reset_index(), 
             x='count', y='recommended_action', orientation='h',
             color='recommended_action', color_discrete_sequence=px.colors.sequential.Magma)
st.plotly_chart(fig, use_container_width=True)

# --- STEP 3: HIGH-VALUE LEAD LIST ---
st.subheader("Top 10 High-Value Targets (Immediate Action)")

top_leads = df.sort_values(by=['churn_prob', 'mortgage_prob'], ascending=False).head(10)

# Display table using the new Human Event column
st.table(top_leads[['user_id', 'Life_Event', 'churn_prob']])

st.success("Dashboard synced with latest Batch Intelligence Engine results.")