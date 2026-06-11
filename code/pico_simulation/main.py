import time
import requests

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

def main():

    # first create game and get game id

    server_url = "http://127.0.0.1:5000/pressed_keys"

    game_id = requests.post(server_url.replace("/pressed_keys", "/make_game")).json().get("game_id")

    matrix = create_matrix(8, 8)

    pressed_keys = [
        [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], 
        [1, 0], [1, 1], [1, 2], [1, 3],         [1, 5], [1, 6], [1, 7],
                                        [3, 4],
        [6, 0], [6, 1], [6, 2], [6, 3], [6, 4], [6, 5], [6, 6], [6, 7],
        [7, 0], [7, 1], [7, 2], [7, 3], [7, 4], [7, 5], [7, 6], [7, 7]
    ]
    timestamp = time.time()
    
    data = {
        "pressed_keys": pressed_keys,
        "matrix": matrix,
        "timestamp": timestamp
    }


    response = requests.post(server_url + f"/?game_id={game_id}", json=data)

    if response.status_code == 200:

        print("Data sent successfully!")
        print("Response:", response.json())

    else:
        
        print("Failed to send data. Status code:", response.status_code)
        print("Response:", response.text)

    time.sleep(5) 

    pressed_keys = [
        [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], 
        [1, 0], [1, 1], [1, 2], [1, 3],         [1, 5], [1, 6], [1, 7],
                                        [3, 4],
        [6, 0], [6, 1],         [6, 3], [6, 4], [6, 5], [6, 6], [6, 7],
                        [4, 2],
        [7, 0], [7, 1], [7, 2], [7, 3], [7, 4], [7, 5], [7, 6], [7, 7]
    ]
    
    timestamp = time.time()
    
    data = {
        "pressed_keys": pressed_keys,
        "matrix": matrix,
        "timestamp": timestamp
    }

    response = requests.post(server_url + f"/?game_id={game_id}", json=data)


    if response.status_code == 200:

        print("Data sent successfully!")
        print("Response:", response.json())

    else:
        
        print("Failed to send data. Status code:", response.status_code)
        print("Response:", response.text)




if __name__ == "__main__":
    
    main()