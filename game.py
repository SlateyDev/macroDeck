import sys

import pygame
import pygame.freetype

from buttonscreen import ButtonScreen
from hostportinputscreen import HostPortInputScreen
from keyboardinputscreen import KeyboardInputScreen
from messagescreen import MessageScreen
from tcpclient import TCPClient

HOST = "127.0.0.1"
PORT = 80


class Game:
    def __init__(self):
        pygame.init()
        self.font = pygame.freetype.Font(None, 20)
        # display_info = pygame.display.Info()
        self.screen_width = 1280  # display_info.current_w
        self.screen_height = 400  # display_info.current_h
        self.screen_size = self.screen_width, self.screen_height
        self.game_screen = pygame.display.set_mode(self.screen_size)
        self.screen_layers = []
        self.tcp_client = TCPClient()
        self.tcp_client.connect(HOST, PORT)

        self.message_screen: MessageScreen = None

        self.game_loop()

    def macro_button_action(self, action):
        if action == 3:
            self.tcp_client.close()

    def not_connected_action(self, action):
        if action == 0:
            self.tcp_client.connect(HOST, PORT)
        elif action == 1:
            self.screen_layers.append(KeyboardInputScreen(self))
        elif action == 2:
            sys.exit()

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                if len(self.screen_layers) > 0:
                    self.screen_layers[len(self.screen_layers) - 1].handle_event(event)

            self.game_screen.fill((0, 0, 0))

            for layer in self.screen_layers:
                layer.render()

            if self.tcp_client.process():
                if self.tcp_client.connect_state == 0:
                    if self.screen_layers.__contains__(self.message_screen):
                        self.screen_layers.remove(self.message_screen)
                        self.message_screen = None

                    message = "Not connected"
                    if self.tcp_client.not_connected_error != "":
                        message += f"\n{self.tcp_client.not_connected_error}"
                    self.message_screen = MessageScreen(self, message, ["Reconnect", "Settings", "Exit"], self.not_connected_action)
                    self.screen_layers.append(self.message_screen)
                elif self.tcp_client.connect_state == 1:
                    if self.screen_layers.__contains__(self.message_screen):
                        self.screen_layers.remove(self.message_screen)
                        self.message_screen = None

                    message = "Attempting to connect"
                    self.message_screen = MessageScreen(self, message, [])
                    self.screen_layers.append(self.message_screen)
                elif self.tcp_client.connect_state == 2:
                    pass
                elif self.tcp_client.connect_state == 3:
                    if self.screen_layers.__contains__(self.message_screen):
                        self.screen_layers.remove(self.message_screen)
                        self.message_screen = None
                    self.screen_layers.append(ButtonScreen(self, self.macro_button_action))

            pygame.display.flip()
