import pygame


class Ui:
    def __init__(self, vertices, edges, width, height):
        self.screen = None
        self.clock = None

        self.vertices = {
            vertex_id: vertex for vertex_id, vertex in vertices.items()
        }

        self.edges = edges

        self.window_size = [width+20, height+20]

        self.colors = {
            'black': (0, 0, 0),
            'red': (255, 0, 0),
            'orange': (255, 102, 0),
            'yellow': (255, 255, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'indigo': (46, 8, 84),
            'violet': (138, 43, 226),
            'pink': (255, 105, 180),
            'gray': (211, 211, 211),
            'chocolate': (210, 105, 30)
        }

        self.init_game('Vertex colouring')

        self.screen.fill((255, 255, 255))

        for edge in self.edges:
            self.draw_line(
                (self.vertices[edge[0]]['x'], self.vertices[edge[0]]['y']),
                (self.vertices[edge[1]]['x'], self.vertices[edge[1]]['y']),
            )


    def init_game(self, title):
        pygame.init()

        self.screen = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption(title)

    def draw_circle(self, x, y, color):
        pygame.draw.circle(
            self.screen,
            self.colors[color],
            (x, y),
            10
        )

    def draw_line(self, start_pos, end_pos):
        pygame.draw.line(
            self.screen,
            self.colors['black'],
            start_pos,
            end_pos
        )

    def update_ui(self, node, open_nodes, closed_nodes):
        variables = node.state.variables

        for variable in sorted(variables.keys()):
            domain = variables[variable]

            if len(domain) != 1:
                self.draw_circle(self.vertices[variable]['x'], self.vertices[variable]['y'], "black")
            else:
                self.draw_circle(self.vertices[variable]['x'], self.vertices[variable]['y'], variables[variable][0])

        self.clock.tick(60)

        pygame.display.update()
