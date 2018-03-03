from Config import *;

class GameBoard:

    # Creates a game board with preset boarder values
    def __init__(self, width, height):
        empty_value = Config.empty_square
        self.board = [[empty_value for x in range(width+2)] for y in range(height+2)]
        # Add border
        for i in range(len(self.board)):
            self.board[i][0] = Config.border
            self.board[i][len(self.board[0])-1] = Config.border
        for i in range(len(self.board[0])-1):
            self.board[0][i] = Config.border
            self.board[len(self.board)-1][i] = Config.border

    # Populates the board using the data in the format specified by BattleSnake
    def populate_board(self, data):
        # Get snake attributes
        self.my_health = data['you']['health']
        self.my_length = data['you']['length']


        # Placing food on the board
        if self.my_health > 50:
            food_value = Config.food_has_high_health
        else:
            food_value = Config.food_has_low_health
        # Populate food on board
        for food in data['food']['data']:
            x = (food['x']) + 1 # +1 to account for borders
            y = (food['y']) + 1
            self.board[y][x] = food_value


        # Placing enemy snakes on the board
        for snake in data['snakes']['data']:
            if snake['length'] > self.my_length:
                enemy_value = Config.enemy_is_bigger
            elif snake['length'] < self.my_length:
                enemy_value = Config.enemy_is_smaller
            else:
                # ADD MORE LOGIC TO THIS
                enemy_value = Config.enemy_is_equal
            for el in snake['body']['data']:
                x = (el['x']) + 1 # +1 to account for borders
                y = (el['y']) + 1
                self.board[y][x] = enemy_value
            # ToDo: Add a check to each enemy snake here. If their head is facing us
            #       and they are smaller, then update the value of their head on the
            #       board.


        # Placing own snake on the board
        for el in data['you']['body']['data']:
            x = (el['x']) + 1 # +1 to account for borders
            y = (el['y']) + 1
            self.board[y][x] = Config.my_snake


    def print_board(self):
        for el in self.board:
            print(el)

        return
