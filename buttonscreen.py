import pygame

from button import Button
from gamescreen import GameScreen


class ButtonScreen(GameScreen):
    def __init__(self, game, action_callback=None):
        button_size = [100, 100]
        button_padding = [25, 25]
        button_margin = [25, 25]
        buttons = [10, 3]

        self.game = game
        self.action_callback = action_callback
        self.mouse_down_button = None
        self.selected_button = None
        self.buttons = []
        for y in range(buttons[1]):
            for x in range(buttons[0]):
                self.buttons.append(Button(game,
                                           str(y * buttons[0] + x + 1),
                                           ((button_size[0] + button_padding[0]) * x + button_margin[0],
                                            (button_size[1] + button_padding[1]) * y + button_margin[1], button_size[0],
                                            button_size[1])))

    def get_pressed_button(self, pos: (int, int)):
        for index, button in enumerate(self.buttons):
            if button.x <= pos[0] <= button.x + button.w and button.y <= pos[1] <= button.y + button.h:
                return index

    def render(self):
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
                    self.action_callback(self.selected_button)

