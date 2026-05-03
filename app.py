import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Uganda ECD Dashboard", layout="wide")

st.title("🇺🇬 Isingiro ECD Dashboard - Uganda IECD Indicators")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("Isingiro_ECD_cleaned.csv", encoding="latin1")
df.columns = df.columns.str.strip()

# =========================
# CLEAN NUMERIC DATA
# =========================
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="ignore")

# =========================
# BASIC ACCESS INDICATORS
# =========================
baby_cols = [c for c in df.columns if "baby" in c.lower()]
middle_cols = [c for c in df.columns if "middle" in c.lower()]
top_cols = [c for c in df.columns if "top" in c.lower()]
att_cols = [c for c in df.columns if "attend" in c.lower()]
caregiver_cols = [c for c in df.columns if "caregiver" in c.lower()]

df[baby_cols + middle_cols + top_cols + att_cols + caregiver_cols] = df[
    baby_cols + middle_cols + top_cols + att_cols + caregiver_cols
].apply(pd.to_numeric, errors="coerce")

df["total_enrollment"] = df[baby_cols + middle_cols + top_cols].sum(axis=1)
df["total_attendance"] = df[att_cols].sum(axis=1)
df["attendance_rate"] = df["total_attendance"] / df["total_enrollment"].replace(0, pd.NA)

df["learner_caregiver_ratio"] = df["total_enrollment"] / df[caregiver_cols].sum(axis=1).replace(0, pd.NA)

# =========================
# YES/NO HELPER FUNCTION
# =========================
def yes_no_pct(col):
    if col in df.columns:
        return (df[col].astype(str).str.lower() == "yes").mean() * 100
    return 0

# =========================
# KPI SECTION (EXECUTIVE SUMMARY)
# =========================
st.header("📊 Executive Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Centres", len(df))
col2.metric("Total Enrollment", int(df["total_enrollment"].sum()))
col3.metric("Attendance Rate", f"{df['attendance_rate'].mean() * 100:.1f}%")
col4.metric("Caregiver Ratio", f"{df['learner_caregiver_ratio'].mean():.1f}")

st.divider()

# =========================
# 1. ACCESS & PARTICIPATION
# =========================
st.subheader("1️⃣ Access & Participation")

st.write("Enrollment vs Attendance")

fig1 = px.bar(
    df,
    y=["total_enrollment", "total_attendance"],
    title="Enrollment vs Attendance",
    barmode="group"
)
st.plotly_chart(fig1, use_container_width=True)

# =========================
# 2. QUALITY OF LEARNING
# =========================
st.subheader("2️⃣ Quality of Learning")

lesson_pct = yes_no_pct("lesson_plan")
scheme_pct = yes_no_pct("scheme_of_work")
framework_pct = yes_no_pct("learning_framework")

quality_df = pd.DataFrame({
    "Indicator": ["Lesson Plans", "Schemes of Work", "Learning Framework"],
    "Coverage (%)": [lesson_pct, scheme_pct, framework_pct]
})

fig2 = px.bar(quality_df, x="Indicator", y="Coverage (%)", color="Indicator")
st.plotly_chart(fig2, use_container_width=True)

# =========================
# 3. CAREGIVER CAPACITY
# =========================
st.subheader("3️⃣ Caregiver Capacity")

trained_pct = yes_no_pct("trained")
qualified_pct = yes_no_pct("qualification")

care_df = pd.DataFrame({
    "Indicator": ["Trained", "Qualified"],
    "Percentage": [trained_pct, qualified_pct]
})

fig3 = px.bar(care_df, x="Indicator", y="Percentage", color="Indicator")
st.plotly_chart(fig3, use_container_width=True)

# =========================
# 4. INCLUSION
# =========================
st.subheader("4️⃣ Inclusion")

sne = df["sne"].sum() if "sne" in df.columns else 0
orphans = df["orphans"].sum() if "orphans" in df.columns else 0
refugees = df["refugees"].sum() if "refugees" in df.columns else 0

inc_df = pd.DataFrame({
    "Category": ["SNE", "Orphans", "Refugees"],
    "Total": [sne, orphans, refugees]
})

fig4 = px.pie(inc_df, names="Category", values="Total")
st.plotly_chart(fig4, use_container_width=True)

# =========================
# 5. HEALTH & NUTRITION
# =========================
st.subheader("5️⃣ Health & Nutrition (IECD Services)")

feeding_pct = yes_no_pct("feeding")
deworming_pct = yes_no_pct("deworming")

health_df = pd.DataFrame({
    "Service": ["Feeding", "Deworming"],
    "Coverage (%)": [feeding_pct, deworming_pct]
})

fig5 = px.bar(health_df, x="Service", y="Coverage (%)", color="Service")
st.plotly_chart(fig5, use_container_width=True)

# =========================
# 6. WASH
# =========================
st.subheader("6️⃣ WASH Indicators")

wash_cols = ["water_source", "handwashing", "toilet"]
wash_available = [c for c in wash_cols if c in df.columns]

if wash_available:
    wash_df = df[wash_available].apply(lambda x: x.astype(str).str.lower().eq("yes").mean() * 100)

    fig6 = px.bar(
        x=wash_df.index,
        y=wash_df.values,
        labels={"x": "Indicator", "y": "Coverage (%)"},
        title="WASH Coverage"
    )
    st.plotly_chart(fig6, use_container_width=True)

# =========================
# 7. GOVERNANCE & COMPLIANCE
# =========================
st.subheader("7️⃣ Governance & Compliance")

cmc_pct = yes_no_pct("cmc")
licensed_pct = yes_no_pct("license_status")

gov_df = pd.DataFrame({
    "Indicator": ["CMC Available", "Licensed"],
    "Percentage": [cmc_pct, licensed_pct]
})

fig7 = px.bar(gov_df, x="Indicator", y="Percentage", color="Indicator")
st.plotly_chart(fig7, use_container_width=True)

# =========================
# RAW DATA
# =========================
with st.expander("🔍 View Raw Data"):
    st.dataframe(df)
