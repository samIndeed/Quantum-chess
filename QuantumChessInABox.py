from flask import Flask, render_template, request, redirect, url_for, session
import chess
import random
import uuid

app = Flask(__name__)
app.secret_key = "replace-this-with-a-secure-key"

# In-memory game store (OK for demo; see notes below)
games = {}

@app.route("/")
def index():
    game_id = str(uuid.uuid4())[:8]
    return redirect(url_for("join", game_id=game_id))

@app.route("/join/<game_id>")
def join(game_id):
    if game_id not in games:
        games[game_id] = chess.Board()

    if "player" not in session:
        session["player"] = "white" if len(session) % 2 == 0 else "black"

    return redirect(url_for("game", game_id=game_id))

@app.route("/game/<game_id>")
def game(game_id):
    board = games.get(game_id)
    if not board:
        return "Game not found", 404

    return render_template(
        "game.html",
        board=board,
        game_id=game_id,
        turn="white" if board.turn else "black",
        player=session.get("player", "spectator")
    )

@app.route("/move/<game_id>", methods=["POST"])
def move(game_id):
    board = games.get(game_id)
    if not board:
        return "Game not found", 404

    if session.get("player") != ("white" if board.turn else "black"):
        return redirect(url_for("game", game_id=game_id))

    move_uci = request.form.get("move")
    try:
        move = chess.Move.from_uci(move_uci)
        if move in board.legal_moves:
            board.push(move)
    except Exception:
        pass

    return redirect(url_for("game", game_id=game_id))

@app.route("/random/<game_id>", methods=["POST"])
def random_move(game_id):
    board = games.get(game_id)
    if not board or board.is_game_over():
        return redirect(url_for("game", game_id=game_id))

    if session.get("player") != ("white" if board.turn else "black"):
        return redirect(url_for("game", game_id=game_id))

    move = random.choice(list(board.legal_moves))
    board.push(move)

    return redirect(url_for("game", game_id=game_id))

if __name__ == "__main__":
    app.run(debug=True)
