import pygame

class Toolbar(object):
    def __init__(self, x_size, y_size, offset_x=0, offset_y=0):
        self.border = 10
        self.x_size = x_size
        self.y_size = y_size
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.WHITE = (255, 255, 255)
        self.buttons = [
            'New Game',
            #'Load',
            #'Save',
            'Helper',
            'Solver'
        ]
        self.button_objects = []
        self.rows = 1
        self.button_color = (42, 102, 199)
        self.button_text_color = (255,255,255)
        self.button_font = pygame.font.Font(None, 40, bold=True)
        self.button_internal_border = 20
        pass

    def draw(self):
        working = pygame.Surface((self.x_size, self.y_size))
        button_size_x = (self.x_size//(len(self.buttons)//self.rows)) - ((len(self.buttons)//self.rows)*self.border)
        button_size_y = self.y_size//self.rows - (self.rows * self.border * 2)
        working_x = self.border
        working_y = self.border
        working.fill(self.WHITE)
        #only currently doing one row
        for button in self.buttons:
            text = self.button_font.render(button, True, self.button_text_color, self.button_color)
            rect = pygame.Rect(working_x, working_y, text.get_width() + (self.button_internal_border * 2), button_size_y)
            pygame.draw.rect(working, self.button_color, rect, 0)
            #text_center_x = (button_size_x - text.get_width()) // 2
            text_center_y = (button_size_y - text.get_height()) // 2
            working.blit(text, (working_x + self.button_internal_border, working_y + text_center_y))
            working_x = working_x + text.get_width() + self.border + (self.button_internal_border * 2)
            button_object = {
                'Rect': rect,
                'Name': button
            }
            self.button_objects.append(button_object)
        return working

    def proccess_event(self, event, mouse_pos):
        x,y = mouse_pos
        #print(f"Mouse Pre-adjust at: {x}, {y}")
        mouse_pos = (x - self.offset_x, y - self.offset_y)
        #x,y = mouse_pos
        #print(f"Mouse Post-adjust at: {x}, {y}")
        if event.type == pygame.MOUSEBUTTONUP:
            #print("here")
            for i in self.button_objects:
                #print("here2")
                if i['Rect'].collidepoint(mouse_pos):
                    #print("here3")
                    return i['Name']   
        return "None"

WHITE = (255,255,255)
WIDTH = 640
HEIGHT = 100
if __name__ == '__main__':
    print("HERE")
    pygame.init()
    pygame.display.set_caption("Press ESC to quit")
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
    background = pygame.Surface(screen.get_size()).convert()
    running = True
    playtime = 0
    clock = pygame.time.Clock()
    fps = 30
    toolbar = Toolbar(WIDTH,HEIGHT)
    while running:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                pass
            print(toolbar.proccess_event(event, pos))
        screen.fill(WHITE)
        milliseconds = clock.tick(fps)
        playtime += milliseconds / 1000.0
        screen.blit(toolbar.draw(), (0,0))
        # self.draw_debug("FPS: {:6.3}{}PLAYTIME: {:6.3} SECONDS".format(
        #                self.clock.get_fps(), " "*5, self.playtime))
        pygame.display.flip()
        screen.blit(background, (0, 0))
    pygame.quit()
         