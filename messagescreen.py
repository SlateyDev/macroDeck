import pygame

from button import Button
from gamescreen import GameScreen


class MessageScreen(GameScreen):
    def __init__(self, game, message: str, buttons=None, action_callback=None):
        button_size = [150, 50]
        button_padding = [25, 25]

        self.game = game
        self.message = message
        self.buttons = []
        for index, button in enumerate(buttons):
            self.buttons.append(Button(self.game,
                                       button,
                                       (self.game.screen_width / 2
                                        - (len(buttons) * (button_size[0] + button_padding[0]) - button_padding[0]) / 2
                                        + (button_size[0] + button_padding[0]) * index,
                                        self.game.screen_height - 100 - button_padding[1], button_size[0],
                                        button_size[1])))
        self.action_callback = action_callback

        self.mouse_down_button = None
        self.selected_button = None

    def get_pressed_button(self, pos: (int, int)):
        for index, button in enumerate(self.buttons):
            if button.x <= pos[0] <= button.x + button.w and button.y <= pos[1] <= button.y + button.h:
                return index

    def render(self):
        self.game.game_screen.fill((32, 32, 176), (50, 50, self.game.screen_width - 100, self.game.screen_height - 100))

        lines = self.message.split("\n")

        for line_index, line in enumerate(lines):
            text_rect = self.game.font.get_rect(line)
            self.game.font.render_to(self.game.game_screen,
                                     (self.game.screen_width / 2 - text_rect.width / 2,
                                      self.game.screen_height / 2 - (text_rect.height + 4) * len(
                                          lines) / 2 + (text_rect.height + 4) * line_index),
                                     line, (255, 255, 255))

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
