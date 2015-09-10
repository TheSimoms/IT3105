import time


class AStar(object):
    def __init__(self, start, ui=None, end=None, task_space=None, sleep_duration=0.0):
        self.task_space = task_space  # Task space.May be needed for nodes in order to generate neighbours

        self.start = start  # Start node
        self.end = end  # End (goal) node

        self.ui = ui  # Function that updates ui
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

        if self.ui:
            self.ui(node)

        return node

    # The agenda loop. Finds the path to the goal
    def agenda_loop(self):
        while self.open:
            node = self.pick_next_node()

            # Search is finished. Return path and lists of nodes
            if node.is_solution():
                return node, self.open, self.closed

            # Expand current node
            for neighbour in node.generate_neighbours(self.task_space):
                # If node already has been generated, replace
                if neighbour.id in self.id_cache:
                    neighbour = self.id_cache[neighbour.id]

                    if node.g + node.arc_cost(neighbour.state) < neighbour.g:
                        neighbour.set_new_parent(node)
                else:
                    self.open_node(neighbour)
                    self.id_cache[neighbour.id] = neighbour

            if self.sleep_duration:
                time.sleep(self.sleep_duration)

        print('No solution found!')

        return None, self.open, self.closed

    # Reports the number of open, closed, and total nodes expanded
    def report(self, final_node, open_nodes, closed_nodes):
        path = self.build_path(final_node)

        print('Path length: %d' % len(path))
        print('Open nodes: %d, closed nodes: %s, total nodes: %d' % (
            len(open_nodes),
            len(closed_nodes),
            len(open_nodes)+len(closed_nodes)
        ))

    # Builds the final path. Returns a list of the nodes in the path
    @staticmethod
    def build_path(node):
        path = []

        while node.parent:
            path.append(node)

            node = node.parent

        return list(reversed(path))

    # Runs the A* algorithm. Reports final path
    def run(self):
        final_node, open_nodes, closed_nodes = self.agenda_loop()

        self.report(final_node, open_nodes, closed_nodes)

        return final_node, open_nodes, closed_nodes
