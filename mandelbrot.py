import io
import os
import pytoml as toml
import pygame


class Config(object):

    @staticmethod
    def get_config(path):
        with io.open(path, encoding='utf-8') as f:
            return toml.load(f)

class Mathematics(object):

    def __init__(self, step, size):
        self.step = step
        self.size = size

    def complex_plane(self, start_x, start_y):
        ''' Returns a generator with all important information:

        If complex number diverges or bounds to 0 under i interation, the x and y coordinates
        in 2 dimensional space, and the 2d pixel mapped to it's complex representation.

        Maybe I should do for y in range(start, stop + 1) so I can decenter the complex plane.

        '''

        for y in range(0, self.size + 1):
            for x in range(0, self.size + 1):
                cpix = self.to_complex(float(x - start_x), float(y - start_y), self.step, self.size)
                yield self.calc_mandelbrot(cpix, 25, 2.0), x, y, cpix

    def to_complex(self, x, y, step, size):
        cx = (x - size / 2) * step
        cy = (y - size / 2) * step
        return complex(cx, cy)

    def calc_mandelbrot(self, complex_num, iterations, threshold):
        count = 0
        z = 0
        while count < iterations:

            # Of course threshold could be just 2.0, but we can't catch how quickly c escapes 0
            if abs(z) > threshold:
                return False
            z = z ** 2 + complex_num
            count += 1
        else:
            return True

class Graphics(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.surface = pygame.Surface((width, height))

    def fill_surface(self, color):
        self.surface.fill(color)

    def blit_screen(self):
        self.screen.blit(self.surface, (0, 0))

    def paint_px(self, pos, color):
        self.surface.set_at(pos, color)

    def update(self):
        pygame.display.flip()

class Buffer(object):

    def __init__(self, size):
        self.buffer = size

    def get_decorator(self, func):
        def wrapper(*args, **kwargs):
            buf = 0


class ComplexPaintor(object):

    def __init__(self, graphics, buffer, painting=False):
        self.graphics = graphics
        self.painting = painting
        self.buffer = buffer

    def decide_colors(self):
        pass

    def draw(self, pos, color):
        self.graphics.paint_px(pos, color)

    def complex_draw(self, complex_plane):
        # Set painting
        self.painting = True

        # Start painting
        buff = 0
        for cnum in complex_plane:
            print cnum
            if cnum[0] == True:
                self.draw((cnum[1], cnum[2]), (255, 255, 255))

            # Buffer logic
            if buff % self.buffer == 0:
                self.graphics.blit_screen()
                self.graphics.update()
            buff += 1

        # Catch unbuffered
        self.graphics.blit_screen()
        self.graphics.update()

        # No longer painting
        self.painting = False

if __name__ == '__main__':
    config = Config.get_config('config.toml')
    settings = config['settings']
    print config
    math = Mathematics(settings['step'], settings['width'])
    cplane = math.complex_plane(0, 0)
    gui = Graphics(settings['width'], settings['height'])
    gui.fill_surface((0, 0, 0))
    gui.blit_screen()
    paintor = ComplexPaintor(gui, settings['buffer'])
    pygame.display.flip()

    while True:

        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gui.fill_surface((0, 0, 0))
                gui.blit_screen()
                pygame.display.flip()
                paintor.complex_draw(cplane)