import bottle
import os
import random

my_x = -2
my_y = -2

curr_target_x = -1
curr_target_y = -1

last_move = ''

safeVar = 0

#Input: game data, a possible move
#Output: boolean
def safeMove(data, my_x, my_y, move, recurseTracker):
    global safeVar
    myLength = data['you']['length']
    myCoords = data['you']['body']['data']

    if (move == 'up'):
        moveTo = [my_x, my_y - 1]
    elif (move == 'down'):
        moveTo = [my_x, my_y + 1]
    elif (move == 'left'):
        moveTo = [my_x - 1, my_y]
    else:
        moveTo = [my_x + 1, my_y]

    #make sure snake won't do anything stupid
    if(recurseTracker == 0):
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

    if (recurseTracker == 1):
      return True

    recurseTracker += 1
    for i in ['up', 'down', 'left', 'right']:
      if (i == opposite(move)):
        break
      print('hit! recurseTracker = {0}').format(recurseTracker)
      if (i == 'up'):
        my_y -= 1
      elif (i == 'down'):
        my_y += 1
      elif (i == 'left'):
        my_x -= 1
      else:
        my_x += 1
      print('({0}, {1})').format(my_x, my_y)
      result = safeMove(data, my_x, my_y, i, recurseTracker)
      if (result == True):
        safeVar += 1

    print('safeVar = {0}').format(safeVar)
    if (safeVar > 0):
        safeVar = 0        
        return True
    else:
        safeVar = 0
        return False
    

def opposite(move):
  if (move == 'up'):
    return 'down'
  if (move == 'down'):
    return 'up'
  if (move == 'left'):
    return 'right'
  if (move == 'right'):
    return 'down'


# Input: snake coordinates, target coordinates
# Output: move
def goTo(my_x, my_y, target_x, target_y, data):
    global last_move
    move_x = my_x - target_x
    move_y = my_y - target_y

    #move to target
    if (move_y > 0 and safeMove(data, my_x, my_y, 'up', 0)):
        last_move = 'up'
        return 'up'
    elif (move_y < 0 and safeMove(data, my_x, my_y, 'down', 0)):
        last_move = 'down'
        return 'down'
    elif (move_x > 0 and safeMove(data, my_x, my_y, 'left', 0)):
        last_move = 'left'
        return 'left'
    elif (move_x < 0 and safeMove(data, my_x, my_y, 'right', 0)):
        last_move = 'right'
        return 'right'
    #if you cannot move towards the target, make any safe move
    elif (safeMove(data, my_x, my_y, 'up', 0)):
        last_move = 'up'
        return 'up'
    elif (safeMove(data, my_x, my_y, 'down', 0)):
        last_move = 'down'
        return 'down'
    elif (safeMove(data, my_x, my_y, 'left', 0)):
        last_move = 'left'
        return 'left'
    elif (safeMove(data, my_x, my_y, 'right', 0)):
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
        print('Food: ({0}, {1}) is {2} squares away'.format(food_x, food_y, distance))

        if (distance < closestDistance):
            closestDistance = distance
            target_x = food_x
            target_y = food_y
    
    print('Closest Food: ({0}, {1}) is {2} squares away'.format(target_x, target_y, closestDistance))

    return [target_x, target_y]

#Input: game data
#Output: the move to send to the battlesnake server
def nextMove(data):
    global curr_target_x, curr_target_y, my_x, my_y
    
    #location of snake's head
    my_x = data['you']['body']['data'][0]['x']
    my_y = data['you']['body']['data'][0]['y']
    print('My Snake: ({0}, {1})'.format(my_x, my_y))

    #find the closest food
    closestFood = findClosestFood(data)
    print('closest food: ({0}, {1})'.format(closestFood[0], closestFood[1]))
    curr_target_x = closestFood[0]
    curr_target_y = closestFood[1]
    print('3. curr_target: ({0}, {1})'.format(curr_target_x, curr_target_y))

    return goTo(my_x, my_y, curr_target_x, curr_target_y, data)


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

    print('START!!! my: ({0},{1})    ,     curr_target: ({2},{3})'.format(my_x, my_y, curr_target_x, curr_target_y))
   

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
    print('Calculating Move (Last Move = {0})'.format(last_move))
    data = bottle.request.json
    print('Inside /move:    my: ({0},{1})    ,     curr_target: ({2},{3})'.format(my_x, my_y, curr_target_x, curr_target_y))
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
