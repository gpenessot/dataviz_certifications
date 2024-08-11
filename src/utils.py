import pandas as pd
from typing import Dict

def calculate_hours_per_year(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby('year')['theorical_workload_h'].sum().reset_index(name='hours')

def calculate_hours_per_skill(df: pd.DataFrame) -> Dict[str, float]:
    skill_hours = {}
    for _, row in df.iterrows():
        if isinstance(row['skills'], str):
            skills = eval(row['skills'])
            for skill in skills:
                if skill in skill_hours:
                    skill_hours[skill] += row['theorical_workload_h']
                else:
                    skill_hours[skill] = row['theorical_workload_h']
    return skill_hours
