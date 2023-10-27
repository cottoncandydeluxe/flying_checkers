class Checkers:
    """Represents a checkerboard, with methods for the users to choose teams, take turns,
    manipulate the board, capture enemy pieces, and win the game. This class will communicate
    with the Player class when create_player is called and a new Player object is created.
    The Player object's data members are accessible via get-methods."""
    def __init__(self):
        """Automatically initializes a virtual checkerboard (list of lists) for a new game with no
        parameters, and returns nothing."""
        self._checkerboard = [[ None,  'White', None,  'White', None,  'White', None,  'White'],
                              ['White', None,  'White', None,  'White', None,  'White', None  ],
                              [ None,  'White', None,  'White', None,  'White', None,  'White'],
                              [ None,   None,   None,   None,   None,   None,   None,   None  ],
                              [ None,   None,   None,   None,   None,   None,   None,   None  ],
                              ['Black', None,  'Black', None,  'Black', None,  'Black', None  ],
                              [ None,  'Black', None,  'Black', None,  'Black', None,  'Black'],
                              ['Black', None,  'Black', None,  'Black', None,  'Black', None  ]]

        self._current_turn = 'Black'
        self._players_dict = {}
        self._last_turn = ['piece color', 0]

    def get_checkerboard(self):
        """Gets checkerboard data."""
        return self._checkerboard

    def create_player(self, player_name, piece_color):
        """Takes as parameter the player_name and piece_color that the player wants to play with
        and creates the player object. The parameter piece_color is a string of value "Black"
        or "White", and it returns the player object."""
        self._players_dict[player_name] = piece_color
        return Player(player_name, piece_color, self)

    def play_game(self, player_name, starting_square_location, destination_square_location):
        """Takes as parameters: player_name, starting_square_location (x,y), and destination_square_location (x,y)
        of the piece that the player wants to move. This method moves this piece, stores its new location, updates
        the old location, and replaces captured pieces with 'None'. It checks for three exceptions for invalid moves:
        OutofTurn, InvalidSquare, and InvalidPlayer. If the destination piece reaches the end of opponent's side it
        is promoted to a king. If the piece crosses back to its original side it then becomes a triple king.
        This method also keeps track of whose turn it is, and allows for a second turn if a player has an opportunity
        for a double jump. This method returns the number of captured pieces during the player's turn, if any."""

        # INVALID PLAYER
        if player_name not in self._players_dict:  # checks to see if the player exists in players_dict
            raise InvalidPlayer

        # OUT OF TURN
        if self._players_dict[player_name] != self._current_turn:  # checks to see that the player's color matches the current_turn
            if self._last_turn[0] == self._players_dict[player_name] and self._last_turn[1] > 0:
                if self._current_turn == 'Black':  # switches turn
                    temp = 'White'
                if self._current_turn == 'White':
                    temp = 'Black'
                self._current_turn = temp
            else:
                raise OutofTurn

        # INVALID STARTING SQUARE
        (row_start, column_start) = starting_square_location  # unpack the tuples
        (row_destination, column_destination) = destination_square_location

        try: # check for user attempting to use a starting_square_location that DNE
            self._checkerboard[row_start][column_start]
        except IndexError:
            raise InvalidSquare

        current_piece = self._checkerboard[row_start][column_start]  # grab the current piece

        if self._players_dict[player_name] == 'Black':  # check to see that piece belongs to 'Black' player
            if current_piece != 'Black' and current_piece != 'Black_king' and current_piece != 'Black_Triple_King':
                raise InvalidSquare
        if self._players_dict[player_name] == 'White':  # check to see that piece belongs to 'White' player
            if current_piece != 'White' and current_piece != 'White_king' and current_piece != 'White_Triple_King':
                raise InvalidSquare

        # MOVE PIECES
        self._checkerboard[row_destination][column_destination] = current_piece  # stick in the destination
        self._checkerboard[row_start][column_start] = None  # clear starting square location

        # CAPTURES
        capture_count = 0
        row_traveled = row_destination
        column_traveled = column_destination
        while (row_traveled, column_traveled) != (row_start, column_start):
            if row_traveled < row_start:
                row_traveled += 1  # travel down
            if row_traveled > row_start:
                row_traveled -= 1  # travel up
            if column_traveled < column_start:
                column_traveled += 1 # travel to the right
            if column_traveled > column_start:
                column_traveled -= 1  # travel to the left
            square = self._checkerboard[row_traveled][column_traveled]
            if self._players_dict[player_name] == 'Black':
                if square == 'White' or square == 'White_king' or square == "White_Triple_King":
                    self._checkerboard[row_traveled][column_traveled] = None
                    capture_count += 1
            if self._players_dict[player_name] == 'White':
                if square == 'Black' or square == 'Black_king' or square == "Black_Triple_King":
                    self._checkerboard[row_traveled][column_traveled] = None
                    capture_count += 1

        # CHECK OUTOFTURN AGAIN FOR DOUBLE JUMPS
        if capture_count == 0 and self._last_turn[0] == self._players_dict[player_name]:
            self._checkerboard[row_destination][column_destination] = None   # clear the destination
            self._checkerboard[row_start][column_start] = current_piece  # put piece back at starting square location
            raise OutofTurn


        # KING CEREMONIES
        if self._checkerboard[row_destination][column_destination] == 'Black' and row_destination == 0: # King ceremony conditions
            self._checkerboard[row_destination][column_destination] = 'Black_king'
        if self._checkerboard[row_destination][column_destination] == 'White' and row_destination == 7:
            self._checkerboard[row_destination][column_destination] = 'White_king'

        if self._checkerboard[row_destination][column_destination] == 'Black_king' and row_destination == 7:  # Triple King ceremony conditions
            self._checkerboard[row_destination][column_destination] = 'Black_Triple_King'
        if self._checkerboard[row_destination][column_destination] == 'White_king' and row_destination == 0:
            self._checkerboard[row_destination][column_destination] = 'White_Triple_King'

        # TURN SWITCHES
        self._last_turn[0] = self._players_dict[player_name]  # update last_turn data member for double jump allowance
        self._last_turn[1] = capture_count
        if self._current_turn == 'Black':  # switches turn at end of player turn
            temp = 'White'
        if self._current_turn == 'White':
            temp = 'Black'
        self._current_turn = temp

        # RETURN CAPTURES
        return capture_count

    def get_checker_details(self, square_location):
        """Takes as parameter a square_location on the checkerboard and returns the value/details in the
         square_location."""
        (row, column) = square_location
        try:
            return self._checkerboard[row][column]
        except IndexError:
            raise InvalidSquare

    def print_board(self):
        """Takes no parameters, prints the current checkerboard as a list of lists."""
        print(self._checkerboard)

    def print_better_board(self):
        """Takes no parameters, but prints the current checkerboard's lists one at time, allowing line breaks
        to improve readability for the user, and improve debugging for the dev."""
        print(['0    ', '1    ', '2    ', '3    ', '4    ', '5    ', '6    ', '7    '])
        column_count = 0
        for row in self._checkerboard:
            print(column_count)
            column_count += 1
            print(row)
        print(' ')
        print(' ')

    def game_winner(self):
        """Takes no parameters, returns the name of player who won the game. If the game has not ended, it
        returns 'Game has not ended'."""
        attendance = 0  # take 'Black' attendance
        for row in self._checkerboard:
            if 'Black' in row or 'Black_king' in row or 'Black_Triple_King' in row:
                attendance += 1
        if attendance > 0:
            black = True
        else:
            black = False

        attendance = 0  # take 'White' attendance
        for row in self._checkerboard:
            if 'White' in row or 'White_king' in row or 'White_Triple_King' in row:
                attendance += 1
        if attendance > 0:
            white = True
        else:
            white = False

        if black and white:
            return 'Game has not ended'

        if not black:  # 'White' wins
            for key in self._players_dict:
                if self._players_dict[key] == 'White':
                    return key

        if not white:  # 'Black' wins
            for key in self._players_dict:
                if self._players_dict[key] == 'Black':
                    return key


class Player:
    """Player object represents the player in a checkers game.
    The Player class will not need to communicate to other classes."""
    def __init__(self, player_name, checker_color, game_object):
        """Creates a Player object with the parameter's player_name and checker_color. Returns nothing."""
        self._player_name = player_name
        self._checker_color = checker_color
        self._game = game_object

    def get_king_count(self):
        """Takes no parameters, returns the count of king pieces that the player has."""
        checkerboard = self._game.get_checkerboard()
        king_count = 0

        if self._checker_color == 'Black':
            for row in checkerboard:
                for square in row:
                    if square == 'Black_king':
                        king_count += 1
            return king_count

        if self._checker_color == 'White':
            for row in checkerboard:
                for square in row:
                    if square == 'White_king':
                        king_count += 1
            return king_count

    def get_triple_king_count(self):
        """Takes no parameter, returns the count of triple king pieces that the player has."""
        checkerboard = self._game.get_checkerboard()
        triple_king_count = 0

        if self._checker_color == 'Black':
            for row in checkerboard:
                for square in row:
                    if square == 'Black_Triple_King':
                        triple_king_count += 1
            return triple_king_count

        if self._checker_color == 'White':
            for row in checkerboard:
                for square in row:
                    if square == 'White_Triple_King':
                        triple_king_count += 1
            return triple_king_count

    def get_captured_pieces_count(self):
        """Takes no parameter, returns the number of opponent pieces that the player has captured."""
        checkerboard = self._game.get_checkerboard()
        enemy_count = 0

        if self._checker_color == 'Black':
            for row in checkerboard:
                for square in row:
                    if square == 'White' or square == 'White_king' or square == 'White_Triple_King':
                        enemy_count += 1
            return 12 - enemy_count

        if self._checker_color == 'White':
            for row in checkerboard:
                for square in row:
                    if square == 'Black' or square == 'Black_king' or square == 'Black_Triple_King':
                        enemy_count += 1
            return 12 - enemy_count


class OutofTurn(Exception):
    """User-defined exception for player is out of turn. This exception will be raised inside
    the Checkers class."""
    pass


class InvalidSquare(Exception):
    """User-defined exception for if a player does not own the checker present in the
    square_location or if the square_location does not exist on the board.
    This exception will be raised inside the Checkers class."""
    pass


class InvalidPlayer(Exception):
    """User-defined exception for an in_valid player_name if the name does not exist. This exception will be
    raised inside the Checkers class."""
    pass




