from __future__ import annotations

from pygame import image, transform


BASE_IMG = transform.scale2x(image.load("assets\\base.png"))


class Base:
    IMG = BASE_IMG
    WIDTH = IMG.get_width()

    def __init__(self, y):
        self.y = y
        self.x_1 = 0
        self.x_2 = self.WIDTH
        self._vel = 5

    def _move(self):
        self.x_1 -= self._vel
        self.x_2 -= self._vel

        if self.x_1 + self.WIDTH < 0:
            self.x_1 = self.x_2 + self.WIDTH

        if self.x_2 + self.WIDTH < 0:
            self.x_2 = self.x_1 + self.WIDTH

    def update(self):
        self._move()

    def draw(self, surface):
        surface.blit(self.IMG, (self.x_1, self.y))
        surface.blit(self.IMG, (self.x_2, self.y))
