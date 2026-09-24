import streamlit as st
import math
import heapq
import networkx as nx
import matplotlib.pyplot as plt
# import the necessary functions and variables from searchAlgos.py
from searchAlgos import (
    hospital_graph,
    locations,
    gbfs,
    a_star
)

# Streamlit GUI
#*******************#

# Set Page Config
st.set_page_config(page_title="Informed Search Visualizer", layout="centered")

# write meaningful title and description for the app
st.title("Emergency Supply Robot - Informed Search")
st.write(
    "Choose a start and goal location in the hospital, pick a search algorithm, "
    "and run Greedy Best-First Search or A* to find a route."
)

# define the nodes and their coordinates
nodes = list(hospital_graph.keys())

# create a selectbox for the user to choose the start and goal nodes
start = st.selectbox(
    "Select Initial Node",
    nodes,
    index=nodes.index("Pharmacy")
)

goal = st.selectbox(
    "Select Goal Node",
    nodes,
    index=nodes.index("Emergency_Ward")
)

# create a selectbox for the user to choose the search algorithm
algorithm = st.selectbox(
    "Select Search Algorithm",
    ["GBFS", "A*"]
)


if st.button("Run Search"):

    if algorithm == "GBFS":

        # run the GBFS algorithm with the selected start and goal nodes
        path, cost, expansion_order = gbfs(hospital_graph, start, goal)
    else:

        # run the A* algorithm with the selected start and goal nodes
        path, cost, expansion_order = a_star(hospital_graph, start, goal)

    if path is None:

        # display a error message indicating that no path was found
        st.error(f"No path found from {start} to {goal}.")

    else:

        # Display result
        st.subheader("Search Result")

        st.write(
            f"**Algorithm:** {algorithm}"
        )

        st.write(
            f"**Expansion Order:** {' → '.join(expansion_order)}"
        )

        st.write(
            f"**Solution Path:** {' → '.join(path)}"
        )

        st.write(
            f"**Total Path Cost:** {cost:.2f}"
        )



        # Visualize NetworkX graph

        G = nx.DiGraph()

        for node, neighbors in hospital_graph.items():

            for neighbor, weight in neighbors.items():

                G.add_edge(node, neighbor, weight=weight)

        pos = locations

        fig, ax = plt.subplots(
            figsize=(10, 6)
        )

        node_colors = []
        for n in G.nodes():
            if n == start:
                node_colors.append("red")
            elif n == goal:
                node_colors.append("gold")
            else:
                node_colors.append("lightblue")

        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1400, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)
        nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle="-|>", arrowsize=15, ax=ax)

        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, ax=ax)

        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(
            G, pos, edgelist=path_edges, edge_color="red", width=3,
            arrows=True, arrowstyle="-|>", arrowsize=20, ax=ax
        )

        ax.set_title(
            f"{algorithm} Solution Path"
        )

        ax.axis("off")

        st.pyplot(fig)
