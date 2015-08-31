class Node:
    def __init__(self, parent, arc_cost, h, state, node_id):
        self.parent = None  # Parent node
        self.children = []  # List of children

        self.arc_cost = arc_cost  # g function

        self.g = 0  # Initial g value. Is updated when a new parent is set
        self.h = h  # h value
        self.state = state  # State of the node
        self.id = node_id  # Node identifier
        self.status = None  # State of the node. Either None (not discovered), True (opened) or False (closed)

        self.add_parent(parent)  # Adds initial parent

    # Adds a new child
    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)

    # Adds a parent for the node
    def add_parent(self, new_parent):
        if new_parent:
            self.parent = new_parent  # Sets self as children of new parent
            self.parent.children.append(self)  # Adds self as children to new parent

            self.g = new_parent.g + self.arc_cost(new_parent.state, self.state)  # Updates g value

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
                new_g = self.g + self.arc_cost(self.state, child.state)  # Calculates new g for child

                # Sets self as new parent if new g is lower than former g
                if new_g < child.g:
                    child.set_new_parent(self)
