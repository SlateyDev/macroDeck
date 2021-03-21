import pygame
import pygame.freetype
import sys
import select
import errno

from pygame.freetype import Font
from pygame.surface import Surface
import socket

screen: Surface
button_mask: Surface
my_font: Font

button_size = [100, 100]
button_padding = [25, 25]
button_margin = [25, 25]
buttons = [10, 3]

HOST = "google.com"
PORT = 80

screen_size = 1280, 400


def get_pressed_button(pos: (int, int)):
    for x in range(buttons[0]):
        for y in range(buttons[1]):
            if (button_size[0] + button_padding[0]) * x + button_margin[0] <= pos[0] <= (
                    button_size[0] + button_padding[0]) * x + button_margin[0] + button_size[0] \
                    and (button_size[1] + button_padding[1]) * y + button_margin[1] <= pos[1] <= (
                    button_size[1] + button_padding[1]) * y + button_margin[1] + button_size[1]:
                return y * buttons[0] + x


class Button:
    def __init__(self, surface, text: str, size: (int, int, int, int)):
        self.surface = surface
        self.text = text
        self.x = size[0]
        self.y = size[1]
        self.w = size[2]
        self.h = size[3]

    def render(self, selected: bool):
        self.surface.fill((176, 32, 32) if selected else (128, 25, 25), (self.x, self.y, self.w, self.h))
        text_rect = my_font.get_rect(self.text)
        my_font.render_to(self.surface, (self.x + self.w / 2 - text_rect.width / 2,
                                         self.y + self.h / 2 - text_rect.height / 2), self.text, (255, 255, 255))


class GameScreen:
    def render(self):
        pass

    def handle_event(self, event):
        pass


class ButtonScreen(GameScreen):
    def __init__(self, surface):
        self.surface = surface
        self.mouse_down_button = None
        self.selected_button = None
        self.buttons = []
        for y in range(buttons[1]):
            for x in range(buttons[0]):
                self.buttons.append(Button(surface,
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

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            self.mouse_down_action(event.button, pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            self.mouse_up_action(event.button, pos)

    def mouse_down_action(self, button: int, pos: (int, int)):
        if button == 1:
            self.mouse_down_button = get_pressed_button(pos)

    def mouse_up_action(self, button: int, pos: (int, int)):
        if button == 1:
            if self.mouse_down_button == get_pressed_button(pos):
                self.selected_button = self.mouse_down_button


# -1 = idle, waiting for status change in current state
# 0 = disconnected
# 1 = start connect
# 2 = connect in progress
# 3 = connected
def game_loop():
    screen_layers = []

    connect_state = 1
    not_connected_error = ""
    my_socket: any = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if len(screen_layers) > 0:
                screen_layers[len(screen_layers) - 1].handle_event(event)

        screen.fill((0, 0, 0))

        for screen_layer in screen_layers:
            screen_layer.render()

        if connect_state == 0:
            screen.fill((32, 32, 176), (50, 50, screen_size[0] - 100, screen_size[1] - 100))
            text_rect = my_font.get_rect("Not connected")
            my_font.render_to(screen,
                              (screen_size[0] / 2 - text_rect.width / 2,
                               screen_size[1] / 2 - text_rect.height / (2 * 1 if not_connected_error == "" else 2)),
                              "Not connected", (255, 255, 255))
            if not_connected_error != "":
                text_rect = my_font.get_rect(not_connected_error)
                my_font.render_to(screen,
                                  (screen_size[0] / 2 - text_rect.width / 2,
                                   screen_size[1] / 2 + text_rect.height),
                                  not_connected_error, (255, 255, 255))
        elif connect_state == 1:
            screen.fill((32, 32, 176), (50, 50, screen_size[0] - 100, screen_size[1] - 100))
            text_rect = my_font.get_rect("Attempting to connect")
            my_font.render_to(screen,
                              (screen_size[0] / 2 - text_rect.width / 2, screen_size[1] / 2 - text_rect.height / 2),
                              "Attempting to connect", (255, 255, 255))
            print("attempting to connect")
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            my_socket.setblocking(False)
            err = my_socket.connect_ex((HOST, PORT))
            if err == errno.EINPROGRESS:
                connect_state = 2
            else:
                print(err, errno.errorcode[err])
                connect_state = 0
                my_socket = None
        elif connect_state == 2:
            screen.fill((32, 32, 176), (50, 50, screen_size[0] - 100, screen_size[1] - 100))
            text_rect = my_font.get_rect("Attempting to connect - trying")
            my_font.render_to(screen,
                              (screen_size[0] / 2 - text_rect.width / 2, screen_size[1] / 2 - text_rect.height / 2),
                              "Attempting to connect - trying", (255, 255, 255))
            print("trying")
            # check if socket is ready
            _, writable, _ = select.select([], [my_socket], [], 0)
            if writable:
                err = my_socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
                if err:
                    print(err, errno.errorcode[err])
                    not_connected_error = f"{err} - {errno.errorcode[err]}"
                    connect_state = 0
                    my_socket = None
                else:
                    print("connected")
                    my_socket.send(b"GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n")
                    connect_state = 3
                    screen_layers.append(ButtonScreen(screen))
        elif connect_state == 3:
            readable, _, _ = select.select([my_socket], [], [], 0)
            for read_socket in readable:
                screen.fill((32, 32, 176), (50, 50, screen_size[0] - 100, screen_size[1] - 100))
                text_rect = my_font.get_rect("Downloading")
                my_font.render_to(screen,
                                  (screen_size[0] / 2 - text_rect.width / 2, screen_size[1] / 2 - text_rect.height / 2),
                                  "Downloading", (255, 255, 255))
                print("new read data")
                read_data = read_socket.recv(1024)
                if len(read_data):
                    print(read_data)
                else:
                    # connection closed
                    print("connection closed")
                    my_socket.shutdown(socket.SHUT_RDWR)
                    connect_state = 0
                    my_socket = None

        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    my_font = pygame.freetype.Font(None, 20)
    display_info = pygame.display.Info()
    # screen_size = display_info.current_w, display_info.current_h
    screen = pygame.display.set_mode(screen_size)

    game_loop()
