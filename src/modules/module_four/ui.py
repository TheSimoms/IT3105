import pygame


class Ui:
    def __init__(self, height=800):
        self.screen = None
        self.clock = None

        self.background = (255, 255, 255)

        self.cell_colors = [
            (255, 255, 255),
            (244, 194, 194),
            (255, 194, 194),
            (255, 28, 0),
            (205, 92, 92),
            (227, 66, 52),
            (215, 59, 62),
            (206, 22, 32),
            (204, 0, 0),
            (178, 34, 34),
            (164, 0, 0),
            (128, 0, 0),
            (112, 28, 28),
            (60, 20, 20),
            (50, 20, 20),
            (25, 10, 10),
            (0, 0, 0),
        ]

        self.cell_size = height / 4
        self.window_size = [height, self.cell_size * 4]

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
                self.cell_size * y,
                self.cell_size,
                self.cell_size
            ]
        )

    def update_ui(self, state):
        self.screen.fill(self.background)

        for x in [0, 1, 2, 3]:
            for y in [0, 1, 2, 3]:
                cell = int(state[y*4+x])

                if cell:
                    self.draw_rect(x, y, self.cell_colors[cell])
                    self.clock.tick(60)

        pygame.display.update()
