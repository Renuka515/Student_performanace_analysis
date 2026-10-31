import streamlit as st
import plotly.express as px
from utils.helper import load_data, prepare_data, get_subject_columns, get_outlier_summary

st.set_page_config(page_title="Statistics", page_icon="📈", layout="wide")
st.title("📈 Statistics & Performance Insights")
data, cleaning = prepare_data(load_data())
subjects = get_subject_columns(data)

st.subheader("Descriptive statistics")
st.dataframe(data[subjects + ["Attendance","Average","Total Marks"]].describe().round(2), use_container_width=True)

st.subheader("Student ranking")
st.dataframe(data[["Rank","Student","Average","Attendance","Grade"]].sort_values("Rank"),
             hide_index=True, use_container_width=True)

left,right = st.columns(2)
with left:
    st.write("**Bottom 5 performers**")
    st.dataframe(data.nsmallest(5,"Average")[["Student","Average","Grade"]], hide_index=True)
with right:
    st.write("**Performance insights**")
    st.metric("Students above 85%", int((data["Average"] > 85).sum()))
    st.metric("Students below 60%", int((data["Average"] < 60).sum()))
    st.metric("Perfect attendance", int((data["Attendance"] == 100).sum()))

st.subheader("Correlation")
corr = data[subjects + ["Attendance","Average"]].corr().round(2)
fig = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu", zmin=-1, zmax=1,
                title="Correlation heatmap")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Outlier check (IQR method)")
st.write(get_outlier_summary(data, subjects))
