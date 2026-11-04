import streamlit as st

import os
import json
import re
from pyvis.network import Network

#global fallbacks to protect against script syntax errors
null = None 
false = False
true = True

# Set the page layout 
st.set_page_config(layout="wide")

# make orignal html file untouched/modified despite filters applied
script_dir = os.path.dirname(os.path.abspath(__file__))
original_content = os.path.join(script_dir, "last_wish_knowledge_graph.html")
filtered_content = os.path.join(script_dir, "filtered_last_wish_knowledge_graph.html")

#configure the sidebar for user interaction
st.sidebar.title("Knowledge Graph Filters")

if st.sidebar.button("Reset Filters"):
    st.rerun()  # Reset the app to its initial state

nodes_to_remove = st.sidebar.multiselect(
    "Select nodes to remove:", 
    options=st.session_state.base_nodes
)

node_groups = {
    "Geralt": "Witcher",
    "Yennefer": "Sorceress",
    "Ciri": "Royalty",
    "Pavetta": "Royalty",
    "Dandelion": "Bard"
}
# Default color palette for the groups
group_colors = {
    "Witcher": "#4A69BD",    # Soft Blue
    "Sorceress": "#9B5DE5",  # Purple
    "Royalty": "#FF6B6B",    # Coral/Red
    "Bard": "#FFD166",       # Yellow
    "Other": "#A2A2A2"       # Grey
}

# Define fallback group for any node extracted from your HTML that isn't mapped above
def get_node_group(node_name):
    return node_groups.get(node_name, "Other")

#Color Customisation Legend
st.sidebar.subheader("Group Colors")
chosen_colors = {}
for group, default_color in group_colors.items():
    # Allows users to change colors on the fly using a native color picker
    chosen_colors[group] = st.sidebar.color_picker(f"{group} Color", default_color)
    

def load_graph_data():
      
    # load the original htlm content and extract nodes and edges first
    if "base_nodes" not in st.session_state:
        if os.path.exists(original_content):
            with open(original_content, "r", encoding="utf-8") as f:
                html_content = f.read()

            # use regular expressions to isolate the JSON strings inside vis.DataSet(...)
            node_match = re.search(r'nodes\s*=\s*new\s+vis\.DataSet\(\s*(\[.*?\])\s*\);', html_content, re.DOTALL)
            edge_match = re.search(r'edges\s*=\s*new\s+vis\.DataSet\(\s*(\[.*?\])\s*\);', html_content, re.DOTALL)

            if node_match and edge_match:
                # Safely parse the JavaScript arrays using JSON decoding
                raw_nodes = json.loads(node_match.group(1))
                raw_edges = json.loads(edge_match.group(1))

                # extract unique string IDs/Labels for your Python backend
                st.session_state.base_nodes = [str(node['id']) for node in raw_nodes]
                st.session_state.base_edges = [(str(edge['from']), 
                                                str(edge['to'])) for edge in raw_edges]
            else:
                st.error("Could not parse data structures inside the original HTML file." \
                " Falling back to default data.")

                # Fallback data if regex matching fails due to an unexpected layout template
                st.session_state.base_nodes = ["Geralt", "Yennefer", "Ciri", "Dandelion", "Pavetta"]
                st.session_state.base_edges = [("Geralt", "Yennefer"), ("Geralt", "Ciri"), ("Yennefer", "Ciri")]
        else:
            st.error(f"Missing base file:  '{original_content}'.  Make sure the con in your project root directory.")
            st.stop()
        return st.session_state.base_nodes, st.session_state.base_edges

st.session_state.base_nodes, st.session_state.base_edges = load_graph_data()


def apply_filters():
    # filter data dynamically based on user selection
    filtered_nodes = [node for node in st.session_state.base_nodes if node not in nodes_to_remove]
    filtered_edges = [
        (source, target) for source, target in st.session_state.base_edges 
        if source in filtered_nodes and target in filtered_nodes
    ]

    # build the temp graph based on filtered nodes and edges
    filtered_net = Network(height="750px", width="100%", notebook=False, cdn_resources='remote')

    for node in filtered_nodes:
        group = get_node_group(node)
        color = chosen_colors.get(group, "#A2A2A2")  # Default to grey if group not found
        filtered_net.add_node(node, label=node, color=color, title=f"Group: {group}")

    for source, target in filtered_edges:
        filtered_net.add_edge(source, target)

    filtered_net.toggle_physics(True) 

    # save the filtered graph to a new HTML file
    filtered_net.save_graph(filtered_content)

# # filter data dynamically based on user selection
# filtered_nodes = [node for node in st.session_state.base_nodes if node not in nodes_to_remove]
# filtered_edges = [
#     (source, target) for source, target in st.session_state.base_edges 
#     if source in filtered_nodes and target in filtered_nodes
# ]

# # build the temp graph based on filtered nodes and edges
# filtered_net = Network(height="750px", width="100%", notebook=False, cdn_resources='remote')

# for node in filtered_nodes:
#     filtered_net.add_node(node, label=node)

# for source, target in filtered_edges:
#     filtered_net.add_edge(source, target)

# filtered_net.toggle_physics(True) 

# # save the filtered graph to a new HTML file
# filtered_net.save_graph(filtered_content)

# 1. Read your HTML file
try:
    with open(filtered_content, "r", encoding="utf-8") as f:
        html_code = f.read()
    
    st.title("Last Wish Knowledge Graph")
    st.iframe(html_code, height=900)

except FileNotFoundError:
    st.error("Error: 'your_file.html' was not found in the root directory. " \
    "Please check the file path.")
