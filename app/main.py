import bottle
import os
import random
from bs_a_star import a_star
from graph import graph

from GameBoard import GameBoard

my_x = -2
my_y = -2

curr_target_x = -1
curr_target_y = -1

last_move = ''

#Input: game data, a possible move
#Output: boolean
def safeMove(data, move, board):
    myCoords = data['you']['body']['data']
    myLength = data['you']['length']

    if (move == 'up'):
        moveTo = [myCoords[0]['x'], myCoords[0]['y'] - 1]
    elif (move == 'down'):
        moveTo = [myCoords[0]['x'], myCoords[0]['y'] + 1]
    elif (move == 'left'):
        moveTo = [myCoords[0]['x'] - 1, myCoords[0]['y']]
    else:
        moveTo = [myCoords[0]['x'] + 1, myCoords[0]['y']]

    #make sure snake won't do anything stupid
    for i in range(1, myLength):
        #make sure snake won't run into itself
        if (moveTo[0] == myCoords[i]['x'] and moveTo[1] == myCoords[i]['y']):
            return False

    #make sure snake won't run into walls
    if ((moveTo[0] == data['width']) or (moveTo[0] == -1) or (moveTo[1] == data['height']) or (moveTo[1] == -1)):
        return False

    #TODO: this only accounts for where the other snakes are at that moment but doesn't anticipate where they will be next move
    #make sure snake won't run into other snakes
    for i in range(len(data['snakes']['data'])):
        for j in range(len(data['snakes']['data'][i]['body']['data'])):
            enemySnake_x = data['snakes']['data'][i]['body']['data'][j]['x']
            enemySnake_y = data['snakes']['data'][i]['body']['data'][j]['y']
            if (moveTo[0] == enemySnake_x and moveTo[1] == enemySnake_y):
                return False

    for i in range(len(data['snakes']['data'])):
        enemy_snake_x = data['snakes']['data'][i]['body']['data'][0]['x']
        enemy_snake_y = data['snakes']['data'][i]['body']['data'][0]['y']
        if (enemy_snake_x != myCoords[0]['x'] and enemy_snake_y != myCoords[0]['y']):
            enemy_snake_neighbours = board.neighbors((enemy_snake_x, enemy_snake_y))
            for j in range(len(enemy_snake_neighbours)):
                if (moveTo[0] == enemy_snake_neighbours[j][0] and moveTo[1] == enemy_snake_neighbours[j][1]):
                    print('NOOOO')
                    return False



    return True


# Input: snake coordinates, target coordinates
# Output: move
def goTo(my_x, my_y, target_x, target_y, data, board):
    global last_move
    move_x = my_x - target_x
    move_y = my_y - target_y

    #move to target
    if (move_y > 0 ):#and safeMove(data, 'up', board)):
        last_move = 'up'
        return 'up'
    elif (move_y < 0 ):#and safeMove(data, 'down', board)):
        last_move = 'down'
        return 'down'
    elif (move_x > 0 ):#and safeMove(data, 'left', board)):
        last_move = 'left'
        return 'left'
    elif (move_x < 0 ):#and safeMove(data, 'right', board)):
        last_move = 'right'
        return 'right'
    #if you cannot move towards the target, make any safe move
    elif (safeMove(data, 'up', board)):
        last_move = 'up'
        return 'up'
    elif (safeMove(data, 'down', board)):
        last_move = 'down'
        return 'down'
    elif (safeMove(data, 'left', board)):
        last_move = 'left'
        return 'left'
    elif (safeMove(data, 'right', board)):
        last_move = 'right'
        return 'right'

#Input: game data
#Output: coordinates of the closest food
def findClosestFood(data):
    closestDistance = 1000

    for i in range(len(data['food']['data'])):
        food_x = data['food']['data'][i]['x']
        food_y = data['food']['data'][i]['y']
        distance_x = abs(my_x - food_x)
        distance_y = abs(my_y - food_y)
        distance = distance_x + distance_y
        #print('Food: ({0}, {1}) is {2} squares away'.format(food_x, food_y, distance))

        if (distance < closestDistance):
            closestDistance = distance
            target_x = food_x
            target_y = food_y

    print('Closest Food: ({0}, {1}) is {2} squares away'.format(target_x, target_y, closestDistance))

    return (target_x, target_y)



def findPath(board, my_coords, closestFood):
    result = a_star(board, my_coords, closestFood)

    path = []
    node = closestFood
    while node != my_coords:
        if (node in result):
            path.append(node)
            node = result[node]
        else:
            path = []
            break
    path.reverse()

    return path

#Input: game data
#Output: the move to send to the battlesnake server
def nextMove(data):
    global curr_target_x, curr_target_y, my_x, my_y
    board = graph()
    board.init(data['width'], data['height'])
    board.refresh(data)
    #location of snake's head
    my_x = data['you']['body']['data'][0]['x']
    my_y = data['you']['body']['data'][0]['y']
    my_coords = (my_x, my_y)
    my_length = data['you']['length']
    print('My Snake: ({0}, {1})'.format(my_x, my_y))

    #find the closest food
    closestFood = findClosestFood(data)
    print(closestFood)
    if (data['you']['health'] < 50):
        #find path to food
        path = findPath(board, my_coords, closestFood)
        if (len(path) == 0):
            i = 0
            print('???')
            while (len(path) == 0):
                path = findPath(board, my_coords, (data['width'] - my_x + i, data['height'] - my_y + i))
    else:
        #find path to tail
        my_tail_x = data['you']['body']['data'][my_length - 1]['x']
        my_tail_y = data['you']['body']['data'][my_length - 1]['y']
        my_tail_coords = (my_tail_x, my_tail_y)
        path = findPath(board, my_coords, my_tail_coords)
        if (len(path) == 0):
            i = 0
            print('!!!')
            while (len(path) == 0):
                path = findPath(board, my_coords, (data['width'] - my_x + i, data['height'] - my_y + i))

    target_coords = path[0]
    curr_target_x = target_coords[0]
    curr_target_y = target_coords[1]
    print('Current Target = ({0}, {1})').format(curr_target_x, curr_target_y)

    return goTo(my_x, my_y, curr_target_x, curr_target_y, data, board)


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    global curr_target_x, curr_target_y, my_x, my_y
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    my_x = -2
    my_y = -2

    curr_target_x = -1
    curr_target_y = -1


    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#FFCCFF',
        'taunt': 'What a fish!',
        'head_url': head_url,
        'name': 'Big Asp',
        'head_type': 'tongue',
        'tail_type': 'fat-rattle'
    }


@bottle.post('/move')
def move():
    # print('Calculating Move (Last Move = {0})'.format(last_move))
    data = bottle.request.json
    # move = nextMove(data)
    # print(move)
    # directions = ['right', 'left', 'up', 'down']

    g = GameBoard(data['width'], data['height'])
    g.populate_board(data)

    values = []
    right = g.get_right()
    values.append(right)
    left = g.get_left()
    values.append(left)
    up = g.get_up()
    values.append(up)
    down = g.get_down()
    values.append(down)

    maximum = max(values)
    indices = [i for i, v in enumerate(values) if v == maximum]

    tmp_arr = []
    if len(indices) > 1:
        for i in indices:
            if i == 0: # right
                tmp_arr.append((g.get_value_for_right_side(), 'right'))
            if i == 1:
                tmp_arr.append((g.get_value_for_left_side(), 'left'))
            if i == 2:
                tmp_arr.append((g.get_value_for_up(), 'up'))
            if i == 3:
                tmp_arr.append((g.get_value_for_down(), 'down'))

                maximum = max(tmp_arr)
    move = maximum[1]

    g.print_board()
    print('The move picked is: ', move)
    print('The values picked is: ', values)
    print('The tmp_arr picked is: ', tmp_arr)

    return {
        'move': move,
        'taunt': 'You Fish!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
