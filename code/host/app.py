from flask import Flask, request
from engine.process_pressed_keys import ProcessPressedKeys as engine

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

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
