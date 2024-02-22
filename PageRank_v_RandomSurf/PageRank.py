import numpy as np
import sys
from timeit import default_timer as timer
import pandas as pd
import random
import csv

iterations_pagerank=4
iterations_randomsurf=10_000_000
m=0.15
filepath=str()

#command line arguments: filepath, iterations_pagerank, iterations_randomsurf
if len(sys.argv)>1:
    filepath=sys.argv[1]
else:
    filepath=input("input filepath: ")
if len(sys.argv)>2:
    iterations_pagerank=int(sys.argv[2])
if len(sys.argv)>3:
    iterations_randomsurf=int(sys.argv[3])

#detect the delimiter in the file
file=open(filepath,"r")
file.readline()
sniffer = csv.Sniffer()
dialect = sniffer.sniff(file.readline())
file.close()
delimiter=dialect.delimiter

#reading in the data using pandas, since it's very fast even for large files (eg.: bigRandom.txt)
time1=timer()
data = pd.read_csv(filepath,engine='c',usecols=[0,1], dtype=np.int32, delimiter=delimiter, comment='#')
header = np.array([int(data.columns[0]),int(data.columns[1])])
data = data.drop_duplicates()
data = np.array(data)
data=np.insert(data,0,header,axis=0)
time2=timer()
print(f"read data in: {time2-time1} seconds\n")
#At this point the variable 'data' is a numpy array containing the rows of the file

first_node = np.min( data )
last_node = np.max( data )

#nodes: a numpy array containing all the nodes
#size: number of nodes in graph
nodes=np.arange(first_node,last_node+1)
size = len(nodes)
one_over_size=1/size

#connected_nodes_forward: all the nodes that have edges coming out of them
#connected_nodes_backward: all the nodes that have edges going into them
#unique_indicies_1&2 are used when making a list of edges
data_sorted_c2 = data[data[:, 1].argsort()] #(data sorted by column 2 of data)
connected_nodes_forward, unique_indicies_1 = np.unique(data[:,0],return_index=True)
connected_nodes_backward, unique_indicies_2 = np.unique(data_sorted_c2[:, 1], return_index=True)

#dangling_nodes: all the nodes that have no outward branches,
#so the difference between all nodes, and the forward connected ones.
dangling_nodes = np.setdiff1d(nodes, connected_nodes_forward)

#edges_out and edges_in are arrays of arrays.
#eg.: edges_out[4] is a list of nodes that node 4 points to.
#eg.: edges_in[4] is a list of nodes that are pointing to node 4.
edges_out = np.split(data[:,1], unique_indicies_1[1:])
edges_in = np.split(data_sorted_c2[:,0], unique_indicies_2[1:])

#Because edges_in, and edges_out are not the length of nodes, it's necessary
#to make all_edges_in, and all_edges_out. They now contain the empty lists
#at indicies where a node doesn't have any connections.
all_edges_out=[[]]*size
for edge_index in range(len(connected_nodes_forward)):
    all_edges_out[ connected_nodes_forward[edge_index] ] = edges_out[edge_index]

all_edges_in=[[]]*size
for edge_index in range(len(connected_nodes_backward)):
    all_edges_in[ connected_nodes_backward[edge_index] ] = edges_in[edge_index]

def RandomSurfer(return_amount=size):
    counter=dict() #counter contains the nodes as keys, number of visits as values
    current_node=random.choice(nodes)
    counter[current_node]=1
    for i in range(iterations_randomsurf):
        rand_factor = random.random() #generate number from 0 to 1
        #if it's a dangling node or rand_factor is less than or equal to m
        if len(all_edges_out[current_node])==0 or rand_factor<=m:
            #choose a random node out of all the nodes
            next_node=random.choice(nodes)
        else:
            #choose a node connected to the current node
            next_node=random.choice(all_edges_out[current_node])
        if next_node in counter.keys():
            counter[next_node]+=1
        else:
            counter[next_node]=1
        current_node=next_node
    #sort the results by value
    result = dict(sorted(counter.items(), key=lambda item: item[1]))
    return list(result.keys())[::-1][:return_amount]
        
        
def PageRank(return_amount=size):
    #one_over_n is an array with elements 1/nj, where nj is the amount of outward edges j has
    #it is needed for calculating the matrix Ax each iteration
    n_edges=np.array( [len(i) for i in all_edges_out] )
    one_over_n = np.divide(1, n_edges, where=n_edges!=0)

    #x is the ranking vector
    x=np.full((size,1),one_over_size)

    #one row from the matrix D
    #that's all that's needed because every row is the same
    D_vector = np.zeros((1,size))
    #put 1/n for the indices of dangling nodes
    np.put(D_vector,dangling_nodes,one_over_size)

    #S*x is a constant, it doesn't change each iteration
    Sx = np.full((size,1),one_over_size)
    mSx = m*Sx

    for i in range(iterations_pagerank):
        #Dx is a column vector filled with: one row of the D matrix, multiplied by x
        Dx=np.full((size,1), D_vector @ x )
        
        #A_ij is 1/nj if node_j connects to node_i, so we have to get the nodes pointing to
        #node i, and multiply their 1/nj value with each corresponding x value.
        #This way all the multiplications by zero are left out.
        Ax=[one_over_n[ all_edges_in[i] ] @ x[ all_edges_in[i],: ] for i in range(size)]
        
        #construct the new x
        x=(1-m)*(Ax+Dx)+mSx
        
    #sort by value, and return the highest ranking nodes
    x=x.flatten()
    indicies=x.argsort()[::-1]
    return list(indicies[:return_amount])
    
time1=timer()
print(f"Calculating with PageRank algorithm: ")
print("-"*50)
print("The 10 highest ranking pages with PageRank algorithm are:")
print(PageRank(10))
print("The list is sorted by rank, and starts with the highest ranking page.")
time2=timer()
print(f"PageRank took: {time2-time1} seconds, with {iterations_pagerank} iterations.\n")

time1=timer()
print(f"Calculating with Random Surfer algorithm: ")
print("-"*50)
print("The 10 most visited sites with Random Surfer algorithm are:")
print(RandomSurfer(10))
time2=timer()
print(f"Random Surfer took: {time2-time1} seconds, with {iterations_randomsurf} iterations.\n")
input("FINISHED.")