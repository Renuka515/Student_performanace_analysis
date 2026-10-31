import streamlit as st
import pandas as pd
from utils.helper import load_data, prepare_data, get_subject_columns

st.set_page_config(page_title="Student Performance Dashboard", page_icon="🎓", layout="wide")
st.title("🎓 Student Performance Dashboard")
st.caption("Explore student marks, attendance and academic performance.")

raw = load_data()
data, cleaning = prepare_data(raw)
subjects = get_subject_columns(data)

c1,c2,c3,c4 = st.columns(4)
c1.metric("Total students", len(data))
c2.metric("Class average", f"{data['Average'].mean():.1f}%")
c3.metric("Average attendance", f"{data['Attendance'].mean():.1f}%")
c4.metric("Class topper", data.loc[data["Average"].idxmax(), "Student"])

st.subheader("Class overview")
left,right = st.columns(2)
with left:
    st.write("**Top 5 performers**")
    st.dataframe(data.nlargest(5, "Average")[["Rank","Student","Average","Grade"]], hide_index=True, use_container_width=True)
with right:
    st.write("**Students requiring improvement (average below 60%)**")
    low = data[data["Average"] < 60][["Student","Average","Grade"]]
    st.dataframe(low if not low.empty else pd.DataFrame({"Message":["No students are below 60%."]}), hide_index=True, use_container_width=True)

st.subheader("Explore a student")
selected = st.selectbox("Select student", data["Student"].tolist())
student = data[data["Student"] == selected].iloc[0]
a,b,c = st.columns(3)
a.metric("Average marks", f"{student['Average']:.1f}%")
b.metric("Total marks", f"{student['Total Marks']:.0f}")
c.metric("Grade", student["Grade"])
st.write("**Subject marks**")
st.bar_chart(pd.DataFrame({"Marks":[student[s] for s in subjects]}, index=subjects))

with st.expander("Data cleaning summary"):
    st.write(cleaning)
    st.info("Zero scores are retained as actual recorded values and flagged for review. Missing numeric values are filled using the column median.")
