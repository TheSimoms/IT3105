import time


class AStar(object):
    def __init__(self, start, ui=None, end=None, task_space=None, sleep_duration=0.0):
        self.task_space = task_space  # Task space.May be needed for nodes in order to generate neighbours

        self.start = start  # Start node
        self.end = end  # End (goal) node. Optional

        self.ui = ui  # Function that updates ui
        self.sleep_duration = sleep_duration  # Time to sleep between iterations. So that one can see the steps taken

        self.open = []  # List of open nodes
        self.closed = []  # List of closed nodes

        self.id_cache = {self.start.id: self.start}  # For checking if a state has been discovered before
        self.open_node(self.start)  # Adds start node to list of open nodes

    # Function to pick next node. May be overwritten to implement breadth- of depth first searches
    def f(self):
        return min(self.open, key=lambda x: (x.g+x.h))

    # Adds node to open list. Updates state of node
    def open_node(self, node):
        node.status = True

        self.id_cache[node.id] = node  # Adds node ID to cache
        self.open.append(node)  # Adds node to open list

    # Adds node to closed list. Updates state of node
    def close_node(self, node):
        node.status = False

        self.open.remove(node)  # Removes node from open list
        self.closed.append(node)  # Adds node to closed list

    # Picks the next node to expand. Closes it. Also updates ui
    def pick_next_node(self):
        node = self.f()

        self.close_node(node)

        # Show current state in the UI
        if self.ui:
            self.ui(node, self.open, self.closed)

        return node

    # The agenda loop. Finds the path to the goal
    def agenda_loop(self):
        while self.open:
            node = self.pick_next_node()  # Picks next node

            # Search is finished. Return goal node, and lists of nodes
            if node.is_solution():
                return node, self.open, self.closed

            # Expand current node
            for neighbour in node.generate_neighbours(self.task_space):
                # If neighbour has already been generated, replace the reference. Else open node
                if neighbour.id in self.id_cache:
                    neighbour = self.id_cache[neighbour.id]

                    # Sets current node as parent when necessary
                    if node.g + node.arc_cost(neighbour.state) < neighbour.g:
                        neighbour.set_new_parent(node)
                else:
                    self.open_node(neighbour)

            # Sleeps, if wanted. To allow changes in UI to be seen
            if self.sleep_duration:
                time.sleep(self.sleep_duration)

        print('No solution found!')

        # Returns open and closed nodes for reporting
        return None, self.open, self.closed

    # Reports the number of open, closed, and total nodes expanded
    def report(self, final_node, open_nodes, closed_nodes):
        path = self.build_path(final_node)

        print('Path length: %d' % len(path))
        print('Open nodes: %d, closed nodes: %s, total nodes: %d\n' % (
            len(open_nodes),
            len(closed_nodes),
            len(open_nodes)+len(closed_nodes)
        ))

    # Builds the final path. Returns a list of the nodes in the path
    @staticmethod
    def build_path(node):
        path = []

        # Traverses parents all the way to the start node
        while node.parent:
            path.append(node)  # Adds node to the path

            node = node.parent

        # Returns path, from start to finish
        return list(reversed(path))

    # Runs the A* algorithm. Reports final path
    def run(self):
        # Runs the algorithm
        final_node, open_nodes, closed_nodes = self.agenda_loop()

        # Reports the results
        self.report(final_node, open_nodes, closed_nodes)

        # Returns final node, and list of nodes. In case they should be used for something later
        return final_node, open_nodes, closed_nodes
