import pygame
from math import acos, cos, sin
from math import sqrt

class Ball:
    '''Simple ball class'''

    def __init__(self,
                 constants,
                 filename,
                 pos = (0.0, 0.0),
                 speed = (0.0, 0.0)):
        '''Create a ball from image'''
        self.constants = constants
        self.image = pygame.image.load(filename)
        # self.image = pygame.Surface((111,111))
        # self.image.fill(pygame.Color('#888888'))
        self.surface = self.image
        self.rect = self.surface.get_rect()
        self.radius = self.rect.height/2
        self.speed = speed
        self.pos = pos
        self.mass = 1
        self.active = True

    def draw(self, surface):
        surface.blit(self.surface, self.rect)

    def action(self):
        '''Proceed some action'''
        if self.active:
            self.pos = self.pos[0]+self.speed[0], self.pos[1]+self.speed[1]
            gravity_addition = int(round(self.constants['gravity'] * 1.0 / self.constants['ticks_in_sec']))
            self.speed = (self.speed[0], self.speed[1] + gravity_addition)

    def logic(self, surface, balls):
        self.reflect(surface)
        self.intersect(balls)

    def reflect(self, surface):
        x, y = self.pos
        dx, dy = self.speed
        if x < self.radius:
            x = self.radius
            dx = -int(dx * (1 - self.constants['dev_percent']))
        elif x > surface.get_width() - self.radius:
            x = surface.get_width() - self.radius
            dx = -int(dx * (1 - self.constants['dev_percent']))
        if y < self.radius:
            y = self.radius
            dy -= int(round(self.constants['gravity'] * 1.0 / self.constants['ticks_in_sec']))
            dy = -int(round(dy * (1 - self.constants['dev_percent'])))
        elif y > surface.get_height() - self.radius:
            y = surface.get_height() - self.radius
            dy -= int(round(self.constants['gravity'] * 1.0 / self.constants['ticks_in_sec']))
            dy = -int(round(dy * (1 - self.constants['dev_percent'])))
        self.pos = x, y
        self.speed = dx, dy
        self.rect.center = intn(*self.pos)

    def intersect(self, balls):
        self_mask = pygame.mask.from_surface(self.surface)
        for ball in balls:
            if ball is not self:
                ball_mask = pygame.mask.from_surface(ball.surface)
                off_x = ball.rect.left - self.rect.left
                off_y = ball.rect.top - self.rect.top
                if self_mask.overlap(ball_mask, (off_x, off_y)):
                    ball_x, ball_y = ball.pos
                    self_x, self_y = self.pos
                    axis_x, axis_y = ball_x - self_x, ball_y - self_y
                    axis_angle = acos(axis_x / sqrt(axis_x * axis_x + axis_y * axis_y))
                    self_nor, self_tan = get_speed_decomposition(self.speed, axis_angle)
                    ball_nor, ball_tan = get_speed_decomposition(ball.speed, axis_angle)
                    sum_mass = self.mass + ball.mass
                    new_self_nor = (self.mass * self_nor - ball.mass * (self_nor - 2 * ball_nor)) / sum_mass
                    new_ball_nor = (ball.mass * ball_nor - self.mass * (ball_nor - 2 * self_nor)) / sum_mass
                    self_newspeed = make_speed((new_self_nor, self_tan), axis_angle)
                    ball_newspeed = make_speed((new_ball_nor, ball_tan), axis_angle)
                    self.speed = self_newspeed
                    ball.speed = ball_newspeed
                    ball_x, ball_y = ball.pos
                    self_x, self_y = self.pos
                    distance_x = (self.radius + ball.radius) * cos(axis_angle)
                    distance_y = (self.radius + ball.radius) * sin(axis_angle)
                    displacement_x = int(round((distance_x - (ball_x - self_x)) / 2))
                    displacement_y = int(round((distance_y - (ball_y - self_y)) / 2))
                    self.pos = (self_x - displacement_x, self_y - displacement_y)
                    ball.pos = (ball_x + displacement_x, ball_y + displacement_y)


class RotatingBall(Ball):
    '''Rotating ball class'''

    def __init__(self,
                 constants,
                 filename,
                 pos = (0.0, 0.0),
                 speed = (0.0, 0.0),
                 angle_speed = 0.0,
                 density = 1.0,
                 size = 1.0):
        '''Create a simple rotating with constant angle speed ball from image'''
        Ball.__init__(self, constants, filename, pos, speed)
        self.angle = 0
        self.size = size
        self.surface = pygame.transform.rotozoom(self.image, self.angle, self.size)
        self.rect = self.surface.get_rect()
        self.radius = self.rect.height/2
        self.angle_speed = angle_speed
        self.mass = density * pygame.mask.from_surface(self.surface).count()
        self.active = True

    def action(self):
        '''Proceed some action'''
        Ball.action(self)
        if self.active:
            self.angle += self.angle_speed
            if self.angle_speed > 360:
                self.angle -= 360
            elif self.angle < -360:
                self.angle += 360
            self.surface = pygame.transform.rotozoom(self.image, self.angle, self.size)
            self.rect = self.surface.get_rect()


def intn(*arg):
    return map(int,arg)


def get_speed_decomposition(speed, axis_angle):
    dx, dy = speed
    speed_abs = sqrt(dx * dx + dy * dy)
    if speed_abs == 0:
        return 0.0, 0.0
    speed_angle = acos(dx / speed_abs)
    speed_decomp_angle = axis_angle - speed_angle
    speed_nor = speed_abs * cos(speed_decomp_angle)
    speed_tan = speed_abs * sin(speed_decomp_angle)
    return speed_nor, speed_tan


def make_speed(decomp_speed, axis_angle):
    nor, tan = decomp_speed
    speed_tan_dx, speed_tan_dy = tan * sin(axis_angle), tan * cos(axis_angle)
    speed_nor_dx, speed_nor_dy = nor * cos(axis_angle), nor * sin(axis_angle)
    return int(round(speed_nor_dx + speed_tan_dx)), int(round(speed_nor_dy + speed_tan_dy))
