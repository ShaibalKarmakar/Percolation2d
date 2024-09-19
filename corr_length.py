import os
import numpy as np
import pickle
import random
import matplotlib.pyplot as plt
from tqdm import tqdm
import multiprocessing

class Graph:
    def __init__(self, n=10, multiplier = 1):
        self.n = int(n*multiplier)
        self.hit_point = n
        x_range = np.arange(-self.n, self.n+1)
        self.vertices = []
        for i in x_range:
            for j in x_range:
                self.vertices.append((i,j))
        
        self.vertex_dict = dict(zip(self.vertices, range(len(self.vertices))))
        self.to_vertex_dict = dict(zip(range(len(self.vertices)), self.vertices))
        # print(self.vertex_dict)
    
    def adj_dict(self, p):
        adj_dict = {}
        # initialize dict
        for vertex in self.vertices: adj_dict[self.vertex_dict[vertex]] = []

        for vertex in self.vertices:
            x,y = vertex
            # print(vertex)
            nbrs = [(x-1,y), (x+1, y), (x,y-1), (x,y+1)]
            for nbr in nbrs:
                a,b = nbr
                if max(abs(a), abs(b)) <= self.n:
                    if random.random() <= p:
                        adj_dict[self.vertex_dict[vertex]].append(self.vertex_dict[nbr])
                        # adj_dict[self.vertex_dict[nbr]].append(self.vertex_dict[vertex])
        return adj_dict
    
    def dfs(self, adj_dict):
        start = self.vertex_dict[(0,0)]
        visited = set()
        stack = [start]
        while stack:
            vertex = stack.pop()
            if vertex in visited:
                continue
            visited.add(vertex)
            for nbr in adj_dict[vertex]:
                stack.append(nbr)
                _,b = self.to_vertex_dict[nbr]
                if b == self.hit_point:
                    return 1
        return 0


def single_process(p, n, multiplier, trials, id, store_folder):
    store_path = os.path.join(store_folder, f"{id}.pkl")

    G = Graph(n, multiplier)
    rec = {"p":p, "n":n, "multiplier":multiplier, "trials_done":0, "hits":0}
    for i in range(trials):
        adj_dict = G.adj_dict(p)
        rec["trials_done"] += 1
        rec["hits"] += G.dfs(adj_dict)
    if (i+1)%100 == 0:
        with open(store_path, "wb") as gp:
            pickle.dump(rec, gp)
    with open(store_path, "wb") as gp:
        pickle.dump(rec, gp)
    

def main(p, n, multiplier, num_trials, num_processes):

    store_folder = os.path.join(os.getcwd(), "all_data")
    if not os.path.exists(store_folder):
        os.mkdir(store_folder)
    existing_numrec = len(os.listdir(store_folder))

    processes = []
    for i in range(num_processes):
        rec_id = i+existing_numrec
        processes.append(multiprocessing.Process(target = single_process, args = (p,n,multiplier, num_trials//num_processes, rec_id, store_folder)))
    
    for process in processes:
        process.start()

    for i, process in enumerate(processes):
        process.join()
        print(f"Process {i} finished for p={p}")

    print(f"p = {p} finished")