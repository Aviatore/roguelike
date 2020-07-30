import ui
import time
import random


def create_board(height, width):
    board = []
    for row_index in range(height):
        row = (". " * width).split(" ")[0:-1]
        row = list(map(lambda x : x.replace('.', ' '), row))
        
        board.append(row)
    
    for row_index in range(height):
        for col_index in range(width):
            if row_index in [0, height - 1]:
                board[row_index][col_index] = 'H'
            elif col_index in [0, width - 1]:
                board[row_index][col_index] = 'H'
    
    return board


def get_object(objects, row, col):
    for object_ in objects:
        if object_['row'] == row and object_['col'] == col:
            return object_
        elif object_['row'] is None:
            objects.remove(object_)
    
    return False


def react_on_object(object_, stdscr, board, msgbox, hero):
    if object_['type'] == 'food':
        stdscr.addstr(24, 5, f"There is an {object_['name']} on the ground.")
        stdscr.addstr(25, 5, f"1. Eat {object_['name']}")
        stdscr.addstr(26, 5, f"0. Exit")
        stdscr.refresh()
        
        user_input = None
        while user_input is None:
            user_input = stdscr.getch()
            
            if user_input == ord('1'):
                ui.clear_msgbox(board, stdscr)
                stdscr.addstr(24, 5, f"Yammy")
                stdscr.addstr(26, 5, f"Your HP increased by {object_['hp']}.")
                board[object_['row']][object_['col']] = ' '
                object_['row'] = None
                object_['col'] = None
                msgbox[0] = 5
            elif user_input == ord('0'):
                ui.clear_msgbox(board, stdscr)
            else:
                user_input = None
    elif object_['type'] == 'orc':
        stdscr.addstr(24, 5, f"The orc {object_['name']} cached you. You must fight!")
        stdscr.addstr(25, 5, f"1. Hit {object_['name']} with your {hero['inventory']['weapon']['name']}.")
        stdscr.refresh()
        
        
        user_input = None
        while user_input is None:
            user_input = stdscr.getch()
            
            if user_input == ord('1'):
                ui.clear_msgbox(board, stdscr)
                
                hero_dmg = hero['inventory']['weapon']['damage']
                hero_dmg_range = int(hero_dmg / 10)
                hero_dmg_random = random.randint(hero_dmg - hero_dmg_range, hero_dmg + hero_dmg_range)
                
                orc_dmg = object_['dmg']
                orc_dmg_range = int(orc_dmg / 10)
                orc_dmg_random = random.randint(orc_dmg - orc_dmg_range, orc_dmg + orc_dmg_range)
                
                object_['hp'] -= hero_dmg_random
                if object_['hp'] < 0:
                    ui.clear_msgbox(board, stdscr)
                    stdscr.addstr(24, 5, f"You killed {object_['name']}.")
                    board[object_['row']][object_['col']] = ' '
                    object_['row'] = None
                    object_['col'] = None
                    continue
                else:
                    stdscr.addstr(24, 5, f"You hit the {object_['name']} by {hero_dmg_random}. {object_['name']}  HP: {object_['hp']}.")
                
                hero['hp'] -= orc_dmg_random
                if hero['hp'] < 0:
                    ui.clear_msgbox(board, stdscr)
                    stdscr.addstr(24, 5, f"You was killed by {object_['name']}.")
                    continue
                else:
                    stdscr.addstr(25, 5, f"{object_['name']} hit you by {orc_dmg_random}. Your HP: {hero['hp']}.")
                    
                user_input = None
            else:
                user_input = None
                
                
def there_is_obstacle(board, row, col, objects, stdscr, msgbox, hero):
    if board[row][col] != ' ' and board[row][col] != 'P':
        object_ = get_object(objects, row, col)
        
        if object_:
            react_on_object(object_, stdscr, board, msgbox, hero)
        
        return True
    
    return False


def move_objects(board, objects, hero, stdscr, msgbox):    
    for object_ in objects:
        if object_['row'] is None:
            objects.remove(object_)
        elif object_['type'] == 'orc':
            
            counter = 0
            
            loop = True
            while loop:
                row_prev = object_['row']
                col_prev = object_['col']
                
                distance_row = abs(hero['row'] - row_prev)
                distance_col = abs(hero['col'] - col_prev)
                
                distance_critical = 6
                distance_min = 5
                
                ui.clear_msgbox(board, stdscr)

                stdscr.addstr(24, 5, f"distance_row: {distance_row}")
                stdscr.addstr(25, 5, f"distance_col: {distance_col}")
                stdscr.addstr(26, 5, f"counter: {counter}")

                stdscr.refresh()

                if distance_row <= 1 and distance_col <= 1:
                    react_on_object(object_, stdscr, board, msgbox, hero)
                    loop = False
                else:
                    if distance_row == 0 and distance_col < distance_critical:
                        if col_prev < hero['col']:
                            object_['col'] += 1
                        elif col_prev > hero['col']:
                            object_['col'] -= 1
                        
                        time.sleep(0.1)
                    elif distance_col == 0 and distance_row < distance_critical:
                        if row_prev < hero['row']:
                            object_['row'] += 1
                        elif row_prev > hero['row']:
                            object_['row'] -= 1
                            
                        time.sleep(0.1)
                    elif hero['direction'] in ['u', 'd'] and distance_row == distance_critical and distance_col < distance_critical:
                        if row_prev < hero['row']:
                            object_['row'] += 1
                        elif row_prev > hero['row']:
                            object_['row'] -= 1
                        
                        time.sleep(0.1)
                    elif hero['direction'] in ['u', 'd'] and distance_col < distance_critical and distance_row < distance_critical:
                        if col_prev < hero['col']:
                            object_['col'] += 1
                        elif col_prev > hero['col']:
                            object_['col'] -= 1
                        
                        time.sleep(0.1)
                    elif hero['direction'] in ['l', 'r'] and distance_col == distance_critical and distance_row < distance_critical:
                        if col_prev < hero['col']:
                            object_['col'] += 1
                        elif col_prev > hero['col']:
                            object_['col'] -= 1
                        
                        time.sleep(0.1)
                    elif hero['direction'] in ['l', 'r'] and distance_col < distance_critical and distance_row < distance_critical:
                        if row_prev < hero['row']:
                            object_['row'] += 1
                        elif row_prev > hero['row']:
                            object_['row'] -= 1
                        
                        time.sleep(0.01)

                    board[row_prev][col_prev] = ' '
                    board[object_['row']][object_['col']] = 'H'
                    

                stdscr.refresh()

                # time.sleep(0.1)
                counter += 1
                if counter == object_['run_speed']:
                    loop = False
            

def move_hero(board, hero, direction, objects, stdscr, msgbox):
    BOARD_HEIGHT = len(board)
    BOARD_WIDTH = len(board[0])
    row = hero['row']
    col = hero['col']
    LEFT = col - 1
    RIGHT = col + 1
    UP = row - 1
    DOWN = row + 1

    if direction == 'up' and row > 1:
        if there_is_obstacle(board, UP, col, objects, stdscr, msgbox, hero):
            pass
        else:
            board[row][col] = ' '
            row = UP
            board[row][col] = 'P'
            hero['direction'] = 'u'
    elif direction == 'down' and row < BOARD_HEIGHT - 2:
        if there_is_obstacle(board, DOWN, col, objects, stdscr, msgbox, hero):
            pass
        else:
            board[row][col] = ' '
            row = DOWN
            board[row][col] = 'P'
            hero['direction'] = 'd'
    elif direction == 'left' and col > 1:
        if there_is_obstacle(board, row, LEFT, objects, stdscr, msgbox, hero):
            pass
        else:
            board[row][col] = ' '
            col = LEFT
            board[row][col] = 'P'
            hero['direction'] = 'l'
    elif direction == 'right' and col < BOARD_WIDTH - 2:
        if there_is_obstacle(board, row, RIGHT, objects, stdscr, msgbox, hero):
            pass
        else:
            board[row][col] = ' '
            col = RIGHT
            board[row][col] = 'P'
            hero['direction'] = 'r'
    
    hero['row'] = row
    hero['col'] = col
    stdscr.refresh()
        
        


def object_random_position(board, object_, character):
    BOARD_HEIGHT = len(board)
    BOARD_WIDTH = len(board[0])
    
    search_coords = True
    
    while search_coords:
        row_random = random.randint(1, BOARD_HEIGHT - 1)
        col_random = random.randint(1, BOARD_WIDTH - 1)
        
        if board[row_random][col_random] == ' ':
            board[row_random][col_random] = character
            object_['row'] = row_random
            object_['col'] = col_random
            search_coords = False            


def object_food_create(board):
    objects = {
        1: {
            'type': 'food',
            'name': 'apple',
            'hp': 10,
            'row': None,
            'col': None
        },
        2: {
            'type': 'food',
            'name': 'banana',
            'hp': 20,
            'row': None,
            'col': None
        }
    }
    
    random_object_id = random.sample(objects.keys(), 1)[0]
    random_object = objects[random_object_id]
    object_random_position(board, random_object, 'F')
    
    return random_object


def object_person_create(board):
    objects = {
        1: {
            'type': 'orc',
            'name': 'Gorbag',
            'hp': 60,
            'dmg': 10,
            'run_speed': 2,
            'row': None,
            'col': None,
            'timer': 0
        },
        2: {
            'type': 'orc',
            'name': 'Azog',
            'hp': 100,
            'dmg': 15,
            'run_speed': 2,
            'row': None,
            'col': None,
            'timer': 0
        }
    }
    
    random_object_id = random.sample(objects.keys(), 1)[0]
    random_object = objects[random_object_id]
    object_random_position(board, random_object, 'H')
    
    return random_object


def object_hero_create(board):
    objects = {
        1: {
            'type': 'Knight',
            'row': None,
            'col': None,
            'hp': 200,
            'walk_speed': 1,
            'inventory': {
                'weapon': {
                    'type': 'weapon',
                    'name': 'Sword',
                    'damage': 40
                }
            },
            'direction': None
        },
        2: {
            'type': 'Wizard',
            'row': None,
            'col': None,
            'hp': 100,
            'mana': 100,
            'walk_speed': 1,
            'inventory': {
                'weapon': {
                    'type': 'weapon',
                    'name': 'Fire ball',
                    'damage': 60
                }
            },
            'direction': None
        },
        3: {
            'type': 'Cutler',
            'row': None,
            'col': None,
            'hp': 150,
            'walk_speed': 1,
            'inventory': {
                'weapon': {
                    'type': 'weapon',
                    'name': 'Dagger',
                    'damage': 30
                }
            },
            'direction': None
        }
    }
    
    random_object_id = random.sample(objects.keys(), 1)[0]
    random_object = objects[random_object_id]
    object_random_position(board, random_object, 'P')
    
    return random_object