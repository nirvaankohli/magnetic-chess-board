import network
import time
from machine import Pin, ADC,  SPI
import ssd1306
from secrets import ssid, password, server_url
import random
import urequests

global move

move = "w"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

endpoint = "/pressed_keys"

# Place Holder Pins(for OLED & buttons)
# Pin declarations

white_button = [Pin(15, Pin.IN, Pin.PULL_DOWN), 0, 200]
black_button = [Pin(26, Pin.IN, Pin.PULL_DOWN), 0, 200]

rows_reed_switch_pins = list(reversed([6, 7, 8, 9, 10, 11, 12, 13]))
columns_reed_switch_pins = [16, 17, 18, 19, 20, 21, 22, 14]

hspi = SPI(1)  

dc = Pin(4) 
rst = Pin(5)   
cs = Pin(15) 

def scan_matrix(row_pins, col_pins):

    active_keys = []
    for row_idx, row_pin in enumerate(row_pins):

        row_pin.value(1)

        for col_idx, col_pin in enumerate(col_pins):

            if col_pin.value() == 1:
                active_keys.append([row_idx, col_idx])

        row_pin.value(0)

    return active_keys


def create_matrix(rows: int, columns: int):

    chess_rows = map(lambda x: str(x), [1, 2, 3, 4, 5, 6, 7, 8])
    chess_columns = ["a", "b", "c", "d", "e", "f", "g", "h"]

    matrix = []

    for row in chess_rows:

        columns = []

        for column in chess_columns:

            columns.append(column + row)

        matrix.append(columns)

    return matrix


def convert_numbers_to_pins(numbers, pins=[Pin.IN, Pin.PULL_DOWN]):
    return [Pin(x, *pins) for x in numbers]


def handle_key_press(pressed_keys, matrix, game_id, chose_key=None):


    global move

    response = urequests.post(
        server_url + endpoint + f"?game_id={game_id}",
        json={"pressed_keys": pressed_keys, "matrix": matrix, "timestamp": time.time(), "chose_key": chose_key},
    )

    if response.status_code == 200:

        
        data = response.json()

        response.close()

        if data.get("status") == "success":

            if data.get("white_to_move"):

                move = "w"

            else:
                
                move = "b"
        
        return data


def handle_button(type_button):

    if type_button == move:

        return True
    
    return False

def handle_next_move(current_pressed, matrix, display, white_button, black_button, game_id, chose_key=None):

    result = handle_key_press(current_pressed, matrix, game_id=game_id, chose_key=chose_key)

    if result.get("status") == "success":

        display.fill(0)
        display.text("Move applied!", 0, 0)
        display.show()

    elif result.get("status") == "error":

        display.fill(0)
        display.text("Error applying move", 0, 0)
        display.text("Invalid move. Try again.", 0, 10)
        display.show()

    elif result.get("status") == "ambigouous":

        display.fill(0)
        display.text("Multiple moves detected!", 0, 0)
        display.text("Select a move:", 0, 10)
        
        list_of_moves = result.get("possible_moves", [])

        for idx, move in enumerate(list_of_moves):

            display.text(f"{idx+1}. {move}", 0, 20 + idx*10)
        

        display.show()

        indicator = 0

        while True:
            current_time = time.ticks_ms()

            if white_button[0].value() == 0 and time.ticks_diff(current_time, white_button[1]) > white_button[2]:

                white_button[1] = current_time

                handle_next_move(current_pressed, matrix, display, white_button, black_button, chose_key=list_of_moves[indicator])

                break

            if black_button[0].value() == 0 and time.ticks_diff(current_time, black_button[1]) > black_button[2]:

                indicator = (indicator + 1) % len(list_of_moves)
                black_button[1] = current_time


matrix = create_matrix(8, 8)

display = ssd1306.SSD1306_SPI(128, 64, hspi, dc, rst, cs)

row_pins = convert_numbers_to_pins(rows_reed_switch_pins, [Pin.OUT])
column_pins = convert_numbers_to_pins(columns_reed_switch_pins, [Pin.IN, Pin.PULL_DOWN])

def play_game():

    last_pressed = []

    # get initial state 

    game_id = urequests.post(server_url + "/make_game").json().get("game_id").json()

    game_id = game_id.get("game_id")

    while True:

        current_time = time.ticks_ms()
        correct_button_pressed = False

        if white_button[0].value() == 0 and time.ticks_diff(current_time, white_button[1]) > white_button[2]:

            correct_button_pressed = handle_button("w")
            white_button[1] = time.ticks_ms()

        if black_button[0].value() == 0 and time.ticks_diff(current_time, black_button[1]) > black_button[2]:
            
            correct_button_pressed = handle_button("b")
            black_button[1] = time.ticks_ms()

        current_pressed = scan_matrix(row_pins, column_pins)

        if current_pressed != last_pressed and correct_button_pressed:

            if current_pressed:

                handle_next_move(current_pressed, matrix, display, white_button, black_button, game_id)
                last_pressed = current_pressed

        if not current_pressed:
            last_pressed = current_pressed





def main():


    while not wlan.isconnected() and wlan.status() >= 0:

        print("Waiting to connect...")
        time.sleep(1)

    # connected, now going to confirm start of game

    display.fill(0)
    display.text("Connected to WiFi!", 0, 0)
    display.show()
    time.sleep(2)

    while True:

        display.fill(0)
        display.text("Start game?", 0, 0)
        display.text("Hold white button to start", 0, 10)
        display.show()

        while True:

            current_time = time.ticks_ms()

            # hold 2 seconds logic

            if white_button[0].value() == 0:

                if press_time == 0:
                    press_time = time.ticks_ms()
                    
                elif not held and time.ticks_diff(time.ticks_ms(), press_time) > 2000:

                    play_game()
                    break

            else:
                    
                press_time = 0

            
            

if __name__ == "__main__":

    main()
