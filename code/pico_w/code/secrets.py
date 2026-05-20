import network
import socket
import time
from machine import Pin, ADC
from secret import ssid, password, server_url
import random
import urequests

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

server_url = server_url


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


def convert_numbers_to_pins(
    numbers: list, pins: list = [machine.Pin.IN, machine.Pin.PULL_DOWN]
):

    return list(
        map(
            lambda x: Pin(x, *pins),
            numbers,
        )
    )


def handle_key_press(pressed_keys, matrix):

    urequests.post(
        server_url,
        json={"pressed_keys": pressed_keys, "matrix": matrix, "timestamp": time.time()},
    )


def main():

    # Define the GPIO pin for the matrix of reed switches

    rows_reed_switch_pins = map(
        lambda x: str(x), reversed([6, 7, 8, 9, 10, 11, 12, 13])
    )

    columns_reed_switch_pins = map(lambda x: str(x), [16, 17, 18, 19, 20, 21, 22, 14])

    matrix = create_matrix(8, 8)

    print("Matrix of reed switches:")

    for row in matrix:
        print(row)

    row_pins = convert_numbers_to_pins(rows_reed_switch_pins)
    column_pins = convert_numbers_to_pins(columns_reed_switch_pins)

    while not wlan.isconnected() and wlan.status() >= 0:

        print("Waiting to connect...")
        time.sleep(1)

    last_pressed = []

    while True:

        current_pressed = scan_matrix(row_pins, column_pins)

        # Only print changes to the console to prevent spamming

        if current_pressed != last_pressed:

            if current_pressed:

                handle_key_press(current_pressed, matrix)

            last_pressed = current_pressed

            time.sleep(0.1)  # Debounce and regulate scan rate


if __name__ == "__main__":

    main()
