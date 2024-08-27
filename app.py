from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

CORS(app)

class Board:
    def __init__(self):
        # Initialize a 5x5 grid with empty strings representing empty spaces
        self.grid = [['' for _ in range(5)] for _ in range(5)]


    def place_character(self, character, position):
        # Place a character on the grid at the given position
        x, y = position
        if self.grid[x][y] == '':
            self.grid[x][y] = character.name
        else:
            raise ValueError("Position already occupied")

    def move_character(self, character, new_position):
        # Move a character from its current position to a new position on the grid
        old_x, old_y = character.position
        new_x, new_y = new_position

        # Ensure the new position is within bounds
        if 0 <= new_x < 5 and 0 <= new_y < 5:
            # Check if the new position is empty or occupied by an opponent's character
            if self.grid[new_x][new_y] == '' or self.grid[new_x][new_y][0] != character.player:
                # Remove the character from the old position
                self.grid[old_x][old_y] = ''
                # Place the character at the new position
                self.grid[new_x][new_y] = character.name
                # Update the character's position
                character.position = new_position
            else:
                raise ValueError("Cannot move to a position occupied by a friendly character")
        else:
            raise ValueError("New position is out of bounds")


class Character:
    def __init__(self, name, player):
        self.name = name
        self.player = player
        self.position = None

    def move(self, direction, board):
        pass  # We'll apply this method in subclasses

    def is_within_bounds(self, position):
        x, y = position
        return 0 <= x < 5 and 0 <= y < 5


class Pawn(Character):
    def move(self, direction, board):
        x, y = self.position

        if self.player == 'A':  # Normal controls for Player A
            if direction == 'L':
                new_position = (x, y + 1)
            elif direction == 'R':
                new_position = (x, y - 1)
            elif direction == 'F':
                new_position = (x + 1, y)
            elif direction == 'B':
                new_position = (x - 1, y)
            else:
                return False   # Invalid direction
        elif self.player == 'B':  # Inverted controls for Player B
            if direction == 'L':
                new_position = (x, y - 1)
            elif direction == 'R':
                new_position = (x, y + 1)
            elif direction == 'F':
                new_position = (x - 1, y)
            elif direction == 'B':
                new_position = (x + 1, y)
            else:
                return False  # Invalid direction

        if self.is_within_bounds(new_position) and self.is_valid_move(new_position, board):
            return self.update_position_and_attack(new_position, board)
        return False

    def is_valid_move(self, new_position, board):
        x, y = new_position
        target_cell = board.grid[x][y]

        # The move is valid if the target cell is either empty or occupied by an opponent's piece
        return target_cell == '' or target_cell[0] != self.player

    def update_position_and_attack(self, new_position, board):
        print(new_position)
        x, y = new_position

        # Check the target cell
        target_cell = board.grid[x][y]

        # Clear the current position
        board.grid[self.position[0]][self.position[1]] = ''

        # If there's an opponent's piece, remove it (capture)
        if target_cell != '' and target_cell[0] != self.player:
            board.grid[x][y] = ''  # Remove opponent's piece

        # Move the Hero2 piece to the new position
        self.position = new_position
        board.grid[x][y] = self.name  # Place Hero2 at the new position

        return True



class Hero1(Character):
    def move(self, direction, board):
        x, y = self.position

        if self.player == 'A':  # Normal controls for Player A
            if direction == 'L':
                new_position = (x, y + 2)
            elif direction == 'R':
                new_position = (x, y - 2)
            elif direction == 'F':
                new_position = (x + 2, y)
            elif direction == 'B':
                new_position = (x - 2, y)
            else:
                return False  # Invalid direction
        elif self.player == 'B':  # Inverted controls for Player B
            if direction == 'L':
                new_position = (x, y - 2)
            elif direction == 'R':
                new_position = (x, y + 2)
            elif direction == 'F':
                new_position = (x - 2, y)
            elif direction == 'B':
                new_position = (x + 2, y)
            else:
                return False  # Invalid direction

        if self.is_within_bounds(new_position) and self.is_valid_move(new_position, board):
            return self.update_position_and_attack(new_position, board)
        return False

    def is_valid_move(self, new_position, board):
        x, y = new_position
        target_cell = board.grid[x][y]

        # The move is valid if the target cell is either empty or occupied by an opponent's piece
        return target_cell == '' or target_cell[0] != self.player

    def update_position_and_attack(self, new_position, board):
        print(new_position)
        x, y = new_position

        # Check the target cell
        target_cell = board.grid[x][y]

        # Clear the current position
        board.grid[self.position[0]][self.position[1]] = ''

        # If there's an opponent's piece, remove it (capture)
        if target_cell != '' and target_cell[0] != self.player:
            board.grid[x][y] = ''  # Remove opponent's piece

        # Move the Hero2 piece to the new position
        self.position = new_position
        board.grid[x][y] = self.name  # Place Hero2 at the new position

        return True



class Hero2(Character):
    def move(self, direction, board):
        x, y = self.position

        # Determine the new position based on the direction
        if self.player == 'A':  # Normal controls for Player A
            if direction == 'FL':
                new_position = (x + 1, y + 1)
            elif direction == 'FR':
                new_position = (x + 1, y - 1)
            elif direction == 'BL':
                new_position = (x - 1, y + 1)
            elif direction == 'BR':
                new_position = (x - 1, y - 1)
            else:
                return False  # Invalid direction

        elif self.player == 'B':  # Inverted controls for Player B
            if direction == 'FL':
                new_position = (x - 1, y - 1)
            elif direction == 'FR':
                new_position = (x - 1, y + 1)
            elif direction == 'BL':
                new_position = (x + 1, y - 1)
            elif direction == 'BR':
                new_position = (x + 1, y + 1)
            else:
                return False  # Invalid direction
            
        print(new_position)

        # Check if the new position is within bounds and not occupied by a friendly piece
        if self.is_within_bounds(new_position) and self.is_valid_move(new_position, board):
            return self.update_position_and_attack(new_position, board)
        return False

    def is_valid_move(self, new_position, board):
        x, y = new_position
        target_cell = board.grid[x][y]

        # The move is valid if the target cell is either empty or occupied by an opponent's piece
        return target_cell == '' or target_cell[0] != self.player

    def update_position_and_attack(self, new_position, board):
        print(new_position)
        x, y = new_position

        # Check the target cell
        target_cell = board.grid[x][y]

        # Clear the current position
        board.grid[self.position[0]][self.position[1]] = ''

        # If there's an opponent's piece, remove it (capture)
        if target_cell != '' and target_cell[0] != self.player:
            board.grid[x][y] = ''  # Remove opponent's piece

        # Move the Hero2 piece to the new position
        self.position = new_position
        board.grid[x][y] = self.name  # Place Hero2 at the new position

        return True



class Player:
    def __init__(self, identifier):
        self.identifier = identifier  # 'A' for Player 1, 'B' for Player 2
        self.characters = []

    def place_characters(self, board):
        # Fixed initial positions for both players
        if self.identifier == 'A':
            characters = ['A-P1', 'A-P2', 'A-H1', 'A-H2', 'A-P3']
            starting_row = 0
        elif self.identifier == 'B':
            characters = ['B-P1', 'B-P2', 'B-H1', 'B-H2', 'B-P3']
            starting_row = 4
        else:
            raise ValueError("Invalid player identifier")

        for i, char_name in enumerate(characters):
            # Create the appropriate character instance based on the character name
            if 'P' in char_name:
                character = Pawn(char_name, self.identifier)
            elif 'H1' in char_name:
                character = Hero1(char_name, self.identifier)
            elif 'H2' in char_name:
                character = Hero2(char_name, self.identifier)
            else:
                raise ValueError("Invalid character name")

            # Set the initial position for the character on the board
            character.position = (starting_row, i)

            # Place the character on the board
            board.grid[starting_row][i] = char_name

            # Add the character to the player's list of characters
            self.characters.append(character)


class Game:
    def __init__(self):
        self.board = Board()
        self.players = [Player('A'), Player('B')]
        self.current_player_index = 0
        self.game_over = False

    def start(self):
        # Place characters for both players at the start of the game
        self.players[0].place_characters(self.board)  # Player A
        self.players[1].place_characters(self.board)  # Player B

    def play_turn(self, move):
        player = self.players[0] if move['player'] == 'A' else self.players[1]
        
        # Find the character the player is trying to move
        character = next((char for char in player.characters if char.name == move['character']), None)

        if not character:
            print(f"Invalid character name: {move['character']} for player {move['player']}")
            return False

        print(f"Character {character.name} found at position {character.position}")

        # Try to move the character
        move_successful = character.move(move['direction'], self.board)
        print(f"Move success: {move_successful}")  # Debug print

        if move_successful:
            # Switch to the next player if the move was successful
            self.current_player_index = 1 - self.current_player_index
            return True
        else:
            print(f"Move failed for character {character.name}")
            return False


    def check_winner(self):
        # Check if any characters of Player A are still on the board
        player_a_has_characters = any(
            character.position is not None for character in self.players[0].characters
        )

        # Check if any characters of Player B are still on the board
        player_b_has_characters = any(
            character.position is not None for character in self.players[1].characters
        )

        # Determine the winner based on remaining characters on the board
        if not player_a_has_characters:  # Player A has no characters left on the board
            print("Player B wins!")
            self.game_over = True
            return True
        elif not player_b_has_characters:  # Player B has no characters left on the board
            print("Player A wins!")
            self.game_over = True
            return True

        return False



# Flask Routes and WebSocket Events
game = Game()
game.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/board')
def get_board_state():
    print("Board route accessed")
    return jsonify(game.board.grid)


connected_players = []

@socketio.on('connect')
def handle_connect():
    global connected_players
    if len(connected_players) < 2:
        player_id = 'A' if len(connected_players) == 0 else 'B'
        connected_players.append(request.sid)
        emit('player_assigned', {'player': player_id}, to=request.sid)
    else:
        emit('message', {'data': 'Game is full!'}, to=request.sid)


@socketio.on('test_event')
def handle_test_event():
    print("Test event received")
    emit('message', {'data': 'Test event acknowledged'})


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('move')
def handle_move(data):
    current_player = game.players[game.current_player_index]
    
    # Process the move
    move_valid = game.play_turn(data)

    if move_valid:
        # Check if the game is over
        if game.check_winner():
            socketio.emit('game_over', {'winner': current_player.identifier}, to='/')
            game.game_over = True
        else:
            # Continue the game by switching turns
            next_player = game.players[game.current_player_index].identifier
            socketio.emit('update', {
                'grid': game.board.grid,
                'current_player': next_player
            }, to='/')  # Emit to all connected clients
    else:
        emit('message', {'data': 'Invalid move'}, to=request.sid)



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

