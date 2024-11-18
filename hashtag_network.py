# Importing necessary libraries
from tqdm import tqdm 
from collections import Counter
from scipy.stats import linregress
from matplotlib.ticker import FuncFormatter
from matplotlib import cm
from matplotlib.colors import Normalize
from os import chmod
from os.path import exists
from fa2_modified import ForceAtlas2 as fa2
from pyvis.network import Network
from webscraping import wait, script_dir
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import json

def network_creation(tagname, captions_file_path):

    with open(captions_file_path) as f:
        try:
            captions = json.load(f)
        except json.JSONDecodeError or FileNotFoundError or not (f.readline().strip()): # Read the first line and remove any leading/trailing whitespace
            raise FileNotFoundError # Raise because the file is empty and count it as nothing existing
        
    # Create a NetworkX graph
    hashtag_graph = nx.Graph()
    
    # Process captions to create the hashtag graph
    for caption in captions:
        # Gather each pair of hashtags in a caption
        for i in range(len(caption)):
            for j in range(i + 1, len(caption)):
                tag1, tag2 = caption[i], caption[j]

                # If a connection between 2 hashtags already exists, increment the edge weight
                if hashtag_graph.has_edge(tag1, tag2):
                    hashtag_graph[tag1][tag2]['weight'] += 1
                else:
                    hashtag_graph.add_edge(tag1, tag2, weight=1) # If a connection between 2 hashtags does not exist, set their edge weight to 1


    main_node = f'{tagname}'[1:]
    
    try:
        hashtag_graph.remove_node(main_node) # Remove the hashtag that was searched from the graph (as it will be #1 anyway due to it being the hashtag every video will contain, so it will be pointless to mention)
    except Exception:
        pass

    # Extract the largest connected component
    hashtag_graph = hashtag_graph.subgraph(max(nx.connected_components(hashtag_graph), key=len))


    n = hashtag_graph.number_of_nodes()
    e = hashtag_graph.number_of_edges()

    # Map node labels to integer indices
    label_to_index = {label: idx for idx, label in enumerate(hashtag_graph.nodes())}
    index_to_label = {idx: label for label, idx in label_to_index.items()}

    # Create an adjacency matrix using integer indices
    n = len(label_to_index)
    adj_matrix = np.zeros((n, n))

    # Add progress bar for adjacency matrix creation
    for u, v in tqdm(hashtag_graph.edges(), desc="Creating Adjacency Matrix", unit="edge", total=e):
        i, j = label_to_index[u], label_to_index[v]
        adj_matrix[i, j] = adj_matrix[j, i] = 1  # Assuming undirected graph

    # Calculate centrality values
    def calculate_betweenness_centrality(adj_matrix):
        n = adj_matrix.shape[0]
        betweenness = {i: 0.0 for i in range(n)}

        # Progress bar for betweenness calculation
        for s in tqdm(range(n), desc="Calculating Betweenness Centrality", unit="node", total=n):
            stack = []
            predecessors = [[] for _ in range(n)]
            sigma = np.zeros(n)
            sigma[s] = 1
            dist = -np.ones(n)
            dist[s] = 0
            queue = [s]

            while queue:
                v = queue.pop(0)
                stack.append(v)
                for w in range(n):
                    if adj_matrix[v, w] > 0:
                        if dist[w] < 0:
                            queue.append(w)
                            dist[w] = dist[v] + 1
                        if dist[w] == dist[v] + 1:
                            sigma[w] += sigma[v]
                            predecessors[w].append(v)

            delta = np.zeros(n)
            while stack:
                w = stack.pop()
                for v in predecessors[w]:
                    delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
                if w != s:
                    betweenness[w] += delta[w]

        betweenness = {node: bc / 2 for node, bc in betweenness.items()}
        return betweenness

    def calculate_closeness_centrality(adj_matrix):
        n = adj_matrix.shape[0]
        closeness = {i: 0.0 for i in range(n)}

        # Progress bar for closeness calculation
        for i in tqdm(range(n), desc="Calculating Closeness Centrality", unit="node", total=n):
            shortest_paths = np.full(n, np.inf)
            shortest_paths[i] = 0
            visited = np.zeros(n, dtype=bool)
            queue = [i]

            while queue:
                v = queue.pop(0)
                visited[v] = True
                for w in range(n):
                    if adj_matrix[v, w] > 0 and not visited[w]:
                        new_dist = shortest_paths[v] + 1
                        if new_dist < shortest_paths[w]:
                            shortest_paths[w] = new_dist
                            queue.append(w)

            sum_distances = np.sum(shortest_paths[shortest_paths != np.inf])
            if sum_distances > 0:
                closeness[i] = (n - 1) / sum_distances

        return closeness

    # Calculate centrality measures with progress tracking in the functions
    betweenness_centrality = calculate_betweenness_centrality(adj_matrix)
    closeness_centrality = calculate_closeness_centrality(adj_matrix)
    eigenvector_centrality = nx.eigenvector_centrality(hashtag_graph)
    weighted_eigenvector = nx.eigenvector_centrality(hashtag_graph, weight='weight')

    # Map results back to original labels
    betweenness_centrality = {index_to_label[i]: bc for i, bc in betweenness_centrality.items()}
    closeness_centrality = {index_to_label[i]: cc for i, cc in closeness_centrality.items()}


    # Sort and get the top 20 highest betweenness centrality nodes
    top_20_betweenness = [node for node, _ in sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:20]]

    # Sort and get the top 20 highest closeness centrality nodes
    top_20_closeness = [node for node, _ in sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:20]]
    
    # Sort and get the top 20 highest eigenvector centrality nodes
    top_20_eigenvector = [node for node, _ in sorted(eigenvector_centrality.items(), key=lambda x: x[1], reverse=True)[:20]]
    
    # Sort and get the top 20 highest eigenvector centrality nodes (weighted)
    top_20_eigen_weighted = [node for node, _ in sorted(weighted_eigenvector.items(), key=lambda x: x[1], reverse=True)[:20]]

    # Get degree and weighted degree and sort to get the top 20 nodes for each
    node_degrees = hashtag_graph.degree()
    top_20_degrees = [node for node, _ in sorted(node_degrees, key=lambda x: x[1], reverse=True)[:20]]

    weighted_node_degrees = hashtag_graph.degree(weight='weight')
    top_20_weighted_degrees = [node for node, _ in sorted(weighted_node_degrees, key=lambda x: x[1], reverse=True)[:20]]

    # Combine all the top 20 lists of hashtags to get an average list based on number of occurences of a node appearing in the list
    all_nodes = top_20_betweenness + top_20_closeness + top_20_degrees + top_20_weighted_degrees + top_20_eigenvector + top_20_eigen_weighted

    # Count occurrences of each node across the combined list
    node_occurrences = {}
    for node in all_nodes:
        if node in node_occurrences:
            node_occurrences[node] += 1
        else:
            node_occurrences[node] = 1

    # Sort nodes by their frequency of occurrence and get the top 20 most frequent nodes
    top_20_nodes_overall = sorted(node_occurrences.keys(), key=lambda x: node_occurrences[x], reverse=True)[:20]
    print(top_20_nodes_overall)
    
    def plot_fa2(graph, top_nodes, expansion_factor=1.0):
        # Initialize ForceAtlas2
        forceatlas2 = fa2(
            outboundAttractionDistribution=True,  # Prevent hubs from attracting too much
            linLogMode=False,
            adjustSizes=False,
            edgeWeightInfluence=1.0,
            jitterTolerance=1.0,
            barnesHutOptimize=True,
            barnesHutTheta=1.2,
            scalingRatio=2.0,
            strongGravityMode=False,
            gravity=1.0,
            verbose=True
        )

        # Generate positions using ForceAtlas2
        positions = forceatlas2.forceatlas2_networkx_layout(graph, pos=None, iterations=2500)

        # Apply expansion factor (scaling positions)
        expanded_positions = {
            node: (pos[0] * expansion_factor, pos[1] * expansion_factor)
            for node, pos in positions.items()
        }

        # Plot the graph
        plt.figure(figsize=(12, 12))

        # Separate top nodes and other nodes
        if top_nodes is None:
            top_nodes = []

        other_nodes = [node for node in graph.nodes if node not in top_nodes]

        # Draw other nodes
        nx.draw_networkx_nodes(
            graph,
            expanded_positions,
            nodelist=other_nodes,
            node_size=20,
            node_color="blue",
            alpha=0.6
        )

        # Draw top nodes
        nx.draw_networkx_nodes(
            graph,
            expanded_positions,
            nodelist=top_nodes,
            node_size=100,
            node_color="red",
            alpha=0.9
        )

        # Draw edges
        nx.draw_networkx_edges(graph, expanded_positions, alpha=0.4, edge_color="black")

        # Add labels for top nodes
        nx.draw_networkx_labels(graph, expanded_positions, labels={node: node for node in top_nodes}, font_size=10, font_color="black")

        # Display plot
        plt.axis("off")
        plt.title("ForceAtlas2 Graph with Highlighted Nodes")
        plt.show()
        
    plot_fa2(hashtag_graph, top_20_nodes_overall, expansion_factor=100)

    while True:
        export_to_gephi = input('Would you like to export to Gephi?\nEnter Y/N: ').lower()
        if export_to_gephi == 'y':
            nx.write_gexf(hashtag_graph, f'{script_dir}/{tagname}graph.gexf')  # Creates a .gexf file to view in network graphing software
            print('Exported!')
            break
        elif export_to_gephi == 'n':
            break
        else:
            print('Enter Y/N please.')
    
    # Output the results
    print("\nTop 20 nodes overall (combined):")
    for node in top_20_nodes_overall:
        print(node)
    
    wait()

    try:
        if exists(f'{script_dir}/{tagname}_top_20_list.txt'):
            print('A top 20 list of hashtags to put in your caption already exists.')
        else:
            with open(f'{script_dir}/{tagname}_top_20_list.txt', 'w') as f:
                for node in top_20_nodes_overall:
                    f.write(f'#{node}\n')
            # Change the permissions of the file to be read only so the user doesn't accidentally edit their list
            chmod(f'{script_dir}/{tagname}_top_20_list.txt', 0o444)
            print('A list of your hashtags has been made into a file.')
    except FileNotFoundError as e:
        print(f'An error occurred: {e}')
