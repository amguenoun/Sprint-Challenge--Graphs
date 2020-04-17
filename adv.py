from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()

# Stack Class for DFT


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

# Queue Class for BFS


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

# Traversal Graph for keeping track of connections


class TraversalGraph:
    def __init__(self):
        self.rooms = {}

    def add_room(self, id, exits):
        '''
        Creates an entry in self.rooms: {id:{'n': '?', 's': '?', 'w': '?', 'e': '?'}}
        '''
        directions = {}
        for direction in exits:
            directions[direction] = '?'
        self.rooms[id] = directions

    def get_opposite_direction(self, direction):
        if direction == 'n':
            return 's'
        if direction == 's':
            return 'n'
        if direction == 'e':
            return 'w'
        if direction == 'w':
            return 'e'

    def connect_rooms(self, begin_room_id, end_room_id, direction):
        opposite_direction = self.get_opposite_direction(direction)
        self.rooms[begin_room_id][direction] = end_room_id
        self.rooms[end_room_id][opposite_direction] = begin_room_id


def get_unexplored_room_path(starting_room, t_map, direction):
    visited = set()
    queue = Queue()
    queue.enqueue(starting_room)
    path = {starting_room.id: []}
    while queue.size() > 0:
        room = queue.dequeue()
        if room.id not in visited:
            visited.add(room.id)
            if '?' in t_map.rooms[room.id].values():
                return path[room.id]
            exits = room.get_exits()
            for ex in exits:
                next_room = room.get_room_in_direction(ex)
                path[next_room.id] = path[room.id] + [ex]
                queue.enqueue(next_room)

    return [direction]


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"


# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)
traversal_map = TraversalGraph()

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# opposite = {'n':'s', 's':"n", "w":"e", "e":"w"}

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)
traversal_map.add_room(player.current_room.id, player.current_room.get_exits())

stack = Stack()
stack.push(player.current_room)
touched = set()

# while stack.size() > 0:
#     room = stack.pop()
#     if room.id not in touched:
#         touched.add(room.id)
#         exits = room.get_exits()
#         # if len(exits) == 1:
#         #     back_path = get_unexplored_room_path(room, traversal_map)
#         #     print("BACK", back_path)
#         #     print("FRONT", traversal_path)
#         #     traversal_path = traversal_path + back_path
#         for ex in exits:  # while exit length > 0, randomly pick and remove a direction
#             # traversal_path.append(ex)  # not working correctly
#             next_room = room.get_room_in_direction(ex)
#             if next_room.id not in traversal_map.rooms:
#                 traversal_map.add_room(next_room.id, next_room.get_exits())
#             traversal_map.connect_rooms(room.id, next_room.id, ex)
#             stack.push(next_room)

opposite = {'n': 's', 's': "n", "w": "e", "e": "w"}


def dft(room, direction=None):
    global traversal_path
    if room.id not in touched:
        print('ROOMID:', room.id)
        if room.id == 4:
            print('ROOM IS TOUCHED')
            print('ROOM DIRECTION', direction)
        if direction:
            traversal_path.append(direction)
        touched.add(room.id)
        exits = room.get_exits()
        if len(exits) == 1:  # This needs more work
            back_path = get_unexplored_room_path(
                room, traversal_map, direction)
            traversal_path += back_path
        for ex in exits:
            next_room = room.get_room_in_direction(ex)
            if next_room.id not in traversal_map.rooms:
                traversal_map.add_room(next_room.id, next_room.get_exits())
            traversal_map.connect_rooms(room.id, next_room.id, ex)
            dft(next_room, ex)


dft(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

listed = []
for room in visited_rooms:
    listed.append(room.id)
listed.sort()
print("VISITED ROOMS,", listed)
print('TOUCHED', touched)

print("traversal_path: ", traversal_path)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
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
