import bottle
import os
import random

# Current Strategy: Go directly to food
def nextMove(data):
    my_x = data['you']['body']['data'][0]['x']
    my_y = data['you']['body']['data'][0]['x']
    print('My Snake: ' my_x + ', ' + my_y)

    food_x = data['food']['data'][0]['x']
    food_y = data['food']['data'][0]['y']
    print('Food: ' food_x + ', ' + food_y)

    move_x = my_x - food_x
    move_y = my_y - food_y

    if (move_x > 0):
        return 'down'
    elif (move_x < 0):
        return 'up'
    elif (move_y > 0):
        return 'left'
    else:
        return 'right'


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

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
    data = bottle.request.json

    # TODO: Do things with data
    move = nextMove(data)
    print(move)
    directions = ['up', 'down', 'left', 'right']

    return {
        'move': move,
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
