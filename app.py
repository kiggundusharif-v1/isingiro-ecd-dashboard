import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE SETUP
# =========================
st.set_page_config(page_title="Uganda ECD Dashboard", layout="wide")
st.title("🇺🇬 Isingiro ECD Dashboard (Uganda IECD Indicators)")

# =========================
# LOAD DATA (SAFE)
# =========================
df = pd.read_csv("Isingiro_ECD_cleaned.csv", encoding="latin1")
df.columns = df.columns.str.strip()

# =========================
# FUNCTION: SAFE COLUMN PICK
# =========================
def get_cols(keyword):
    return [c for c in df.columns if keyword in c.lower()]

# =========================
# IDENTIFY COLUMNS SAFELY
# =========================
baby_cols = get_cols("baby")
middle_cols = get_cols("middle")
top_cols = get_cols("top")
att_cols = get_cols("attend")
caregiver_cols = get_cols("caregiver")

# =========================
# COMBINE ONLY EXISTING COLUMNS
# =========================
all_numeric_cols = list(set(
    baby_cols + middle_cols + top_cols + att_cols + caregiver_cols
))

# keep only columns that actually exist (VERY IMPORTANT)
all_numeric_cols = [c for c in all_numeric_cols if c in df.columns]

# =========================
# CONVERT SAFELY (NO ERRORS)
# =========================
for col in all_numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# =========================
# CORE INDICATORS
# =========================
df["total_enrollment"] = df[baby_cols + middle_cols + top_cols].sum(axis=1, min_count=1)
df["total_attendance"] = df[att_cols].sum(axis=1, min_count=1)

df["attendance_rate"] = df["total_attendance"] / df["total_enrollment"].replace(0, pd.NA)

# caregiver ratio (safe)
if caregiver_cols:
    df["learner_caregiver_ratio"] = df["total_enrollment"] / df[caregiver_cols].sum(axis=1).replace(0, pd.NA)
else:
    df["learner_caregiver_ratio"] = None

# =========================
# YES/NO FUNCTION
# =========================
def yes_no_pct(col):
    if col in df.columns:
        return (df[col].astype(str).str.lower() == "yes").mean() * 100
    return 0

# =========================
# DASHBOARD HEADER KPIs
# =========================
st.header("📊 Executive Summary")

col1, col2, col3, col4 = st.columns(4)

# Enrollment by gender (safe fallback if columns exist)
boys_cols = [c for c in df.columns if "boy" in c.lower()]
girls_cols = [c for c in df.columns if "girl" in c.lower()]

boys_enroll = df[boys_cols].sum().sum() if boys_cols else 0
girls_enroll = df[girls_cols].sum().sum() if girls_cols else 0

# total enrollment
total_enrollment = df["total_enrollment"].sum()

# caregiver ratio (already computed earlier)
caregiver_ratio = df["learner_caregiver_ratio"].mean()

col1.metric("Total Centres", len(df))
col2.metric("Total Enrollment", int(total_enrollment))
col3.metric("Boys Enrollment", int(boys_enroll))
col4.metric("Girls Enrollment", int(girls_enroll))

st.divider()

st.metric(
    "Learner–Caregiver Ratio",
    f"{caregiver_ratio:.1f} : 1" if pd.notna(caregiver_ratio) else "N/A",
    help="Number of children per caregiver. Lower is better (ECD quality indicator)."
)

# =========================
# ACCESS & PARTICIPATION
# =========================
st.subheader("1️⃣ Access & Participation")

fig1 = px.bar(
    df,
    y=["total_enrollment", "total_attendance"],
    title="Enrollment vs Attendance"
)
st.plotly_chart(fig1, use_container_width=True)

# =========================
# QUALITY OF LEARNING
# =========================
st.subheader("2️⃣ Quality of Learning")

quality_cols = ["lesson_plan", "scheme_of_work", "learning_framework"]

quality_data = {
    "Indicator": [],
    "Coverage (%)": []
}

for c in quality_cols:
    if c in df.columns:
        quality_data["Indicator"].append(c.replace("_", " ").title())
        quality_data["Coverage (%)"].append(yes_no_pct(c))

fig2 = px.bar(quality_data, x="Indicator", y="Coverage (%)", color="Indicator")
st.plotly_chart(fig2, use_container_width=True)

# =========================
# CAREGIVERS
# =========================
st.subheader("3️⃣ Caregiver Capacity")

care_cols = ["trained", "qualification"]

care_data = {
    "Indicator": [],
    "Coverage (%)": []
}

for c in care_cols:
    if c in df.columns:
        care_data["Indicator"].append(c.title())
        care_data["Coverage (%)"].append(yes_no_pct(c))

fig3 = px.bar(care_data, x="Indicator", y="Coverage (%)", color="Indicator")
st.plotly_chart(fig3, use_container_width=True)

# =========================
# INCLUSION
# =========================
st.subheader("4️⃣ Inclusion")

inc_data = {
    "Category": [],
    "Total": []
}

for c in ["sne", "orphans", "refugees"]:
    if c in df.columns:
        inc_data["Category"].append(c.upper())
        inc_data["Total"].append(df[c].sum())

fig4 = px.pie(inc_data, names="Category", values="Total")
st.plotly_chart(fig4, use_container_width=True)

# =========================
# HEALTH & NUTRITION
# =========================
st.subheader("5️⃣ Health & Nutrition")

health_cols = ["feeding", "deworming"]

health_data = {
    "Service": [],
    "Coverage (%)": []
}

for c in health_cols:
    if c in df.columns:
        health_data["Service"].append(c.title())
        health_data["Coverage (%)"].append(yes_no_pct(c))

fig5 = px.bar(health_data, x="Service", y="Coverage (%)", color="Service")
st.plotly_chart(fig5, use_container_width=True)

# =========================
# GOVERNANCE
# =========================
st.subheader("6️⃣ Governance & Compliance")

gov_cols = ["cmc", "license_status"]

gov_data = {
    "Indicator": [],
    "Coverage (%)": []
}

for c in gov_cols:
    if c in df.columns:
        gov_data["Indicator"].append(c.upper())
        gov_data["Coverage (%)"].append(yes_no_pct(c))

fig6 = px.bar(gov_data, x="Indicator", y="Coverage (%)", color="Indicator")
st.plotly_chart(fig6, use_container_width=True)

# =========================
# RAW DATA
# =========================
with st.expander("🔍 View Raw Data"):
    st.dataframe(df)
