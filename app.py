import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE SETUP
# =========================
st.set_page_config(page_title="Isingiro ECD Report", layout="wide")

st.title("🇺🇬 Isingiro District ECD Report (IECD Dashboard 2022 Style)")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("Isingiro_ECD_cleaned.csv", encoding="latin1")
df.columns = df.columns.str.strip()

# =========================
# HELPERS
# =========================
def yes_no(col):
    if col in df.columns:
        return (df[col].astype(str).str.lower() == "yes").mean() * 100
    return 0

def sum_cols(keyword):
    cols = [c for c in df.columns if keyword in c.lower()]
    return df[cols].sum().sum() if cols else 0

# =========================
# CLEAN NUMERIC
# =========================
for c in df.columns:
    df[c] = pd.to_numeric(df[c], errors="ignore")

# =========================
# =========================
# 1. EXECUTIVE SUMMARY
# =========================
st.header("📊 Executive Summary")

col1, col2, col3, col4 = st.columns(4)

total_centres = len(df)
enrollment = sum_cols("enroll")

boys = sum_cols("boy")
girls = sum_cols("girl")

col1.metric("ECD Centres", total_centres)
col2.metric("Total Enrollment", int(enrollment))
col3.metric("Boys", int(boys))
col4.metric("Girls", int(girls))

st.divider()

# =========================
# 2. SNE ENROLMENT
# =========================
st.subheader("👶 SNE Enrolment")

sne_total = sum_cols("sne")

st.metric("Total SNE Learners", int(sne_total))

# =========================
# 3. ECD CENTRE STATUS
# =========================
st.subheader("🏫 Centre Status")

licensed = yes_no("license")
registered = yes_no("register")

status_df = pd.DataFrame({
    "Status": ["Licensed", "Registered"],
    "Coverage (%)": [licensed, registered]
})

fig1 = px.bar(status_df, x="Status", y="Coverage (%)", color="Status")
st.plotly_chart(fig1, use_container_width=True)

# =========================
# 4. IECD SERVICES
# =========================
st.subheader("🧼 IECD Services Coverage")

services = ["deworm", "vitamin", "feeding", "birth", "immun"]

service_data = {
    "Service": [],
    "Coverage (%)": []
}

for s in services:
    cols = [c for c in df.columns if s in c.lower()]
    if cols:
        pct = (df[cols[0]].astype(str).str.lower() == "yes").mean() * 100
        service_data["Service"].append(s.title())
        service_data["Coverage (%)"].append(pct)

fig2 = px.bar(service_data, x="Service", y="Coverage (%)", color="Service")
st.plotly_chart(fig2, use_container_width=True)

# =========================
# 5. CAREGIVERS
# =========================
st.subheader("👩‍🏫 Caregivers")

caregivers = sum_cols("caregiver")

st.metric("Total Caregivers", int(caregivers))

# =========================
# 6. LEARNING MATERIALS
# =========================
st.subheader("📚 Learning & Play Materials")

materials = yes_no("material")

st.metric("Centres with Materials (%)", f"{materials:.1f}%")

# =========================
# 7. INFRASTRUCTURE
# =========================
st.subheader("🏗 Infrastructure")

permanent = yes_no("permanent")
temporary = yes_no("temporary")

infra_df = pd.DataFrame({
    "Type": ["Permanent", "Temporary"],
    "Coverage (%)": [permanent, temporary]
})

fig3 = px.bar(infra_df, x="Type", y="Coverage (%)", color="Type")
st.plotly_chart(fig3, use_container_width=True)

# =========================
# 8. GOVERNANCE (CMC)
# =========================
st.subheader("🏛 Centre Management Committees")

cmc = yes_no("cmc")

st.metric("Centres with CMC (%)", f"{cmc:.1f}%")

# =========================
# 9. SCHOOL FEEDING
# =========================
st.subheader("🍲 School Feeding")

feeding = yes_no("feeding")

st.metric("Centres Providing Meals (%)", f"{feeding:.1f}%")

# =========================
# 10. WASH
# =========================
st.subheader("🚰 WASH")

water = yes_no("water")
handwash = yes_no("hand")

wash_df = pd.DataFrame({
    "Indicator": ["Water Access", "Handwashing"],
    "Coverage (%)": [water, handwash]
})

fig4 = px.bar(wash_df, x="Indicator", y="Coverage (%)", color="Indicator")
st.plotly_chart(fig4, use_container_width=True)

# =========================
# RAW DATA
# =========================
with st.expander("🔍 View Raw Data"):
    st.dataframe(df)
