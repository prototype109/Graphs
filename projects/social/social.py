# Understand
## Social connection application
## Input: dictionary{key(int) : set(int)}
## From the input I need to traverse through the relationships
## between the user_id which is an int and the graph that is generated and
## stored in self.friendships. I need to find the shortest path between the
## user_id and the other nodes in the graph so I am thinking of using a BFS.
## That means I need a Queue() to store my path.
import random

class User:
    def __init__(self, name):
        self.name = name

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

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def fisher_yates_shuffel(self, l):
        for i in range(0, len(l)):
            random_index = random.randint(i, len(l) - 1)
            l[i], l[random_index] = l[random_index], l[i]

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        for user in range(num_users):
            self.add_user(user)

        # Create friendships
        friendship_combinations = []

        for user in range(1, self.last_id + 1):
            for friend in range(1, self.last_id + 1):
                friendship_combinations.append((user, friend))

        self.fisher_yates_shuffel(friendship_combinations)

        total_friendships = num_users * avg_friendships

        friends_to_make = friendship_combinations[:(total_friendships // 2)]

        for friendship in friends_to_make:
            self.add_friendship(friendship[0], friendship[1])

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        path = [user_id]
        q = Queue()
        q.enqueue(path)

        visited[user_id] = []
        # Need a while loop
        while q.size():
            current_path = q.dequeue()

            current_vertex = current_path[-1]

            if current_vertex == user_id:
                visited[current_vertex] = current_path
            
            if current_vertex not in visited:
                visited[current_vertex] = []
                neighbors = self.friendships[current_vertex]
                for neighbor in neighbors:
                   neighbor_path = current_path[:]
                   neighbor_path.append(neighbor)
                   q.enqueue(neighbor_path)
        
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    # connections = sg.get_all_social_paths(1)
    # print(connections)
