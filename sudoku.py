import random, signal

class Square(object):
    def __init__(self):
        self.value = 0
        self.possible = []
        self.wrong = False
    def __str__(self):
        return "% s" % self.value
    def __repr__(self):
        return "% s" % self.value
    #__slots__ = ['value', 'possible']

class Sudoku(object):
    def __init__(self, file=None, difficulty='Easy'):
        #signal.signal(signal.SIGINT, self.keyboardInterruptHandler)
        self.difficulties = {
            'Easy': 32,
            'Medium': 27,
            'Hard': 22
        }
        self.difficulty = difficulty
        self.grid = self.new()
        self.solution = self.new()
        self.init = self.new()
        if file == None:
            self.generate()
        else:
            self.load()


    def print_grid(self, board = None):
        if board == None:
            board = self.grid
        for y in range(0,9):
            line = ""
            for x in range(0,9):
                line += f"{board[x][y]} "
            print(line)

    def keyboardInterruptHandler(self, signal, frame):       
        self.print_grid()

    def change_cell(self, number, x, y):
        self.grid[x][y].wrong = not self.validate(x, y, number) 
        self.grid[x][y].value = number


    def new(self):
        #for x in range(0,9):
        #    for y in range(0,9):
        return [ [ Square() for j in range(9) ] for i in range(9) ]        

    def validate(self, x, y, number=None, board=None):
        if board == None:
            board = self.grid
        if number == None:
            number = board[x][y]
        # Validate row
        for i in range(0, 9):
            if (board[i][y].value == number) and (i != x):
                return False

        # Validate column
        for i in range(0,9):
            if (board[x][i].value == number) and (i != y):
                return False
                
        # Validate block
        # Find which block the digit exists in.
        block_x = (x // 3) * 3
        block_y = (y // 3) * 3
        #print(f"Checking Block: {block_x}, {block_y}")
        for x_delta in range(0,3):
            for y_delta in range(0,3):
                same_position = ((block_x + x_delta) == x) and ((block_y + y_delta) == y)
                #print(f"Checking Position: {block_x + x_delta}, {block_y + y_delta}")
                if (board[block_x + x_delta][block_y + y_delta] == number) and not same_position:
                    #print("Validation Failed")
                    return False
        #print("Validation Passed")
        return True

    def solve_single_freqs_single_row(self, row, board=None):
        if board == None:
            board = self.grid  
        #Lets start with rows
        frequencies = [0 for i in range(9)]
        for i in range(9):
            self.get_possible_for_cell(i,row)
            possibles = board[i][row].possible
            for possible in possibles:
                frequencies[possible-1] = frequencies[possible-1] + 1
        
        for i in range(9):
            if frequencies[i] == 1:
                print(frequencies)
                print(f"Found {i+1} only has 1 instance on row {row}")
                for i2 in range(9):
                    if ((i+1) in board[i2][row].possible) and (len(board[i2][row].possible)>1):
                        board[i2][row].possible_values = []
                        board[i2][row].value = i+1    
                        print(f"Assign value {i+1} to {i2},{row}")  

    def solve_single_freqs_single_column(self, column, board=None):
        if board == None:
            board = self.grid  
        #Lets start with column
        frequencies = [0 for i in range(9)]
        for i in range(9):
            self.get_possible_for_cell(column,i)
            possibles = board[column][i].possible
            for possible in possibles:
                frequencies[possible-1] = frequencies[possible-1] + 1
        
        for i in range(9):
            if frequencies[i] == 1:
                print(frequencies)
                print(f"Found {i+1} only has 1 instance on column {column}")
                for i2 in range(9):
                    if ((i+1) in board[column][i2].possible) and (len(board[column][i2].possible)>1):
                        board[column][i2].possible_values = []
                        board[column][i2].value = i+1    
                        print(f"Assign value {i+1} to {column},{i2}")  

    def solve_single_freqs_single_grid(self, x, y, board=None):
        if board == None:
            board = self.grid  
        x = (x // 3) * 3
        y = (y // 3) * 3
        #Lets start with column
        frequencies = [0 for i in range(9)]
        for x_delta in range(3):
            for y_delta in range(3):
                x_loc = x_delta + x
                y_loc = y_delta + y
                self.get_possible_for_cell(x_loc, y_loc)
                possibles = board[x_loc][y_loc].possible
                for possible in possibles:
                    frequencies[possible-1] = frequencies[possible-1] + 1
        
        for i in range(9):
            if frequencies[i] == 1:
                print(frequencies)
                print(f"Found {i+1} only has 1 instance on block {x},{y}")
                for x_delta in range(3):
                    for y_delta in range(3):
                        x_loc = x_delta + x
                        y_loc = y_delta + y
                        if ((i+1) in board[x_loc][y_loc].possible) and (len(board[x_loc][y_loc].possible)>1):
                            board[x_loc][y_loc].possible_values = []
                            board[x_loc][y_loc].value = i+1    
                            print(f"Assign value {i+1} to {x_loc},{y_loc}")  

    def solve_single_freqs(self, board=None):
        #Find rows, columns or blocks where a number only occurs once
        if board == None:
            board = self.grid
        
        for row in range(9):
            self.solve_single_freqs_single_row(row,board)
        
        for column in range(9):
            self.solve_single_freqs_single_column(column,board)

        for x in range(0,9,3):
            for y in range(0,9,3):
                self.solve_single_freqs_single_grid(x,y,board)



    def solve(self, board = None):
        # Should generate the following returns
        if board == None:
            board = self.grid
        #self.print_grid(board)
        solved = False
        count = 0
        while not solved:
            for x in range(9):
                for y in range(9):
                    if board[x][y].value == 0:
                        self.get_possible_for_cell(x, y, board)
                        if len(board[x][y].possible) == 1:
                            board[x][y].value = board[x][y].possible.pop()
            if count == 90:
                print(f"Attempt {count}")
                self.print_grid(board)

            self.solve_single_freqs(board)
            count = count + 1
            # There is only 81 things to actually solve.
            if count > 90:
                return False
        
        return True



    def get_possible_for_cell(self,x,y, board=None):
        if board == None:
            board = self.grid

        numbers = []
        # get numbers in row
        for i in range(0,9):
            numbers.append(board[i][y].value)

        # get numbers in column
        for i in range(0,9):
            numbers.append(board[x][i].value)

        # get numbers in block
        block_x = (x // 3) * 3
        block_y = (y // 3) * 3
        for x_delta in range(0,3):
            for y_delta in range(0,3):
                numbers.append(board[block_x + x_delta][block_y + y_delta].value)

        numbers = sorted(list(set(numbers)))

        board[x][y].possible.clear()
        for i in range(1, 10):
            if not (i in numbers):
                board[x][y].possible.append(i)


    def random_fill_grid(self, x, y):
        #Ensure x and y are actually the start of grid
        x = (x // 3) * 3
        y = (y // 3) * 3
        numbers = [i for i in range(1,10)]
        random.shuffle(numbers)
        for x_pos in range(x, x+3):
            for y_pos in range(y, y+3):
                #print(f"Validating at {x_pos},{y_pos}")
                found = False
                found_count = 0
                while not found:
                    test_number = numbers.pop()
                    #print(f"Attempting to place {test_number}")
                    if self.validate(x_pos, y_pos, test_number):
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

    def copy_grid(self, a, b):
        for x in range(0,9):
            for y in range(0,9):
                b[x][y].value = a[x][y].value
    
    def get_number_frequencies(self, grid=None):
        if grid == None:
            grid = self.grid
        frequencies = [0 for i in range(9)]
        for i in range(9):
            search_number = i + 1
            search_count = 0
            for x in range(9):
                for y in range(9):
                    if grid[x][y].value == search_number:
                        search_count = search_count + 1
            frequencies[i] = search_count
        return frequencies

    def game_won(self, board=None):
        if board == None:
            board = self.grid
        for x in range(9):
            for y in range(9):
                if (not self.validate(x,y)) or (board[x][y].value == 0) :
                    return False
        return True
        

    def solvable(self, board=None):
        basic = False
        if not basic:
            if board==None:
                board = self.grid
            # Create temp board to test with 
            temp = self.new()
            self.copy_grid(board,temp)
            #Attempt solve on temp board
            self.solve(temp)
            return self.game_won(temp)
        else:
            #check 8 out of 9 numbers have some frequency
            numbers_with_frequency = 0
            frequencies = self.get_number_frequencies()
            #print(frequencies)
            for i in range(9):
                if frequencies[i] > 0:
                    numbers_with_frequency = numbers_with_frequency + 1
            if numbers_with_frequency >= 8:
                temp = self.new()
                self.copy_grid(self.grid, temp)
                #return self.solve(temp)
                return True
            return False


    def generate_difficulty(self, board=None):
        if board == None:
            board = self.grid

        # while not solvable:
        #     #9*9-1 minus the number to remain is the number to delete
        #     to_delete = 80 - self.difficulties[self.difficulty]
        #     #print(to_delete)
        #     grid_positions = [i for i in range(81)]
        #     random.shuffle(grid_positions)
        #     for i in range(to_delete):
        #         position = grid_positions.pop()
        #         x = position % 9
        #         y = position // 9
        #         self.grid[x][y].value = 0
        #     solvable = self.solvable()
        #     if not solvable:
        #         self.copy_grid(self.solution, self.grid)       
        #We are looking to remove this many items
        to_delete = 80 - self.difficulties[self.difficulty]

        grid_positions = [i for i in range(81)]
        random.shuffle(grid_positions)
        while to_delete > 0:
            position = grid_positions.pop()
            x = position % 9
            y = position // 9
            temp_value = board[x][y].value
            board[x][y].value = 0
            if self.solvable(board):
                to_delete = to_delete - 1
            else:
                board[x][y].value = temp_value





    def generate(self):
        grid_x = 0
        while grid_x < 3:
            grid_y = 0
            while grid_y < 3:
                #print(f"Filling grid at {grid_x} , {grid_y}" )
                while not self.random_fill_grid(grid_x * 3, grid_y * 3):
                    self.empty_grid()
                    grid_x = 0
                    grid_y = 0
                grid_y = grid_y + 1
            grid_x = grid_x + 1

        self.copy_grid(self.grid, self.solution)
        self.generate_difficulty()
        self.copy_grid(self.grid, self.init)


        return

    def load(self, filename):
        f = open(filename, "r")
        data = f.read()
        next_pos = self.read_board(data, self.grid)
        next_pos = self.read_board(data, self.init, next_pos)
        self.read_board(data, self.solution, next_pos)

    def read_board(self, data, board=None, start_pos=0):
        if board == None:
            board = self.grid
        for x in range(9):
            for y in range(9):
                self.grid[x][y].value = data[(x*9)+y+start_pos]
        return start_pos + 9*9

    def stringify_board(self, board=None):
        if board == None:
            board = self.grid
        data = ""
        #Stringify
        for x in range(9):
            for y in range(9):
                data += board[x][y].value
        return data
    
    def save(self, filename, board=None):
        if board == None:
            board = self.grid
        # Format contains board in play, init board, solved board.
        data = self.stringify_board(board)
        data += self.stringify_board(self.init)
        data += self.stringify_board(self.solution)
        f = open(filename, "w")
        f.write(data)
        f.close()

    def run(self):
        # for x in range(0,9):
        #     for y in range(0,9):
        #         print(self.grid[x][y])
        print(self.grid)


if __name__ == '__main__':
    Sudoku().run()