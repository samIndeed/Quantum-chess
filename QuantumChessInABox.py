import tkinter as tk
import chess
import chess.svg
import random
import cmath
from flask import Flask

app=Flask("MyFlask")

@app.route('/',methods=['GET'])
def welcome():
    return "Hello"




SQUARE_SIZE = 60

def manhattan_distance(move):
    f1 = chess.square_file(move.from_square)
    r1 = chess.square_rank(move.from_square)
    f2 = chess.square_file(move.to_square)
    r2 = chess.square_rank(move.to_square)
    return abs(f2 - f1) + abs(r2 - r1)

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.board = chess.Board()
        self.selected_square = None

        self.canvas = tk.Canvas(root, width=8*SQUARE_SIZE, height=8*SQUARE_SIZE)
        self.canvas.pack()

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack()

        self.random_btn = tk.Button(btn_frame, text="Put in box for 2 turns", command=self.play_random_move)
        self.random_btn.pack(side=tk.LEFT)

        self.reset_btn = tk.Button(btn_frame, text="Reset", command=self.reset_board)
        self.reset_btn.pack(side=tk.LEFT)

        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")

        colors = ["#EEEED2", "#769656"]
        for rank in range(8):
            for file in range(8):
                color = colors[(rank + file) % 2]
                x1 = file * SQUARE_SIZE
                y1 = (7 - rank) * SQUARE_SIZE
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        # Draw pieces (unicode)
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                file = chess.square_file(square)
                rank = chess.square_rank(square)
                x = file * SQUARE_SIZE + SQUARE_SIZE // 2
                y = (7 - rank) * SQUARE_SIZE + SQUARE_SIZE // 2

                symbol = piece.unicode_symbol()
                self.canvas.create_text(x, y, text=symbol, font=("Arial", 32),fill="Black")

    def on_click(self, event):
        file = event.x // SQUARE_SIZE
        rank = 7 - (event.y // SQUARE_SIZE)
        square = chess.square(file, rank)

        if self.selected_square is None:
            self.selected_square = square
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                self.board.push(move)
            self.selected_square = None

        self.draw_board()

    def play_random_move(self):
        if self.board.is_game_over():
            print("Game over:", self.board.result())
            return
        
        statedict=dict()

        for move in self.board.legal_moves:
            square=move.to_square
            piece = self.board.piece_at(move.from_square)
            file = chess.square_file(square)
            rank = chess.square_rank(square)
            x = file * SQUARE_SIZE + SQUARE_SIZE // 2
            y = (7 - rank) * SQUARE_SIZE + SQUARE_SIZE // 2
            symbol = piece.unicode_symbol()
            self.canvas.create_text(x, y, text=symbol, font=("Arial", 32),fill="Purple")
            self.canvas.update()
            tempboard=self.board.copy()
            tempboard.push(move)
            for secondmove in tempboard.legal_moves:
                square=secondmove.to_square
                piece = self.board.piece_at(secondmove.from_square)
                file = chess.square_file(square)
                rank = chess.square_rank(square)
                x = file * SQUARE_SIZE + SQUARE_SIZE // 2
                y = (7 - rank) * SQUARE_SIZE + SQUARE_SIZE // 2
                symbol = piece.unicode_symbol()
                self.canvas.create_text(x, y, text=symbol, font=("Arial", 32),fill="Pink")
                self.canvas.update()
                tempboard2=tempboard.copy()
                tempboard2.push(secondmove)
                for thirdmove in tempboard2.legal_moves:
                    # square=thirdmove.to_square
                    # piece = tempboard2.piece_at(thirdmove.from_square)
                    # file = chess.square_file(square)
                    # rank = chess.square_rank(square)
                    # x = file * SQUARE_SIZE + SQUARE_SIZE // 2
                    # y = (7 - rank) * SQUARE_SIZE + SQUARE_SIZE // 2
                    # symbol = piece.unicode_symbol()
                    # self.canvas.create_text(x, y, text=symbol, font=("Arial", 32),fill="Orange")
                    # self.canvas.update()
                    tempboard3=tempboard2.copy()
                    tempboard3.push(thirdmove)
                    for fourthmove in tempboard3.legal_moves:
                        # square=fourthmove.to_square
                        # piece = tempboard3.piece_at(fourthmove.from_square)
                        # file = chess.square_file(square)
                        # rank = chess.square_rank(square)
                        # x = file * SQUARE_SIZE + SQUARE_SIZE // 2
                        # y = (7 - rank) * SQUARE_SIZE + SQUARE_SIZE // 2
                        # symbol = piece.unicode_symbol()
                        # self.canvas.create_text(x, y, text=symbol, font=("Arial", 32),fill="Pink")
                        # self.canvas.update()
                        
                        tempboard4=tempboard3.copy()
                        tempboard4.push(fourthmove)
                        action=cmath.pi/32*(manhattan_distance(move)**2+manhattan_distance(secondmove)**2+manhattan_distance(thirdmove)**2+manhattan_distance(fourthmove)**2)
                        if tempboard4.board_fen() in statedict.keys():
                            statedict[tempboard4.board_fen()]+=cmath.exp(1j*action)

                        else:
                            statedict.update({tempboard4.board_fen():cmath.exp(1j*action)})

        statedict.update((x, (y*y.conjugate()).real) for x, y in statedict.items())
        chosenfen=random.choices(list(statedict.keys()), weights=statedict.values(), k=1)[0]

        if self.board.turn==chess.BLACK:
            self.board.set_fen(chosenfen)
            self.board.push(chess.Move.null())
        else:
            self.board.set_fen(chosenfen)

   
        # if 1/(statedict[chosenfen]/sum(statedict.values()))>len(statedict):
        #     print("Destructive Interference!")
        # else:
        #     print("Constructive Interference!")

        print("Out of", len(statedict), "possibilities, the probabilitiy of this outcome was one in", 1/(statedict[chosenfen]/sum(statedict.values())))
        self.draw_board()

    def reset_board(self):
        self.board.reset()
        self.draw_board()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Quantum Chess in a Box")
    gui = ChessGUI(root)
    root.mainloop()
