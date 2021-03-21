import pygame

from button import Button
from gamescreen import GameScreen


class HostPortInputScreen(GameScreen):
    def __init__(self, game, action_callback=None):
        keys = [
            ["7", (0, 0, 1, 1)],
            ["8", (1, 0, 1, 1)],
            ["9", (2, 0, 1, 1)],
            ["4", (0, 1, 1, 1)],
            ["5", (1, 1, 1, 1)],
            ["6", (2, 1, 1, 1)],
            ["1", (0, 2, 1, 1)],
            ["2", (1, 2, 1, 1)],
            ["3", (2, 2, 1, 1)],
            ["0", (0, 3, 2, 1)],
            [".", (2, 3, 1, 1)],
            ["DEL", (0, 4, 3, 1)]
        ]

        keys_x = 3
        # keys_y = 5
        key_width = 40
        key_height = 40
        key_padding = 8

        self.game = game
        self.buttons = []
        for index, button in enumerate(keys):
            self.buttons.append(Button(self.game,
                                       button[0],
                                       (self.game.screen_width / 2
                                        - (keys_x * ((key_width + key_padding) - key_padding)) / 2
                                        + (key_width + key_padding) * button[1][0],
                                        100 + (key_height + key_padding) * button[1][1],
                                        key_width * button[1][2] + key_padding * (button[1][2] - 1),
                                        key_height * button[1][3] + key_padding * (button[1][3] - 1))))
        self.action_callback = action_callback

        self.mouse_down_button = None
        self.selected_button = None

    def get_pressed_button(self, pos: (int, int)):
        for index, button in enumerate(self.buttons):
            if button.x <= pos[0] <= button.x + button.w and button.y <= pos[1] <= button.y + button.h:
                return index

    def render(self):
        self.game.game_screen.fill((32, 32, 176), (50, 50, self.game.screen_width - 100, self.game.screen_height - 100))

        for index, button in enumerate(self.buttons):
            button.render(index == self.selected_button)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            self.mouse_down_action(event.button, pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            self.mouse_up_action(event.button, pos)

    def mouse_down_action(self, button: int, pos: (int, int)):
        if button == 1:
            self.mouse_down_button = self.get_pressed_button(pos)

    def mouse_up_action(self, button: int, pos: (int, int)):
        if button == 1:
            if self.mouse_down_button == self.get_pressed_button(pos):
                self.selected_button = self.mouse_down_button
                if self.action_callback is not None:
                    self.action_callback(self.selected_button)
