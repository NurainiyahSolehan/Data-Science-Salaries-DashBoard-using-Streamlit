import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title='Data Science Salaries Dashboard',
    page_icon=':bar_chart:',
    layout='wide'
)

# Load dataset
df = pd.read_csv('Preprocessing.csv')

# Format angka agar lebih rapi tanpa koma untuk analisis
df['work_year'] = df['work_year'].astype(str)
df['salary_in_usd'] = df['salary_in_usd'].astype(float)  # Pastikan tipe data float

# Sidebar Filters
st.sidebar.header('Please Filter Here:')
year = st.sidebar.multiselect(
    "Select the Year:",
    options=df['work_year'].unique(),
    default=df['work_year'].unique(),
)

location = st.sidebar.multiselect(
    "Select the Location:",
    options=df['company_location'].unique(),
    default=df['company_location'].unique(),
)

# Filter the dataframe
df_selection = df[
    (df['work_year'].isin(year)) &
    (df['company_location'].isin(location))
]

# Main Page
st.title(":bar_chart: Data Science Salaries Dashboard")
st.markdown("##")

# TOP
total_employees = df_selection.shape[0]  
average_salary = round(df_selection['salary_in_usd'].mean(), 2) 

left_column, right_column = st.columns(2, gap = 'large')

with left_column:
    st.subheader("Total Employees")
    st.subheader(f"{total_employees:,}") 

with right_column:
    st.subheader("Average Salaries")
    st.subheader(f"US $ {average_salary:,}")

st.markdown("---")


if not df_selection.empty:
# Salaries by Job Categories
    salaries_job = df_selection.groupby('job_category')['salary_in_usd'].mean().reset_index()
    salaries_job.columns = ['Job Categories', 'Salaries']

    fig_salaries_job= px.bar(
        salaries_job,
        x="Salaries",
        y="Job Categories",
        orientation="h",
        color_discrete_sequence=["#D32F2F"],
        template="plotly_white",
    )

# Top 10 Jobs
    employees_count= df_selection.groupby('job_title').size().reset_index()
    employees_count.columns = ['Jobs', 'Employees']

    top_10_jobs = employees_count.sort_values(by='Employees', ascending=False).head(10)

    fig_top_10_jobs = px.bar(
        top_10_jobs,
        x="Jobs",
        y="Employees",
        color_discrete_sequence=["#D32F2F"],  # Warna merah lembut
        template="plotly_white",
    )

# Salaries by Experience Level
    salaries_experience = df_selection.groupby('experience_level')['salary_in_usd'].mean().reset_index()
    salaries_experience.columns = ['Experience Level', 'Salaries']
    salaries = salaries_experience.sort_values(by='Salaries', ascending=False)

    fig_salaries_experience = px.bar(
        salaries,
        x="Experience Level",
        y="Salaries",
        color_discrete_sequence=["#D32F2F"],  
        template="plotly_white",
    )

# Distribution of Experience Levels in Companies by Size
    job_count = df_selection.groupby(['company_size', 'experience_level']).size().reset_index(name='count')
    fig_company_experience = px.bar(
    job_count,
    x='company_size',
    y='count',
    color='experience_level',
    barmode='group', 
    labels={
        "company_size": "Company Size",
        "count": "Employees",
        "experience_level": "Experience Level"
    },
    color_discrete_sequence=["#FF9999", "#FF6666", "#FF3333", "#D32F2F"] 
)

# Distribution of Job Categories by Employment Type
    job_count = df_selection.groupby(['job_category', 'employment_type']).size().reset_index(name='count')
    fig_employment_type = px.bar(
    job_count,
    x='job_category',
    y='count',
    color='employment_type',
    barmode='group', 
    labels={
        "job_category": "Job Categories",
        "count": "Employees",
        "employment_type": "Employment Type"
    },
    color_discrete_sequence=["#FF9999", "#FF6666", "#FF3333", "#D32F2F"] 
)

#  Top 5 Remote Jobs
    remote_jobs = df_selection[df_selection['remote_ratio'] == 100]
    remote_jobs = remote_jobs['job_title'].value_counts().reset_index()
    remote_jobs.columns = ['Jobs', 'Employees']

    top_remote_locations = remote_jobs.head(5)

    fig_remote_locations = px.bar(
        top_remote_locations,
        x="Jobs",
        y="Employees",
        color_discrete_sequence=["#D32F2F"],  
        template="plotly_white",
    )


else:
    st.write("No data available for the selected filters.")

col1, col2 = st.columns(2)

# Grafik 1: Salaries by Job Categories
with col1:
    st.subheader("Salaries by Job Categories")
    st.plotly_chart(fig_salaries_job, use_container_width=True)

# Grafik 2: Top 10 Jobs by Emploment Ty
with col2:
    st.subheader("Salaries by Employment Level")
    st.plotly_chart(fig_salaries_experience, use_container_width=True)

col3, col4 = st.columns(2)

# Grafik 3: Distribution of Experience Levels in Companies by Size
with col3:
    st.subheader("Distribution of Job Categories by Employment Type")
    st.plotly_chart(fig_employment_type, use_container_width=True)

# Grafik 4: Distribution of Experience Levels in Companies by Size
with col4:
    st.subheader("Distribution of Experience Levels in Companies by Size")
    st.plotly_chart(fig_company_experience , use_container_width=True)

col5, col6 = st.columns(2)

# Grafik 5: Distribution of Experience Levels in Companies by Size
with col5:
    st.subheader("Top 10 Jobs by Employee Count")
    st.plotly_chart(fig_top_10_jobs, use_container_width=True)


# Grafik 6: Top 5 Remote Jobs
with col6:
    st.subheader("Top 5 Remote Jobs")
    st.plotly_chart(fig_remote_locations , use_container_width=True)

# Hide streamlit style
hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

