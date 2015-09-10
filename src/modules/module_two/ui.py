from threading import Thread
from Tkinter import Tk, Canvas as BaseCanvas


class Ui(Thread):
    def __init__(self, vertices, edges, width, height):
        Thread.__init__(self)

        self.vertices = vertices
        self.edges = edges

        self.width = width
        self.height = height

        self.root_window = None
        self.ui = None

        self.start()

    def quit(self):
        self.root_window.destroy()

    def run(self):
        self.root_window = Tk()

        self.root_window.protocol('WM_DELETE_WINDOW', self.quit)
        self.root_window.title('GAC + A*')

        self.ui = Canvas(self.root_window, self.vertices, self.edges, self.width, self.height)
        self.ui.pack()

        self.root_window.mainloop()

    def update_ui(self, node):
        if self.ui:
            self.ui.update_ui(node)


class Canvas(BaseCanvas):
    def __init__(self, parent_window, vertices, edges, width, height):
        BaseCanvas.__init__(self, parent_window, width=width, height=height)

        self.vertices = vertices
        self.edges = edges

        for edge in edges:
            self.create_line(
                vertices[edge[0]]['x'],
                vertices[edge[0]]['y'],
                vertices[edge[1]]['x'],
                vertices[edge[1]]['y'],
            )

        self.vertices = {
            vertex_id: self.create_circle(vertex['x'], vertex['y'], 10, fill="black")
            for vertex_id, vertex in vertices.items()
        }

    def create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def set_vertex_color(self, color, vertex_id):
        self.itemconfig(self.vertices[vertex_id], fill=color)

    def update_ui(self, node):
        variables = node.state.variables

        for variable, domain in variables.items():
            if len(domain) != 1:
                self.set_vertex_color("black", variable)
            else:
                self.set_vertex_color(domain[0], variable)
