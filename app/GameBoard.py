from Config import *;

# ToDo:
#      - Take into consideration where other snakes are facing,
#      - etc. Change their weights based on these things.

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
        self.my_snake_coordinates = []

    # Populates the board using the data in the format specified by BattleSnake
    def populate_board(self, data):
        # Get snake attributes
        self.my_health = data['you']['health']
        self.my_length = data['you']['length']
        self.my_snake_coordinates = []


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
            self.my_snake_coordinates.append((x,y))

    # Print the board to the console
    def print_board(self):
        for el in self.board:
            print(el)

        return

    # Retrieves own snake position on the board.
    # Returns a list of (x,y) coordinates. First coordinate on the list is the
    # head of the snake
    def get_my_snake_position(self):
        return self.my_snake_coordinates
        # ToDo: Include the direction the snake is travelling in the return

    def get_right(self):
        my_snake_head_x = self.my_snake_coordinates[0][0]
        my_snake_head_y = self.my_snake_coordinates[0][1]
        value = 0;
        for i in range(my_snake_head_x+1, len(self.board[my_snake_head_y])):
            value = value + self.board[my_snake_head_y][i]
        return value

    def get_left(self):
        my_snake_head_x = self.my_snake_coordinates[0][0]
        my_snake_head_y = self.my_snake_coordinates[0][1]
        value = 0;
        for i in range(my_snake_head_x-1, -1, -1):
            value = value + self.board[my_snake_head_y][i]
        return value

    def get_up(self):
        my_snake_head_x = self.my_snake_coordinates[0][0]
        my_snake_head_y = self.my_snake_coordinates[0][1]
        value = 0;
        for i in range(my_snake_head_y-1, -1, -1):
            value = value + self.board[i][my_snake_head_x]
        return value

    def get_down(self):
        my_snake_head_x = self.my_snake_coordinates[0][0]
        my_snake_head_y = self.my_snake_coordinates[0][1]
        value = 0;
        for i in range(my_snake_head_y+1, len(self.board)):
            value = value + self.board[i][my_snake_head_x]
        return value

    # Obtains the total values for a side of the board and divides it
    # by the number of squares looked at to obtain that value.
    # This is used for as a tie breaker between values
    def get_value_for_right_side(self):
        my_snake_head_x = self.my_snake_coordinates[0][0]
        my_snake_head_y = self.my_snake_coordinates[0][1]
        # loop to obtain value
        count = 0
        value = 0

        for i in range(my_snake_head_x+1, len(self.board[0])):
            for j in range(len(self.board)):
                count = count+1
                value = value + self.board[j][i]
        print('Got value: ', value, ' and count: ', count)
        print('Returned: ', value/count)
        return value/count

    def get_value_for_left_side(self):
        my_snake_head_x = self.my_snake_coordinates[0][0]
        my_snake_head_y = self.my_snake_coordinates[0][1]                # loop to obtain value
        count = 0
        value = 0

        for i in range(my_snake_head_x-1, -1, -1):
            for j in range(len(self.board)):
                count = count+1
                value = value + self.board[j][i]
        print('Got value: ', value, ' and count: ', count)
        print('Returned: ', value/count)
        return value/count

    def get_value_for_up(self):
        my_snake_head_x = self.my_snake_coordinates[0][0]
        my_snake_head_y = self.my_snake_coordinates[0][1]                # loop to obtain value
        count = 0
        value = 0

        for i in range(len(self.board[0])):
            for j in range(my_snake_head_y-1, -1, -1):
                count = count+1
                value = value + self.board[j][i]
        print('Got value: ', value, ' and count: ', count)
        print('Returned: ', value/count)
        return value/count

    def get_value_for_down(self):
        my_snake_head_x = self.my_snake_coordinates[0][0]
        my_snake_head_y = self.my_snake_coordinates[0][1]                # loop to obtain value
        count = 0
        value = 0

        for i in range(len(self.board[0])):
            for j in range(my_snake_head_y+1, len(self.board)):
                count = count+1
                value = value + self.board[j][i]
        print('Got value: ', value, ' and count: ', count)
        print('Returned: ', value/count)
        return value/count
