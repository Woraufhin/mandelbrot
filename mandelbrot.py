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

    step = 0.1

    def __init__(self, size, iterations, threshold):
        self.size = size
        self.iterations = iterations
        self.threshold = threshold

    def complex_plane(self, start_x, start_y):
        cx = (start_x * self.step) - (self.size / 2) * self.step
        cy = (start_y * self.step) - (self.size / 2) * self.step
        ''' Returns a generator with all important information:

        If complex number diverges or bounds to 0 under i interation, the x and y coordinates
        in 2 dimensional space, and the 2d pixel mapped to it's complex representation.

        Maybe I should do for y in range(start, stop + 1) so I can decenter the complex plane.

        '''

        for y in range(0, self.size + 1):
            cy += self.step
            for x in range(0, self.size + 1):
                cx += self.step
                cpix = self.to_complex(float(cx), float(cy), self.step, self.size)
                yield self.calc_mandelbrot(cpix), x, y, cpix
            cx = (start_x * self.step) - (self.size / 2) * self.step

    def to_complex(self, x, y, step, size):
        #cx = (x - size / 2) * step
        #cy = (y - size / 2) * step
        cx = x
        cy = y
        return complex(cx, cy)

    def calc_mandelbrot(self, complex_num):
        count = 0
        z = 0
        while count < self.iterations:

            # Of course threshold could be just 2.0, but we can't catch how quickly c escapes 0
            if abs(z) > self.threshold:
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

    buffer_size = 0

    def __init__(self):
        self.check = 0

    def __decorator(self, func):
        def wrapper(*args, **kwargs):
            self.check += 1

            # I assume I will only hand paintors to the buffer
            if self.check % self.buffer_size == 0:
                args[0].graphics.blit_screen()
                args[0].graphics.update()

            return func(*args, **kwargs)
        return wrapper

    @staticmethod
    def flush(graphics):
        graphics.graphics.blit_screen()
        graphics.graphics.update()

    @staticmethod
    def decorate():
        return Buffer().__decorator

class ComplexPaintor(object):

    def __init__(self, graphics, painting=False):
        self.graphics = graphics
        self.painting = painting

    def decide_colors(self):
        pass

    @Buffer.decorate()
    def draw(self, pos, color):
        self.graphics.paint_px(pos, color)

    def complex_draw(self, complex_plane):

        for cnum in complex_plane:
            print cnum
            if cnum[0] == True:
                self.draw((cnum[1], cnum[2]), (255, 255, 255))
            else:
                self.draw((cnum[1], cnum[2]), (130, 122, 111))

        Buffer.flush(self)

def cli():
    config = Config.get_config(os.path.expanduser('~/.config/mandelbrot/config.toml'))
    settings = config['settings']
    Buffer.buffer_size = settings['buffer']
    Mathematics.step = settings['step']
    math = Mathematics(settings['width'], settings['iterations'], settings['threshold'])
    cplane = math.complex_plane(0, 0)
    gui = Graphics(settings['width'], settings['height'])
    paintor = ComplexPaintor(gui)
    paintor.complex_draw(cplane)

    while True:

        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                Mathematics.step /= settings['zoom']
                x, y = event.pos
                cplane = math.complex_plane(x, y)
                paintor.complex_draw(cplane)

if __name__ == '__main__':
    cli()