from __future__ import annotations

import os
import sys
from time import time

import pygame as pg

from bird import Bird
from pipes import Pipes
from base import Base


# Constants
ROOT_DIR = os.path.dirname(__file__)
START_TIME = time()
WIDTH, HEIGHT = 600, 800
FPS = 30

BACKGROUND_IMG = pg.transform.scale(pg.image.load("assets\\background-day.png"), (600, 900))
MESSAGE_IMG = pg.transform.scale2x(pg.image.load("assets\\message.png"))
NUMBER_IMGS = [pg.transform.scale2x(pg.image.load(f"assets\\{i}.png")) for i in range(10)]
GAME_OVER_IMG = pg.transform.scale2x(pg.image.load("assets\\gameover.png"))


# Pygame
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Flappy Bird')
clock = pg.time.Clock()


def _quit_program():
    print("--- %s seconds ---" % round(time() - START_TIME, 2))
    pg.quit()
    sys.exit()


def get_center(img_dims, offset=(WIDTH / 2, HEIGHT / 2)):
    return int(offset[0] - (img_dims[0] / 2)), int(offset[1] - (img_dims[1] / 2))


class FlappyBird(object):
    FLOOR = 730
    STARTING_POINT = get_center((Bird.WIDTH, Bird.HEIGHT), (WIDTH / 2, HEIGHT * (5/8)))
    PIPE_SPAWN_RATE = 100

    def __init__(self, bird_count=1):
        self.bird_count = bird_count
        self.birds = []
        self.pipes = []
        self.base = None
        self.tick_count = 0

    def reset(self):
        self.birds = [Bird(*self.STARTING_POINT) for _ in range(self.bird_count)]
        self.pipes = [Pipes(WIDTH + 50)]
        self.base = Base(self.FLOOR)
        self.tick_count = 0

    def is_alive(self):
        for bird in self.birds:
            if bird.alive:
                return True
        return False

    def _spawn_pipes(self):
        if self.tick_count % self.PIPE_SPAWN_RATE == 0 and self.tick_count != 0:
            self.pipes.append(Pipes(WIDTH))

    def _update_birds(self):
        for bird in self.birds:
            if bird.pos[1] + bird.img.get_height() >= self.FLOOR or bird.pos[1] < -5:
                bird.kill(self.tick_count)

    def _update_pipes(self):
        temp_pipes = self.pipes
        for pipe in temp_pipes:
            for bird_key, bird in enumerate(self.birds):
                if bird.collide(pipe):
                    bird.kill(self.tick_count)

                if pipe.x + pipe.WIDTH < 0:
                    self.pipes.remove(pipe)

                if bird_key not in pipe.passed and (pipe.x + pipe.WIDTH) < bird.pos[0]:
                    bird.score += 1
                    pipe.passed.append(bird_key)

        self._spawn_pipes()

    def update(self):
        self.tick_count += 1

        self._update_birds()
        self._update_pipes()

        for bird in self.birds:
            bird.update()
        for pipe in self.pipes:
            pipe.update()
        self.base.update()

    def draw(self, surface):
        surface.blit(BACKGROUND_IMG, (0, 0))
        for bird in self.birds:
            bird.draw(surface)
        for pipe in self.pipes:
            pipe.draw(surface)
        self.base.draw(surface)


def _intro(player, base):
    """
    Introduction is the first scene of the game, also known as the starting screen.

    :return: continue
    :rtype: bool
    """
    message_pos = get_center(MESSAGE_IMG.get_size())
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE or event.type == pg.MOUSEBUTTONDOWN:
                player.jump()
                return True

        player.update(move=False)
        base.update()

        screen.blit(BACKGROUND_IMG, (0, 0))
        screen.blit(MESSAGE_IMG, message_pos)
        player.draw(screen)
        base.draw(screen)
        pg.display.update()
        clock.tick(30)


def _game_over(player):
    """
    The Game Over scene usually commences once the player bird dies and
    displays the score.

    :return: continue
    :rtype: bool
    """
    game_over_pos = get_center(GAME_OVER_IMG.get_size())

    # Calculates the offset for each number image
    number_gap = 5
    numbers, numbers_pos = [], [0]
    for i, digit in enumerate(str(player.score)):
        numbers.append(NUMBER_IMGS[int(digit)])
        if i > 0:
            numbers_pos.append(numbers_pos[-1] + numbers[-1].get_width() + number_gap)
    numbers_offset = WIDTH // 2 - (numbers_pos[-1] + numbers[-1].get_width()) // 2

    screen.blit(GAME_OVER_IMG, game_over_pos)
    for i, number in enumerate(numbers):
        screen.blit(number, ((numbers_offset + numbers_pos[i]), HEIGHT // 4))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE or event.type == pg.MOUSEBUTTONDOWN:
                return True
        pg.display.update()
        clock.tick(30)


def _main():
    flappy_bird = FlappyBird()
    run = True
    while run:
        flappy_bird.reset()
        run = _intro(flappy_bird.birds[0], flappy_bird.base)

        while run and flappy_bird.is_alive():
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    break
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE or event.type == pg.MOUSEBUTTONDOWN:
                    flappy_bird.birds[0].jump()

            flappy_bird.update()
            flappy_bird.draw(screen)
            pg.display.update()
            clock.tick(FPS)

        if run:
            run = _game_over(flappy_bird.birds[0])
    _quit_program()


if __name__ == '__main__':
    _main()
