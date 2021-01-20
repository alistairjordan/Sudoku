#!/usr/bin/env python
 
"""
"""
 
####
from tkinter import filedialog
import pygame
from sudoku import Sudoku
from toolbar import Toolbar
 
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (150, 150, 150)

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
        self.helper = False
        self.x_loc = 30
        self.y_loc = 30
        self.x_size = 450
        self.y_size = 450
        self.x_inc = self.x_size / 9 #number of columns
        self.y_inc = self.y_size / 9 #number of rows
        self.grid_x = -1
        self.grid_y = -1
        self.stats_x_loc = self.x_loc + self.x_size + 30
        self.stats_y_loc = self.y_loc
        self.stats_x_size = 50
        self.stats_y_size = 450
        self.toolbar_x_loc = 20
        self.toolbar_y_loc = self.y_loc + self.y_size + 70
        self.toolbar_x_size = 600
        self.toolbar_y_size = 80
        self.toolbar = Toolbar(self.toolbar_x_size,self.toolbar_y_size, self.toolbar_x_loc, self.toolbar_y_loc)
        #print(pygame.font.get_fonts())

    def select_tile(self, pos):
        x, y = pos
        x_low = self.x_loc
        x_high = self.x_loc + (self.x_inc * 9)
        y_low = self.y_loc
        y_high = self.y_loc + (self.y_inc * 9)
        if (x_low > x) or (y_low > y) or (x_high < x) or (y_high < y):
            print("No Collision")
            self.grid_x = -1
            self.grid_y = -1
            return
        
        self.grid_x = int((x - self.x_loc) // self.x_inc)
        self.grid_y = int((y - self.y_loc) // self.y_inc)

        print(f"Selection at {self.grid_x}, {self.grid_y}")
        
    def process_toolbar(self, raw_event, pos):
        event = self.toolbar.proccess_event(raw_event, pos)
        if event == 'New Game':
            self.playtime = 0.0
            self.sudoku = Sudoku()
            self.run()
        elif event == 'Load': 
            filename = filedialog.askopenfilename(filetypes=(("Alistair Sudoku Files", ".ajs"),   ("All Files", "*.ajs")))
            self.playtime = 0.0
            self.sudoku.load(filename)
            self.run()
        elif event == 'Save':
            filename = filedialog.asksaveasfile(filetypes=[("Alistair Sudoku Files", "*.ajs")])
            self.sudoku.save(filename)
        elif event == 'Helper':
            self.helper = not self.helper
        elif event == 'Solver':
            self.sudoku.solve()



    def run(self):
        """The mainloop
        """
        running = True
        while running:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    numbers = [i for i in range(0,10)]
                    number = -1
                    try:
                        number = int(chr(event.key))
                    except:
                        pass
                    if (number in numbers) and (self.grid_y>-1) and (self.grid_x>-1):
                        print(number)
                        self.sudoku.change_cell(number, self.grid_x, self.grid_y)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.select_tile(pos)
                self.process_toolbar(event, pos)
            self.screen.fill(WHITE)
            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0
            # self.draw_debug("FPS: {:6.3}{}PLAYTIME: {:6.3} SECONDS".format(
            #                self.clock.get_fps(), " "*5, self.playtime))
            self.draw_sudoku()
            self.draw_stats()
            self.screen.blit(self.toolbar.draw(), (self.toolbar_x_loc,self.toolbar_y_loc))
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
        x_loc = self.x_loc
        y_loc = self.y_loc
        x_size = self.x_size
        y_size = self.y_size
        x_inc = self.x_inc #number of columns
        y_inc = self.y_inc #number of rows
        #Draw grid
        if self.sudoku.game_won():
            grid_color = GREEN
        else:
            grid_color = BLACK
        for y in range(0,3):
            for x in range(0,3):
                x_dest = x_loc + (x_inc * 3 * x)
                y_dest = y_loc + (y_inc * 3 * y)
                rect = self.pygame.Rect(x_dest, y_dest, x_inc * 3, y_inc * 3)
                self.pygame.draw.rect(self.screen, grid_color, rect, 3)

        for y in range(0,9):
            for x in range(0,9):
                x_dest = x_loc + (x_inc * x)
                y_dest = y_loc + (y_inc * y)
                rect = self.pygame.Rect(x_dest, y_dest, x_inc, y_inc)
                #self.screen.blit(rect, (x_loc, y_loc))
                if (self.grid_x == x) and (self.grid_y == y):
                    self.pygame.draw.rect(self.screen, RED, rect, 3)
                else:
                    self.pygame.draw.rect(self.screen, grid_color, rect, 1)

        #Draw Cell contents
        i = 0
        for y in range(0,9):
            for x in range(0,9):
                self.sudoku.get_possible_for_cell(x,y)
                x_dest = x_loc + (x_inc * x)
                y_dest = y_loc + (y_inc * y)
                if (self.sudoku.grid[x][y].value == 0) and self.helper:
                    i2 = 1
                    y2_inc = y_inc / 3
                    x2_inc = x_inc / 3
                    for y2 in range(0,3):
                        for x2 in range(0,3):                       
                            x2_dest = x_dest + (x2_inc * x2)
                            y2_dest = y_dest + (y2_inc * y2)
                            if i2 in self.sudoku.grid[x][y].possible:
                                text = self.font.tiny.render(str(i2), True, BLACK, WHITE)
                                text_center_x = (x2_inc - text.get_width()) // 2
                                text_center_y = (y2_inc - text.get_height()) // 2
                                self.screen.blit(text, (x2_dest + text_center_x, y2_dest + text_center_y))
                            i2 = i2 + 1
                elif self.sudoku.grid[x][y].value != 0:
                    if self.sudoku.grid[x][y].wrong:
                        text = self.font.default.render(str(self.sudoku.grid[x][y]), True, RED, WHITE)
                    else:
                        text = self.font.default.render(str(self.sudoku.grid[x][y]), True, BLACK, WHITE)
                    text_center_x = (x_inc - text.get_width()) // 2
                    text_center_y = (y_inc - text.get_height()) // 2
                    self.screen.blit(text, (x_dest + text_center_x, y_dest + text_center_y))
                i = i + 1
        
    def draw_stats(self):
        x_loc = self.stats_x_loc
        y_loc = self.stats_y_loc
        x_size = self.stats_x_size
        y_size = self.stats_y_size
        edge_x = 10
        edge_y = 10
        text_1 = f"Time Taken: {int(self.playtime)}"
        frequencies = self.sudoku.get_number_frequencies()
        surface_1 = self.font.default.render(text_1, True, BLACK, WHITE)
        self.screen.blit(surface_1, (y_loc, x_loc))
        for i in range(9):
            text_2 = f"{i+1}: {frequencies[i]}"
            surface_2 = self.font.default.render(text_2, True, BLACK, WHITE)
            self.screen.blit(surface_2, (self.x_loc * 2 + self.x_size,self.y_loc + (edge_y * i) + surface_2.get_height() * i))
            #(y_loc + (edge_y * 2), x_loc + edge_x + surface_1.get_height()))
    
 
####
 
if __name__ == '__main__':
 
    # call with width of window and fps
    PygView(640, 640).run()