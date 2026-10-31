# Student Performance Dashboard

A beginner-friendly interactive dashboard built with Python, Streamlit, Pandas and Plotly.

## Features
- Student performance overview and KPI cards
- Student dropdown and individual subject marks
- Dataset preview, missing-value handling and cleaning summary
- Subject-wise bar charts, histograms, box plots and attendance scatter plot
- Descriptive statistics, rankings, correlation heatmap and IQR outlier summary
- Download processed data as CSV

## Project structure
```text
student-performance-dashboard/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── student_performance.csv
├── pages/
│   ├── 01_Dataset.py
│   ├── 02_Visualizations.py
│   └── 03_Statistics.py
├── utils/
│   └── helper.py
├── assets/
│   └── dashboard.png
└── notebooks/
    └── analysis.ipynb
```

## Run locally
1. Install Python 3.10 or later.
2. Open a terminal in this folder.
3. Create and activate a virtual environment (optional but recommended).
4. Install dependencies:
   `pip install -r requirements.txt`
5. Start the dashboard:
   `streamlit run app.py`

## Dataset and cleaning notes
The sample dataset contains 25 students and four subject scores plus attendance.
Missing numeric values are filled with the median of the corresponding column.
Recorded zero values are kept and counted in the cleaning summary so they can be reviewed rather than silently changed.

## Pages
- **Home:** KPIs, top performers and selected-student details.
- **Dataset:** raw data, data types, missing values, processed data and CSV download.
- **Visualizations:** subject charts, distribution, attendance comparison and box plot.
- **Statistics:** descriptive statistics, ranking, insights, correlation and outlier check.
