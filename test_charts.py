# test_charts1.py modifications
import pandas as pd
import sqlalchemy
from sqlalchemy import text
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import math
import streamlit as st

postgresql_url = "postgresql://postgres:dell1234@localhost:5432/MIMIC-IV"
engine = sqlalchemy.create_engine(postgresql_url)

def is_patient_alive(subject_id, engine):
    try:
        subject_id_int = int(subject_id)
    except ValueError:
        return False, "Patient ID must be an integer"
    query = text("""
    SELECT 
    CASE
        WHEN a.hospital_expire_flag = 1 OR p.dod IS NOT NULL THEN 1
        ELSE 0
    END as patient_expired
FROM 
    admissions a
LEFT JOIN 
    patients p ON a.subject_id = p.subject_id
WHERE 
    a.subject_id = :subject_id
ORDER BY 
    a.admittime DESC
LIMIT 1;
    """)
    with engine.connect() as conn:  # Obtain a connection from the engine
        try:
            result = conn.execute(query, {"subject_id": subject_id_int}).fetchone()
            if result is not None:
                return result[0] == 0, "Patient has expired." if result[0] != 0 else "Patient is alive."
        except Exception as e:
            return False, f"An error occurred: {e}"

    return False, "No data available for this subject ID."

def process_patient_data(subject_id, engine):
    alive, message = is_patient_alive(subject_id, engine)
    if alive:
        df = fetch_data(subject_id, engine)
        if df is not None and not df.empty:
            fig = generate_chart_for_subject(df, subject_id)
            return message, fig
        else:
            return "No data available for the alive patient.", None
    else:
        return message, None


def fetch_data(subject_id, engine):
    try:
        subject_id_int = int(subject_id)
    except ValueError:
        raise ValueError("Patient ID must be an integer")

    # Use a parameterized query to prevent SQL injection
    query = text("""
WITH date_labeled_visits AS (
    SELECT 
        CAST(l.charttime AS DATE) AS date, 
        AVG(l.valuenum) AS average_valuenum,
        MIN(l.ref_range_lower) AS ref_range_lower, 
        MAX(l.ref_range_upper) AS ref_range_upper,
        dl.label,
        l.flag,
        l.valueuom as uom,
        ROW_NUMBER() OVER(PARTITION BY dl.label ORDER BY CAST(l.charttime AS DATE) DESC) AS visit_rank
    FROM 
        labevents l
    INNER JOIN 
        d_labitems dl ON l.itemid = dl.itemid
    WHERE 
        dl.label IN ('Bun', 'Hemoglobin', 'pH', 'Sodium', 'Potassium', 'WBC', 'Creatinine')
        AND l.subject_id = :subject_id
    GROUP BY 
        CAST(l.charttime AS DATE), 
        dl.label,l.flag, l.valueuom
)
SELECT 
    date,
    COALESCE(average_valuenum, 0) AS average_valuenum,
    label,
    ref_range_lower,
    ref_range_upper,
    uom
    
FROM 
    date_labeled_visits
WHERE 
    visit_rank <= 7
ORDER BY 
    date DESC, 
    label;""")
    try:
        df = pd.read_sql_query(query, engine, params={"subject_id": subject_id_int})
    except Exception as e:
        print(f"An error occurred when fetching data for subject_id {subject_id_int}: {e}")
        raise

    return df
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def generate_chart_for_subject(df, subject_id):
    # Correcting 'uom' to 'unit' as per previous context. If 'uom' is correct, change 'unit' back to 'uom'.
    unique_labels_units = df[['label', 'uom']].drop_duplicates().reset_index(drop=True)
    num_charts = len(unique_labels_units)
    cols_per_row = 3
    rows = math.ceil(num_charts / cols_per_row)

    subplot_width = 350  # Example width for each subplot
    subplot_height = 350  # Example height for each subplot
    total_width = subplot_width * cols_per_row  # Total width for all charts in a row

    # Creating subplot figure with calculated rows, columns, and custom titles
    fig = make_subplots(
        rows=rows, 
        cols=cols_per_row, 
        subplot_titles=[
            f"{row['label']} ({row['uom']})" for _, row in unique_labels_units.iterrows()
        ]
    )

    # Index for plotting in correct subplot
    index_for_plotting = 1  # Start with 1 for subplot indexing

    for _, row in unique_labels_units.iterrows():
        label = row['label']
        unit = row['uom']
        label_df = df[df['label'] == label]

        if not label_df.empty:
            ref_lower = label_df['ref_range_lower'].fillna(0).iloc[0]
            ref_upper = label_df['ref_range_upper'].fillna(0).iloc[0]

            # Calculate the row and column for the subplot
            row_num = (index_for_plotting - 1) // cols_per_row + 1
            col_num = (index_for_plotting - 1) % cols_per_row + 1

            # Adding the test values trace
            fig.add_trace(
                go.Scatter(
                    x=label_df['date'], 
                    y=label_df['average_valuenum'], 
                    mode='lines+markers', 
                    name=f"{label} ({unit})"
                ),
                row=row_num, col=col_num
            )

            # Adding reference range lines
            fig.add_trace(
                go.Scatter(
                    x=[min(label_df['date']), max(label_df['date'])], 
                    y=[ref_lower, ref_lower], 
                    mode='lines', 
                    name='Lower Ref Range', 
                    line=dict(color='green', dash='dash')
                ),
                row=row_num, col=col_num
            )

            fig.add_trace(
                go.Scatter(
                    x=[min(label_df['date']), max(label_df['date'])], 
                    y=[ref_upper, ref_upper], 
                    mode='lines', 
                    name='Upper Ref Range', 
                    line=dict(color='green', dash='dash')
                ),
                row=row_num, col=col_num
            )

            index_for_plotting += 1  # Increment index for next subplot

    # Updating the layout to fit the plots
    fig.update_layout(
        height=subplot_height * rows, 
        width=total_width,
        showlegend=False  # Toggle legend visibility as needed
    )

    return fig
