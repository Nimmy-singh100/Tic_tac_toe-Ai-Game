"""
AI Tic-Tac-Toe with Tkinter GUI (Interactive Dark Theme)
- Minimax with alpha-beta pruning
- Difficulty: Easy / Medium / Hard
- Choose player symbol & who starts
- Scoreboard, restart, reset
"""

import tkinter as tk
from tkinter import messagebox
import random, math

WIN_LINES = [
    (0,1,2), (3,4,5), (6,7,8),
    (0,3,6), (1,4,7), (2,5,8),
    (0,4,8), (2,4,6)
]

# ---------- Game Logic ----------
def check_winner(board):
    for a,b,c in WIN_LINES:
        if board[a] and board[a]==board[b]==board[c]:
            return board[a]
    if all(cell is not None for cell in board):
        return 'Draw'
    return None

def available_moves(board):
    return [i for i,v in enumerate(board) if v is None]

def evaluate_board(board, ai, human):
    score = 0
    if board[4] == ai: score += 1
    elif board[4] == human: score -= 1
    for a,b,c in WIN_LINES:
        line = [board[a], board[b], board[c]]
        if line.count(ai)==2 and line.count(None)==1: score += 3
        if line.count(human)==2 and line.count(None)==1: score -= 3
    return score

def minimax(board, maximizing, ai, human, depth=None, alpha=-math.inf, beta=math.inf):
    winner = check_winner(board)
    if winner == ai: return (10, None)
    elif winner == human: return (-10, None)
    elif winner == 'Draw': return (0, None)
    if depth is not None and depth <= 0:
        return (evaluate_board(board, ai, human), None)

    best_move = None
    if maximizing:
        best_score = -math.inf
        for mv in available_moves(board):
            board[mv] = ai
            score, _ = minimax(board, False, ai, human, None if depth is None else depth-1, alpha, beta)
            board[mv] = None
            if score > best_score:
                best_score, best_move = score, mv
            alpha = max(alpha, best_score)
            if beta <= alpha: break
        return (best_score, best_move)
    else:
        best_score = math.inf
        for mv in available_moves(board):
            board[mv] = human
            score, _ = minimax(board, True, ai, human, None if depth is None else depth-1, alpha, beta)
            board[mv] = None
            if score < best_score:
                best_score, best_move = score, mv
            beta = min(beta, best_score)
            if beta <= alpha: break
        return (best_score, best_move)

# ---------- GUI ----------
class TicTacToeApp:
    def __init__(self, master):
        self.master = master
        master.title("AI Tic-Tac-Toe (Dark Neon)")
        master.config(bg="#0d0d0d")

        self.board = [None]*9
        self.buttons = [None]*9
        self.player_symbol = 'X'
        self.ai_symbol = 'O'
        self.human_starts = True
        self.game_over = False

        self.human_score = 0
        self.ai_score = 0
        self.draws = 0
        self.difficulty = tk.StringVar(value='Hard')

        self.build_ui()
        self.reset_board()

    def build_ui(self):
        # Top Options
        top = tk.Frame(self.master, bg="#0d0d0d")
        top.pack(pady=8)

        opt = tk.Frame(top, bg="#0d0d0d")
        opt.grid(row=0, column=0)
        tk.Label(opt, text="You are:", fg="#00FFFF", bg="#0d0d0d").grid(row=0,column=0)
        self.sym_var = tk.StringVar(value='X')
        tk.Radiobutton(opt, text='X', variable=self.sym_var, value='X',
                       command=self.on_symbol_change, bg="#0d0d0d", fg="#FFFFFF",
                       selectcolor="#1a1a1a").grid(row=0,column=1)
        tk.Radiobutton(opt, text='O', variable=self.sym_var, value='O',
                       command=self.on_symbol_change, bg="#0d0d0d", fg="#FFFFFF",
                       selectcolor="#1a1a1a").grid(row=0,column=2)

        tk.Label(opt, text="Start:", fg="#00FFFF", bg="#0d0d0d").grid(row=1,column=0)
        self.start_var = tk.BooleanVar(value=True)
        tk.Radiobutton(opt, text='You', variable=self.start_var, value=True,
                       command=self.on_start_change, bg="#0d0d0d", fg="#FFFFFF",
                       selectcolor="#1a1a1a").grid(row=1,column=1)
        tk.Radiobutton(opt, text='Computer', variable=self.start_var, value=False,
                       command=self.on_start_change, bg="#0d0d0d", fg="#FFFFFF",
                       selectcolor="#1a1a1a").grid(row=1,column=2)

        diff = tk.Frame(top, bg="#0d0d0d")
        diff.grid(row=0,column=1,padx=20)
        tk.Label(diff, text="Difficulty:", fg="#FF00FF", bg="#0d0d0d").pack()
        for d in ['Easy','Medium','Hard']:
            tk.Radiobutton(diff, text=d, variable=self.difficulty, value=d,
                           bg="#0d0d0d", fg="#FFFFFF", selectcolor="#1a1a1a").pack(anchor='w')

        ctrl = tk.Frame(top, bg="#0d0d0d")
        ctrl.grid(row=0,column=2,padx=10)
        tk.Button(ctrl, text="Restart", command=self.restart_same,
                  bg="#222222", fg="#00FFFF").pack(fill='x')
        tk.Button(ctrl, text="Reset Scores", command=self.reset_scores,
                  bg="#222222", fg="#FF00FF").pack(fill='x',pady=4)
        tk.Button(ctrl, text="Clear Board", command=self.reset_board,
                  bg="#222222", fg="#FFFFFF").pack(fill='x')

        # Scoreboard
        self.score_label = tk.Label(self.master, text=self.score_text(),
                                    font=('Consolas',12,'bold'), fg="#FFFFFF", bg="#0d0d0d")
        self.score_label.pack(pady=5)

        # Board
        board_frame = tk.Frame(self.master, bg="#0d0d0d")
        board_frame.pack()
        for i in range(9):
            btn = tk.Button(board_frame, text='', width=6, height=3,
                            font=('Consolas',20,'bold'), bg="#1a1a1a", fg="#FFFFFF",
                            activebackground="#333333",
                            command=lambda i=i: self.on_click(i))
            btn.grid(row=i//3, column=i%3, padx=4, pady=4)
            btn.bind("<Enter>", lambda e,b=btn: b.config(bg="#222255"))
            btn.bind("<Leave>", lambda e,b=btn: b.config(bg="#1a1a1a" if not b['text'] else b['bg']))
            self.buttons[i] = btn

        # Status
        self.status = tk.Label(self.master, text="Welcome! Choose options to start.",
                               font=('Consolas',11), fg="#00FFFF", bg="#0d0d0d")
        self.status.pack(pady=8)

    def on_symbol_change(self):
        self.player_symbol = self.sym_var.get()
        self.ai_symbol = 'O' if self.player_symbol=='X' else 'X'
        self.reset_board()

    def on_start_change(self):
        self.human_starts = self.start_var.get()
        self.reset_board()

    def score_text(self):
        return f"Player ({self.player_symbol}): {self.human_score}   AI ({self.ai_symbol}): {self.ai_score}   Draws: {self.draws}"

    def restart_same(self): self.reset_board()
    def reset_scores(self):
        self.human_score = self.ai_score = self.draws = 0
        self.score_label.config(text=self.score_text())

    def reset_board(self):
        self.board = [None]*9
        self.game_over = False
        for b in self.buttons:
            b.config(text='', bg="#1a1a1a", state='normal')
        self.status.config(text="Your move." if self.human_starts else "AI starting...")
        if not self.human_starts:
            self.master.after(500, self.ai_move)

    def on_click(self, i):
        if self.game_over or self.board[i] is not None:
            return
        self.board[i] = self.player_symbol
        self.update_button(i, self.player_symbol)
        self.check_state(player=True)

    def update_button(self, i, sym):
        color = "#00FFFF" if sym=='X' else "#FF00FF"
        self.buttons[i].config(text=sym, fg=color, state='disabled', bg="#222222")

    def check_state(self, player=False):
        winner = check_winner(self.board)
        if winner:
            self.finish_game(winner)
        elif not winner and not player:
            self.status.config(text="Your turn.")
        elif not winner and player:
            self.status.config(text="AI thinking...")
            self.master.after(400, self.ai_move)

    def ai_move(self):
        if self.game_over: return
        moves = available_moves(self.board)
        if not moves:
            self.finish_game('Draw')
            return
        diff = self.difficulty.get()
        if diff == 'Easy':
            mv = random.choice(moves)
        elif diff == 'Medium':
            _, mv = minimax(self.board, True, self.ai_symbol, self.player_symbol, depth=2)
            if mv is None: mv = random.choice(moves)
        else:
            _, mv = minimax(self.board, True, self.ai_symbol, self.player_symbol)
            if mv is None: mv = random.choice(moves)
        self.board[mv] = self.ai_symbol
        self.update_button(mv, self.ai_symbol)
        self.check_state(player=False)

    def finish_game(self, winner):
        self.game_over = True
        if winner == 'Draw':
            self.status.config(text="It's a draw!", fg="#FFFF00")
            self.draws += 1
            for b in self.buttons: b.config(bg="#444444")
        else:
            color = "#00FF00" if winner==self.player_symbol else "#FF3333"
            self.status.config(text="You Win! 🎉" if winner==self.player_symbol else "AI Wins 💻", fg=color)
            if winner==self.player_symbol: self.human_score += 1
            else: self.ai_score += 1
            self.highlight_win(winner)
        self.score_label.config(text=self.score_text())
        for b in self.buttons: b.config(state='disabled')

    def highlight_win(self, sym):
        for (a,b,c) in WIN_LINES:
            if self.board[a]==self.board[b]==self.board[c]==sym:
                for i in (a,b,c):
                    self.buttons[i].config(bg="#00AA55" if sym==self.player_symbol else "#AA0033")
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
