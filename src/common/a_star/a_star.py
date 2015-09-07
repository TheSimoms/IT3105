import time


class AStar(object):
    def __init__(self, task_space, start, end, ui, sleep_duration=0.0):
        self.task_space = task_space  # Task space
        self.start = start  # Start node
        self.end = end  # End (goal) node

        self.ui = ui
        self.sleep_duration = sleep_duration  # Time to sleep between iterations. So that one can see the steps taken

        self.open = []  # List of open nodes
        self.closed = []  # List of closed nodes

        self.id_cache = {self.start.id: self.start}  # For checking if a state has been discovered before
        self.open_node(self.start)  # Adds start node to list of open nodes

    # Function to pick next node
    def f(self):
        return sorted(self.open, key=lambda x: -1 if x.is_solution() else (x.g+x.h))[0]

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
        node = self.f()

        self.close_node(node)
        self.ui(node)

        return node

    # The agenda loop. Finds the path to the goal
    def agenda_loop(self):
        while True:
            if not self.open:
                print('No solution found!')

                return None, self.open, self.closed

            node = self.pick_next_node()

            if node.is_solution():
                return self.build_path(node), self.open, self.closed

            for neighbour in node.generate_neighbours(self.task_space):
                if neighbour.id in self.id_cache:
                    neighbour = self.id_cache[neighbour.id]

                if neighbour.status is None:
                    self.id_cache[neighbour.id] = neighbour
                    self.open_node(neighbour)
                elif node.g + node.arc_cost(neighbour.state) < neighbour.g:
                    neighbour.set_new_parent(node)

            if self.sleep_duration:
                time.sleep(self.sleep_duration)

    # Reports the number of open, closed, and total nodes expanded
    def report(self, open_nodes, closed_nodes):
        raise NotImplementedError

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
