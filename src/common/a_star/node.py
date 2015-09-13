class Node(object):
    def __init__(self, parent, state, end_state=None):
        self.state = state  # State of the node
        self.id = self.generate_id()  # Node identifier

        self.parent = None  # Parent node
        self.children = []  # List of children
        self.status = None  # State of the node. Either None (not discovered), True (opened) or False (closed)
        self.end_state = end_state  # Goal state

        self.g = 0  # Initial g value. Is updated when a new parent is set
        self.h = self.heuristic(self.end_state)  # h value

        self.add_parent(parent)  # Adds initial parent

    # Function for getting neighbour states
    def generate_neighbours(self, task_space=None):
        raise NotImplementedError

    # Node identifier
    def generate_id(self):
        raise NotImplementedError

    # h function
    def heuristic(self, end_state=None):
        raise NotImplementedError

    # Returns whether the node is a solution or not
    def is_solution(self):
        raise NotImplementedError

    # g function
    def arc_cost(self, neighbour_state=None):
        return 1

    # Adds a new child
    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)

    # Adds a parent for the node
    def add_parent(self, new_parent):
        if new_parent:
            self.parent = new_parent  # Sets self as children of new parent
            self.parent.add_child(self)  # Adds self as children to new parent

            self.g = new_parent.g + new_parent.arc_cost(self.state)  # Updates g value

    # Removes current parent
    def remove_parent(self):
        if self.parent:
            self.parent = None

    # Sets new parent
    def set_new_parent(self, new_parent):
        self.remove_parent()  # Removes old parent
        self.add_parent(new_parent)  # Sets new parent

        # Updates children's g value where necessary
        for child in self.children:
            if child.parent != self:
                new_g = self.g + self.arc_cost(child.state)  # Calculates new g for child

                # Sets self as new parent if new g is lower than former g
                if new_g < child.g:
                    child.set_new_parent(self)
