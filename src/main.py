import streamlit as st
import pandas as pd
import numpy as np
import json
from graph import CertificationGraph
from analysis import display_kpis, display_analysis_graphs

st.set_page_config(layout="wide", page_title="Certification Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv('../data/cleaned_data.csv')
    df['skills'] = df['skills'].apply(lambda x: eval(x) if isinstance(x, str) else [])
    return df

def get_unique_values(df, column):
    if column == 'skills':
        return sorted(set(skill for skills in df[column] for skill in skills if skills))
    unique_values = df[column].unique()
    valid_values = [str(val) for val in unique_values if pd.notna(val)]
    return sorted(valid_values)

def display_certification_details(cert_info):
    st.subheader(cert_info['name'])
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Plateforme:** {cert_info['platform_name']}")
        st.write(f"**Partenaire:** {cert_info['partner_name']}")
        st.write(f"**Certification principale:** {cert_info['main_cert']}")
        st.write(f"**Niveau:** {cert_info['level']}")
        st.write(f"**Date d'obtention:** {cert_info['certificate_issue_date']}")
        
    with col2:
        st.write(f"**Charge de travail théorique:** {cert_info['theorical_workload_h']} heures")
        st.write(f"**Score personnel:** {cert_info['personal_score']}")
        st.write(f"**Certification finale:** {cert_info['final_certification']}")
    
    st.write("**Compétences:**")
    st.write(", ".join(eval(cert_info['skills'])))
    
    if cert_info['certificate_url']:
        st.markdown(f"[Lien vers le certificat]({cert_info['certificate_url']})")
    if cert_info['syllabus_url']:
        st.markdown(f"[Lien vers le syllabus]({cert_info['syllabus_url']})")

def main():
    df = load_data()

    st.sidebar.title("Filtres")
    
    cert_filter = st.sidebar.multiselect(
        "Filtrer par nom de certification",
        options=get_unique_values(df, 'name'),
        key="cert_filter"
    )
    
    main_cert_filter = st.sidebar.multiselect(
        "Filtrer par certification principale",
        options=get_unique_values(df, 'main_cert'),
        key="main_cert_filter"
    )
    
    skills_filter = st.sidebar.multiselect(
        "Filtrer par compétences",
        options=get_unique_values(df, 'skills'),
        key="skills_filter"
    )

    filtered_df = df.copy()
    if cert_filter:
        filtered_df = filtered_df[filtered_df['name'].isin(cert_filter)]
    if main_cert_filter:
        filtered_df = filtered_df[filtered_df['main_cert'].astype(str).isin(main_cert_filter)]
    if skills_filter:
        filtered_df = filtered_df[filtered_df['skills'].apply(lambda x: any(skill in x for skill in skills_filter))]

    tab1, tab2 = st.tabs(["Graphe", "Analyse"])

    with tab1:
        st.title("Graphe des Certifications")
        show_skills = st.checkbox("Afficher les compétences", value=False)
        
        graph = CertificationGraph(filtered_df)
        graph.create_graph(show_skills)
        
        html = graph.get_html()
        
        html = html.replace('</script>',
        """
        network.on("click", function(params) {
            if (params.nodes.length > 0) {
                var node = params.nodes[0];
                var nodeInfo = network.body.nodes[node].options.title;
                window.parent.postMessage({type: "NODE_CLICKED", nodeInfo: nodeInfo}, "*");
            }
        });
        </script>
        """)
        
        st.components.v1.html(html, height=700, scrolling=False)
        
        if 'node_info' not in st.session_state:
            st.session_state.node_info = None
        
        def handle_node_click(msg):
            if msg.get("type") == "NODE_CLICKED":
                st.session_state.node_info = json.loads(msg.get("nodeInfo", "{}"))
                st.experimental_rerun()
        
        st.components.v1.html("""
        <script>
        window.addEventListener('message', function(event) {
            if (event.data.type === "NODE_CLICKED") {
                window.Streamlit.setComponentValue(event.data);
            }
        });
        </script>
        """, height=0)
        
        if st.session_state.node_info:
            display_certification_details(st.session_state.node_info)

    with tab2:
        st.title("Analyse des Certifications")
        display_kpis(filtered_df)
        display_analysis_graphs(filtered_df)

if __name__ == "__main__":
    main()
