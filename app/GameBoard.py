from Config import *;

class GameBoard:

    # Creates a game board with preset boarder values
    def __init__(self, width, height):
        self.board = [[0 for x in range(width+2)] for y in range(height+2)]
        # Add border
        for i in range(len(self.board)):
            self.board[i][0] = Config.border
            self.board[i][len(self.board[0])-1] = Config.border
        for i in range(len(self.board[0])-1):
            self.board[0][i] = Config.border
            self.board[len(self.board)-1][i] = Config.border

    # Populates the board using the data in the format specified by BattleSnake
    def populate_board(self, data):
        # Get snake health
        self.my_health = 100

        # Placing food on the board
        if self.my_health > 50:
            food_value = Config.food_has_high_health
        else:
            food_value = Config.food_has_low_health
        # Populate food on board
        for el in data['food']['data']:
            x = (el['x']) + 1 # +1 to account for borders
            y = (el['y']) + 1
            self.board[y][x] = food_value

        return
