import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Isingiro ECD Dashboard", layout="wide")

st.title("🇺🇬 Isingiro District ECD Dashboard (IECD Report Style)")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("Isingiro_ECD_cleaned.csv", encoding="latin1")
df.columns = df.columns.str.strip()

# =========================
# SAFE NUMERIC CONVERSION
# =========================
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# =========================
# HELPER FUNCTIONS (SAFE)
# =========================
def sum_keyword(keyword):
    cols = [c for c in df.columns if keyword in c.lower()]
    if not cols:
        return 0

    temp = df[cols].copy()
    temp = temp.apply(pd.to_numeric, errors="coerce")

    return temp.fillna(0).sum().sum()

def yes_no_pct(keyword):
    cols = [c for c in df.columns if keyword in c.lower()]
    if not cols:
        return 0

    col = cols[0]
    return (df[col].astype(str).str.lower() == "yes").mean() * 100

# =========================
# CORE INDICATORS
# =========================
total_enrollment = sum_keyword("enroll")
boys = sum_keyword("boy")
girls = sum_keyword("girl")
sne = sum_keyword("sne")
caregivers = sum_keyword("caregiver")

df["total_enrollment"] = sum_keyword("enroll")
df["total_attendance"] = sum_keyword("attend")

df["attendance_rate"] = df["total_attendance"] / df["total_enrollment"].replace(0, pd.NA)

# =========================
# EXECUTIVE SUMMARY
# =========================
st.header("📊 Executive Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("ECD Centres", len(df))
col2.metric("Total Enrollment", int(total_enrollment))
col3.metric("Boys Enrollment", int(boys))
col4.metric("Girls Enrollment", int(girls))

st.divider()

col5, col6 = st.columns(2)

col5.metric("SNE Learners", int(sne))
col6.metric("Caregivers", int(caregivers))

st.divider()

# =========================
# 1. ACCESS & PARTICIPATION
# =========================
st.subheader("1️⃣ Access & Participation")

fig1 = px.bar(
    df,
    y=["total_enrollment", "total_attendance"],
    title="Enrollment vs Attendance"
)
st.plotly_chart(fig1, use_container_width=True)

# =========================
# 2. QUALITY OF LEARNING
# =========================
st.subheader("2️⃣ Quality of Learning")

quality_items = ["lesson", "scheme", "framework"]

quality_data = {"Indicator": [], "Coverage (%)": []}

for item in quality_items:
    pct = yes_no_pct(item)
    if pct > 0:
        quality_data["Indicator"].append(item.title())
        quality_data["Coverage (%)"].append(pct)

if quality_data["Indicator"]:
    fig2 = px.bar(quality_data, x="Indicator", y="Coverage (%)", color="Indicator")
    st.plotly_chart(fig2, use_container_width=True)

# =========================
# 3️⃣ IECD SERVICES
# =========================
st.subheader("3️⃣ IECD Services")

services = ["deworm", "vitamin", "feeding", "birth", "immun"]

service_data = {"Service": [], "Coverage (%)": []}

for s in services:
    pct = yes_no_pct(s)
    if pct > 0:
        service_data["Service"].append(s.title())
        service_data["Coverage (%)"].append(pct)

if service_data["Service"]:
    fig3 = px.bar(service_data, x="Service", y="Coverage (%)", color="Service")
    st.plotly_chart(fig3, use_container_width=True)

# =========================
# 4️⃣ INCLUSION
# =========================
st.subheader("4️⃣ Inclusion")

inc_data = {"Category": [], "Total": []}

for c in ["sne", "orphans", "refugees"]:
    cols = [x for x in df.columns if c in x.lower()]
    if cols:
        inc_data["Category"].append(c.upper())
        inc_data["Total"].append(df[cols].fillna(0).sum().sum())

if inc_data["Category"]:
    fig4 = px.pie(inc_data, names="Category", values="Total")
    st.plotly_chart(fig4, use_container_width=True)

# =========================
# 5️⃣ INFRASTRUCTURE
# =========================
st.subheader("5️⃣ Infrastructure")

infra_items = ["permanent", "temporary"]

infra_data = {"Type": [], "Coverage (%)": []}

for i in infra_items:
    pct = yes_no_pct(i)
    if pct > 0:
        infra_data["Type"].append(i.title())
        infra_data["Coverage (%)"].append(pct)

if infra_data["Type"]:
    fig5 = px.bar(infra_data, x="Type", y="Coverage (%)", color="Type")
    st.plotly_chart(fig5, use_container_width=True)

# =========================
# 6️⃣ GOVERNANCE
# =========================
st.subheader("6️⃣ Governance")

gov_items = ["cmc", "license"]

gov_data = {"Indicator": [], "Coverage (%)": []}

for g in gov_items:
    pct = yes_no_pct(g)
    if pct > 0:
        gov_data["Indicator"].append(g.upper())
        gov_data["Coverage (%)"].append(pct)

if gov_data["Indicator"]:
    fig6 = px.bar(gov_data, x="Indicator", y="Coverage (%)", color="Indicator")
    st.plotly_chart(fig6, use_container_width=True)

# =========================
# RAW DATA
# =========================
with st.expander("🔍 View Raw Data"):
    st.dataframe(df)
