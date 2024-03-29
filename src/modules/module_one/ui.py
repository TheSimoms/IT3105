import pygame


class Ui:
    def __init__(self, title, task_space):
        self.task_space = task_space

        self.screen = None
        self.clock = None

        self.wall = (0, 0, 0)
        self.route = (255, 0, 0)
        self.ground = (255, 255, 255)
        self.open = (127, 127, 127)
        self.closed = (64, 64, 64)

        self.window_size = [800, 800]
        self.cell_size = [self.window_size[0] // len(self.task_space), self.window_size[0] // len(self.task_space[0])]

        self.init_game(title)

    def init_game(self, title):
        pygame.init()

        self.screen = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption(title)

    def draw_rect(self, x, y, color):
        pygame.draw.rect(self.screen, color,
                         [self.cell_size[0] * x,
                          self.window_size[1]-self.cell_size[1]-self.cell_size[1] * y,
                          self.cell_size[0],
                          self.cell_size[1]])

    def draw_node(self, node, open_nodes, closed_nodes):
        self.screen.fill(self.ground)

        for open_node in open_nodes:
            self.draw_rect(open_node.state[0], open_node.state[1], self.open)

        for closed_node in closed_nodes:
            self.draw_rect(closed_node.state[0], closed_node.state[1], self.closed)

        for x in xrange(len(self.task_space)):
            for y in xrange(len(self.task_space[x])):
                if self.task_space[x][y] == 'x':
                    self.draw_rect(x, y, self.wall)

        while node:
            self.draw_rect(node.state[0], node.state[1], self.route)

            node = node.parent

        self.clock.tick(60)

        pygame.display.update()
