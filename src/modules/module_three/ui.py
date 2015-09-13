import pygame


class Ui:
    def __init__(self, dimensions, height=800):
        self.screen = None
        self.clock = None

        self.dimensions = dimensions

        self.background = (255, 255, 255)
        self.uncertain = (128, 128, 128)
        self.filled = (0, 0, 255)

        self.cell_size = 800 / self.dimensions[0]
        self.window_size = [height, self.cell_size * self.dimensions[1]]

        self.init_game('Nonogram')

    def init_game(self, title):
        pygame.init()

        self.screen = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption(title)

    def draw_rect(self, x, y, color):
        pygame.draw.rect(
            self.screen, color,
            [
                self.cell_size * x,
                self.window_size[1] - self.cell_size - self.cell_size * y,
                self.cell_size,
                self.cell_size
            ]
        )

    def update_ui(self, node):
        self.screen.fill(self.background)

        variables = node.state.variables

        for x in range(self.dimensions[1]):
            column = variables['c%d' % x]
            column_len = len(column)

            for y in range(self.dimensions[0]):
                row = variables['r%d' % y]
                row_len = len(row)

                if column_len > 1 or row_len > 1:
                    color = self.uncertain
                else:
                    color = self.filled if int(column[0].string[y]) else self.background

                self.draw_rect(x, y, color)
                self.clock.tick(60)

        pygame.display.update()
