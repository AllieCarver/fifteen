"""
Loyd's Fifteen puzzle - solver and visualizer

Use the arrows key to swap blank tile with its neighbors
"""

import fifteengui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]
        self._solved_tiles = {}
        self._indices = []
        self._solved_tile_init()
        
    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans
    
    def _solved_tile_init(self):
        """
        solved tiles dictionary
        """
        count = 0
        for row in range(self._height):
            for col in range(self._width):
                self._solved_tiles[(row,col)] = count
                self._indices.append((row,col))
                count += 1

                
    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = (self._grid[zero_row][zero_col
                                                                          - 1])
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = (self._grid[zero_row][zero_col
                                                                          + 1])
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = (self._grid[zero_row
                                                             - 1][zero_col])
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = (self._grid[zero_row
                                                            + 1][zero_col])
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods0

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
       
        tile = self.get_number(target_row,target_col)
        tile_idx = self._indices.index((target_row, target_col))
        if tile == 0:
            for cord in self._indices[tile_idx+1:]:
                if self._solved_tiles[(cord[0], cord[1])] != self.get_number(
                                                            cord[0],cord[1]):
                    return False
            return True
        return False

    def position_tile(self, target_row, target_col, called_from_col0 = False):
        """
        place zero to the left of target tile, if target tile is in row 0
        moves target tile down a row
        """
        current_row, current_col = self.current_position(target_row, target_col)
        if called_from_col0:
            move_str = "u" * ((target_row -1) - current_row)
        else:
            move_str = "u" * (target_row - current_row)
        self.update_puzzle(move_str)
        current_row, current_col = self.current_position(target_row, target_col)
        if current_col == target_col and not called_from_col0:
            move_str += "ld"
            self.update_puzzle("ld")
            return move_str
        if called_from_col0:
            if current_col == 1:
                move_str += "ld"
                self.update_puzzle("ld")
                return move_str
        if current_col <= target_col:
            if called_from_col0:
                move = ("l")               
            else:
                move = "l" * (target_col - current_col)
            move_str += move
            self.update_puzzle(move)
        else:
            if called_from_col0:
                move = "r" * ((current_col-2) - target_col)
            else:
                move = "r" * ((current_col-1) - target_col)
            move_str += move
            self.update_puzzle(move)
        if current_row == 0:
            move_str += "druld"
            self.update_puzzle("druld")
        return move_str
    
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        move_str = self.position_tile(target_row, target_col)

        current_row, current_col = self.current_position(target_row, target_col)
        move = ""
        while current_col != target_col:
            if current_col > target_col:
                move += "rulld"
                current_col -= 1
            else: 
                move += "urrdl"
                current_col +=1
        move_str += move

        self.update_puzzle(move)
        move = ""
        while current_row != target_row:
            move += "druld"            
            current_row += 1 
        move_str += move  

        self.update_puzzle(move)
        
        return move_str

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move 
        
        """
        move_str = "ur"
        self.update_puzzle("ur") 
        current_row, current_col = self.current_position(target_row, 0)
        if current_row == target_row:
            move_str += "r" * (self._width-2)        
            self.update_puzzle("r" * (self._width-2))
            return move_str
        move_str += self.position_tile(target_row, 0, True)
        current_row, current_col = self.current_position(target_row, 0)
        move = ""
        while current_col > 1:
            move += "rulld"
            current_col -= 1
        move_str += move
        self.update_puzzle(move)
        move = ""
        while current_row < target_row -1:
            move += "druld"
            current_row += 1 
        move += "ruldrdlurdluurddlur" + "r" * (self._width - 2)
        move_str += move       
        self.update_puzzle(move)
        return move_str
 
   
    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        
        
        zero_pos = self.current_position(0,0)
        if zero_pos != (0,target_col):
            return False
        if self._solved_tiles[(1, target_col)] != self.get_number(1, target_col):
            return False        
        tile_idx = self._indices.index((1,self._width-1))        
        for cord in self._indices[tile_idx+1:]:
            if self._solved_tiles[(cord[0], cord[1])] != self.get_number(
                                                        cord[0],cord[1]):
                    return False
        if target_col > self._width - 1:
            for col in range(target_col + 1, self._width):
                if self._solved_tiles[(0, col)] != self.get_number(0, col):
                    return False         
                if self._solved_tiles[(1, col)] != self.get_number(1, col):
                    return False       
        
        return True
    
    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        zero_pos = self.current_position(0,0)
        if zero_pos != (1,target_col):
            return False
        
        tile_idx = self._indices.index((1,self._width-1))        
        for cord in self._indices[tile_idx+1:]:
            if self._solved_tiles[(cord[0], cord[1])] != self.get_number(
                                                        cord[0],cord[1]):
                    return False
        if target_col < self._width - 1:
            for col in range(target_col + 1, self._width):
                if self._solved_tiles[(0, col)] != self.get_number(0, col):
                    return False         
                if self._solved_tiles[(1, col)] != self.get_number(1, col):
                    return False       
        
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
       
        move_str = "ld"
        self.update_puzzle(move_str)
        tile_pos = self.current_position(0, target_col)
        if tile_pos[1] == target_col:
            return move_str
        
#        tile_pos = self.current_position(0, target_col)
        move = "l" * ((target_col - 1)  - tile_pos[1])
        tile_pos = self.current_position(0, target_col)
        if tile_pos[0] == 0:
            move += "u"
            if tile_pos[1] == 0:
                move += "rdl"
            else: move += "ld"
        move_str += move
        self.update_puzzle(move)
        current_col = self.current_position(0, target_col)[1]
        while current_col < target_col - 1:
            move_str += "urrdl"
            self.update_puzzle("urrdl")
            current_col += 1
        if current_col < target_col:     
            move_str += "urdlurrdluldrruld"
            self.update_puzzle("urdlurrdluldrruld")
        return move_str
            
    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        tile_pos = self.current_position(1, target_col)
        move = "l" * (target_col - tile_pos[1])
        move_str = ""
        
        if tile_pos[0] == 0:
            move += "u"
            if tile_pos[1] == 0:
                move += "rdlur"
        else: move += "ur"        
        move_str += move
    
        self.update_puzzle(move)
        tile_pos = self.current_position(1, target_col)
        while tile_pos[1] < target_col:
            move_str += "rdlur"
            self.update_puzzle("rdlur")
            tile_pos = self.current_position(1, target_col)
        if self.current_position(0, 0)[0] != 0:
            move_str += "ur"
            self.update_puzzle("ur")
        return move_str

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        zero_pos = self.current_position(0, 0)
        move_str = ""
        tiles = [(0,1), (1,0), (1, 1)]
        if zero_pos[0] == 1:
            move_str += "u"
        if zero_pos[1] == 1:
            move_str += "l"
        self.update_puzzle(move_str)
        while True:
            count = 0
            for tile in tiles:
                if self._solved_tiles[tile] == self.get_number(tile[0],tile[1]):
                    count += 1
            if count == 3:               
                return move_str
            else:
                move_str += "rdlu"
                self.update_puzzle("rdlu")

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        count = 0
        for tile in self._indices:
            if self.get_number(tile[0], tile[1]) == self._solved_tiles[tile]:
                count += 1
            else: break
        if count == len(self._indices):
            return ""
        #move zero to lower right of puzzle
        zero_pos = self.current_position(0, 0)
        move_str = "r" * ((self._width -1) - zero_pos[1])
        move_str += "d" * ((self._height - 1) - zero_pos[0])
        
        self.update_puzzle(move_str)
        #solve lower rows
        for row in range(2,self._height)[::-1]:
            for col in range(1,self._width)[::-1]:
               
                move = self.solve_interior_tile(row,col)

                move_str += move
            move = self.solve_col0_tile(row)
            
            move_str += move

        #solve right most width-2 cols in upper 2 rows
        for col in range(2, self._width)[::-1]:
            move_str += self.solve_row1_tile(col)
            move_str += self.solve_row0_tile(col)
        move_str += self.solve_2x2()
        return move_str
    
# Start interactive simulation
fifteengui.FifteenGUI(Puzzle(4, 4))
