from pathlib import Path
import json
import re
import time
import chess
import chess.svg 

def board_to_2d_array(board):

    arr = []

    for rank in (range(8)):
        row = []
        for file in range(8):
            piece = board.piece_at(chess.square(file, rank))
            row.append(piece.symbol() if piece else " ")
        arr.append(row)
    return arr

def board_to_magnetic_state(board):
    return [[1 if board.piece_at(chess.square(file, rank)) else 0 for file in range(8)] for rank in (range(8))]

def square_to_row_col(square, matrix):
    name = chess.square_name(square)
    for r in range(8):
        for c in range(8):
            if matrix[r][c] == name:
                return [r, c]
    return None

class ProcessPressedKeys:
    def __init__(self, data, game_id):
        
        self.game_id = re.sub(r'[^a-zA-Z0-9]', '', game_id) if game_id else "default"
        self.update_data(data)

    def load_game_state(self):
        game_state_path = Path(__file__).parent.parent.resolve() / "game_state" / f"{self.game_id}.json"
        
        if game_state_path.exists():
            with open(game_state_path, "r") as f:
                return json.load(f)
        else:
            with open(game_state_path, "w") as f:
                initial_state = {
                    "fen": chess.STARTING_FEN,
                    "board": board_to_2d_array(chess.Board()),
                    "magnetic_state": board_to_magnetic_state(chess.Board()),
                    "white_to_move": True,
                    "white_timer": 300,
                    "game_over": False,
                    "current_game_id": self.game_id,
                    "black_timer": 300,
                    "last_move_timestamp": self.timestamp,
                    "move_history": []
                }
                json.dump(initial_state, f, indent=4)
            return initial_state
    
        
    
    def update_data(self, data):
        self.data = data
        self.pressed_keys = data["pressed_keys"]
        self.matrix = data["matrix"]
        self.chose_key = data.get("chose_key", None)
        self.timestamp = data["timestamp"]

    def process(self):

        self.game_state = self.load_game_state()

        if not self.game_state:
        
            return {"status": "error", "message": "Failed to load game state"}

        fen = self.game_state.get("fen", chess.STARTING_FEN)
        board = chess.Board(fen)


        try:

            physical_occupied = set(chess.parse_square(self.matrix[r][c]) for r, c in self.pressed_keys)

        except Exception as e:

            return {"status": "error", "message": f"Invalid coordinates received: {str(e)}"}


        current_occupied = set(sq for sq in chess.SQUARES if board.piece_at(sq) is not None)
        
        if physical_occupied == current_occupied:
            
            return {
                "status": "idle",
                "message": "No move made.",
                "game_state": self.game_state
            }


        matched_moves = []
        
        for move in board.legal_moves:

            board.push(move)
            simulated_occupied = set(sq for sq in chess.SQUARES if board.piece_at(sq) is not None)
            board.pop()
            
            if physical_occupied == simulated_occupied:
            
                matched_moves.append(move)

        if self.chose_key:

            self.chose_key = chess.Move.from_uci(self.chose_key)

            if self.chose_key in matched_moves:

                matched_moves = [self.chose_key]


        if not matched_moves:
            raise Exception("Invalid move")


        if len(matched_moves) > 1:

            # Change from last time - so basically if we have multiple matches, and those matches are promotion we promote the queen
            # If not we send back ambigouous 

            is_promotion = any(move.promotion for move in matched_moves)

            if is_promotion:

                matched_move = next((m for m in matched_moves if m.promotion == chess.QUEEN), matched_moves[0])
            
            else:

                return {

                    "status": "ambiguous",
                    "message": "Multiple possible moves detected. Please clarify the move.",
                    "possible_moves": [chess.Move.uci(move) for move in matched_moves]

                }

        

        else:
           
            matched_move = matched_moves[0]


        from_sq = matched_move.from_square
        to_sq = matched_move.to_square
        piece_moved_obj = board.piece_at(from_sq)
        piece_moved = piece_moved_obj.symbol() if piece_moved_obj else None

        if board.is_en_passant(matched_move):
            piece_taken = "p" if board.turn == chess.WHITE else "P"
        else:
            piece_taken_obj = board.piece_at(to_sq)
            piece_taken = piece_taken_obj.symbol() if piece_taken_obj else None

        from_square = square_to_row_col(from_sq, self.matrix)
        to_square = square_to_row_col(to_sq, self.matrix)

        move_entry = {
            "from_square": from_square,
            "to_square": to_square,
            "piece_moved": piece_moved,
            "piece_taken": piece_taken
        }


        white_turn = board.turn == chess.WHITE
        time_elapsed = self.timestamp - self.game_state.get("last_move_timestamp", self.timestamp)
        white_timer = self.game_state.get("white_timer", 300)
        black_timer = self.game_state.get("black_timer", 300)

        if white_turn:
            white_timer -= time_elapsed
        else:
            black_timer -= time_elapsed


        board.push(matched_move)
        game_over = board.is_game_over()

        self.game_state["fen"] = board.fen()
        self.game_state["board"] = board_to_2d_array(board)
        self.game_state["magnetic_state"] = board_to_magnetic_state(board)
        self.game_state["white_to_move"] = board.turn == chess.WHITE
        self.game_state["white_timer"] = white_timer
        self.game_state["black_timer"] = black_timer
        self.game_state["last_move_timestamp"] = self.timestamp
        self.game_state["game_over"] = game_over
        self.game_state["move_history"].append(move_entry)



        game_state_path = Path(__file__).parent.parent.resolve() / "game_state" / f"{self.game_id}.json"
        
        with open(game_state_path, "w") as f:
            json.dump(self.game_state, f, indent=4)

        return {
            "status": "success",
            "message": f"Move {chess.square_name(from_sq)} to {chess.square_name(to_sq)} applied successfully.",
            "game_state": self.game_state
        }
