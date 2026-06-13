import json

from flask import Flask, request, render_template, send_from_directory, url_for
from engine.process_pressed_keys import ProcessPressedKeys as engine
from pathlib import Path


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/game_state/<filename>")
def serve_game_state(filename):
    game_state_dir = Path(__file__).parent.resolve() / "game_state"
    return send_from_directory(game_state_dir, filename)

@app.route("/game/<game_id>")
def view_game(game_id):

    list_of_moves = []
    game_state_dir = Path(__file__).parent.resolve() / "game_state"

    with open(game_state_dir / f"{game_id}.json", "r") as f:
        game_state = json.load(f)
        list_of_moves = game_state.get("move_history", [])

    game_state_img_url = url_for("serve_game_state", filename=f"{game_id}.svg", _external=True)

    return render_template("template.html", game_id=game_id, file_name=game_state_img_url, moves=list_of_moves)

@app.route("/make_game", methods=["POST"])
def make_game():

    # generate random string for game id

    import random
    import string
    game_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    return {
        "status": "success",
        "game_id": game_id
    }

@app.route("/pressed_keys", methods=["POST"])

def receive_pressed_keys():

    params = request.args

    game_id = params.get("game_id", None)

    try:

        data = request.get_json()
        engine_instance = engine(data, game_id=game_id)
        processed_data = engine_instance.process()
        
        return processed_data
    
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
