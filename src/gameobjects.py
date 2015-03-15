import pygame


class Ball:
    '''Simple ball class'''

    def __init__(self,
                 constants,
                 filename,
                 pos = (0.0, 0.0),
                 speed = (0.0, 0.0),
                 angle_speed = 0.0,
                 density = 1.0,
                 size = 1.0):
        '''Create a ball from image'''
        self.constants = constants
        self.image = pygame.image.load(filename)
        self.angle = 0
        self.surface = pygame.transform.rotozoom(self.image, self.angle, size)
        self.rect = self.surface.get_rect()
        self.speed = speed
        self.angle_speed = angle_speed
        self.size = size
        self.pos = pos
        self.mass = density * pygame.mask.from_surface(self.surface).count()
        self.active = True

    def draw(self, surface):
        surface.blit(self.surface, self.rect)

    def action(self):
        '''Proceed some action'''
        if self.active:
            self.pos = self.pos[0]+self.speed[0], self.pos[1]+self.speed[1]
            gravity_addition = int(round(self.constants['gravity'] * 1.0 / self.constants['ticks_in_sec']))
            self.speed = (self.speed[0], self.speed[1] + gravity_addition)
            self.angle += self.angle_speed
            if self.angle_speed > 360:
                self.angle -= 360
            elif self.angle < -360:
                self.angle += 360
            self.surface = pygame.transform.rotozoom(self.image, self.angle, self.size)

    def logic(self, surface):
        x,y = self.pos
        dx, dy = self.speed
        if x < self.rect.width/2:
            x = self.rect.width/2
            dx = -int(dx * (1 - self.constants['dev_percent']))
        elif x > surface.get_width() - self.rect.width/2:
            x = surface.get_width() - self.rect.width/2
            dx = -int(dx * (1 - self.constants['dev_percent']))
        if y < self.rect.height/2:
            y = self.rect.height/2
            dy -= int(round(self.constants['gravity'] * 1.0 / self.constants['ticks_in_sec']))
            dy = -int(round(dy * (1 - self.constants['dev_percent'])))
        elif y > surface.get_height() - self.rect.height/2:
            y = surface.get_height() - self.rect.height/2
            dy -= int(round(self.constants['gravity'] * 1.0 / self.constants['ticks_in_sec']))
            dy = -int(round(dy * (1 - self.constants['dev_percent'])))
        self.pos = x,y
        self.speed = dx,dy
        self.rect.center = intn(*self.pos)


def intn(*arg):
    return map(int,arg)

