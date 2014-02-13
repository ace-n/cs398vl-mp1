#!/usr/bin/env python

freq_th = 2

import networkx as nx
import cPickle
import os

# SAVED DATA
# 1) Relative frequency table (node size)
# 2) Distances between words (edge wt)

# Filepath
filepath = "1"

# Load data
ch_relFreq = cPickle.load(open("./data/ch_" + filepath + "_table.p"))
ch_dist = cPickle.load(open("./data/ch_" + filepath + "_dists.p"))

def graph():

    # === Make graph ===
    G=nx.Graph()
    nodeSize = dict()
    edgeWidth = []
    
    # Add nodes
    for w in ch_relFreq.keys():
      
       if ch_relFreq[w] < freq_th:
          continue
      
       G.add_node(w)
       nodeSize[w] = abs(ch_relFreq[w]) / 1000
    
    edgeCount = 0
    for w_a in ch_relFreq.keys():
    
      if ch_relFreq[w_a] < freq_th:
          continue
    
      for w_b in ch_relFreq.keys():
      
         if ch_relFreq[w_b] < freq_th:
          continue
      
         # Skip identical or repeated
         if w_a == w_b:
            continue
         
         # Form edge
         if not G.has_edge(w_a, w_b):
            edge = G.add_edge(w_a, w_b)
            edgeCount += 1
         
            # Weight edge
            edgeWidth.append(30/max(1, abs(ch_dist[w_a][w_b])))
         
    print "EDGE COUNT: " + str(edgeCount)
    return (G, nodeSize, edgeWidth)

def main():
    import networkx as nx
    import matplotlib.pyplot as plt
    
    G_tuple = graph()
    G = G_tuple[0]
    nodeSize = G_tuple[1]
    edgeWidth = G_tuple[2]
    
    print "EDGES: " + str(len(edgeWidth))
    
    try:
        pos=nx.graphviz_layout(G)
    except:
        pos=nx.spring_layout(G,iterations=20)

    stage = 1
    stages = 5

    print "STAGE " + str(stage) + "/" + str(stages); stage += 1
    #plt.rcParams['text.usetex'] = False
    plt.figure(figsize=(20, 20))
    nx.draw_networkx_edges(G,pos,alpha=0.3,width=edgeWidth, edge_color='m')
    print "STAGE " + str(stage) + "/" + str(stages); stage += 1
    nx.draw_networkx_nodes(G,pos,node_size=[abs(ch_relFreq[w]*150) for w in G],node_color='w',alpha=1)
    print "STAGE " + str(stage) + "/" + str(stages); stage += 1
    print "STAGE " + str(stage) + "/" + str(stages); stage += 1
    nx.draw_networkx_labels(G,pos,fontsize=14)
    font = {'fontname'   : 'Helvetica',
            'color'      : 'k',
            'fontweight' : 'bold',
            'fontsize'   : 14}
    plt.title("Once and Future King - Chapter 1", font)

    # change font and write text (using data coordinates)
    plt.axis('off')
    print "STAGE " + str(stage) + "/" + str(stages); stage += 1
    plt.savefig("vizzed_ch1.png",dpi=50)
    print("Wrote image")
    
# Go
main()
