import streamlit as st
import pandas as pd
from utils.helper import load_data, prepare_data, get_subject_columns

st.set_page_config(page_title="Dataset", page_icon="📄", layout="wide")
st.title("📄 Dataset & Data Cleaning")
raw = load_data()
data, summary = prepare_data(raw)

st.subheader("Original dataset")
st.dataframe(raw, use_container_width=True)
st.subheader("Dataset information")
info = pd.DataFrame({"Column": raw.columns, "Data type": [str(x) for x in raw.dtypes], "Missing values": [int(raw[c].isna().sum()) for c in raw.columns]})
st.dataframe(info, hide_index=True, use_container_width=True)

st.subheader("Cleaning summary")
cols = st.columns(len(summary))
for col, (label, value) in zip(cols, summary.items()):
    col.metric(label, value)

st.subheader("Processed dataset")
st.dataframe(data, use_container_width=True)
st.download_button("⬇️ Download processed CSV", data.to_csv(index=False).encode("utf-8"),
                   file_name="processed_student_performance.csv", mime="text/csv")
