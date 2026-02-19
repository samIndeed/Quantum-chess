from flask import Flask, render_template, request, jsonify
import chess
import random
import uuid

app = Flask(__name__)

# In-memory game storage (for demo only)
games = {}

def new_game():
    return chess.Board()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_game")
def create_game():
    game_id = str(uuid.uuid4())
    games[game_id] = new_game()
    return jsonify({"game_id": game_id})

@app.route("/get_board/<game_id>")
def get_board(game_id):
    board = games.get(game_id)
    if not board:
        return jsonify({"error": "Game not found"}), 404
    return jsonify({"fen": board.fen()})

@app.route("/move/<game_id>", methods=["POST"])
def make_move(game_id):
    board = games.get(game_id)
    if not board:
        return jsonify({"error": "Game not found"}), 404

    data = request.json
    move_uci = data.get("move")

    try:
        move = chess.Move.from_uci(move_uci)
        if move in board.legal_moves:
            board.push(move)
            return jsonify({"status": "ok", "fen": board.fen()})
        else:
            return jsonify({"error": "Illegal move"}), 400
    except Exception:
        return jsonify({"error": "Bad move format"}), 400

@app.route("/random_move/<game_id>", methods=["POST"])
def random_move(game_id):
    board = games.get(game_id)
    if not board:
        return jsonify({"error": "Game not found"}), 404

    if board.is_game_over():
        return jsonify({"result": board.result()})

    move = random.choice(list(board.legal_moves))
    board.push(move)
    return jsonify({"move": move.uci(), "fen": board.fen()})

if __name__ == "__main__":
    app.run(debug=True)
