# by: Abdulrhman Menshawi
# @Amenshawi on github

from PIL import Image
import math
import numpy as np
import timeit

draw_start = timeit.default_timer()

img = Image.open(r'maze101x101.png')
pix_list = list(img.getdata())

length = int(math.sqrt(pix_list.__len__()))

path = list()
start = None

# variables for stats only
paths_count = 0
nodes_count = 0


class Node:

    def __init__(self, row, col):
        global nodes_count  # For calculating stats only
        nodes_count += 1  # For calculating stats only

        super().__init__()

        self.row = row
        self.col = col
        self.connections = list()
        self.is_start = False
        self.is_end = False
        self.edges = {}

    def __str__(self):
        s = 'i = ' + str(self.row) + ' j = ' + str(self.col)
        return s


def is_a_node(i, j):
    node = True
    if pix_matrix[i+1, j] == 0 and pix_matrix[i-1, j] == 0:
        node = False
    if pix_matrix[i, j+1] == 0 and pix_matrix[i, j-1] == 0:
        node = False
    return node

# Replacing only intersection between paths with nods to
# minimize the # of checks needed to find the correct path


def connect_nodes(i, j):
    edges = list()
    for k in range(j, -1, -1):

        if isinstance(pix_matrix[i, k], Node) and k != j:
            pix_matrix[i, j].connections.append(pix_matrix[i, k])
            pix_matrix[i, k].connections.append(pix_matrix[i, j])

            pix_matrix[i, j].edges[str(pix_matrix[i, k])] = edges
            pix_matrix[i, k].edges[str(pix_matrix[i, j])] = edges
            break

        elif pix_matrix[i, k] == 1:
            edges.append((i, k))
            continue
        elif pix_matrix[i, k] == 0:
            break

    edges = list()
    for z in range(i, -1, -1):

        if isinstance(pix_matrix[z, j], Node) and z != i:
            pix_matrix[i, j].connections.append(pix_matrix[z, j])
            pix_matrix[z, j].connections.append(pix_matrix[i, j])

            pix_matrix[i, j].edges[str(pix_matrix[z, j])] = edges
            pix_matrix[z, j].edges[str(pix_matrix[i, j])] = edges

            break

        elif pix_matrix[z, j] == 1:
            edges.append((z, j))
            continue

        elif pix_matrix[z, j] == 0:
            break


def draw():
    path_pix = np.zeros((length, length, 3), dtype=np.uint8)
    path_pix[0:length, 0:length] = [0, 0, 0]
    for i in range(length):
        for j in range(length):
            pix = pix_matrix[i][j]

            if isinstance(pix, Node):
                path_pix[i][j] = [255, 255, 255]

            elif pix != 0:
                path_pix[i][j] = [255, 255, 255]
    for i in range(path.__len__()):
        p = path[i]
        path_pix[p.row][p.col] = [255, 0, 0]
        for key, edges in p.edges.items():
            if key == str(path[i-1]):
                for edge in edges:
                    if i != 0:
                        path_pix[edge[0]][edge[1]] = [255, 0, 0]
    img = Image.fromarray(path_pix, 'RGB')
    img.save('solved.png')
    img.show()


visited = set()  # Set to keep track of visited nodes.


def dfs(visited, node):
    global paths_count
    if node.connections.__len__() <= 1:  # For calculating stats only
        global paths_count
        paths_count += 1
    found = False
    if node.is_end:
        path.append(node)
        found = True
    elif node not in visited:

        path.append(node)
        visited.add(node)
        for node in node.connections:
            if dfs(visited, node):
                found = True
                break
        if not found:
            path.pop()
    return found


# Each colored pixel will be considered a wall and the white pixels are paths
for i in range(pix_list.__len__()):
    if pix_list[i][0] != 255:
        pix_list[i] = 0
    else:
        pix_list[i] = 1

# turning the list into a length X length matrix
# used tmp to be able to store objects in the array
tmp = np.array(pix_list).reshape((length, length))
pix_matrix = np.zeros((length, length), dtype=object)
for i in range(length):
    for j in range(length):
        pix_matrix[i][j] = tmp[i][j]

# placing the nodes and connecting them
for i in range(length):
    for j in range(length):
        if pix_matrix[i][j] == 1:
            if i == 0:
                pix_matrix[i, j] = Node(i, j)
                pix_matrix[i, j].is_start = True
                start = pix_matrix[i, j]
                print(start)
                print(pix_matrix[i, j])
                connect_nodes(i, j)

            elif i == length-1:
                pix_matrix[i, j] = Node(i, j)
                pix_matrix[i, j].is_end = True
                connect_nodes(i, j)

            elif is_a_node(i, j):
                pix_matrix[i, j] = Node(i, j)
                connect_nodes(i, j)


print('-----------------')
draw_stop = timeit.default_timer()
print('time to proccess the maze: ', draw_stop - draw_start)

dfs(visited, start)
solve_stop = timeit.default_timer()
print('-----------------')
print('time to solve: ', solve_stop - draw_stop)

draw()
print('number of nodes: ', nodes_count)
print('paths count: ', paths_count)
print('soultion length: ', path.__len__(), ' nodes')
print('-----------------')
