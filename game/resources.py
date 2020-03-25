import pygame

import pygame_gui


class Resources:
    instance = None

    def __init__(self, manager, food, population, territory):
        Resources.instance = self

        self.__dict__["food"] = food
        self.__dict__["population"] = population
        self.__dict__["territory"] = territory

        self.food_display = pygame_gui.elements.UILabel(
            manager=manager,
            relative_rect=pygame.Rect(10, 10, 218, 40),
            text=f"Food: {self.food}",
            object_id="food_display",
        )
        self.population_display = pygame_gui.elements.UILabel(
            manager=manager,
            relative_rect=pygame.Rect(238, 10, 296, 40),
            text=f"Population: {self.population}",
            object_id="population_display",
        )
        self.territory_display = pygame_gui.elements.UILabel(
            manager=manager,
            relative_rect=pygame.Rect(544, 10, 283, 40),
            text=f"Territory: {self.territory}",
            object_id="territory_display",
        )

    def __setattr__(self, name, value):
        display = False
        if name == "food":
            display = self.food_display
        if name == "population":
            display = self.population_display
        if name == "territory":
            display = self.territory_display

        if display:
            display.set_text(f"{name.capitalize()}: {value}")
            display.rebuild()

        self.__dict__[name] = value
