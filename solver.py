# Put your solution here.

import networkx as nx
import random


def solve(client):
    client.end()
    client.start()
    #all_students = list(range(1, client.students + 1))
    #non_home = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))
    mst = nx.algorithms.tree.minimum_spanning_tree(client.G)
    dfs = nx.algorithms.traversal.dfs_successors(mst, source=client.h)
    #solver_with_scout(client)
    #mst_with_scout(dfs, client)
    #mst_with_scout(dfs, client)
    solver_with_MW(client)
    client.end()

#scout and mst
def solver(dfs, client):
    all_students = list(range(1, client.students+1))

    total = 0
    num_bots = {}
    for n in range(1, client.n + 1):
        num_bots[n] = 0
        


    vertex_scores = {} #maps vertex -> student score

    for node in range(1, client.v+1):
        if node != client.h:
            scout_dict = client.scout(node, all_students)
            points = 0
            for s in range(1, client.students + 1):
                if scout_dict[s]:
                    points += 1
            vertex_scores[node] = points 

    while total < client.l:
        best_node = max(vertex_scores.keys(), key = lambda node: vertex_scores[node])
        del vertex_scores[best_node]
        path = nx.shortest_path(client.G, best_node, client.h, weight="weight")
        bots_remoted = client.remote(path[0], path[1])
        total += bots_remoted - num_bots[best_node]
        num_bots[best_node] = 0
        num_bots[path[1]] += bots_remoted 


    def traverse(node, prev):
        if node in dfs:
            children = dfs[node]
            for child in children:
                traverse(child, node)
        if prev is not None:
            if num_bots[node] > 0:
                bots = client.remote(node, prev)
                num_bots[prev] += bots
    
    traverse(client.h, None)

#optimal solver designed by Sanchit
#scout with dijkstra
def solver_with_scout(client):
    points = [0 for i in range(client.v+1)]
    points[client.h] = -100
    points[0] = -100
    all_students = list(range(1, client.students + 1))
    for v in range(1, client.v+1):
        if v == client.h:
            continue
        scout_dict = client.scout(v,all_students)
        curr_points = 0
        for s in range(1, client.students + 1):
            if scout_dict[s]:
                curr_points += 1
        points[v] = curr_points

    num_bots = 0
    bots_at_vertex = {}
    for n in range(1, client.n + 1):
        bots_at_vertex[n] = 0
    for i in range(len(points)):
        if num_bots == client.l:
            break
        best = points.index(max(points))
        path = nx.shortest_path(client.G, best, client.h, weight="weight")
        bots_remoted = client.remote(path[0], path[1])
        if bots_remoted > 0:
            num_bots += bots_remoted
            bots_at_vertex[path[1]] += bots_remoted 
            bots_at_vertex[path[0]] = 0

            for j in range(1, len(path) - 1):
                bots_remoted = client.remote(path[j], path[j+1])
                num_bots += (bots_remoted - bots_at_vertex[path[j]])
                bots_at_vertex[path[j+1]] += bots_remoted 
                bots_at_vertex[path[j]] = 0

        points[best] = -100
    print(client.students)


#experimental solver with random sampling
# not optimal
def random_scout(client):
    all_students = list(range(1, client.students + 1))
    non_home = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))
    def pick_random(list):
        return random.sample(list, 10)

    samples = {}
    step_size = int(100 / (len(all_students) / 10))
    start = 0
    end = step_size
    def sample_vertices():
        nonlocal samples, all_students, start, end
        students = all_students
        while end < 100 + step_size:
            if len(all_students) > 10:
                students = pick_random(all_students)
                all_students = [i for i in all_students if i not in students]

            for i in range(start, min(end, len(non_home))):
                vertex = non_home[i]
                samples[vertex] = 0
                temp_sample = client.scout(vertex, students)
                for student in students:
                    samples[vertex] = samples[vertex] + temp_sample[student]
            start += step_size
            end += step_size
    sample_vertices()

    def remote_vertices():
        count_bot = 0
        while client.l > count_bot:
            max_vertex = max(samples.keys(), key= lambda x: samples[x])
            samples[max_vertex] = -1
            path = nx.shortest_path(client.G, max_vertex, client.h, weight="weight")
            remoted = client.remote(path[0], path[1])
            if remoted > 0:
                count_bot += remoted
                prev = remoted
                for j in range(1, len(path) - 1):
                    curr = client.remote(path[j], path[j + 1]) - prev
                    count_bot += curr
                    prev += curr
    remote_vertices()

def delete_solver(client):
    all_students = list(range(1, client.students + 1))
    non_home = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))

    student_count = {}
    for student in all_students:
        student_count[student] = []

    samples = {}

    for vertex in non_home:
        scouts = client.scout(vertex, all_students)
        samples[vertex] = 0
        for student in all_students:
            if scouts[student]:
                samples[vertex] = samples[vertex] + 1
                student_count[student] = student_count[student] + [vertex]

    while len(student_count.keys()) > 10:
        max_student = max(student_count.keys(), key=lambda x: len(student_count[x]))
        for vertex in student_count.pop(max_student):
            samples[vertex] = samples[vertex] - 1


    def remote_vertices():
        count_bot = 0
        while client.l > count_bot:
            max_vertex = max(samples.keys(), key= lambda x: samples[x])
            samples[max_vertex] = -1
            path = nx.shortest_path(client.G, max_vertex, client.h, weight="weight")
            remoted = client.remote(path[0], path[1])
            if remoted > 0:
                count_bot += remoted
                prev = remoted
                for j in range(1, len(path) - 1):
                    curr = client.remote(path[j], path[j + 1]) - prev
                    count_bot += curr
                    prev += curr
    remote_vertices()

def solver_with_MW(client):
    all_students = list(range(1, client.students + 1))
    non_home = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))

    student_count = {}
    for student in all_students:
        student_count[student] = []

    epsilon = 0.5

    samples = {}

    student_weights = {}

    for student in all_students:
        student_weights[student] = 1

    def update_belief():
        nonlocal samples
        for vertex in samples.keys():
            samples[vertex] = 0
            for student in all_students:
                if vertex in student_count[student]:
                    samples[vertex] = samples[vertex] + student_weights[student]
                else:
                    samples[vertex] = samples[vertex] - student_weights[student]

    for vertex in non_home:
        scouts = client.scout(vertex, all_students)
        samples[vertex] = 0
        for student in all_students:
            if scouts[student]:
                samples[vertex] = samples[vertex] + 1
                student_count[student] = student_count[student] + [vertex]
            else:
                samples[vertex] = samples[vertex] - 1

    def update_weights(remote, vertex):
        nonlocal student_weights
        for student in all_students:
            if remote > 0:
                if vertex not in student_count[student]:
                    student_weights[student] = student_weights[student] * (1 - epsilon)
            else:
                if vertex in student_count[student]:
                    student_weights[student] = student_weights[student] * (1 - epsilon)

    def remote_vertices():
        count_bot = 0
        while client.l > count_bot:
            max_vertex = max(samples.keys(), key=lambda x: samples[x])
            del samples[max_vertex]
            path = nx.shortest_path(client.G, max_vertex, client.h, weight="weight")
            remoted = client.remote(path[0], path[1])
            update_weights(remoted, max_vertex)
            update_belief()
            if remoted > 0:
                count_bot += remoted
                prev = remoted
                for j in range(1, len(path) - 1):
                    curr = client.remote(path[j], path[j + 1]) - prev
                    if path[j] in samples:
                        del samples[path[j]]
                    count_bot += curr
                    prev += curr
    remote_vertices()