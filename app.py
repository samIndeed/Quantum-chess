from flask import Flask, render_template, request, jsonify
import chess
import random
import uuid

app = Flask(__name__)

games = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_game")
def create_game():
    game_id = str(uuid.uuid4())
    games[game_id] = chess.Board()
    return jsonify({"game_id": game_id})

@app.route("/get_fen/<game_id>")
def get_fen(game_id):
    board = games.get(game_id)
    if not board:
        return jsonify({"error": "not found"}), 404
    return jsonify({"fen": board.fen()})

@app.route("/move/<game_id>", methods=["POST"])
def move(game_id):
    board = games.get(game_id)
    if not board:
        return jsonify({"error": "not found"}), 404

    move_uci = request.json["move"]
    move = chess.Move.from_uci(move_uci)
    if move in board.legal_moves:
        board.push(move)
        return jsonify({"fen": board.fen()})
    return jsonify({"error": "illegal"}), 400

@app.route("/random/<game_id>", methods=["POST"])
def random_move(game_id):
    board = games.get(game_id)
    if board and not board.is_game_over():
        m = random.choice(list(board.legal_moves))
        board.push(m)
        return jsonify({"move": m.uci(), "fen": board.fen()})
    return jsonify({"error": "game over"})

if __name__ == "__main__":
    app.run()
