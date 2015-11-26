import pygame


class Ui:
    def __init__(self, height=800):
        self.screen = None
        self.clock = None

        self.background = (255, 255, 255)

        self.cell_colors = [
            (255, 153, 153),
            (255, 127, 127),
            (255, 102, 102),
            (255, 76, 76),
            (255, 50, 50),
            (255, 25, 25),
            (255, 0, 0),
            (229, 0, 0),
            (204, 0, 0),
            (178, 0, 0),
            (153, 0, 0),
            (127, 0, 0),
            (102, 0, 0),
            (76, 0, 0),
            (51, 0, 0),
            (25, 0, 0),
            (0, 0, 0)
        ]

        self.cell_size = int(height / 4)
        self.font_size = int(self.cell_size / 3)

        self.window_size = [height, self.cell_size * 4]

        self.font = None

        self.init_game('2048')

    def init_game(self, title):
        pygame.init()

        self.font = pygame.font.SysFont('Comic Sans MS', self.font_size)

        self.screen = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption(title)

    def draw_rect(self, x, y, color):
        pygame.draw.rect(
            self.screen, color,
            [
                self.cell_size * x,
                self.cell_size * y,
                self.cell_size,
                self.cell_size
            ]
        )

    def draw_text(self, x, y, value):
        self.screen.blit(
            self.font.render(value, 1, (0, 0, 0)),
            (
                self.cell_size * (0.5 + x) - 0.30 * self.font_size*len(value),
                self.cell_size * (0.5 + y) - 50
            )
        )

    def update_ui(self, state):
        self.screen.fill(self.background)

        for x in [0, 1, 2, 3]:
            for y in [0, 1, 2, 3]:
                cell = state[x][y]

                if cell:
                    self.draw_rect(x, y, self.cell_colors[cell.value])
                    self.draw_text(x, y, str(2 ** cell.value))

                    self.clock.tick(60)

        pygame.display.update()
