from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

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

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class MazeRunner():
    def __init__(self, path):
        self.path = path
        self.visited = {}
        self.touched_rooms = set()
        self.all_rooms = {num for num in range(500)}

    def get_opposite_room(self, room_direction):
        if room_direction == 'n':
            return 's'
        elif room_direction == 'e':
            return 'w'
        elif room_direction == 'w':
            return 'e'
        else:
            return 'n'

    def dead_end(self, start_room):
        room_queue = Queue()

        path = [(start_room, None)]

        visited = set()

        room_queue.enqueue(path)

        found_unvisited_room = False

        while room_queue.size():
            current_path = room_queue.dequeue()
            current_room = current_path[-1][0]  

            if current_room not in visited:
                visited.add(current_room)
                exits = self.visited[current_room].items()
                
                for direction, room_id in exits:
                    new_path = current_path[:]
                    new_path.append((room_id, direction))
                    room_queue.enqueue(new_path)
                    if room_id is None:
                        return [direction for room, direction in current_path[1:]]

    def run_maze(self):
        s = Stack()

        just_spawned = True

        s.push(self.path)

        while len(self.visited) < len(room_graph):
            self.path = s.pop()
            can_move = False
            unvisited_room_count = 0
            current_room = player.current_room.id

            if just_spawned:
                previous_room_id = None
                previous_direction = None
                current_direction = None

            if current_room not in self.visited:
                directions = player.current_room.get_exits()
                self.visited[current_room] = {key: None for key in directions}
                if not just_spawned:
                    self.visited[current_room][self.get_opposite_room(previous_direction)] = previous_room_id
                else:
                    just_spawned = False
            
            room_status = self.visited[current_room]

            for direction, room_value in room_status.items():
                if room_value is None:
                    unvisited_room_count += 1

                    new_path = self.path[:]
                    current_direction = direction
                    new_path.append(direction)
                    s.push(new_path)

                    can_move = True

            if unvisited_room_count == 0:
                bfs_result = self.dead_end(current_room)
                if bfs_result:
                    reverse_iterate = len(bfs_result) - 1
                    for direction in bfs_result:
                        previous_room_id = player.current_room.id
                        previous_direction = direction
                        self.path.append(direction)
                        player.travel(direction)
                    s.push(self.path)

            unvisited_room_count = 0
                
            if can_move:
                previous_room_id = current_room
                previous_direction = current_direction
                
                player.travel(current_direction)

                self.visited[previous_room_id][previous_direction] = player.current_room.id
runner = MazeRunner(traversal_path)
runner.run_maze()
traversal_path = runner.path
# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
