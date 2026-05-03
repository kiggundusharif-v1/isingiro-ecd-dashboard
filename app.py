import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Uganda ECD Dashboard", layout="wide")

st.title("🇺🇬 Uganda Early Childhood Development (ECD) Dashboard")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("Isingiro_ECD_cleaned.csv", encoding="latin1")

# =========================
# CLEAN COLUMN NAMES
# =========================
df.columns = df.columns.str.strip()

# =========================
# IDENTIFY COLUMNS
# =========================
enroll_cols = [c for c in df.columns if "enroll" in c.lower()]
att_cols = [c for c in df.columns if "attend" in c.lower()]

# =========================
# CONVERT TO NUMERIC SAFELY
# =========================
df[enroll_cols] = df[enroll_cols].apply(pd.to_numeric, errors="coerce")
df[att_cols] = df[att_cols].apply(pd.to_numeric, errors="coerce")

# =========================
# BASIC INDICATORS
# =========================
df["total_enrollment"] = df[enroll_cols].sum(axis=1)
df["total_attendance"] = df[att_cols].sum(axis=1)
df["attendance_rate"] = df["total_attendance"] / df["total_enrollment"].replace(0, pd.NA)

# =========================
# ECD DOMAIN INDICATORS
# =========================
health_cols = [c for c in df.columns if "health" in c.lower()]
nutrition_cols = [c for c in df.columns if "nutrition" in c.lower()]
learning_cols = [c for c in df.columns if "learn" in c.lower() or "literacy" in c.lower()]
protection_cols = [c for c in df.columns if "protect" in c.lower()]

df[health_cols] = df[health_cols].apply(pd.to_numeric, errors="coerce")
df[nutrition_cols] = df[nutrition_cols].apply(pd.to_numeric, errors="coerce")
df[learning_cols] = df[learning_cols].apply(pd.to_numeric, errors="coerce")
df[protection_cols] = df[protection_cols].apply(pd.to_numeric, errors="coerce")

df["health_score"] = df[health_cols].mean(axis=1) if health_cols else 0
df["nutrition_score"] = df[nutrition_cols].mean(axis=1) if nutrition_cols else 0
df["learning_score"] = df[learning_cols].mean(axis=1) if learning_cols else 0
df["protection_score"] = df[protection_cols].mean(axis=1) if protection_cols else 0

# =========================
# DASHBOARD METRICS
# =========================
st.subheader("📊 Key ECD Indicators")

col1, col2, col3 = st.columns(3)

col1.metric("Total Enrollment", int(df["total_enrollment"].sum()))
col2.metric("Total Attendance", int(df["total_attendance"].sum()))
col3.metric("Avg Attendance Rate", f"{df['attendance_rate'].mean() * 100:.2f}%")

# =========================
# DOMAIN PERFORMANCE
# =========================
st.subheader("🧠 ECD Development Domains")

domain_df = df[["health_score", "nutrition_score", "learning_score", "protection_score"]].mean().reset_index()
domain_df.columns = ["Domain", "Score"]

fig = px.bar(domain_df, x="Domain", y="Score", title="ECD Domain Performance")
st.plotly_chart(fig, use_container_width=True)

# =========================
# ATTENDANCE DISTRIBUTION
# =========================
st.subheader("📈 Attendance Rate Distribution")

fig2 = px.histogram(df, x="attendance_rate", nbins=20, title="Attendance Rate Distribution")
st.plotly_chart(fig2, use_container_width=True)

# =========================
# RAW DATA VIEW
# =========================
with st.expander("🔍 View Raw Data"):
    st.dataframe(df)
