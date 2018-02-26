import bottle
import os
import random

my_x = -2
my_y = -2

curr_target_x = -1
curr_target_y = -1

# Input: snake coordinates, target coordinates
# Output: move
def goTo(my_x, my_y, target_x, target_y):
    
    move_x = my_x - target_x
    move_y = my_y - target_y

    if (move_y > 0):
        return 'up'
    elif (move_y < 0):
        return 'down'
    elif (move_x > 0):
        return 'left'
    else:
        return 'right'

def findClosestFood(data):
    closestDistance = 1000

    for i in range(len(data['food']['data'])):
        food_x = data['food']['data'][i]['x']
        food_y = data['food']['data'][i]['y']
        distance_x = abs(my_x - food_x)
        distance_y = abs(my_y - food_y)
        distance = distance_x + distance_y
        print('Food: ({0}, {1}) is {2} squares away'.format(food_x, food_y, distance))

        if (distance < closestDistance):
            closestDistance = distance
            target_x = food_x
            target_y = food_y
    
    print('Closest Food: ({0}, {1}) is {2} squares away'.format(target_x, target_y, closestDistance))

    return [target_x, target_y]

def updateGlobals(x, y):
    global curr_target_x, curr_target_y
    curr_target_x = closestFood[0]
    curr_target_y = closestFood[1]

def nextMove(data):
    global curr_target_x, curr_target_y, my_x, my_y
    print('1. curr_target: ({0}, {1})'.format(curr_target_x, curr_target_y))
    
    my_x = data['you']['body']['data'][0]['x']
    my_y = data['you']['body']['data'][0]['y']
    print('My Snake: ({0}, {1})'.format(my_x, my_y))
    print('2. curr_target: ({0}, {1})'.format(curr_target_x, curr_target_y))
    if((my_x == curr_target_x and my_y == curr_target_y) or (curr_target_x == -1 and curr_target_y == -1)):
        print('Food was eaten')
        closestFood = findClosestFood(data)
        print('closest food: ({0}, {1})'.format(closestFood[0], closestFood[1]))
        updateGlobals(closestFood[0], closestFood[1])

    print('3. curr_target: ({0}, {1})'.format(curr_target_x, curr_target_y))

    return goTo(my_x, my_y, curr_target_x, curr_target_y)


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

    print('my: ({0},{1})    ,     curr_target: ({2},{3})'.format(my_x, my_y, curr_target_x, curr_target_y))


    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#FF9333',
        'taunt': 'What a fish!',
        'head_url': head_url,
        'name': 'Big Asp',
        'head_type': 'tongue',
        'tail_type': 'curled'
    }


@bottle.post('/move')
def move():
    print('Calculating Move')
    data = bottle.request.json

    print('Inside /move:    my: ({0},{1})    ,     curr_target: ({2},{3})'.format(my_x, my_y, curr_target_x, curr_target_y))
    # TODO: Do things with data
    move = nextMove(data)
    print(move)
    directions = ['up', 'down', 'left', 'right']

    return {
        'move': move,
        'taunt': 'You Fish!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
