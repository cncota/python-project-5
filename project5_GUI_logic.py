
from tkinter import *
from project5_logic_classes import *
import project5_create_board
import point

def first_window():
    '''makes first window to take parameters to start othello game'''
    f2 = Tk()
    rows = IntVar()
    rows.set(1)  
    number_rows = [
        ("4 rows",4),
        ("6 rows",6),
        ("8 rows",8),
        ("10 rows",10),
        ("12 rows",12),
        ("14 rows",14),
        ("16 rows",16)
    ]
    row_label = Label(f2, 
          text="""Choose the number of rows:""",
          justify = LEFT,
          padx = 20).grid(row = 0, column =0)
    rn = 2
    for txt, val in number_rows:
        b =Radiobutton(f2, 
                    text=txt,
                    padx = 20, 
                    variable=rows, 
                    value=val).grid(row = rn, column = 0)            
        rn += 1


    col = IntVar()
    col.set(1)  
    number_cols = [
        ("4 columns",4),
        ("6 columns",6),
        ("8 columns",8),
        ("10 columns",10),
        ("12 columns",12),
        ("14 columns",14),
        ("16 columns",16)
    ]
    col_label = Label(f2, 
          text="""Choose the number of columns:""",
          justify = LEFT).grid(row = 0, column = 1)
    cn = 2
    for txt, val in number_cols:
         Radiobutton(f2, 
                    text=txt,
                    padx = 20, 
                    variable=col, 
                    value=val).grid(row = cn, column = 1)
         cn += 1


    first_player = StringVar()
    first_player.set("B")  
    players = [
        ("Black","B"),
        ("White","W"),   
    ]
    first_player_label = Label(f2, 
          text="""Choose the first player:""",
          justify = LEFT,
          padx = 20).grid(row = 0, column =2)
    fn = 2
    for txt, val in players:
        b =Radiobutton(f2, 
                    text=txt,
                    padx = 20, 
                    variable=first_player, 
                    value=val).grid(row = fn, column = 2)        
        fn += 1


    top_left_color = StringVar()
    top_left_color.set("B")  
    top_left_colors = [
        ("Black","B"),
        ("White","W"),   
    ]
    top_left_label = Label(f2, 
          text="""Choose the top left color:""",
          justify = LEFT,
          padx = 20).grid(row = 4, column =2)
    fn = 5
    for txt, val in top_left_colors:
        b =Radiobutton(f2, 
                    text=txt,
                    padx = 20, 
                    variable=top_left_color, 
                    value=val).grid(row = fn, column = 2)        
        fn += 1


    most_or_least = StringVar()
    most_or_least.set(">")  
    most_or_least_set = [
        ("Most",">"),
        ("Least","<"),   
    ]
    most_least_label = Label(f2, 
          text="""Choose if the player with the least or most wins:""",
          justify = LEFT,
          padx = 20).grid(row = 7, column =2)
    fn = 8
    for txt, val in most_or_least_set:
        b =Radiobutton(f2, 
                    text=txt,
                    padx = 20, 
                    variable=most_or_least, 
                    value=val).grid(row = fn, column = 2)        
        fn += 1

    Button(f2, text='PLAY', command=lambda:make_game(f2,rows, col, first_player, top_left_color, most_or_least)).grid(row=13, column=3)

   
def make_game(f2,rows,col,player,color, mode):
    '''starts the game of othello'''
    game = OthelloGUI(rows, col, player, color, mode)
    f2.destroy()
    game.start()
    return game
    
    



class OthelloGUI:
    '''prints and updates Othello game state'''
    def __init__(self, row, col, first_player, top_left, most_or_least):
        self._window = Tk()
        self._f1 = Frame(self._window)
        self._f1.grid(row=0, column=0, sticky='news')
        self._row = row.get()
        self._col = col.get()
        self._first_player = first_player.get()
        self._top_left = top_left.get()
        self._most_or_least = most_or_least.get()
        board = project5_create_board.middle_four((project5_create_board.create_board(self._row, self._col)), self._top_left, self._row, self._col )
        self._game = Gamestate(board, self._first_player, self._most_or_least, self._row, self._col)
        self._game.all_available_places()
        
        
        
        self._canvas = Canvas(master= self._f1, width= 600, height = 600,background = 'green')
        self._canvas.grid(row = 1, column = 0, sticky = N+S+W+E)

        
        
        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)
        self._f1.rowconfigure(0, weight = 0)
        self._f1.rowconfigure(1, weight = 1)
        self._f1.columnconfigure(0, weight = 1)
        
        self._game.count_disc()
        black = self._game.return_black_num()
        white = self._game.return_white_num()
        text1 = ('FULL    |    TURN: {}     |     B: {}   W: {}'.format(self._game.whose_turn(),black, white))
        Label(self._f1, text=text1).grid(row=0, column=0)


    def make_game(self):
        '''creates board'''
        board = project5_create_board.middle_four((project5_create_board.create_board(self._row, self._col)), self._top_left, self._row, self._col )
        self._game = Gamestate(board, self._first_player, self._most_or_least, self._row, self._col)
        self._game.all_available_places()
    def start(self) -> None:
        '''starts the mainloop of the window'''
        self._f1.mainloop()

    def _get_canvas_dimensions(self) -> (int,int):
        '''returns current width and height of canvas'''
        return self._canvas.winfo_width(), self._canvas.winfo_height()
    def _on_canvas_clicked(self, event:Event) -> None:
        '''generates a event.x and event.y coordinate to determine where
        the click occured and then calls the appropriate functions to redraw
        the board with the letter created by the click if the move is legal'''
        
        width, height = self._get_canvas_dimensions()

        click_point = point.from_pixel(
            (event.x, event.y), (width, height))

        self._handle_click(click_point)
        self._game.count_disc()
        black = self._game.return_black_num()
        white = self._game.return_white_num()
        text3 = ('FULL  |  TURN: {}     |     B: {}   W: {}'.format(self._game.whose_turn(),black, white))
        Label(self._f1, text=text3).grid(row=0, column=0)

        self._draw_board()
    def _on_canvas_resized(self, event: Event) -> None:
        '''when canvas is resized, redraws board to fit to window'''
        self._draw_board()
        
    def _get_square(self, click_point: point.Point) -> (int,int):
        '''returns row and column of the board where board was clicked'''
        point_x, point_y = click_point.frac()
        click_row = None
        click_col = None
        
        for n in range(self._row):
            for m in range(self._col):
                upper = (n+1)/self._row
                lower = (m)/self._col

                if lower < point_y < upper:
                    click_row = int(n)
                    
                if lower < point_x < upper:
                    click_col = int(m)

        return click_row, click_col
    
    def _handle_click(self, click_point: point.Point) -> None:
        '''runs functions to determine if a valid tictactoe move'''
        try:
            moves = self._game.valid_moves()
            players_move = self._get_square(click_point)
            player_move = ((int(players_move[0]), int(players_move[1])))
            if player_move in moves:
                flip = self._game.change_board(int(players_move[0]), int(players_move[1]), str(self._game.whose_turn()))
                self._game.flip_places(flip)
                self._game.change_turn()
        finally:
            self._game.valid_moves()
            if self._game.any_moves() == False:
                self._game.change_turn()
                self._game.valid_moves()
                if self._game.any_moves() == False:
                    self._winner()
    
            

    def _winner(self):
        '''returns winner banner'''
        self._canvas.delete(tkinter.ALL)
        self._game.count_disc()
        black = self._game.return_black_num()
        white = self._game.return_white_num()
        text1 = ('WINNER: {}     |     B: {}   W: {}'.format(self._game.winner(),black, white))
        Label(self._f1, text=text1).grid(row=0, column=0)
        self._draw_board()
        
       
        
    def _draw_board(self) -> None:
        '''draws the current board'''
        self._canvas.delete(ALL)

        width, height = self._get_canvas_dimensions()
        
        self._draw_grid(width, height)
        self._draw_letters(width, height)

    def _draw_grid(self, canvas_width, canvas_height) -> None:
        '''draws the grid created by dividing the canvas into rows/columns'''
        for row in range((self._row) - 1):
            self._canvas.create_line(
                0, (canvas_height * ((1 + row) / int(self._row))),
                canvas_width, (canvas_height * ((1 + row) / self._row)))

        for col in range((self._col) - 1):
            self._canvas.create_line(
                (canvas_width * ((1 + col) / int(self._col))), 0,
                (canvas_width * ((1 + col) / int(self._col))), canvas_height)

    def _draw_letters(self, canvas_width, canvas_height) -> None:
        '''draws any letters currently on the board'''
        board = self._game.board()
        for row in range(self._row):
            for col in range(self._col):
                if board[row][col] == 'B':
                    self._canvas.create_oval(
                        (canvas_width * ((col) / self._col)), (canvas_height * (row/self._row)),
                        (canvas_width * ((1+col)/self._col)), (canvas_height * ((row+1)/self._row)),
                        fill = 'black')
                    
                elif board[row][col] == 'W':
                    self._canvas.create_oval(
                        (canvas_width * ((col) / self._col)), (canvas_height * (row/self._row)),
                        (canvas_width * ((1+col)/self._col)), (canvas_height * ((row+1)/self._row)),
                        fill = 'white')

    

if __name__ == '__main__':
    game = first_window()
    

