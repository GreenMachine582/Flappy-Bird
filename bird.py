from __future__ import annotations

from pygame import image, mask, transform


BIRD_IMGS = [transform.scale2x(image.load(f"assets\\yellowbird-{i}.png")) for i in range(3)]


class Bird(object):
    SPRITES = BIRD_IMGS
    WIDTH, HEIGHT = BIRD_IMGS[0].get_size()
    ANIMATION_CYCLE = [0, 1, 2, 1]
    ANIMATION_TIME = 5

    MAX_ROTATION = 20
    ROTATION_VEL = 18

    JUMP_HEIGHT = -10.5
    ACCELERATION = 3
    TERMINAL_VEL = 16
    GRAVITY = 0.5

    def __init__(self, x, y):
        self.pos = [x, y]
        self.tilt = 0
        self.tick_count = 0
        self._vel = 0
        self.start_of_jump = y
        self.animation_index = 0
        self.img = self.SPRITES[self.ANIMATION_CYCLE[self.animation_index]]

        self.alive = True
        self.score = 0
        self.result = 0

    def jump(self):
        self._vel = self.JUMP_HEIGHT
        self.tick_count = 0
        self.start_of_jump = self.pos[1]

    def _move(self):
        displacement = (self._vel * self.tick_count) + (0.5 * self.ACCELERATION * (self.tick_count ** 2))

        terminal_vel = min(displacement + self.GRAVITY, self.TERMINAL_VEL)

        self.pos[1] += terminal_vel

        if terminal_vel < 0 or self.pos[1] < (self.start_of_jump + 50):
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            self.tilt = max(-90, self.tilt - self.ROTATION_VEL)

    def _animation(self):
        if self.tick_count % self.ANIMATION_TIME == 0 and self.tick_count != 0:
            self.animation_index += 1
        if self.animation_index >= len(self.ANIMATION_CYCLE):
            self.animation_index = 0
        if self.tilt <= -80:
            self.animation_index = 1

        self.img = self.SPRITES[self.ANIMATION_CYCLE[self.animation_index]]

    def update(self, **kwargs):
        if self.alive:
            self.tick_count += 1
            if 'move' not in kwargs or kwargs['move']:
                self._move()
            self._animation()

    def draw(self, surface):
        rotated_image = transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=self.pos).center)
        surface.blit(rotated_image, new_rect.topleft)

    def collide(self, pipes):
        if self.alive:
            bird_mask = mask.from_surface(self.img)
            top_pipe_mask, bottom_pipe_mask = pipes.get_masks()

            top_top_offset = (pipes.x - self.pos[0], pipes.top - round(self.pos[1]))
            bottom_pipe_offset = (pipes.x - self.pos[0], pipes.bottom - round(self.pos[1]))

            if bird_mask.overlap(top_pipe_mask, top_top_offset):
                return True
            elif bird_mask.overlap(bottom_pipe_mask, bottom_pipe_offset):
                return True
            return False

    def kill(self, tick_count):
        self.alive = False
        self.result = self.score + (tick_count / 1000)
