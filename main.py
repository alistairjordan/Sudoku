#!/usr/bin/env python
 
"""
002_display_fps_pretty.py
 
Display framerate and playtime.
Works with Python 2.7 and 3.3+.
 
URL:     http://thepythongamebook.com/en:part2:pygame:step002
Author:  yipyip
License: Do What The Fuck You Want To Public License (WTFPL)
         See http://sam.zoy.org/wtfpl/
"""
 
####
 
import pygame
from sudoku import Sudoku
 
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

class PygFont(object):
    def __init__(self, pygame):
        self.debug = pygame.font.Font(None, 20, bold=True)
        self.default = pygame.font.Font(None, 40, bold=True)
        self.tiny = pygame.font.Font(None, 17, bold=True)
####
 
class PygView(object):
 
 
    def __init__(self, width=640, height=400, fps=30):
        """Initialize pygame, window, background, font,...
        """
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
        self.pygame = pygame
        self.width = width
        self.height = height
        #self.height = width // 4
        self.display = pygame.display
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = PygFont(pygame)
        self.sudoku = Sudoku()
        #print(pygame.font.get_fonts())
 
    def run(self):
        """The mainloop
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            self.screen.fill(WHITE)
            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0
            self.draw_debug("FPS: {:6.3}{}PLAYTIME: {:6.3} SECONDS".format(
                           self.clock.get_fps(), " "*5, self.playtime))
            self.draw_sudoku()
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
 
        pygame.quit()
 
 
    def draw_debug(self, text):
        """Center text in window
        """
        surface = self.font.debug.render(text, True, GREEN, BLACK)
        # // makes integer division in python3
        self.screen.blit(surface, (0, 0))
    
    def draw_sudoku(self):
        x_loc = 30
        y_loc = 30
        x_size = 450
        y_size = 450
        x_inc = x_size / 9 #number of columns
        y_inc = y_size / 9 #number of rows
        #Draw grid
        for y in range(0,9):
            for x in range(0,9):
                x_dest = x_loc + (x_inc * x)
                y_dest = y_loc + (y_inc * y)
                rect = self.pygame.Rect(x_dest, y_dest, x_inc, y_inc)
                #self.screen.blit(rect, (x_loc, y_loc))
                self.pygame.draw.rect(self.screen, BLACK, rect, 1)
        for y in range(0,3):
            for x in range(0,3):
                x_dest = x_loc + (x_inc * 3 * x)
                y_dest = y_loc + (y_inc * 3 * y)
                rect = self.pygame.Rect(x_dest, y_dest, x_inc * 3, y_inc * 3)
                self.pygame.draw.rect(self.screen, BLACK, rect, 3)

        #Draw Cell contents
        mini = False
        i = 0
        for y in range(0,9):
            for x in range(0,9):
                x_dest = x_loc + (x_inc * x)
                y_dest = y_loc + (y_inc * y)
                if self.sudoku.grid[x][y].value == 0:
                    i2 = 0
                    y2_inc = y_inc / 3
                    x2_inc = x_inc / 3
                    for y2 in range(0,3):
                        for x2 in range(0,3):
                            text = self.font.tiny.render(str(i2), True, BLACK, WHITE)
                            x2_dest = x_dest + (x2_inc * x2)
                            y2_dest = y_dest + (y2_inc * y2)
                            text_center_x = (x2_inc - text.get_width()) // 2
                            text_center_y = (y2_inc - text.get_height()) // 2
                            self.screen.blit(text, (x2_dest + text_center_x, y2_dest + text_center_y))
                            i2 = i2 + 1
                else:
                    text = self.font.default.render(str(self.sudoku.grid[x][y]), True, BLACK, WHITE)
                    text_center_x = (x_inc - text.get_width()) // 2
                    text_center_y = (y_inc - text.get_height()) // 2
                    self.screen.blit(text, (x_dest + text_center_x, y_dest + text_center_y))
                i = i + 1

                

 
####
 
if __name__ == '__main__':
 
    # call with width of window and fps
    PygView(640, 640).run()