# Contains all the values

class Config:

    # Border of board value
    border = -1000

    # Food values
    food_has_low_health = 6
    food_has_high_health = 8

    # Enemy Snake values
    enemy_is_smaller = 2
    enemy_is_bigger = 0
    enemy_is_equal = 0 # Fix this with a condition on whether you can get to the food before them
