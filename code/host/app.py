from flask import Flask, request
from engine.process_pressed_keys import ProcessPressedKeys as engine
from pico_return_schema import return_schema

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/pressed_keys", methods=["POST"])

def receive_pressed_keys():

    data = request.get_json()
    engine_instance = engine(data)
    processed_data = engine_instance.process()

    return processed_data
