from Node import Node


class AStar:
    def __init__(self, arc_cost, h, f, get_neighbour_states, node_id, ui, start, end):
        self.arc_cost = arc_cost  # g function
        self.h = h  # h function
        self.f = f  # Function for getting next node

        self.get_neighbour_states = get_neighbour_states  # Function for getting a node's neighbour states
        self.node_id = node_id  # Function for generating node ID
        self.ui = ui  # Function for drawing the UI representation of the solution

        self.start = Node(None, self.arc_cost, self.h(start, end), start, self.node_id(start))  # Start node
        self.end = Node(None, self.arc_cost, 0, end, self.node_id(end))  # End (goal) node

        self.open = []  # List of open nodes
        self.closed = []  # List of closed nodes

        self.id_cache = {self.start.id: self.start}  # For checking if a state has been discovered before
        self.open_node(self.start)  # Adds start node to list of open nodes

        self.run()

    # Adds node to open list. Updates state of node
    def open_node(self, node):
        node.status = True

        self.open.append(node)

    # Adds node to closed list. Updates state of node
    def close_node(self, node):
        node.status = False

        self.open.remove(node)
        self.closed.append(node)

    # Picks the next node to expand and closes it. Also updates ui
    def pick_next_node(self):
        node = self.f(self.open)

        self.ui(node)
        self.close_node(node)

        return node

    # Generates a new node
    def generate_new_node(self, parent, state):
        node = Node(parent, self.arc_cost, self.h(state, self.end.state), state, self.node_id(state))
        self.id_cache[node.id] = node

        return node

    # Returns the proper neighbour node; either a new node or the reference to a node.
    # Updates node children if necessary
    def get_neighbour_node(self, node, state):
        neighbour_id = self.node_id(state)

        if neighbour_id == node.id:
            return

        if neighbour_id in self.id_cache:
            neighbour = self.id_cache[neighbour_id]
            node.add_child(neighbour)
        else:
            neighbour = self.generate_new_node(node, state)

        return neighbour

    # The agenda loop. Finds the path to the goal
    def agenda_loop(self):
        while True:
            if not self.open:
                print 'No solution found!'

                exit()

            node = self.pick_next_node()

            if node.id == self.end.id:
                return self.build_path(node), self.open, self.closed

            for neighbour_state in self.get_neighbour_states(node.state):
                neighbour = self.get_neighbour_node(node, neighbour_state)

                if not neighbour:
                    continue

                if neighbour.status is None:
                    self.open_node(neighbour)
                elif node.g + self.arc_cost(node.state, neighbour.state) < neighbour.g:
                    neighbour.set_new_parent(node)

    # Reports the number of open, closed, and total nodes expanded
    @staticmethod
    def report(open_nodes, closed_nodes):
        print 'Open: %d, closed: %s, total: %d' % (
            len(open_nodes),
            len(closed_nodes),
            len(open_nodes)+len(closed_nodes)
        )

    # Builds the final path. Returns a list of the nodes in the path
    @staticmethod
    def build_path(node):
        path = []

        while node.parent:
            path.append(node)

            node = node.parent

        return reversed(path)

    # Runs the A* algorithm. Reports final path
    def run(self):
        path, open_nodes, closed_nodes = self.agenda_loop()

        self.report(open_nodes, closed_nodes)
