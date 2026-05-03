import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Isingiro ECD Dashboard")

# Load data
df = pd.read_csv("Isingiro_ECD_cleaned.csv")

# Basic metrics
enroll_cols = [c for c in df.columns if "enroll" in c]
att_cols = [c for c in df.columns if "attend" in c]

df["total_enrollment"] = df[enroll_cols].sum(axis=1)
df["total_attendance"] = df[att_cols].sum(axis=1)
df["attendance_rate"] = df["total_attendance"] / df["total_enrollment"]

# KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Centres", len(df))
c2.metric("Enrollment", int(df["total_enrollment"].sum()))
c3.metric("Attendance", int(df["total_attendance"].sum()))
c4.metric("Attendance Rate", f"{df['attendance_rate'].mean():.1%}")

# Enrollment chart
fig = px.histogram(df, x="total_enrollment", nbins=30, title="Enrollment Distribution")
st.plotly_chart(fig, use_container_width=True)

# Attendance chart
fig2 = px.box(df, y="attendance_rate", title="Attendance Rate")
fig2.update_yaxes(tickformat=".0%")
st.plotly_chart(fig2, use_container_width=True)

# Licensing
license_col = [c for c in df.columns if "licen" in c]
if license_col:
    lic = df[license_col[0]].value_counts().reset_index()
    lic.columns = ["Status", "Centres"]

    fig3 = px.bar(lic, x="Status", y="Centres", text="Centres")
    fig3.update_traces(textposition="outside")
    st.plotly_chart(fig3, use_container_width=True)

# Records example
record_cols = [c for c in df.columns if "register" in c]

data = []
for col in record_cols[:5]:
    pct = (df[col] == "Yes").mean()
    data.append({"Record": col, "Percent": pct})

rec_df = pd.DataFrame(data)

fig4 = px.bar(rec_df, x="Record", y="Percent", text="Percent")
fig4.update_traces(texttemplate="%{text:.1%}", textposition="outside")
fig4.update_yaxes(tickformat=".0%")
st.plotly_chart(fig4, use_container_width=True)