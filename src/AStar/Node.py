class Node:
    def __init__(self, parent, arc_cost, h, state, node_id):
        self.parent = None
        self.children = []

        self.arc_cost = arc_cost

        self.g = 0
        self.h = h
        self.state = state
        self.id = node_id
        self.status = None

        self.add_parent(parent)

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)

    def add_parent(self, new_parent):
        if new_parent:
            self.parent = new_parent
            self.parent.children.append(self)

            self.g = new_parent.g + self.arc_cost(new_parent.state, self.state)

    def remove_parent(self):
        if self.parent:
            self.parent.children.remove(self)
            self.parent = None

    def set_new_parent(self, new_parent):
        self.remove_parent()
        self.add_parent(new_parent)

        # Updates children
        for child in self.children:
            if child.parent != self:
                new_g = self.g + self.arc_cost(self.state, child.state)

                if new_g < child.g:
                    child.set_new_parent(self)
