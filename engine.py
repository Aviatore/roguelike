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
    def __init__(self, board_id, screen, height=None, width=None):
        self.height = height
        self.width = width
        self.board = []
        self.board_id = board_id
        self.screen = screen
        self.doors_destination = {}
        self.freePass_destination = {
            'left': None,
            'right': None,
            'up': None,
            'down': None
        }

    def board_init(self):
        for row_index in range(self.height):
            row = (". " * self.width).split(" ")[0:-1]
            row = list(map(lambda x : x.replace('.', ' '), row))
            
            self.board.append(row)

    def create_board(self, **doors): # np. create_board(board1=[0,5], board2=[5,0])
        for board_id in doors.keys():
            door_id = ":".join(map(str, doors[board_id])) # door_id=<row_index>:<col_index>
            
            self.doors_destination[door_id] = board_id
        
        self.board_init()
        
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
    
    def template_to_list(self, template):
        template_list = []
        
        for line in template.split('\n'):
            if len(line) > 0:
                template_list.append(list(line))
            
        return template_list
    
    def create_board_template(self, template, door_dest_board_ids=None, freePass_destination=None):
        template_list = self.template_to_list(template)
        if freePass_destination is not None:
            self.freePass_destination = freePass_destination
        
        self.height = len(template_list)
        self.width = len(template_list[0])
        
        self.board_init()
        
        for row_index in range(self.height):
            for col_index in range(self.width):
                if template_list[row_index][col_index] == '-':
                    door_id = f"{row_index}:{col_index}"
                    self.doors_destination[door_id] = door_dest_board_ids[0]
                    door_dest_board_ids.pop(0)                    
                    
                self.board[row_index][col_index] = template_list[row_index][col_index]
    
    def door_coords(self, board_id):
        for door_id in self.doors_destination.keys():
            if self.doors_destination[door_id] == board_id:
                return list(map(int, door_id.split(":")))
        
        return False        


# class Items:
#     def __init__(self):
#         self.visit_number = 0
#         self.items = [] # Lista obiektów
        

class Action:
    def __init__(self):
        self.visit_number = 0
        self.required_items = [] # Lista obiektów
        self.label = None
        self.options = [] # Lista stringów odpowiadających możliwym opcjom
        self.reactions = {} # Kluczem jest id opcji, wartością jest funkcja lub obiekt klasy Action
    
    def add_required_items(self, item):
        self.required_items.append(item)
    
    def add_label(self, label):
        self.label = label
    
    def add_option(self, option):
        self.options.append(option)
    
    def add_options(self, options):
        self.options.extend(options)
    
    def add_reaction(self, option_id, reaction):
        self.reactions[option_id] = reaction
        
    def react(self, hero, multilinePrinter):
        user_input = None
        next_round = False
        
        while user_input is None:
            multilinePrinter.clear()
            multilinePrinter.reset_line()
            multilinePrinter.print_line(self.label)
            
            if len(self.options) > 0:
                for index, option in enumerate(self.options):
                    multilinePrinter.print_line(f"{index + 1}. {option}")
                
                multilinePrinter.print_line("0. Exit")
                
                user_input = multilinePrinter.Printer.screen.getch()
        
                if not str(chr(user_input)).isdigit():
                    user_input = None
                    continue
            
                user_input_chr = chr(user_input)
                
                user_input_int = int(user_input_chr)
                
                if user_input_int in list(range(1, len(self.options) + 1)):
                    self.reactions[user_input_chr].react(hero, multilinePrinter)
                elif user_input_int == 0:
                    multilinePrinter.clear()
                    return
                else:
                    user_input = None
                        
                next_round = True
            else:
                multilinePrinter.Printer.screen.getch()
                multilinePrinter.clear()
                user_input = ""
            


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
        
    def set_mark(self, mark):
        self.mark = mark
    
    def set_name(self, name):
        self.name = name
    
    def set_position(self, row, col):
        self.row = row
        self.col = col
        self.put_on_board()


class Person_custom:
    def __init__(self, object_type, all_boards, printer):
        self.type = object_type
        self.all_boards = all_boards
        self.Board = self.all_boards.current_board
        self.name = None
        self.row = None
        self.col = None
        self.mark = None
        self.action = None
        self.printer = printer
        self.multilinePrinter = MultiLinePrinter(self.printer)
    
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
        
    def set_mark(self, mark):
        self.mark = mark
    
    def set_name(self, name):
        self.name = name
    
    def set_position(self, row, col):
        self.row = row
        self.col = col
        self.put_on_board()
    
    def add_action(self, action):
        self.action = action
    
    def react(self, hero):
        self.action.react(hero, self.multilinePrinter)


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
        self.Hero.dmg = self.Hero.dmg + self.weapon.dmg
    
    def put_down_weapon(self):
        self.weapon = None
        self.Hero.dmg = self.Hero.dmg - self.weapon.dmg
        
    def put_on_armor(self, armor):
        self.armor = armor
        self.Hero.protection = self.Hero.protection + armor.protection
        
    def put_down_armor(self):
        self.armor = None
        self.Hero.protection = self.Hero.protection - self.armor.protection



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
    
    def drop_item(self, item_type, item):
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
        freePass_direction = None
        
        if direction == 'up':
            next_row = self.row - 1
            next_col = self.col
            
            row_door_offset = -1
            col_door_offset = 0
            
            if next_row == -1:
                freePass_direction = 'up'
            
            direction = 'u'
        elif direction == 'down':
            next_row = self.row + 1
            next_col = self.col
            
            row_door_offset = 1
            col_door_offset = 0
            
            if next_row == self.Board.height:
                freePass_direction = 'down'
            
            direction = 'd'
        elif direction == 'left':
            next_row = self.row
            next_col = self.col - 1
            
            if next_col == -1:
                freePass_direction = 'left'
            
            row_door_offset = 0
            col_door_offset = -1
            
            direction = 'l'
        elif direction == 'right':
            next_row = self.row
            next_col = self.col + 1
            
            row_door_offset = 0
            col_door_offset = 1
            
            if next_col == self.Board.width:
                freePass_direction = 'right'
            
            direction = 'r'
        
        current_board_id = self.Board.board_id
        
        try:
            current_mark = self.Board.board[next_row][next_col]
        except IndexError:
            current_mark = None        
        
        if current_mark == '-' or freePass_direction is not None:
            self.Board.board[self.row][self.col] = ' '
            
            # Getting destination board id
            if current_mark == '-':
                door_id = f"{str(next_row)}:{str(next_col)}"
                destination_board_id = self.all_boards.current_board.doors_destination[door_id]
            else:
                destination_board_id = self.Board.freePass_destination[freePass_direction]
            
            # Updating the new board and board-specific objects
            self.all_boards.set_current_board(destination_board_id)
            self.all_objects.set_current_objects(destination_board_id)
            self.printer.update_board()
            self.update_board()
            self.update_objects()
            
            # Setting hero's initial position on the next board
            if current_mark == '-':
                current_door_row, current_door_col = self.Board.door_coords(current_board_id)
                self.row = current_door_row + row_door_offset
                self.col = current_door_col + col_door_offset
            else:
                current_door_row, current_door_col = self.freePass_coords(freePass_direction)
                self.row = current_door_row
                self.col = current_door_col
            
            self.put_on_board()
            self.printer.clear_screen()
        elif current_mark == ' ':
            self.Board.board[self.row][self.col] = ' '
            self.Board.board[next_row][next_col] = 'P'
            
            self.row = next_row
            self.col = next_col
            
            self.direction = direction
        elif self.there_is_obstacle(next_row, next_col):
            pass
    
    def freePass_coords(self, freePass_direction):
        if freePass_direction == 'left':
            return self.row, self.Board.width - 1
        elif freePass_direction == 'right':
            return self.row, 0
        elif freePass_direction == 'up':
            return self.Board.height - 1, self.col
        elif freePass_direction == 'down':
            return 0, self.col
    
    def there_is_obstacle(self, row, col):
        if self.Board.board[row][col] in self.all_objects.all_objects_marks:
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
        self.all_objects_marks = set()
    
    def add_objects_marks(self, marks):
        new_marks = set(marks).difference(self.all_objects_marks)
        
        for mark in new_marks:
            self.all_objects_marks.add(mark)
        
    
    def add_objects(self, objects_id, objects):
        self.all_objects[objects_id] = objects
        
        self.add_objects_marks(objects.marks)        
        
    
    def set_current_objects(self, objects_id):
        self.current_objects = self.all_objects[objects_id]



class Objects:
    def __init__(self, objects_id, Board, Printer):
        self.objects_list = []
        self.objects_id = objects_id
        self.Board = Board
        self.Printer = Printer
        self.marks = []
        
    def add_object(self, new_object):
        self.objects_list.append(new_object)
        
        if new_object.mark not in self.marks:
            self.marks.append(new_object.mark)
    
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
            