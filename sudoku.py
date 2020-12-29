import random, signal

class Square(object):
    def __init__(self):
        self.value = 0
        self.possible = []
    def __str__(self):
        return "% s" % self.value
    def __repr__(self):
        return "% s" % self.value
    #__slots__ = ['value', 'possible']

class Sudoku(object):
    def __init__(self, file=None):
        signal.signal(signal.SIGINT, self.keyboardInterruptHandler)
        self.grid = self.new()
        if file == None:
            self.generate()
        else:
            self.load()

    def print_grid(self):
        for y in range(0,9):
            line = ""
            for x in range(0,9):
                line += f"{self.grid[x][y]} "
            print(line)

    def keyboardInterruptHandler(self, signal, frame):       
        self.print_grid()



    def new(self):
        #for x in range(0,9):
        #    for y in range(0,9):
        return [ [ Square() for j in range(9) ] for i in range(9) ]        

    def validate(self, number, x, y):
        # Validate row
        for i in range(0, 9):
            if (self.grid[i][y].value == number) and (i != x):
                return False

        # Validate column
        for i in range(0,9):
            if (self.grid[x][i].value == number) and (i != y):
                return False
                
        # Validate block
        # Find which block the digit exists in.
        block_x = x // 3
        block_y = y // 3
        for x_delta in range(0,3):
            for y_delta in range(0,3):
                same_position = ((block_x + x_delta) == x) and ((block_y + y_delta) == y)
                if (self.grid[block_x + x_delta][block_y + y_delta] == number) and not same_position:
                    return False
        
        return True

    def random_fill_grid(self, x, y):
        #Ensure x and y are actually the start of grid
        x = (x // 3) * 3
        y = (y // 3) * 3
        numbers = [i for i in range(1,10)]
        random.shuffle(numbers)
        for x_pos in range(x, x+3):
            for y_pos in range(y, y+3):
                print(f"Validating at {x_pos},{y_pos}")
                found = False
                found_count = 0
                while not found:
                    test_number = numbers.pop()
                    print(f"Attempting to place {test_number}")
                    if self.validate(test_number, x_pos, y_pos):
                        self.grid[x_pos][y_pos].value = test_number
                        found = True
                    else:
                        numbers = [test_number] + numbers
                    found_count = found_count + 1
                    if found_count > 12:
                        return False
        return True
    
    def empty_cell(self, x, y):
        #Ensure x and y are actually the start of grid
        x = (x // 3) * 3
        y = (y // 3) * 3   
        for x_delta in range(0,3):
            for y_delta in range(0,3):
                self.grid[x+x_delta][y+y_delta].value = 0  
    
    def empty_grid(self):
        self.grid = self.new()

    def generate(self):
        # # Generate a 2 by 2 square
        # # validate if the its possible 2 actually get in the 3rd rows, if not regenerate
        # valid = False
        # while not valid:
        #     for grid_x in range(0,2):
        #         for grid_y in range(0,2):
        #             while not self.random_fill_grid(grid_x * 3, grid_y * 3):
        #                 self.empty_cell(grid_x * 3, grid_y * 3)
            

        #for grid_x in range(0,3):
        #    for grid_y in range(0,3):
        grid_x = 0
        while grid_x < 3:
            grid_y = 0
            while grid_y < 3:
            #grid_y  = 0 
                print(f"Filling grid at {grid_x} , {grid_y}" )
                while not self.random_fill_grid(grid_x * 3, grid_y * 3):
                    self.empty_cell(grid_x * 3, grid_y * 3)
                    # #Additionally we need to clear all last column and last row if we are trying to fit in the last grid
                    # if (grid_x == 2) and (grid_y == 2):
                    #     self.empty_cell(2 * 3, 0)
                    #     self.empty_cell(2 * 3, 1 * 3)
                    #     self.empty_cell(0, 2 * 3)
                    #     self.empty_cell(1 * 3, 2 * 3)
                    #     grid_x = 0
                    #     grid_y = 2
                    # self.print_grid()
                    self.empty_grid()
                    grid_x = 0
                    grid_y = 0
                grid_y = grid_y + 1
            grid_x = grid_x + 1

        return

    def load(self):
        return

    def run(self):
        # for x in range(0,9):
        #     for y in range(0,9):
        #         print(self.grid[x][y])
        print(self.grid)


if __name__ == '__main__':
    Sudoku().run()