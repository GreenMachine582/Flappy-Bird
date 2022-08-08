from __future__ import annotations

from random import randrange

from pygame import image, mask, transform


PIPE_IMG = transform.scale2x(image.load("assets\\pipe-green.png"))


class Pipes(object):
    TOP_PIPE = transform.flip(PIPE_IMG, False, True)
    BOTTOM_PIPE = PIPE_IMG
    WIDTH = PIPE_IMG.get_width()
    GAP = 200

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0

        self._vel = 5

        self.passed = []

        self.height = randrange(50, 450)
        self.top = self.height - self.TOP_PIPE.get_height()
        self.bottom = self.height + self.GAP

    def _move(self):
        self.x -= self._vel

    def update(self, **kwargs):
        if 'move' not in kwargs or kwargs['move']:
            self._move()

    def draw(self, surface):
        surface.blit(self.TOP_PIPE, (self.x, self.top))
        surface.blit(self.BOTTOM_PIPE, (self.x, self.bottom))

    def get_masks(self):
        return mask.from_surface(self.TOP_PIPE), mask.from_surface(self.BOTTOM_PIPE)
