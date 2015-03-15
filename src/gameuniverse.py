import pygame


class Universe:
    '''Game universe'''

    def __init__(self, grav_acc, dev_percent, msec, tickevent = pygame.USEREVENT):
        '''Run a universe with msec tick'''
        self.ga = grav_acc      # gravitation acceleration
        self.dp = dev_percent   # percent of consumed energy on objects impacts
        self.msec = msec
        self.tickevent = tickevent

    def get_constants(self):
        constants = {}
        constants['gravity'] = self.ga
        constants['dev_percent'] = self.dp
        constants['ticks_in_sec'] = 1000.0 / self.msec
        return constants

    def get_possible_events(self):
        pos_events = {}
        pos_events['tick'] = self.tickevent
        return pos_events

    def Start(self):
        '''Start running'''
        pygame.time.set_timer(self.tickevent, self.msec)

    def Finish(self):
        '''Shut down an universe'''
        pygame.time.set_timer(self.tickevent, 0)

