import pygame
import time
pygame.font.init()

# 
# SUDOKU SOLVER WITH BACK TRACING
# 
def find_next_empty(puzzle):
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == -1: # Finds an empty slot
                return r, c

    return None, None # If no spaces are empty

def is_valid(puzzle, guess, row, col):
    row_vals = puzzle[row]
    if guess in row_vals:
        return False

    col_vals = [puzzle[i][col] for i in range(9)]
    if guess in col_vals:
        return False

    row_start = (row // 3) * 3
    col_start = (col // 3) * 3

    for r in range(row_start, row_start+3):
        for c in range(col_start, col_start+3):
            if puzzle[r][c] == guess:
                return False

    return True


def solve_sudoku(puzzle):
    row, col = find_next_empty(puzzle)

    if row is None:
        return True
    
    for guess in range(1,10):
        if is_valid(puzzle, guess, row, col):
            puzzle[row][col] = guess
            if solve_sudoku(puzzle):
                return True

        puzzle[row][col] = -1

    return False



# 
# GRID
# 
class Grid:
    board = [
        [ 3,  9, -1,   -1,  5, -1,   -1, -1, -1],
        [-1, -1, -1,    2, -1, -1,   -1, -1,  5],
        [-1, -1, -1,    7,  1,  9,   -1,  8, -1],

        [-1,  5, -1,   -1,  6,  8,   -1, -1, -1],
        [ 2, -1,  6,   -1, -1,  3,   -1, -1, -1],
        [-1, -1, -1,   -1, -1, -1,   -1, -1,  4],

        [ 5, -1, -1,   -1, -1, -1,   -1, -1, -1],
        [ 6,  7, -1,    1, -1,  5,   -1,  4, -1],
        [ 1, -1,  9,   -1, -1, -1,    2, -1, -1],
    ]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.model = None
        self.width = width
        self.height = height
        self.selected = None
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]

        self.solve_model()

    def solve_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]
        solve_sudoku(self.model)

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == -1:
            self.cubes[row][col].set(val)
            
            if self.cubes[row][col].value == self.model[row][col]:
                return True
            else:
                self.cubes[row][col].set(-1)
                self.cubes[row][col].set_temp(0)
                return False

    def draw(self, win):
        gap = self.width / 9
        
        for i in range(self.rows+1): # Grid lines
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (0,0,0), (i*gap, 0), (i*gap, self.height), thick)

        for i in range(self.rows): # Draws cubes
            for j in range(self.cols):
                self.cubes[i][j].draw(win)


    def select(self, row, col): # Selects a cube
        for i in range(self.rows): # Reset all the selected
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True # Sets selected
        self.selected = (row, col)


    def clear(self): # Clearing selected cube
        row, col = self.selected
        if self.cubes[row][col].value == -1:
            self.cubes[row][col].set_temp(0)


    def sketch(self, key): # Setting temp number
        row, col = self.selected
        self.cubes[row][col].set_temp(key)
    

    def click(self, pos): # Finds the selected cube with x and y
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9

            x = pos[0] // gap
            y = pos[1] // gap

            return(int(y), int(x))
        else:
            return None



# 
# CUBE
# 
class Cube:
    ROWS = 9
    COLS = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height

        self.temp = 0
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 24)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap
        
        if self.temp != 0 and self.value == -1:
            text = fnt.render(str(self.temp), 1, (128, 128,128))
            win.blit(text, (x+5, y+5))
        
        elif not(self.value == -1):
            text = fnt.render(str(self.value), 1, (0,0,0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap/2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(win, (0, 0, 255), (x, y, gap, gap), 3)


    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

#
# Main functions
#
def redraw_window(win, board):
    win.fill((255, 255, 255))

    board.draw(win)


def main():
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540)
    key = None
    run = True
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear() 
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != -1:
                        if board.place(board.cubes[i][j].temp):
                            print("It worked")
                        else:
                            print("No it didn't")
                        
                        key = None

            # Mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos() # gets x & y
                clicked = board.click(pos) # Finds on the grid

                if(clicked):
                    board.select(clicked[0], clicked[1]) # Selects pos
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board)
        pygame.display.update()




#
# Start of program
#
if __name__ == '__main__':
    main()
    pygame.quit()




