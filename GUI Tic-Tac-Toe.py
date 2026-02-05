import tkinter as tk  # Tkinter is Python's built-in GUI library
from tkinter import messagebox  # For popup messages

# Global variables
board = [" ", " ", " ",         # Using spaces for the game slots
         " ", " ", " ",
         " ", " ", " "]
currentplayer = "X"         # player which is going to move
winner = None           # still we have none means nothing
game_active = True      # start the loop we will use it later (renamed for GUI)
Owins = 0                #initializing the variables for result
Xwins = 0
ties = 0
game_mode = 1          # 1 = Human vs Computer, 2 = Two Players

#checking rows
def checkRow(board):
    global winner
    if board[0] == board[1] == board[2] and board[1] != " ":
        winner = board[0]
        return True
    elif board[3] == board[4] == board[5] and board[3] != " ":
        winner = board[3]
        return True
    elif board[6] == board[7] == board[8] and board[6] != " ":
        winner = board[6]
        return True
    return False

#checking columns
def checkColumn(board):
    global winner
    # Column 1 (LEFT): positions 0, 3, 6
    if board[0] == board[3] == board[6] and board[0] != " ":
        winner = board[0]
        return True
    # Column 2 (MIDDLE): positions 1, 4, 7
    elif board[1] == board[4] == board[7] and board[1] != " ":
        winner = board[1]
        return True
    # Column 3 (RIGHT): positions 2, 5, 8
    elif board[2] == board[5] == board[8] and board[2] != " ":
        winner = board[2]
        return True
    return False

#for diagonals
def diagonal_1(board):
    global winner
    if board[0] == board[4] == board[8] and board[0] != " ":
        winner = board[0]
        return True
    return False

def diagonal_2(board):
    global winner
    if board[2] == board[4] == board[6] and board[6] != " ":
        winner = board[2]
        return True
    return False

#if the main loop was end by any of the winner  >> winner = true >> gameloop >> end
def checkWin(board):
    return (checkColumn(board) or checkRow(board) or
            diagonal_1(board) or diagonal_2(board))

#if tie
def checkTie(board):
    return " " not in board and not checkWin(board)

#to switch the player after every move 
def switchPlayer():
    global currentplayer
    if currentplayer == "X":
        currentplayer = "O"
    else:
        currentplayer = "X"

# for computers move
def computerMove(board):
    emptySlots = [i for i in range(9) if board[i] == " "]

    # 1. Win if possible
    for pos in emptySlots:
        board[pos] = "O"
        if checkWin(board):
            board[pos] = " "
            return pos
        board[pos] = " "

    # 2. Block human
    for pos in emptySlots:
        board[pos] = "X"
        if checkWin(board):
            board[pos] = " "
            return pos
        board[pos] = " "

    # 3. Center
    if 4 in emptySlots:
        return 4

    # 4. Corners
    for pos in [0, 2, 6, 8]:
        if pos in emptySlots:
            return pos

    # 5. Edges
    for pos in [1, 3, 5, 7]:
        if pos in emptySlots:
            return pos

    return None

#TKINTER GUI SETUP 
def create_gui():
    global window, buttons, status_label, score_label  #variable of the tkinter
    
    window = tk.Tk()                         #main window that opens
    window.title("Tic Tac Toe - GUI Version")   #window name
    window.geometry("400x550")                 #size
    window.configure(bg="#f0f0f0")
    
    title = tk.Label(window, text="<<< TIC TAC TOE >>> ",            #label widget is used to write the text
                     font=("Arial", 20, "bold"),
                     bg="#f0f0f0")
    title.pack(pady=10)                                        #pack is the way to use the widgets
    
    mode_frame = tk.Frame(window, bg="#f0f0f0")
    mode_frame.pack(pady=5)
    
    tk.Button(mode_frame, text="Human vs Computer",       #button widget
              command=set_human_vs_computer_mode).pack(side="left", padx=5) #tells which function to run when clicked
    
    tk.Button(mode_frame, text="Two Players",
              command=set_two_players_mode).pack(side="left", padx=5)
    
    status_label = tk.Label(window, text="Player X's Turn",
                            font=("Arial", 14, "bold"),
                            bg="#f0f0f0")
    status_label.pack(pady=10)
    
    board_frame = tk.Frame(window, bg="black")
    board_frame.pack(pady=10)
    
    buttons = []
    for i in range(9):
        btn = tk.Button(board_frame, text=" ",
                        font=("Arial", 24, "bold"),
                        width=3, height=1,
                        command=lambda pos=i: make_move(pos))   #need to know which cell was clicked
        btn.grid(row=i//3, column=i%3)
        buttons.append(btn)
    
    control_frame = tk.Frame(window, bg="#f0f0f0")  #frame wigget is organize 
    control_frame.pack(pady=15)
    
    tk.Button(control_frame, text="New Game",
              command=reset_game).pack(side="left", padx=10)
    
    tk.Button(control_frame, text="Quit",
              command=window.quit).pack(side="left", padx=10)
    
    score_label = tk.Label(window,
        text="X Wins: 0 | O Wins: 0 | Ties: 0",
        font=("Arial", 12),
        bg="#f0f0f0")
    score_label.pack(pady=10)
    
    return window


def set_human_vs_computer_mode():
    global game_mode
    game_mode = 1
    reset_game()

def set_two_players_mode():
    global game_mode
    game_mode = 2
    reset_game()

def make_move(position):
    global board, currentplayer, game_active, Xwins, Owins, ties
    
    if not game_active or board[position] != " ":
        return
    
    board[position] = currentplayer
    buttons[position].config(text=currentplayer, state="disabled")
    
    if checkWin(board):
        game_active = False
        if winner == "X":
            Xwins += 1
        else:
            Owins += 1
        update_score()
        messagebox.showinfo("Game Over", f"Player {winner} wins!")
        return
    
    if checkTie(board):
        game_active = False
        ties += 1
        update_score()
        messagebox.showinfo("Game Over", "It's a tie!")
        return
    
    switchPlayer()
    update_status(f"Player {currentplayer}'s Turn")
    
    if game_mode == 1 and currentplayer == "O":
        window.after(400, computer_turn)

def computer_turn():
    if not game_active:
        return
    pos = computerMove(board)
    if pos is not None:
        make_move(pos)

def reset_game():
    global board, currentplayer, winner, game_active
    board = [" "] * 9
    currentplayer = "X"
    winner = None
    game_active = True
    for btn in buttons:
        btn.config(text=" ", state="normal")
    update_status("Player X's Turn")

def update_status(text):
    status_label.config(text=text)

def update_score():
    score_label.config(text=f"X Wins: {Xwins} | O Wins: {Owins} | Ties: {ties}")

# START THE GAME 

def start_gui_game():
    create_gui()
    window.mainloop()

# main program

if __name__ == "__main__":
    start_gui_game()
