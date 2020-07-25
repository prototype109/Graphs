# Understand
## Parent and child graph spanning multiple generations, need to find the earliest known ancestor of a specific node
## input is a tuple of ints (parent, child) output is the node int that is the furthest away ancestor of the starting node
## if there is more than one ancestor that is the earliest in the graph then I use the one with the lower numerical id
## if no earliest ancestor exists then I return -1

## My understanding is that this is a directed graph with no cyclical edges, as in on vertex has one neihbor that it points to
## since I have to find the earliest ancestor which means the path to the earliest ancestor is the largest one from the given input
## I need to use depth first traversal as that gives me the longest path to the node I am searching the largest path for.
## 
## This is how the graph is structured, it seems like a graph that goes from parent to child directional wise:
#       10
#      /
#     1   2   4  11
#      \ /   / \ /
#       3   5   8
#        \ / \   \
#         6   7   9
#
## My thinking is that I want to flip this to make dfs a little easier maybe, turn it into this instead:
# 9   7   6
#  \   \ / \
#   8   5   3
#  / \ /   / \
# 11  4   2   1
#              \
#               10
#
## So if I want to get the the longest path of 6 I don't have to pick random start points seeing which is the largest path
## I just have to have 6 as my starting vertex and do a depth first traversal and store all the paths that it goes through
## and finally look through and find the path with the largest amount of vertices in it and declare that the earliest ancestor
## in terms of a tie in length I would just need to compare the last elements in the paths gathered that were the largest
## and find the numerically smallest one.
##
## An idea I have to achieve this kind of graph instead is to take the input of (parent, child) and within my function flip it
## to (child, parent) to be stored in a dictionary of sets {child: {parent1, parent2}}
## once I got to an end node this way this would be a completed path.

# Pseudocode
## function take in list of ancestors[(parent, child), ...] as well as starting node:
##
##      need a list to store the paths I am taking
##      paths list[]
##      final_paths list[]
##      
##      need to store the tuple list inside a graph list representation
##      ancestor_graph dict{}        
##              
##          loop through input of ancestors: 
##              get ancestor put child as key
##              and add parent to set
##              need to see if child exists in graph though
##              or need to make an empty set
##
##      since this is a dft I will be using a Stack()
##          I want to push the current value into the stack
##          stack Stack()
##
##          loop through stack if there is a value in it, because stack will hold
##          the current node which are values I will be going through and if the stack
##          is empty then I have no more values to check that are connected to my 
##          starting node
##
##              pop it from the stack and hold it in a variable
##              current_node int
##
##              need to get the neighbors of current node
##              neigbors set()
##
##              don't need to check for visited nodes as the path is one directional
##              with no repeated connections
##
##              check if current node has any neihbors
##              if it does then:
##                  copy existing path and add
##                  add neihbors to the copied path
##                  add path to stack
##              else:
##                  add current path to final path
##              
##          after loop
##              compare which path is the largest
##              if there are multiple largest then collect them in a list and
##              compare them, index of smallest value in the list will be used
##              to determine which final path should be used

# 9   7   6
#  \   \ / \
#   8   5   3
#  / \ /   / \
# 11  4   2   1
#              \
#               10
#
# [[6]] stack push
#
# [] stack pop
# current_path = [6]
# current_node = 6
# neighbors = {5, 3}
# [6] copy path
# [6, 5] add neighbor
# [[6, 5]] stack push
# [6] copy path
# [6, 3] add neihbor
# [[6, 5], [6, 3]] stack push

# [[6, 5]] stack pop
# current_path = [6, 3]
# current_node = 3
# neighbors = {2, 1}
# [6, 3] copy path
# [6, 3, 2] add neighbor
# [[6, 5], [6, 3, 2]] stack push
# [6, 3] copy path
# [6, 3, 1] add neighbor
# [[6, 5], [6, 3, 2], [6, 3, 1]] stack push

# [[6, 5], [6, 3, 2]] stack pop
# current_path = [6, 3, 1]
# current_node = 1
# neighbors = {10}
# [6, 3, 1] copy path
# [6, 3, 1, 10] add neighbor
# [[6, 5], [6, 3, 2], [6, 3, 1, 10]] stack push

# [[6, 5], [6, 3, 2]] stack pop
# current_path = [6, 3, 1, 10]
# current_node = 10
# neighbors = {}
# final_paths = [[6, 3, 1, 10]]

# [[6, 5]] stack pop
# current_path = [6, 3, 2]
# current_node = 2
# neighbors = {}
# final_paths = [[6, 3, 1, 10], [6, 3, 2]]

# [[6, 5]] stack pop
# current_path = [6, 3, 2]
# current_node = 2
# neighbors = {}
# final_paths = [[6, 3, 1, 10], [6, 3, 2]]

# [] stack pop
# current_path = [6, 5]
# current_node = 5
# neighbors = {4}
# [6, 5] copy path
# [6, 5, 4] add neighbor
# [[6, 5, 4]] stack push

# [] stack pop
# current_path = [6, 5, 4]
# current_node = 4
# neighbors = {}
# final_paths = [[6, 3, 1, 10], [6, 3, 2], [6, 5, 4]]

# stack empty
# find largest array, if multiple then get the last value from all and compare

# Execute
class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

def earliest_ancestor(ancestors, starting_node):
    paths = [starting_node]
    final_paths = []
    largest_paths = []
    ancestor_graph = {}
    ancestor_stack = Stack()

    ancestor_stack.push(paths)

    for parent_child in ancestors:
        ## in this for loop I am taking the child and using it as
        ## the key, because I want the direction of the graph to be
        ## pointed in the opossite direction and be able to tell
        ## when i've finished a path by it having no neighbors
        if parent_child[1] in ancestor_graph:
            ancestor_graph[parent_child[1]].add(parent_child[0])
        else:
            ancestor_graph[parent_child[1]] = {parent_child[0]}

    while ancestor_stack.size():
        current_path = ancestor_stack.pop()
        current_node = current_path[-1]

        ## checks if current_node has neighbors
        ## if it does not then it appends the
        ## current_path to the list of final_paths
        ## else it gets the neighbors fo the current_node
        ## and pushes the neighbors new_paths to the stack
        if current_node not in ancestor_graph:
            final_paths.append(current_path)
        else:
            neighbors = ancestor_graph[current_node]
            for neighbor in neighbors:
                new_path = current_path[:]
                new_path.append(neighbor)
                ancestor_stack.push(new_path)

    if len(final_paths[0]) == 1:
        return -1

    for path in final_paths:
        if len(largest_paths) == 0:
            largest_paths.append(path)
        else:
            if len(path) > len(largest_paths[0]):
                largest_paths = []
                largest_paths.append(path)
            elif len(path) == len(largest_paths[0]):
                largest_paths.append(path)

    min_value = largest_paths[0][-1]
    for path in largest_paths:
        if path[-1] < min_value:
            min_value = path[-1]
        
    return min_value
# Review