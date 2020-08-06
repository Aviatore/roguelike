import ui
import time
import random


class Boards:
    def __init__(self):
        self.boards = {}
        self.current_board = None
    
    def add_board(self, board):
        self.boards[board.board_id] = board
    
    def set_current_board(self, board_id):
        self.current_board = self.boards[board_id]
        


class Board:
    def __init__(self, board_id, height, width, screen):
        self.height = height
        self.width = width
        self.board = []
        self.board_id = board_id
        self.screen = screen
        self.doors_destination = {}

    def create_board(self, **doors): # np. create_board(board1=[0,5], board2=[5,0])
        for board_id in doors.keys():
            door_id = ":".join(map(str, doors[board_id])) # door_id=<row_index>:<col_index>
            
            self.doors_destination[door_id] = board_id
        
        for row_index in range(self.height):
            row = (". " * self.width).split(" ")[0:-1]
            row = list(map(lambda x : x.replace('.', ' '), row))
            
            self.board.append(row)
        
        for row_index in range(self.height):
            for col_index in range(self.width):
                if row_index in [0, self.height - 1]:
                    if [row_index, col_index] in doors.values():
                        self.board[row_index][col_index] = '-'
                    else:
                        self.board[row_index][col_index] = '#'
                elif col_index in [0, self.width - 1]:
                    if [row_index, col_index] in doors.values():
                        self.board[row_index][col_index] = '-'
                    else:
                        self.board[row_index][col_index] = '#'
    
    def door_coords(self, board_id):
        for key in self.doors_destination:
            if self.doors_destination[key] == board_id:
                return list(map(int, key.split(":")))
        
        return False
        


class Person:
    def __init__(self, object_type, all_boards):
        self.type = object_type
        self.all_boards = all_boards
        self.Board = self.all_boards.current_board
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
    
    def update_board(self):
        self.Board = self.all_boards.current_board



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
    def __init__(self, type, all_boards, all_objects, printer):
        super().__init__(type, all_boards)
        self.mark = 'P'
        self.hp = None
        self.dmg = 0
        self.protection = None
        self.walk_speed = 1
        self.direction = None
        self.Inventory = Inventory(self)
        self.Backpack = Backpack()
        self.all_objects = all_objects
        self.Objects = self.all_objects.current_objects
        self.printer = printer
        self.printer.clear_screen()
    
    def set_hp(self, hp):
        self.hp = hp
    
    def set_dmg(self, dmg):
        self.dmg = dmg
    
    def move(self, direction):
        self.printer.clear_screen()
        
        LEFT = self.col - 1
        RIGHT = self.col + 1
        UP = self.row - 1
        DOWN = self.row + 1
        
        if direction == 'up':
            if self.Board.board[UP][self.col] == '-':
                current_board_id = self.Board.board_id
                self.Board.board[self.row][self.col] = ' '
                
                door_id = f"{str(UP)}:{str(self.col)}"
                destination_board_id = self.all_boards.current_board.doors_destination[door_id]
                
                self.all_boards.set_current_board(destination_board_id)
                self.all_objects.set_current_objects(destination_board_id)
                self.printer.update_board()
                self.update_board()
                self.update_objects()
                prev_door_row, prev_door_col = self.Board.door_coords(current_board_id)
                
                
                self.row = prev_door_row - 1
                self.col = prev_door_col
                self.put_on_board()
                self.printer.clear_screen()
                
            elif self.Board.board[UP][self.col] == '#':
                pass
            elif self.there_is_obstacle(UP, self.col):
                pass
            else:
                self.Board.board[self.row][self.col] = ' '
                self.row = UP
                self.Board.board[self.row][self.col] = 'P'
                self.direction = 'u'
        elif direction == 'down':
            if self.Board.board[DOWN][self.col] == '-':
                current_board_id = self.Board.board_id
                self.Board.board[self.row][self.col] = ' '
                
                door_id = f"{str(DOWN)}:{str(self.col)}"
                destination_board_id = self.all_boards.current_board.doors_destination[door_id]
                
                self.all_boards.set_current_board(destination_board_id)
                self.all_objects.set_current_objects(destination_board_id)
                self.printer.update_board()
                self.update_board()
                self.update_objects()
                prev_door_row, prev_door_col = self.Board.door_coords(current_board_id)
                
                self.row = prev_door_row + 1
                self.col = prev_door_col
                self.put_on_board()
                self.printer.clear_screen()
            elif self.Board.board[DOWN][self.col] == '#':
                pass
            elif self.there_is_obstacle(DOWN, self.col):
                pass
            else:
                self.Board.board[self.row][self.col] = ' '
                self.row = DOWN
                self.Board.board[self.row][self.col] = 'P'
                self.direction = 'd'
        elif direction == 'left':
            if self.Board.board[self.row][LEFT] == '-':
                current_board_id = self.Board.board_id
                self.Board.board[self.row][self.col] = ' '
                
                door_id = f"{str(self.row)}:{str(LEFT)}"
                destination_board_id = self.all_boards.current_board.doors_destination[door_id]
                
                self.all_boards.set_current_board(destination_board_id)
                self.all_objects.set_current_objects(destination_board_id)
                self.printer.update_board()
                self.update_board()
                self.update_objects()
                prev_door_row, prev_door_col = self.Board.door_coords(current_board_id)
                
                self.row = prev_door_row
                self.col = prev_door_col - 1
                self.put_on_board()
                self.printer.clear_screen()
            elif self.Board.board[self.row][LEFT] == '#':
                pass
            elif self.there_is_obstacle(self.row, LEFT):
                pass
            else:
                self.Board.board[self.row][self.col] = ' '
                self.col = LEFT
                self.Board.board[self.row][self.col] = 'P'
                self.direction = 'l'
        elif direction == 'right':
            if self.Board.board[self.row][RIGHT] == '-':
                current_board_id = self.Board.board_id
                self.Board.board[self.row][self.col] = ' '
                
                door_id = f"{str(self.row)}:{str(RIGHT)}"
                destination_board_id = self.all_boards.current_board.doors_destination[door_id]
                
                self.all_boards.set_current_board(destination_board_id)
                self.all_objects.set_current_objects(destination_board_id)
                self.printer.update_board()
                self.update_board()
                self.update_objects()
                prev_door_row, prev_door_col = self.Board.door_coords(current_board_id)
                
                self.row = prev_door_row
                self.col = prev_door_col + 1
                self.put_on_board()
                self.printer.clear_screen()
            elif self.Board.board[self.row][RIGHT] == '#':
                pass
            elif self.there_is_obstacle(self.row, RIGHT):
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

    def update_objects(self):
        self.Objects = self.all_objects.current_objects
        


class AllObjects:
    def __init__(self):
        self.all_objects = {}
        self.current_objects = None
    
    def add_objects(self, objects_id, objects):
        self.all_objects[objects_id] = objects
    
    def set_current_objects(self, objects_id):
        self.current_objects = self.all_objects[objects_id]



class Objects:
    def __init__(self, objects_id, Board, Printer):
        self.objects_list = []
        self.objects_id = objects_id
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
    def __init__(self, all_boards, printer):
        super().__init__('food', all_boards)
        self.mark = 'F'
        self.hp = None
        self.name = None
        self.printer = printer
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
    def __init__(self, all_boards, printer):
        super().__init__('orc', all_boards)
        self.mark = 'H'
        self.hp = None
        self.dmg = None
        self.run_speed = 1
        self.name = None
        self.printer = printer
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
        

# Below function needs to be implemented within Hero class
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
            