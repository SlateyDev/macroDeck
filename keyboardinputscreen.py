import pygame

from button import Button
from gamescreen import GameScreen


class KeyboardInputScreen(GameScreen):
    def __init__(self, game, action_callback=None):
        keys = [
            ["`", (0, 0, 1, 1)],
            ["1", (1, 0, 1, 1)],
            ["2", (2, 0, 1, 1)],
            ["3", (3, 0, 1, 1)],
            ["4", (4, 0, 1, 1)],
            ["5", (5, 0, 1, 1)],
            ["6", (6, 0, 1, 1)],
            ["7", (7, 0, 1, 1)],
            ["8", (8, 0, 1, 1)],
            ["9", (9, 0, 1, 1)],
            ["0", (10, 0, 1, 1)],
            ["-", (11, 0, 1, 1)],
            ["+", (12, 0, 1, 1)],
            ["Backspace", (13, 0, 2, 1)],

            ["Tab", (0, 1, 1.5, 1)],
            ["Q", (1.5, 1, 1, 1)],
            ["W", (2.5, 1, 1, 1)],
            ["E", (3.5, 1, 1, 1)],
            ["R", (4.5, 1, 1, 1)],
            ["T", (5.5, 1, 1, 1)],
            ["Y", (6.5, 1, 1, 1)],
            ["U", (7.5, 1, 1, 1)],
            ["I", (8.5, 1, 1, 1)],
            ["O", (9.5, 1, 1, 1)],
            ["P", (10.5, 1, 1, 1)],
            ["[", (11.5, 1, 1, 1)],
            ["]", (12.5, 1, 1, 1)],
            ["\\", (13.5, 1, 1.5, 1)],

            ["Caps", (0, 2, 1.75, 1)],
            ["A", (1.75, 2, 1, 1)],
            ["S", (2.75, 2, 1, 1)],
            ["D", (3.75, 2, 1, 1)],
            ["F", (4.75, 2, 1, 1)],
            ["G", (5.75, 2, 1, 1)],
            ["H", (6.75, 2, 1, 1)],
            ["J", (7.75, 2, 1, 1)],
            ["K", (8.75, 2, 1, 1)],
            ["L", (9.75, 2, 1, 1)],
            [";", (10.75, 2, 1, 1)],
            ["'", (11.75, 2, 1, 1)],
            ["Enter", (12.75, 2, 2.25, 1)],

            ["Shift", (0, 3, 2.5, 1)],
            ["Z", (2.5, 3, 1, 1)],
            ["X", (3.5, 3, 1, 1)],
            ["C", (4.5, 3, 1, 1)],
            ["V", (5.5, 3, 1, 1)],
            ["B", (6.5, 3, 1, 1)],
            ["N", (7.5, 3, 1, 1)],
            ["M", (8.5, 3, 1, 1)],
            [",", (9.5, 3, 1, 1)],
            [".", (10.5, 3, 1, 1)],
            ["/", (11.5, 3, 1, 1)],
            ["Shift", (12.5, 3, 2.5, 1)],

            ["Ctrl", (0, 4, 1.5, 1)],
            ["Alt", (1.5, 4, 1.5, 1)],
            ["", (3, 4, 9, 1)],
            ["Alt", (12, 4, 1.5, 1)],
            ["Ctrl", (13.5, 4, 1.5, 1)],

            ["Num", (17 + 0, 0, 1, 1)],
            ["/", (17 + 1, 0, 1, 1)],
            ["*", (17 + 2, 0, 1, 1)],
            ["-", (17 + 3, 0, 1, 1)],
            ["7", (17 + 0, 1, 1, 1)],
            ["8", (17 + 1, 1, 1, 1)],
            ["9", (17 + 2, 1, 1, 1)],
            ["+", (17 + 3, 1, 1, 2)],
            ["4", (17 + 0, 2, 1, 1)],
            ["5", (17 + 1, 2, 1, 1)],
            ["6", (17 + 2, 2, 1, 1)],
            ["1", (17 + 0, 3, 1, 1)],
            ["2", (17 + 1, 3, 1, 1)],
            ["3", (17 + 2, 3, 1, 1)],
            ["Enter", (17 + 3, 3, 1, 2)],
            ["0", (17 + 0, 4, 2, 1)],
            [".", (17 + 2, 4, 1, 1)],
        ]

        keys_x = 17 + 4
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

    def handle_touch_down(self, coords):
        self.mouse_down_action(1, coords)

    def handle_touch_up(self, coords):
        self.mouse_up_action(1, coords)

    def handle_event(self, event):
        pass
        #if event.type == pygame.MOUSEBUTTONDOWN:
        #    pos = pygame.mouse.get_pos()
        #    self.mouse_down_action(event.button, pos)
        #elif event.type == pygame.MOUSEBUTTONUP:
        #    pos = pygame.mouse.get_pos()
        #    self.mouse_up_action(event.button, pos)

    def mouse_down_action(self, button: int, pos: (int, int)):
        if button == 1:
            self.mouse_down_button = self.get_pressed_button(pos)

    def mouse_up_action(self, button: int, pos: (int, int)):
        if button == 1:
            if self.mouse_down_button == self.get_pressed_button(pos):
                self.selected_button = self.mouse_down_button
                if self.action_callback is not None:
                    self.action_callback(self.buttons[self.selected_button])
