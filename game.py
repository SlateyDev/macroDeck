import sys

import pygame
import pygame.freetype
import evdev
import select
import subprocess
import random

from buttonscreen import ButtonScreen
from hostportinputscreen import HostPortInputScreen
from keyboardinputscreen import KeyboardInputScreen
from messagescreen import MessageScreen
from tcpclient import TCPClient

HOST = "www.google.com"
PORT = 80


class Game:
    def __init__(self):
        pygame.init()
        self.font = pygame.freetype.Font(None, 20)
        # display_info = pygame.display.Info()
        self.screen_width = 1280  # display_info.current_w
        self.screen_height = 400  # display_info.current_h
        self.screen_size = self.screen_width, self.screen_height
        self.game_screen = pygame.display.set_mode(self.screen_size, pygame.FULLSCREEN)
        pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
        self.screen_layers = []
        self.tcp_client = TCPClient()
        self.tcp_client.connect(HOST, PORT)

        self.message_screen: MessageScreen = None

        self.game_loop()

    def keyboard_button_action(self, action):
        if action.text == "Enter":
            self.screen_layers.remove(self.screen_layers[len(self.screen_layers) - 1])

    def macro_button_action(self, action):
        if action == 3:
            self.tcp_client.close()

    def not_connected_action(self, action):
        if action == 0:
            self.tcp_client.connect(HOST, PORT)
        elif action == 1:
            self.screen_layers.append(KeyboardInputScreen(self, self.keyboard_button_action))
        elif action == 2:
            sys.exit()

    def getPixelsFromCoordinates(self, coords):
        x = float(coords[0]) / float(4096) * float(self.screen_width)
        y = self.screen_height - float(coords[1]) / float(4096) * float(self.screen_height)
        return (int(x), int(y))

    def game_loop(self):
        touch = evdev.InputDevice("/dev/input/event0")
        touch.grab()
        print(touch)

        X = 0
        Y = 0
        MT_SLOT = 0
        p = (0,0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                if len(self.screen_layers) > 0:
                    self.screen_layers[len(self.screen_layers) - 1].handle_event(event)

            r,w,x = select.select([touch], [], [], 0)
            if (touch in r):
                for event in touch.read():
                    #if event.type == evdev.ecodes.EV_ABS or event.type == evdev.ecodes.EV_KEY:
                    #    print(event.type, event.code, event.value)
                    if event.type == evdev.ecodes.EV_ABS:
                        if event.code == 47:
                            MT_SLOT = event.value
                        elif event.code == 54:
                            if MT_SLOT == 0:
                                X = event.value
                                p = self.getPixelsFromCoordinates((X,Y))
                        elif event.code == 53:
                            if MT_SLOT == 0:
                                Y = event.value
                                p = self.getPixelsFromCoordinates((X,Y))
                        elif event.code == 1:
                            X = event.value
                            p = self.getPixelsFromCoordinates((X,Y))
                        elif event.code == 0:
                            Y = event.value
                            p = self.getPixelsFromCoordinates((X,Y))
                    elif event.type == evdev.ecodes.EV_KEY:
                        if event.code == 330 and event.value == 1:
                            if len(self.screen_layers) > 0:
                                self.screen_layers[len(self.screen_layers) - 1].handle_touch_down(p)
                        elif event.code == 330 and event.value == 0:
                            if len(self.screen_layers) > 0:
                                self.screen_layers[len(self.screen_layers) - 1].handle_touch_up(p)

            self.game_screen.fill((0, 0, 0))

            for layer in self.screen_layers:
                layer.render()

            # self.font.render_to(self.game_screen, (p[0],p[1]), str((p[0], p[1])), (255,255,255))

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
