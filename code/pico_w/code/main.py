import network
import socket
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

server_url = server_url
endpoint = "/pressed_keys"


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


def handle_key_press(pressed_keys, matrix):

    response = urequests.post(
        server_url + endpoint,
        json={"pressed_keys": pressed_keys, "matrix": matrix, "timestamp": time.time()},
    )

    if response.status_code == 200:

        response_data = response.json()

        if response_data.get("white_to_move"):

            move = "w"

        else:

            move = "b"

def handle_button(type_button):

    if type_button == move:

        return True
    
    return False


def main():

    # Place Holder Pins(for OLED & buttons)

    white_button = [Pin(15, Pin.IN, Pin.PULL_DOWN), 200]
    black_button = [Pin(26, Pin.IN, Pin.PULL_DOWN), 0, 200]

    rows_reed_switch_pins = list(reversed([6, 7, 8, 9, 10, 11, 12, 13]))
    columns_reed_switch_pins = [16, 17, 18, 19, 20, 21, 22, 14]

    hspi = SPI(1)  

    dc = Pin(4) 
    rst = Pin(5)   
    cs = Pin(15) 

    matrix = create_matrix(8, 8)

    display = ssd1306.SSD1306_SPI(128, 64, hspi, dc, rst, cs)


    print("Matrix of reed switches:")
    for row in matrix:
        print(row)


    row_pins = convert_numbers_to_pins(rows_reed_switch_pins, [Pin.OUT])
    column_pins = convert_numbers_to_pins(columns_reed_switch_pins, [Pin.IN, Pin.PULL_DOWN])

    while not wlan.isconnected() and wlan.status() >= 0:

        print("Waiting to connect...")
        time.sleep(1)

    last_pressed = []

    while True:

        current_time = time.ticks_ms()
        correct_button_pressed = False

        if white_button[0].value() == 0 and time.ticks_diff(current_time, white_button[1]) > white_button[2]:

            correct_button_pressed = handle_button("w")
            white_button[1] = current_time

        if black_button[0].value() == 0 and time.ticks_diff(current_time, black_button[1]) > black_button[2]:
            
            correct_button_pressed = handle_button("b")
            black_button[1] = current_time

        current_pressed = scan_matrix(row_pins, column_pins)

        if current_pressed != last_pressed and correct_button_pressed:

            if current_pressed:

                handle_key_press(current_pressed, matrix)

if __name__ == "__main__":

    main()
