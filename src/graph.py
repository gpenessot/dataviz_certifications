import pandas as pd
import math
from typing import List, Tuple, Dict, Any, Optional
from pyvis.network import Network
from collections import defaultdict

# Constants
CENTER_RADIUS = 0
MAIN_CERT_RADIUS = 333
SUB_CERT_RADIUS = 666
SKILL_RADIUS = 1000

CENTER_COLOR = '#FF5733'
MAIN_CERT_COLOR = '#FFC300'
SUB_CERT_COLOR = '#DAF7A6'
SKILL_COLOR = '#FF69B4'
BACKGROUND_COLOR = '#222222'
FONT_COLOR = 'white'

class CertificationGraph:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.net = self._create_network()
        self.cert_groups, self.non_specialized_certs = self._group_certifications()
        self.main_certs, self.sub_certs, self.skills = self._collect_nodes_and_leaves()

    def _create_network(self) -> Network:
        net = Network(height='600px', width='100%', bgcolor=BACKGROUND_COLOR, font_color=FONT_COLOR)
        net.add_node(0, label="Gael", color=CENTER_COLOR, size=50, x=0, y=0, physics=False)
        return net

    def _group_certifications(self) -> Tuple[Dict[str, List[Any]], List[Any]]:
        cert_groups = defaultdict(list)
        non_specialized_certs = []
        for _, row in self.df.iterrows():
            if pd.notna(row['main_cert']):
                cert_groups[row['main_cert']].append(row)
            else:
                non_specialized_certs.append(row)
        return dict(cert_groups), non_specialized_certs

    def _collect_nodes_and_leaves(self) -> Tuple[List[Tuple[str, float]], List[Tuple[str, float, Optional[str]]], List[Tuple[str, None]]]:
        main_certs = []
        sub_certs = []
        skills = set()

        for main_cert, certs in self.cert_groups.items():
            total_workload = sum(cert['theorical_workload_h'] for cert in certs if pd.notna(cert['theorical_workload_h']))
            main_certs.append((main_cert, total_workload))
            
            for cert in certs:
                sub_certs.append((cert['name'], cert['theorical_workload_h'], main_cert))
                if isinstance(cert['skills'], str):
                    skills.update(eval(cert['skills']))

        for cert in self.non_specialized_certs:
            sub_certs.append((cert['name'], cert['theorical_workload_h'], None))
            if isinstance(cert['skills'], str):
                skills.update(eval(cert['skills']))

        return main_certs, sub_certs, [(skill, None) for skill in skills]

    @staticmethod
    def _get_node_size(workload: float) -> float:
        if pd.isna(workload):
            return 20  # Default size for unknown workload
        return max(20, min(50, workload / 2))  # Size between 20 and 50, scaled by workload

    def _add_nodes_in_circle(self, items: List[Tuple[Any, ...]], radius: float, color: str, start_id: int, 
                             main_cert_dict: Optional[Dict[str, int]] = None, is_main_cert: bool = False) -> Tuple[int, Dict[str, int]]:
        node_ids = {}
        total_items = len(items)
        
        for i, item in enumerate(items):
            angle = 2 * math.pi * i / total_items
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            
            node_id = start_id + i
            if len(item) == 3:
                label, workload, parent_cert = item
            else:
                label, workload = item
                parent_cert = None
            
            size = self._get_node_size(workload) if workload is not None else 15
            
            self.net.add_node(node_id, label=label, color=color, x=x, y=y, size=size, physics=False)
            
            if is_main_cert:
                self.net.add_edge(0, node_id)
                node_ids[label] = node_id
            elif radius == SUB_CERT_RADIUS:
                if parent_cert and main_cert_dict and parent_cert in main_cert_dict:
                    self.net.add_edge(main_cert_dict[parent_cert], node_id)
                else:
                    self.net.add_edge(0, node_id)  # Connect non-specialized certs directly to the center
            elif radius == SKILL_RADIUS:
                closest_sub_cert = min(range(1, start_id), 
                                       key=lambda j: math.hypot(self.net.get_node(j)['x'] - x, self.net.get_node(j)['y'] - y))
                self.net.add_edge(closest_sub_cert, node_id)
        
        return start_id + total_items, node_ids

    def create_graph(self, show_skills: bool = False):
        self.net = self._create_network()
        
        next_id = 1
        next_id, main_cert_dict = self._add_nodes_in_circle(self.main_certs, MAIN_CERT_RADIUS, MAIN_CERT_COLOR, next_id, is_main_cert=True)
        next_id, _ = self._add_nodes_in_circle(self.sub_certs, SUB_CERT_RADIUS, SUB_CERT_COLOR, next_id, main_cert_dict)
        if show_skills:
            self._add_nodes_in_circle(self.skills, SKILL_RADIUS, SKILL_COLOR, next_id)

    def get_html(self) -> str:
        return self.net.generate_html(notebook=False)
