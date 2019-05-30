#Claudia Cota 60341850

class InvalidMoveError(Exception):
    '''Raised when an invalid move is made'''
    pass

class GameOverError(Exception):
    '''Raised when the game is over'''
    pass

class Gamestate:
    def __init__(self, board, player, most_or_least, row, column):
        self._turn = player
        self._board = board
        self._most_or_least_win = most_or_least
        self._row_num = row
        self._column_num = column
        self._black_disc = 0
        self._white_disc = 0
        self._available_places = None
        self._valid_moves = True 
        self._winner = None
    
    def whose_turn(self):
        '''returns the current players turn'''
        return self._turn

    def change_turn(self):
        '''changes the turn of player'''
        if self._turn == "W":
            self._turn = "B"
        else:
            self._turn = "W"

    def count_disc(self):
        '''counts the number of disc for each color and updates the number for each in the __init__'''
        black_disc = 0
        white_disc = 0
        for row in self._board:
            for item in row:
                if item == "B":
                    black_disc += 1
                elif item == "W":
                    white_disc +=1
        self._black_disc = black_disc
        self._white_disc = white_disc

    def return_black_num(self):
        '''returns the current number of discs for the black player'''
        return self._black_disc

    def return_white_num(self):
        '''returns the current number of discs for the white player'''
        return self._white_disc

    def board(self):
        '''returns the board in the __init__'''
        return self._board

    def all_available_places(self):
        '''makes a list of all the index tuples that are available given the rows and columns of the board and updates it in the __init__'''
        places = []
        for row in range(self._row_num):
            for col in range(self._column_num):
                places.append((row,col))
        self._available_places = places

    def any_moves(self):
        '''returns True if there are any moves available for current player and False if there are no available moves for current player's turn'''
        return self._valid_moves

    def valid_moves(self):
        '''makes a list with the index tuples of the available moves a player can make depending of current player's turn and updates the _valid_moves with True or False'''
        moves = []
        directions = [(-1,0),(0,-1),(0,+1),(+1,0),(-1,-1),(-1,+1),(+1,-1),(+1,+1)]
        temp_place = None
        if self._turn == "B":
            for row in range(len(self._board)):
                for col in range(self._column_num):
                    if self._board[row][col] == "B":
                        for direction in directions:
                            row_num = direction[0]
                            col_num = direction[1]
                            moves_num = 1
                            for num in range(17):
                                if ((row+row_num*moves_num,col+col_num*moves_num)) in self._available_places:
                                    if self._board[row+row_num*moves_num][col+col_num*moves_num] == "W":
                                        moves_num += 1
                                        if ((row+row_num*moves_num,col+col_num*moves_num)) in self._available_places:
                                            if self._board[row+row_num*moves_num][col+col_num*moves_num] == "." and moves_num >= 2:
                                                moves.append(((row+row_num*moves_num)+1,(col+col_num*moves_num)+1))
                                    else:
                                        continue
                                else:
                                    continue
                            
                                
        elif self._turn == "W":
            for row in range(len(self._board)):
                for col in range(self._column_num):
                    if self._board[row][col] == "W":
                        for direction in directions:
                            row_num = direction[0]
                            col_num = direction[1]
                            moves_num = 1
                            for num in range(17):
                                if ((row+row_num*moves_num,col+col_num*moves_num)) in self._available_places:
                                    if self._board[row+row_num*moves_num][col+col_num*moves_num] == "B":
                                        moves_num += 1
                                        if ((row+row_num*moves_num,col+col_num*moves_num)) in self._available_places:
                                            if self._board[row+row_num*moves_num][col+col_num*moves_num] == "." and moves_num >= 1:
                                                moves.append(((row+row_num*moves_num)+1,(col+col_num*moves_num)+1))
                                       
                                    else:
                                        continue
                                else:
                                    continue

       
        if len(moves) == 0:
            self._valid_moves = False
        else:
            self._valid_moves = True
            
        return moves
                
    
    def winner(self):
        '''returs and updates the winner in __init__ using the number of each colors discs and whether it is the most or least that wins'''
        if self._most_or_least_win == ">":
            if self._black_disc > self._white_disc:
                self._winner = "B"
            elif  self._white_disc > self._black_disc:
                self._winner = "W"
            elif self._white_disc == self._black_disc:
                self._winner = "NONE"
       
        elif self._most_or_least_win == "<":
            if self._black_disc < self._white_disc:
                self._winner = "B"
            elif  self._white_disc < self._black_disc:
                self._winner = "W"
            elif self._white_disc == self._black_disc:
                self._winner = "NONE"
        return self._winner
        

    def is_game_over(self):
        '''raises a GameOverError exception if the game is over'''
        if self._winner != None:
            raise GameOverError()

    def change_board(self, row, column, color):
        '''makes the move of the player by changing the board and also returns a list of the disc affected by that move that need to flip'''
        directions = [(-1,0),(0,-1),(0,+1),(+1,0),(-1,-1),(-1,+1),(+1,-1),(+1,+1)]
        flip_moves = []
        new_row = row-1
        new_col = column-1
        if self._board[new_row][new_col] == ".":
            self._board[new_row][new_col] = color
        for direction in directions:
            row_num = direction[0]
            col_num = direction[1]
            moves_num = 1
            flip_places = []
            for num in range(17):
                if ((new_row+row_num*moves_num,new_col+col_num*moves_num)) in self._available_places:
                    if color == "B":
                        if self._board[new_row+row_num*moves_num][new_col+col_num*moves_num] == "W":
                            flip_places.append((new_row+row_num*moves_num,new_col+col_num*moves_num))
                            moves_num += 1
                            if ((new_row+row_num*moves_num,new_col+col_num*moves_num)) in self._available_places:
                                if self._board[new_row+row_num*moves_num][new_col+col_num*moves_num] == "B" and moves_num >= 2:
                                    flip_moves.extend(flip_places)
                    if color == "W":
                        if self._board[new_row+row_num*moves_num][new_col+col_num*moves_num] == "B":
                            flip_places.append((new_row+row_num*moves_num,new_col+col_num*moves_num))
                            moves_num += 1
                            if ((new_row+row_num*moves_num,new_col+col_num*moves_num)) in self._available_places:
                                if self._board[new_row+row_num*moves_num][new_col+col_num*moves_num] == "W" and moves_num >= 2:
                                    flip_moves.extend(flip_places)
        return flip_moves

    def flip_places(self, flip_list: list):
        '''given the list of the index tuples of discs that need to flip, it makes the changes to the board'''
        for item in flip_list:
            flip_row = item[0]
            flip_col = item[1]
            if self._board[flip_row][flip_col] == "B":
                self._board[flip_row][flip_col] = "W"
            elif self._board[flip_row][flip_col] == "W":
                self._board[flip_row][flip_col] = "B"
                                      
        
    

        
