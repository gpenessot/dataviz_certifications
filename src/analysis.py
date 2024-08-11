import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def extract_year(date_string):
    """
    Extract the year from a date string in the format dd/mm/yyyy.
    
    Args:
        date_string (str): Date string in the format dd/mm/yyyy.
    
    Returns:
        int: The year extracted from the date string.
    """
    try:
        return datetime.strptime(date_string, '%d/%m/%Y').year
    except ValueError:
        return None

def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare the dataframe by extracting the year from certificate_issue_date.
    
    Args:
        df (pd.DataFrame): The original dataframe.
    
    Returns:
        pd.DataFrame: The dataframe with an additional 'year' column.
    """
    df['year'] = df['certificate_issue_date'].apply(extract_year)
    return df.dropna(subset=['year'])

def display_kpis(df: pd.DataFrame):
    prepared_df = prepare_data(df)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Nombre de certifications passées", len(prepared_df))
    
    with col2:
        total_hours = prepared_df['theorical_workload_h'].sum()
        st.metric("Volume d'heures théorique total", f"{total_hours:.0f}")
    
    with col3:
        years = prepared_df['year'].max() - prepared_df['year'].min() + 1
        avg_hours_per_year = total_hours / years
        st.metric("Nombre d'heures par an moyen", f"{avg_hours_per_year:.1f}")

def calculate_hours_per_year(df: pd.DataFrame) -> pd.DataFrame:
    prepared_df = prepare_data(df)
    return prepared_df.groupby('year')['theorical_workload_h'].sum().reset_index(name='hours')

def calculate_hours_per_skill(df: pd.DataFrame) -> pd.DataFrame:
    skill_hours = {}
    for _, row in df.iterrows():
        if isinstance(row['skills'], str):
            skills = eval(row['skills'])
            for skill in skills:
                if skill in skill_hours:
                    skill_hours[skill] += row['theorical_workload_h']
                else:
                    skill_hours[skill] = row['theorical_workload_h']
    return pd.DataFrame(list(skill_hours.items()), columns=['skill', 'hours']).sort_values('hours', ascending=False)

def display_analysis_graphs(df: pd.DataFrame):
    # Graphique à barres des heures par an
    hours_per_year = calculate_hours_per_year(df)
    fig1 = px.bar(hours_per_year, x='year', y='hours', title="Nombre d'heures par an")
    st.plotly_chart(fig1)

    # Graphique à barres des heures par compétence
    hours_per_skill = calculate_hours_per_skill(df)
    fig2 = px.bar(hours_per_skill, x='skill', y='hours', title="Nombre d'heures par compétence")
    fig2.update_layout(xaxis_title="Compétence", yaxis_title="Heures")
    st.plotly_chart(fig2)