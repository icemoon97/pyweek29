import pygame
import pygame.freetype
import textwrap
import random

import pygame_gui

from game import loader


def scale_image(image, scalar):
    return pygame.transform.scale(
        image, (int(image.get_width() * scalar), int(image.get_height() * scalar))
    )


def find_center(image):
    return pygame.Vector2(image.get_width() / 2, image.get_height() / 2)


class Newspaper:
    def __init__(self, message, *args):
        newspaper = pygame.image.load(loader.filepath("newspaper.png"))
        newspaper = scale_image(newspaper, 4)
        newspaper = newspaper.convert_alpha()

        messages = [mes.title() for mes in [message, *args]]

        self.font = pygame.freetype.Font(loader.filepath("lora/Lora-Bold.ttf"))

        self._fit_text_to_rect(newspaper, pygame.Rect(12, 12, 564, 90), messages[0])

        messages = messages[1:]

        areas = [
            pygame.Rect(12, 115, 128, 80),
            pygame.Rect(152, 115, 164, 80),
            pygame.Rect(328, 115, 246, 80),
        ]
        random.shuffle(areas)

        for i in range(3):
            if messages:
                mes = messages.pop()
                area = areas.pop()
                self._fit_text_to_rect(newspaper, area, mes)
            else:
                area = areas.pop()

        self.image = newspaper
        self.location = pygame.Vector2(640, 360)

        self.next_event = "_" #needed for common interface with decisions

    def _fit_text_to_rect(self, image, rect, text):
        # pygame.draw.rect(image, (40,200,75), rect) #shows relevant area

        considering = set()

        for i in range(10, 50):
            t = textwrap.wrap(text, i)
            maxlen = max([len(line) for line in t])
            font_size = 1.9 * (rect.width / maxlen)
            # print(f"{len(t)} lines at {font_size}")
            if font_size * 1.1 * len(t) > rect.height:
                pass
            else:
                considering.add((font_size, tuple(t)))

        if not considering:
            considering.add((rect.height / 1.1, (text,)))

        considering = list(considering)
        considering.sort(key=lambda x: x[0])

        prefs = considering[-1]
        font_size = int(prefs[0])
        lines = prefs[1]

        # used for vertical centering
        vertical_space = len(lines) * font_size + (1.1 * (len(lines) - 1))
        starting_y = rect.y + (rect.height / 2 - vertical_space / 2)

        for i, text in enumerate(lines):
            rendered = self.font.render(text, size=font_size)[0]
            x = (
                rect.x + rect.width / 2 - rendered.get_width() / 2
            )  # horizontal centering by line
            image.blit(rendered, (x, int(starting_y + i * font_size * 1.1)))

    def ready(self):
        self.rotation = 0
        self.maxrotation = 720
        self.rotating = True
        self.finished = False

        self.manager = pygame_gui.UIManager((1280, 720))

    def display(self, time_delta):
        screen = pygame.display.get_surface()

        if self.rotating:
            self.rotation += time_delta * 350

        if self.rotation > self.maxrotation:
            self.rotation = 0
            self.rotating = False
            self.next_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(490, 600, 300, 50),
                text="Next",
                manager=self.manager,
            )

        if self.rotating:
            im = scale_image(self.image, self.rotation / self.maxrotation)
        else:
            im = self.image
            
        im = pygame.transform.rotate(im, self.rotation)

        loc = self.location - find_center(im)

        screen.blit(im, loc)

        self.manager.update(time_delta)
        self.manager.draw_ui(pygame.display.get_surface())

        return self.finished

    def process_events(self, event):
        self.manager.process_events(event)

        if event.type == pygame.USEREVENT:
            if event.user_type == "ui_button_pressed":
                if event.ui_element == self.next_button:
                    self.finished = True
