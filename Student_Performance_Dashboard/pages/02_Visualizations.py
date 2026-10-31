import streamlit as st
import plotly.express as px
from utils.helper import load_data, prepare_data, get_subject_columns

st.set_page_config(page_title="Visualizations", page_icon="📊", layout="wide")
st.title("📊 Student Visualizations")
data, _ = prepare_data(load_data())
subjects = get_subject_columns(data)

subject = st.selectbox("Choose a subject", subjects)
c1,c2 = st.columns(2)
with c1:
    fig = px.bar(data.sort_values(subject, ascending=False), x="Student", y=subject,
                 color=subject, title=f"{subject} marks by student", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
with c2:
    fig = px.histogram(data, x=subject, nbins=10, title=f"Distribution of {subject} marks")
    st.plotly_chart(fig, use_container_width=True)

c3,c4 = st.columns(2)
with c3:
    fig = px.scatter(data, x="Attendance", y="Average", color="Grade", hover_name="Student",
                     title="Attendance vs average marks")
    st.plotly_chart(fig, use_container_width=True)
with c4:
    subject_means = data[subjects].mean().rename_axis("Subject").reset_index(name="Average marks")
    fig = px.bar(subject_means, x="Subject", y="Average marks", color="Subject",
                 title="Average marks by subject", text_auto=".1f")
    st.plotly_chart(fig, use_container_width=True)

fig = px.box(data.melt(id_vars="Student", value_vars=subjects, var_name="Subject", value_name="Marks"),
             x="Subject", y="Marks", color="Subject", title="Subject-wise marks spread")
st.plotly_chart(fig, use_container_width=True)
