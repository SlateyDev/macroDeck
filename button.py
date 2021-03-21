class Button:
    def __init__(self, game, text: str, size: (int, int, int, int)):
        self.game = game
        self.text = text
        self.x = size[0]
        self.y = size[1]
        self.w = size[2]
        self.h = size[3]

    def render(self, selected: bool):
        self.game.game_screen.fill((176, 32, 32) if selected else (128, 25, 25), (self.x, self.y, self.w, self.h))
        text_rect = self.game.font.get_rect(self.text)
        self.game.font.render_to(self.game.game_screen, (self.x + self.w / 2 - text_rect.width / 2,
                                                         self.y + self.h / 2 - text_rect.height / 2), self.text,
                                 (255, 255, 255))
