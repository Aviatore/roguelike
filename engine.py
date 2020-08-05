import ui
import time
import random


class Board:
    def __init__(self, height, width, screen):
        self.height = height
        self.width = width
        self.board = []
        self.screen = screen


    def create_board(self):
        for row_index in range(self.height):
            row = (". " * self.width).split(" ")[0:-1]
            row = list(map(lambda x : x.replace('.', ' '), row))
            
            self.board.append(row)
        
        for row_index in range(self.height):
            for col_index in range(self.width):
                if row_index in [0, self.height - 1]:
                    self.board[row_index][col_index] = 'H'
                elif col_index in [0, self.width - 1]:
                    self.board[row_index][col_index] = 'H'
        

class Person:
    def __init__(self, object_type, Board):
        self.type = object_type
        self.Board = Board
        self.name = None
        self.row = None
        self.col = None
        self.mark = None
    
    
    def put_on_board(self):
        self.Board.board[self.row][self.col] = self.mark
    
    
    def object_random_position(self):       
        search_coords = True
        
        while search_coords:
            row_random = random.randint(1, self.Board.height - 1)
            col_random = random.randint(1, self.Board.width - 1)
            
            
            try:
                if self.Board.board[row_random][col_random] == ' ':
                    self.Board.board[row_random][col_random] = self.mark
                    self.row = row_random
                    self.col = col_random
                    search_coords = False
            except:
                self.Board.screen.addstr(5, 5, f"DEBUG: {self.type}")
                self.Board.screen.getch()
    
    def random_range_values(self, basic_value, divider):
        min_max = int(basic_value / divider)
        
        return random.randint(basic_value - min_max, basic_value + min_max)





class Weapon:
    def __init__(self, name, dmg):
        self.name = name
        self.dmg = dmg
    
    
    def set_dmg(self, dmg):
        self.dmg = dmg


class Armor:
    def __init__(self, name, protection):
        self.name = name
        self.protection = protection
    
    
    def set_protection(self, protection):
        self.protection = protection



class Inventory:
    def __init__(self, Hero):
        self.weapon = None
        self.armor = None
        self.Hero = Hero
    
    
    def put_on_weapon(self, weapon):
        self.weapon = weapon
        self.Hero.dmg = self.Hero.dmg + weapon.dmg
    
    
    def put_down_weapon(self):
        self.weapon = None
        self.Hero.dmg = self.Hero.dmg - weapon.dmg
        
    
    def put_on_armor(self, armor):
        self.armor = armor
        self.Hero.protection = self.Hero.protection + armor.protection
        
    
    def put_down_armor(self):
        self.armor = None
        self.Hero.protection = self.Hero.protection - armor.protection


class Backpack:
    def __init__(self):
        self.weapons = []
        self.armors = []
        self.foods = []
        
        
    def add_item(self, item_type, item):
        if item_type == 'weapon':        
            self.weapons.append(item)
        elif item_type == 'armor':
            self.armors.append(item)
        elif item_type == 'food':
            self.foods.append(item)
    
    
    def drop_item(self, item_type, index):
        if item_type == 'weapon':        
            self.weapons.pop(item)
        elif item_type == 'armor':
            self.armors.pop(item)
        elif item_type == 'food':
            self.foods.pop(item)
    

class Hero(Person):
    def __init__(self, type, Board, Objects):
        super().__init__(type, Board)
        self.mark = 'P'
        self.hp = None
        self.dmg = 0
        self.protection = None
        self.walk_speed = 1
        self.direction = None
        self.Inventory = Inventory(self)
        self.Backpack = Backpack()
        self.Objects = Objects
    
    
    def set_hp(self, hp):
        self.hp = hp
    
    def set_dmg(self, dmg):
        self.dmg = dmg
    
    def move(self, direction):
        LEFT = self.col - 1
        RIGHT = self.col + 1
        UP = self.row - 1
        DOWN = self.row + 1
        
        if direction == 'up' and self.row > 1:
            if self.there_is_obstacle(UP, self.col):
                pass
            else:
                self.Board.board[self.row][self.col] = ' '
                self.row = UP
                self.Board.board[self.row][self.col] = 'P'
                self.direction = 'u'
        elif direction == 'down' and self.row < self.Board.height - 2:
            if self.there_is_obstacle(DOWN, self.col):
                pass
            else:
                self.Board.board[self.row][self.col] = ' '
                self.row = DOWN
                self.Board.board[self.row][self.col] = 'P'
                self.direction = 'd'
        elif direction == 'left' and self.col > 1:
            if self.there_is_obstacle(self.row, LEFT):
                pass
            else:
                self.Board.board[self.row][self.col] = ' '
                self.col = LEFT
                self.Board.board[self.row][self.col] = 'P'
                self.direction = 'l'
        elif direction == 'right' and self.col < self.Board.width - 2:
            if self.there_is_obstacle(self.row, RIGHT):
                pass
            else:
                self.Board.board[self.row][self.col] = ' '
                self.col = RIGHT
                self.Board.board[self.row][self.col] = 'P'
                self.direction = 'r'
    
    
    def there_is_obstacle(self, row, col):
        if self.Board.board[row][col] != ' ' and self.Board.board[row][col] != 'P':
            object_index = self.Objects.get_object_index(row, col)
            
            if isinstance(object_index, int):
                
                self.Objects.react_on_object(object_index, self)
            
            return True
        
        return False
        

class Objects:
    def __init__(self, Board, Printer):
        self.objects_list = []
        self.Board = Board
        self.Printer = Printer
        
    def add_object(self, new_object):
        self.objects_list.append(new_object)
    
    def get_object_index(self, row, col):
        for index, element in enumerate(self.objects_list):
            if element.row == row and element.col == col:
                return index
            elif element.row is None:
                self.objects_list.remove(element)
        
        return False
    
    def react_on_object(self, object_index, hero):
        obj = self.objects_list[object_index]
        
        obj.react(hero)


class MultiLinePrinter:
    def __init__(self, Printer):
        self.Printer = Printer
        
        self.row = self.Printer.Board.height + 3
        self.current_row = self.row
        
        self.col = 5
        self.current_col = self.col
    
    def print_line(self, msg):
        self.Printer.screen.addstr(self.current_row, self.current_col, msg)
        self.current_row += 1
    
    def reset_line(self):
        self.current_row = self.row
        self.current_col = self.col
    
    def refresh(self):
        self.Printer.screen.refresh()
    
    def clear(self):
        self.Printer.clear_screen()
        


class Food(Person):
    def __init__(self, Board):
        super().__init__('food', Board)
        self.mark = 'F'
        self.hp = None
        self.name = None
        self.printer = ui.Printer(self.Board)
        self.multilinePrinter = MultiLinePrinter(self.printer)
    
    def create_random(self):
        names = ['apple', 'berries', 'pear']
        
        basic_hp = 30
        hp_divider = 4
        
        self.hp = self.random_range_values(basic_hp, hp_divider)
        
        self.name = random.sample(names, 1)[0]
    
    def react(self, hero):
        user_input = None
        next_round = False
        
        while user_input is None:
            if next_round:
                user_input = self.printer.screen.getch()
                
            self.multilinePrinter.clear()
            self.multilinePrinter.reset_line()
            self.multilinePrinter.print_line(f"There is an {self.name} on the ground.")
            self.multilinePrinter.print_line(f"1. Eat {self.name}.")
            self.multilinePrinter.print_line("0. Exit")
            self.multilinePrinter.print_line(" ")
            self.multilinePrinter.refresh()
        
            if user_input == ord('1'):
                self.multilinePrinter.print_line(f"You have eaten {self.name}.")
                self.multilinePrinter.print_line(f"Your HP increased by {self.hp}.")
                
                self.Board.board[self.row][self.col] = ' '
                
                self.row = None
                self.col = None
                
                return
            elif user_input == ord('0'):
                self.multilinePrinter.clear()
            else:
                user_input = None
            
            next_round = True
        

class Orc(Person):
    def __init__(self, Board):
        super().__init__('orc', Board)
        self.mark = 'H'
        self.hp = None
        self.dmg = None
        self.run_speed = 1
        self.name = None
        self.printer = ui.Printer(self.Board)
        self.multilinePrinter = MultiLinePrinter(self.printer)
        
        
    def create_random(self):
        names = ['Gorbag', 'Azog']
        basic_hp = 80
        hp_divider = 4
        
        basic_dmg = 20
        dmg_divider = 2
        
        self.hp = self.random_range_values(basic_hp, hp_divider)
        
        self.dmg = self.random_range_values(basic_dmg, dmg_divider)
        
        self.name = random.sample(names, 1)[0]
    
    def react(self, hero):        
        user_input = None
        next_round = False
        
        while user_input is None:
            if next_round:
                user_input = self.printer.screen.getch()
            
            self.multilinePrinter.clear()
            self.multilinePrinter.reset_line()
            self.multilinePrinter.print_line(f"The orc {self.name} cached you. You must fight!")
            self.multilinePrinter.print_line(f"1. Hit {self.name} with your {hero.Inventory.weapon.name}.")
            self.multilinePrinter.print_line("0. Exit")
            self.multilinePrinter.print_line(" ")
            self.multilinePrinter.refresh()            
            
            if user_input == ord('1'):
                hero_dmg_range = int(hero.dmg / 10)
                hero_dmg_random = random.randint(hero.dmg - hero_dmg_range, hero.dmg + hero_dmg_range)
                
                orc_dmg_range = int(self.dmg / 10)
                orc_dmg_random = random.randint(self.dmg - orc_dmg_range, self.dmg + orc_dmg_range)
                
                self.hp -= hero_dmg_random
                if self.hp < 0:
                    self.multilinePrinter.print_line(f"You killed {self.name}.")
                    
                    self.Board.board[self.row][self.col] = ' '
                    
                    self.row = None
                    self.col = None
                    
                    return
                else:
                    self.multilinePrinter.print_line(f"You hit the {self.name} by {hero_dmg_random}. {self.name}  HP: {self.hp}.")
                    user_input = None

                hero.hp -= orc_dmg_random
                
                if hero.hp < 0:
                    self.multilinePrinter.print_line(f"You was killed by {self.name}.")
                    
                    return
                else:
                    self.multilinePrinter.print_line(f"{self.name} hit you by {orc_dmg_random}. Your HP: {hero.hp}.")
                    user_input = None
            elif user_input == ord('0'):
                self.multilinePrinter.clear()
            else:
                user_input = None
            
            next_round = True
        

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