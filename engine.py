import ui
import time
import random
import util
import time


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


class Items:
    def __init__(self):
        self.items = [] # Lista obiektów
        self.item_ids = []
        self.item_number_per_id = {}
    
    def add_item(self, item):
        self.items.append(item)
        self.__item_id_counter()
    
    def __item_id_counter(self):
        self.item_number_per_id = {}
        self.item_ids = []
        
        for item in self.items:
            self.item_number_per_id[item.id] = self.item_number_per_id.get(item.id, 0) + 1
        
        self.item_ids.extend(list(set(self.item_number_per_id.keys())))
            
        
class Task:
    def __init__(self, task_id, items, gift):
        self.task_id = task_id
        self.req_items = items # obiekt klasy Items
        self.gift_objects = gift # Lista obiektów


class Action:
    def __init__(self):
        self.visit_number = 0
        self.task_req_item_ids = {}
        self.task_gift_items = {}
        self.label = None
        self.options = [] # Lista stringów odpowiadających możliwym opcjom
        self.reactions = {} # Kluczem jest id opcji, wartością jest funkcja lub obiekt klasy Action
        self.task_react_req_item = {}
        self.task_react_gift_item = {}
        self.task = None
    
    def add_task_req_item_ids(self, task_id, item_id):
        if task_id in self.task_req_item_ids.keys():
            self.task_req_item_ids[task_id].append(item_id)
        else:
            self.task_req_item_ids[task_id] = [item_id]
    
    def add_task_gift_items(self, task_id, item):
        if task_id in self.task_gift_items.keys():
            self.task_gift_items[task_id].append(item)
        else:
            self.task_gift_items[task_id] = [item]
    
    def add_label(self, label):
        self.label = label
    
    def add_option(self, option):
        self.options.append(option)
    
    def add_options(self, options):
        self.options.extend(options)
    
    def add_reaction(self, option_id, reaction):
        self.reactions[option_id] = reaction
    
    def add_task_react_req_item(self, task_id, reaction):
        self.task_react_req_item[task_id] = reaction
    
    def add_task_react_gift_item(self, task_id, reaction):
        self.task_react_gift_item[task_id] = reaction
    
    def add_task(self, task):
        self.task = task
    
        
    def react(self, hero, multilinePrinter):
        user_input = None
        next_round = False
        stop = False
        
        while user_input is None:
            for task_id in self.task_req_item_ids.keys():
                for item_id in self.task_req_item_ids[task_id]:
                    if self.task_req_item_ids[task_id].count(item_id) == hero.Backpack.get_amount('other', item_id):
                        if self.task_gift_items[task_id]:
                            for item in self.task_gift_items[task_id]:                                
                                item_type = item.type
                                item = item
                                hero.Backpack.add_item(item_type, item)
                                hero.Backpack.drop_item_by_id('other', item_id)
                        
                        self.task_react_req_item[task_id].react(hero, multilinePrinter)
                        multilinePrinter.print_line(f"You have got a {item.name}.")
                        stop = True
                        
            if stop:
                multilinePrinter.Printer.screen.getch()
                multilinePrinter.clear()
                user_input = ""
                continue      
            
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
                if len(self.reactions) > 0:
                    multilinePrinter.print_line('Press ENTER to continue ...')
                    multilinePrinter.Printer.screen.getch()
                    self.reactions['1'].react(hero, multilinePrinter)
                    
                    if self.task_react_gift_item[task_id]:
                            self.task_react_gift_item[task_id].react(hero, multilinePrinter)
                    
                    
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
    def __init__(self, id, name, dmg):
        self.name = name
        self.dmg = dmg
        self.id = id
        self.type = 'weapon'
        self.fight_messages = []
    
    def set_dmg(self, dmg):
        self.dmg = dmg
    
    def add_fight_messages(self, msg):
        self.fight_messages.append(msg)
    
    def fight_message(self):
        return random.sample(self.fight_messages, 1)[0]



class Armor:
    def __init__(self, id, name, protection):
        self.name = name
        self.protection = protection
        self.id = id
        self.type = 'armor'
    
    def set_protection(self, protection):
        self.protection = protection


class Item(Person):
    def __init__(self, all_boards, printer, id, name):
        super().__init__('other', all_boards)
        self.mark = 'I'
        self.id = id
        self.name = name
        self.printer = printer
        self.multilinePrinter = MultiLinePrinter(self.printer)
    
    def react(self, hero):
        user_input = None
        next_round = False
        
        while user_input is None:
            if next_round:
                user_input = self.printer.screen.getch()
                
            self.multilinePrinter.clear()
            self.multilinePrinter.reset_line()
            self.multilinePrinter.print_line(f"There is an {self.name} on the ground.")
            self.multilinePrinter.print_line(f"1. Pick up {self.name}.")
            self.multilinePrinter.print_line("0. Exit")
            self.multilinePrinter.print_line(" ")
            self.multilinePrinter.refresh()
        
            if user_input == ord('1'):
                hero.Backpack.add_item('other', self)
                
                self.multilinePrinter.print_line(f"You put the {self.name} to your backpack.")
                
                self.Board.board[self.row][self.col] = ' '
                
                self.row = None
                self.col = None
                
                return
            elif user_input == ord('0'):
                self.multilinePrinter.clear()
            else:
                user_input = None
            
            next_round = True

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
        self.other = []
        self.money = 80
        self.recycles = {
            'Can': 0,
            'Bottle': 0
        }
        
    def add_item(self, item_type, item):
        if item_type == 'weapon':        
            self.weapons.append(item)
        elif item_type == 'armor':
            self.armors.append(item)
        elif item_type == 'food':
            self.foods.append(item)
        elif item_type == 'other':
            self.other.append(item)
    
    def drop_item(self, item_type, item):
        if item_type == 'weapon':        
            self.weapons.pop(item)
        elif item_type == 'armor':
            self.armors.pop(item)
        elif item_type == 'food':
            self.foods.pop(item)
        elif item_type == 'other':
            self.other.pop(item)
    
    def drop_item_by_id(self, item_type, item_id):
        if item_type == 'weapon':        
            for item in self.other:
                if item.id == item_id:
                    self.weapon.remove(item)
        elif item_type == 'armor':
            for item in self.other:
                if item.id == item_id:
                    self.armor.remove(item)
        elif item_type == 'food':
            for item in self.other:
                if item.id == item_id:
                    self.food.remove(item)
        elif item_type == 'other':
            for item in self.other:
                if item.id == item_id:
                    self.other.remove(item)
    
    def get_amount(self, item_type, id):
        if item_type == 'weapon':
            matched_items = [item for item in self.weapons if item.id == id]
            return len(matched_items)
        elif item_type == 'armor':
            matched_items = [item for item in self.armors if item.id == id]
            return len(matched_items)
        elif item_type == 'food':
            matched_items = [item for item in self.food if item.id == id]
            return len(matched_items)
        elif item_type == 'other':
            matched_items = [item for item in self.other if item.id == id]
            return len(matched_items)
    
class Task:
    def __init__(self, task_id, label):
        self.task_id = task_id
        self.label = label
        

class Hero(Person):
    def __init__(self, type, all_boards, all_objects, printer):
        super().__init__(type, all_boards)
        self.mark = 'P'
        self.hp = None
        self.dmg = 30
        self.protection = None
        self.walk_speed = 1
        self.direction = None
        self.Inventory = Inventory(self)
        self.Backpack = Backpack()
        self.all_objects = all_objects
        self.Objects = self.all_objects.current_objects
        self.printer = printer
        self.printer.clear_screen()
        self.tasks = []
        self.rhetoric = 10
        self.dir = 1
        self.dir_offset = 0
        self.distance_row = 0
        self.distance_col = 0
        self.interest_lvl = 0
        self.closest_row = 0
        self.closest_col = 0
        self.reverse_offset = False
        self.last_visited_coords = []
        self.fight_messages = [
            'You take a swing and punch {name}.',
            'You hit {name} with a fist.'
        ]
        
    def fight_message(self):
        return random.sample(self.fight_messages, 1)[0]
   
    def add_task(self, task):
        self.tasks.append(task)
    
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
            self.Board.board[self.row][self.col] = ' '
            self.Board.board[next_row][next_col] = 'P'
            self.row = next_row
            self.col = next_col
            self.direction = direction
    
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
                
            if self.Board.board[row][col] in ['C', 'B']:
                return True
            else:
                return False
        
        return False

    def update_objects(self):
        self.Objects = self.all_objects.current_objects
    
    def atack_hero_decide(self, object_):
        IMPACT_MONEY = 10
        IMPACT_CANS = 20
        IMPACT_BOTTLES = 30
        
        if object_.interest_loss == 0:
            self.interest_lvl = 0
            
            self.interest_lvl += self.Backpack.money // IMPACT_MONEY
            self.interest_lvl += self.Backpack.recycles['Can'] // IMPACT_CANS
            self.interest_lvl += self.Backpack.recycles['Bottle'] // IMPACT_BOTTLES
            
            distance_row = abs(object_.row - self.row)
            distance_col = abs(object_.col - self.col)

            if max(distance_row, distance_col) < self.interest_lvl:
                return True
            else:
                return False
        
    
    def find_closest_object(self, object_):
        closest_recycle = None
        min_distance = None
        
        for recycle in [element for element in self.Objects.objects_list if element.type == 'Recycle']:
            if recycle.row is not None:
                distance_row = abs(object_.row - recycle.row)
                distance_col = abs(object_.col - recycle.col)
                
                if min_distance is not None:
                    if max(distance_row, distance_col) < min_distance:
                        min_distance = max(distance_row, distance_col)
                        closest_recycle = recycle
                else:
                    min_distance = max(distance_row, distance_col)
                    closest_recycle = recycle
        
        if self.atack_hero_decide(object_):
            closest_recycle = self
        # distance_row = abs(object_.row - self.row)
        # distance_col = abs(object_.col - self.col)
        
        # if min_distance is not None:
        #     if max(distance_row, distance_col) < min_distance:
        #         min_distance = max(distance_row, distance_col)
        #         closest_recycle = self
        # else:
        #     min_distance = max(distance_row, distance_col)
        #     closest_recycle = self
        
        return closest_recycle
    
    def add_coords(self, row, col):
        self.last_visited_coords.append([row, col])
        
        if len(self.last_visited_coords) > 200:
            self.last_visited_coords.pop(0)
    
    def reverse_offset_direction(self):
        if self.reverse_offset:
            self.reverse_offset = False
        else:
            self.reverse_offset = True
    
    def add_offset(self):
        if self.reverse_offset:
            if self.dir_offset > 0:
                self.dir_offset -= 1
            else:
                self.dir_offset = 3
        else:        
            if self.dir_offset < 3:
                self.dir_offset += 1
            else:
                self.dir_offset = 0
    
    def reduce_offset(self):
        if self.reverse_offset:
            if self.dir_offset < 3:
                self.dir_offset += 1
            else:
                self.dir_offset = 0
        else:
            if self.dir_offset > 0:
                self.dir_offset -= 1
            else:
                self.dir_offset = 0
    
    def get_dir_offset(self):
        return (self.dir + self.dir_offset) % 4
    
    def move_objects(self):    
        for object_ in [element for element in self.Objects.objects_list if element.type == 'Lump']:                
            closest_recycle = self.find_closest_object(object_)
            if closest_recycle:
                self.closest_row = closest_recycle.row
            else:
                self.closest_row = 'None'
            
            if closest_recycle:
                self.closest_col = closest_recycle.col
            else:
                self.closest_col = 'None'
            
            if closest_recycle:
            
                loop = True
                while loop:
                    row_prev = object_.row
                    col_prev = object_.col
                    
                    
                    if abs(closest_recycle.row - row_prev) <= 1 and abs(closest_recycle.col - col_prev) <= 1:
                        if closest_recycle.type == 'hero':
                            object_.react(self)
                        else:
                            self.printer.Board.board[closest_recycle.row][closest_recycle.col] = ' '
                            closest_recycle.row = None
                            closest_recycle.col = None
                        return
                    
                    distance_row = abs(closest_recycle.row - row_prev)
                    self.distance_row = distance_row
                                        
                    distance_col = abs(closest_recycle.col - col_prev)
                    self.distance_col = distance_col

                    if distance_row == 0:
                        if col_prev < closest_recycle.col:
                            self.dir = 1
                        else:
                            self.dir = 3
                    elif distance_row < distance_col and self.dir_offset == 0:
                        if col_prev < closest_recycle.col:
                            self.dir = 1
                        else:
                            self.dir = 3
                    elif distance_col == 0:
                        if row_prev < closest_recycle.row:
                            self.dir = 2
                        else:
                            self.dir = 0
                    elif distance_row > distance_col and self.dir_offset == 0:
                        if row_prev < closest_recycle.row:
                            self.dir = 2
                        else:
                            self.dir = 0
                    elif distance_row == distance_row and self.dir_offset == 0:
                        if self.dir == 1:
                            self.dir = 1
                        elif self.dir == 3:
                            self.dir = 3
                        elif self.dir == 0:
                            self.dir = 0
                        elif self.dir == 2:
                            self.dir = 2                        
                    
                    row_tmp = object_.row
                    col_tmp = object_.col
                    find_best_way = True
                    while find_best_way:
                        if self.get_dir_offset() == 0:
                            if self.Board.board[row_tmp - 1][col_tmp] == ' ':
                                object_.row -= 1
                                self.reduce_offset()
                                find_best_way = False
                            else:
                                self.add_offset()
                        elif self.get_dir_offset() == 1:
                            if self.Board.board[row_tmp][col_tmp + 1] == ' ':
                                object_.col += 1
                                self.reduce_offset()
                                find_best_way = False
                            else:
                                self.add_offset()
                        elif self.get_dir_offset() == 2:
                            if self.Board.board[row_tmp + 1][col_tmp] == ' ':
                                object_.row += 1
                                self.reduce_offset()
                                find_best_way = False
                            else:
                                self.add_offset()
                        elif self.get_dir_offset() == 3:
                            if self.Board.board[row_tmp][col_tmp - 1] == ' ':
                                object_.col -= 1
                                self.reduce_offset()
                                find_best_way = False
                            else:
                                self.add_offset()
                    
                    self.Board.board[row_prev][col_prev] = ' '
                    self.Board.board[object_.row][object_.col] = object_.mark
                    
                    self.add_coords(object_.row, object_.col)
                    
                    if self.last_visited_coords.count([object_.row, object_.col]) > 4:
                        self.reverse_offset_direction()

                    loop = False
                
        if object_.interest_loss > 0:
            object_.interest_loss -= 1
        


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
    
    def recreate(self):
        for objects in self.all_objects.values():
            for element in objects.objects_list:
                if element.type == 'Recycle' and element.row is None:
                    if element.recreate_timer == 20:
                        element.create_random()
                        self.add_objects_marks(element.mark)
                        element.object_random_position()
                        element.put_on_board()
                        element.recreate_timer = 0
                    else:
                        element.recreate_timer += 1



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
            # elif element.row is None:
            #     self.objects_list.remove(element)
        
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
        self.Printer.print_hero_stats()


class Buyer(Person):
    def __init__(self, all_boards, printer):
        super().__init__('Buyer', all_boards)
        self.mark = '!'
        self.printer = printer
        self.multilinePrinter = MultiLinePrinter(self.printer)
        self.name = 'Bruce'
        self.sell_price = {
            'Can': 1,
            'Bottle': 2
        }
    
    def buyer_question(self):
        questions = [
            'What do you want to sell?'
        ]
        
        return random.sample(questions, 1)[0]

    def calc_revenue(self, amount, item_type):
        multiplier = amount // 30
        
        if multiplier > 0:
            return int((self.sell_price[item_type] * multiplier) * amount)
        else:
            return int(self.sell_price[item_type] * amount)
    
    def sell_reaction(self, item_type, hero):
        self.multilinePrinter.clear()
        self.multilinePrinter.reset_line()
        
        item_amount = hero.Backpack.recycles[item_type]
        
        answers = []
        if item_amount > 1:
            self.multilinePrinter.print_line(f"You opened your bag and take out {item_amount} {item_type}s.")
        else:
            self.multilinePrinter.print_line(f"You opened your bag and take out {item_amount} {item_type}.")
        
        self.multilinePrinter.refresh()
        time.sleep(2)
        if item_amount < 5:
            self.multilinePrinter.print_line(f"{self.name}: You must be joking. I won't buy {item_amount} {item_type}s from you.")
            self.multilinePrinter.print_line(f"Come back if you collect more.")
            self.multilinePrinter.refresh()
            
            time.sleep(2)
            self.multilinePrinter.print_line(f"You put your {item_type}s back to you bag and go away.")
        elif item_amount < 30:
            self.multilinePrinter.print_line(f"{self.name}: Only {item_amount} {item_type}s?")
            self.multilinePrinter.print_line(f"I can give you {self.calc_revenue(item_amount, item_type)} coins.")
            self.multilinePrinter.refresh()
            
            time.sleep(2)
            self.multilinePrinter.print_line(f"You put earnd coins into you wallet.")
            hero.Backpack.recycles[item_type] = 0
            hero.Backpack.money += self.calc_revenue(item_amount, item_type)
        elif item_amount >= 30:
            self.multilinePrinter.print_line(f"For {item_amount} I can give you {self.calc_revenue(item_amount, item_type)} coins.")
            self.multilinePrinter.refresh()
            
            time.sleep(2)
            self.multilinePrinter.print_line(f"You put earnd coins into you wallet.")
            hero.Backpack.recycles[item_type] = 0
            hero.Backpack.money += self.calc_revenue(item_amount, item_type)
        
        self.multilinePrinter.refresh()
        
    
    def react(self, hero):
        user_input = None
        next_round = False
        
        while user_input is None:
            if next_round:
                user_input = self.printer.screen.getch()
            
            self.multilinePrinter.clear()
            self.multilinePrinter.reset_line()
            self.multilinePrinter.print_line(self.buyer_question())
            self.multilinePrinter.print_line(f"1. Cans")
            self.multilinePrinter.print_line(f"2. Bottles")
            self.multilinePrinter.print_line("0. Exit")
            self.multilinePrinter.print_line(" ")
            self.multilinePrinter.refresh()
            
            if user_input == ord('1'):
                self.sell_reaction('Can', hero)
                
                hero.printer.print_hero_stats()
                
                self.multilinePrinter.refresh()
                self.printer.screen.getch()
            elif user_input == ord('2'):
                self.sell_reaction('Bottle', hero)
                hero.printer.print_hero_stats()
                
                self.multilinePrinter.refresh()
                self.printer.screen.getch()
                
            elif user_input == ord('0'):
                self.multilinePrinter.clear()
            else:
                user_input = None
            
            next_round = True
    
        


class Recycle_item(Person):
    def __init__(self, all_boards, printer):
        super().__init__('Recycle', all_boards)
        self.mark = None
        self.printer = printer
        self.multilinePrinter = MultiLinePrinter(self.printer)
        self.name = None
        self.amount = None
        self.recreate_timer = 0
    
    def create_random(self):
        recycle_items = ['Can', 'Bottle']
        item_random_name = random.sample(recycle_items, 1)[0]
        self.name = item_random_name
        self.mark = item_random_name[0]
        basic_amount = 3
        divider = 2
        self.amount = self.random_range_values(basic_amount, divider)
    
    def react(self, hero):
        self.multilinePrinter.clear()
        self.multilinePrinter.reset_line()
        
        if self.amount == 1:
            name = self.name
        else:
            name = self.name + 's'
        
        self.printer.msg = f"You picked up {self.amount} {name}."
        hero.Backpack.recycles[self.name] += self.amount
        self.printer.Board.board[self.row][self.col] = ' '
        self.row = None
        self.col = None
        

class Seller(Person):
    def __init__(self, all_boards, printer):
        super().__init__('Seller', all_boards)
        self.mark = 'H'
        self.name = None
        self.printer = printer
        self.multilinePrinter = MultiLinePrinter(self.printer)
        self.gender = None
        self.encounter_counter = 0
        self.stock = {}
    
    def create_random(self):
        NAME_INDEX = 1
        GENDER_INDEX = 3
        
        people_data = util.read_csv('people_names.csv')
        
        man_random = random.sample(people_data, 1)[0]
        self.name = man_random[NAME_INDEX]
        self.gender = man_random[GENDER_INDEX]
    
    def seller_question(self):
        questions = [
            'What do you want to buy?'
        ]
        
        return random.sample(questions, 1)[0]
    
    def react(self, hero):
        self.encounter_counter += 1
        user_input = None
        next_round = False
        
        while user_input is None:
            if next_round:
                user_input = self.printer.screen.getch()
            
            self.multilinePrinter.clear()
            self.multilinePrinter.reset_line()
            self.multilinePrinter.print_line(self.seller_question())
            self.multilinePrinter.print_line(f"1. Ask {self.name} for a money.")
            self.multilinePrinter.print_line("0. Exit")
            self.multilinePrinter.print_line(" ")
            self.multilinePrinter.refresh()
            
            if user_input == ord('1'):
                revenue = self.calc_revenue(hero)
                question = self.create_questions(hero)
                
                answers = []
                if self.encounter_counter >= 3:
                    answers.append("It's you again. I won't give you more money. Go away.")
                    answers.append(f"You turned back and go away.")
                else:
                    answers.append(f"{self.name} gives you {revenue} coins.")
                
                self.multilinePrinter.clear()
                self.multilinePrinter.reset_line()
                self.multilinePrinter.print_line(f"You: {question}")
                self.multilinePrinter.refresh()
                
                time.sleep(3)
                
                for line in answers:
                    self.multilinePrinter.print_line(line)
                
                hero.Backpack.money += revenue
                # hero.printer.print_hero_stats()
                
                self.multilinePrinter.refresh()
                self.printer.screen.getch()
                
            elif user_input == ord('0'):
                self.multilinePrinter.clear()
            else:
                user_input = None
            
            next_round = True


class Lump(Person):
    def __init__(self, all_boards, printer):
        super().__init__('Lump', all_boards)
        self.mark = 'L'
        self.name = None
        self.dmg = 20
        self.hp = 50
        self.interest_loss = 0
        self.printer = printer
        self.multilinePrinter = MultiLinePrinter(self.printer)
        
    
    def create_random(self):
        names = ['Boris', 'Nikita', 'Andrei', 'Vasily', 'Vlad', 'Dmitry', 'Ivan', 'Igor']
        basic_hp = 80
        hp_divider = 4
        
        basic_dmg = 30
        dmg_divider = 2
        
        self.hp = self.random_range_values(basic_hp, hp_divider)
        
        self.dmg = self.random_range_values(basic_dmg, dmg_divider)
        
        self.name = random.sample(names, 1)[0]
        
    def lump_question(self, reason):
        questions_attack = [
            'Hey you, give me your stuf!'
        ]
        questions_conversation = [
            'What do you want?'
        ]
        
        if reason == 'attack':
            return random.sample(questions_attack, 1)[0]
        elif reason == 'conversation':
            return random.sample(questions_conversation, 1)[0]
    
    def dmg_calculation(self, hero):
        pass
    
    def hero_revenue_calculation(self):
        revenue = {
            'coins': 0,
            'cans': 0,
            'bottles': 0
        }
        
        basic_revenue = 30
        revenue_divider = 2
        
        for item in revenue.keys():
            revenue[item] = self.random_range_values(basic_revenue, revenue_divider)
        
        return revenue

    def perc_lost_calc(self, value):
        lost = (random.randint(50, 100)) / 100
        return int(value * lost)

    def hero_lost_calculation(self, hero):
        lost = {
            'coins': self.perc_lost_calc(hero.Backpack.money),
            'cans': self.perc_lost_calc(hero.Backpack.recycles['Can']),
            'bottles': self.perc_lost_calc(hero.Backpack.recycles['Bottle'])
        }
        
        return lost
    
    def fight(self, hero, input):
        fighting = True
        next_round = False
        
        while fighting:
            if next_round:
                user_input = self.printer.screen.getch()
                
            user_input = input
            self.multilinePrinter.clear()
            self.multilinePrinter.reset_line()
            
            hero_dmg_range = int(hero.dmg / 10)
            hero_dmg_random = random.randint(hero.dmg - hero_dmg_range, hero.dmg + hero_dmg_range)
            
            lump_dmg_range = int(self.dmg / 10)
            lump_dmg_random = random.randint(self.dmg - lump_dmg_range, self.dmg + lump_dmg_range)
            
            self.hp -= hero_dmg_random
            
            if self.hp < 0:
                self.multilinePrinter.print_line(f"You defeated {self.name}.")
                self.printer.screen.refresh()
                time.sleep(1)
                
                self.multilinePrinter.print_line(f"You earned:")
                self.printer.screen.refresh()
                
                revenue = self.hero_revenue_calculation()
                for item in ['coins', 'cans', 'bottles']:
                    time.sleep(0.5)
                    
                    self.multilinePrinter.print_line(f"{revenue[item]} {item}")
                    if item == 'coins':
                        hero.Backpack.money += revenue[item]
                    elif item == 'cans':
                        hero.Backpack.recycles['Can'] += revenue[item]
                    elif item == 'bottles':
                        hero.Backpack.recycles['Bottle'] += revenue[item]
                        
                    self.printer.print_hero_stats()
                    self.printer.refresh()
                self.printer.screen.getch()
                    
                    # time.sleep(0.5)
                
                # self.Board.board[self.row][self.col] = ' '
                
                # self.row = None
                # self.col = None
                
                return 1
            else:                
                if hero.Inventory.weapon:
                    self.multilinePrinter.print_line(hero.Inventory.weapon.fight_message())
                else:
                    self.multilinePrinter.print_line(hero.fight_message().format(name=self.name))
                
                self.printer.screen.refresh()
                
                time.sleep(0.5)
                
                self.multilinePrinter.print_line(f"You did {hero_dmg_random} damage to {self.name}. {self.name}'s HP: {self.hp}.")
                self.printer.screen.refresh()
                
            hero.hp -= lump_dmg_random
            # time.sleep(0.5)
            
            if hero.hp < 0:
                self.multilinePrinter.print_line(f"You was defeated by {self.name}.")
                self.printer.screen.refresh()
                time.sleep(1)
                
                self.multilinePrinter.print_line(f"You lost:")
                self.printer.screen.refresh()
                
                lost = self.hero_lost_calculation(hero)
                for item in ['coins', 'cans', 'bottles']:
                    time.sleep(0.5)
                    
                    self.multilinePrinter.print_line(f"{lost[item]} {item}")
                    
                    if item == 'coins':
                        hero.Backpack.money -= lost[item]
                    elif item == 'cans':
                        hero.Backpack.recycles['Can'] -= lost[item]
                    elif item == 'bottles':
                        hero.Backpack.recycles['Bottle'] -= lost[item]
                        
                    self.printer.print_hero_stats()
                    self.printer.refresh()
                self.printer.screen.getch()
                
                # time.sleep(1)
                return 1
            else:
                time.sleep(0.5)
                self.multilinePrinter.print_line(f"{self.name} hit you by {lump_dmg_random}. Your HP: {hero.hp}.")
                self.printer.screen.refresh()
            next_round = True
    
    def react(self, hero):
        user_input = None
        next_round = False
        
        while user_input is None:
            if next_round:
                user_input = self.printer.screen.getch()
            
            self.multilinePrinter.clear()
            self.multilinePrinter.reset_line()
            
            if hero.Backpack.recycles['Can'] > 10 or hero.Backpack.recycles['Bottle'] > 10:
                self.multilinePrinter.print_line(self.lump_question('attack'))
                self.multilinePrinter.print_line(f"1. Attack.")
                self.multilinePrinter.print_line(f"2. Try to get along with {self.name}.")
                self.multilinePrinter.print_line("0. Exit")
                self.multilinePrinter.print_line(" ")
                self.multilinePrinter.refresh()
                
                if user_input == ord('1'):
                    user_input = self.fight(hero, user_input)
                    
                elif user_input == ord('2'):
                    pass
                elif user_input == ord('0'):
                    self.multilinePrinter.clear()
                else:
                    user_input = None
                
                # next_round = True
            else:
                self.multilinePrinter.print_line(self.lump_question('conversation'))
                self.multilinePrinter.print_line(f"1. Attack.")
                self.multilinePrinter.print_line(f"2. Try to take {self.name}'s stuff.")
                self.multilinePrinter.print_line("0. Exit")
                self.multilinePrinter.print_line(" ")
                self.multilinePrinter.refresh()
                
                if user_input == ord('1'):
                    user_input = self.fight(hero, user_input)
                    
                elif user_input == ord('2'):
                    pass
                elif user_input == ord('0'):
                    self.multilinePrinter.clear()
                else:
                    user_input = None
            
            next_round = True
    


class Pedestrian(Person):
    def __init__(self, all_boards, printer):
        super().__init__('Pedestrian', all_boards)
        self.mark = 'H'
        self.name = None
        self.printer = printer
        self.multilinePrinter = MultiLinePrinter(self.printer)
        self.gender = None
        self.money_amount = None
        self.politeness = None
        self.encounter_counter = 0
        self.hero_questions = {
            10: [
                'Hey boss. Can you give me some money?',
                'Give me some money.',
            ],
            15: [
                'Sorry, may I ask you for some money?'
            ],
            20: [
                'Sorry to bother you, but could you lend me some money?'
            ]
        }
    
    def create_random(self):
        NAME_INDEX = 1
        GENDER_INDEX = 3
        
        people_data = util.read_csv('people_names.csv')
        
        basic_money_amount = 30
        money_divider = 4        
        self.money_amount = self.random_range_values(basic_money_amount, money_divider)
        
        basic_politeness = 5
        polite_divider = 2
        self.politeness = self.random_range_values(basic_politeness, polite_divider) / 100
        
        man_random = random.sample(people_data, 1)[0]
        self.name = man_random[NAME_INDEX]
        self.gender = man_random[GENDER_INDEX]
    
    def calc_revenue(self, hero):
        politeness_mod = self.politeness - (self.encounter_counter / 100)
        politeness_mod = (hero.rhetoric * politeness_mod) + politeness_mod
        revenue = self.money_amount * politeness_mod
        
        return int(revenue)

    def create_questions(self, hero):
        questions = []
        for key in sorted(self.hero_questions.keys(), reverse=True):
            if hero.rhetoric >= key:
                questions.extend(self.hero_questions[key])
        
        return random.sample(questions[0:3], 1)[0]
    
    def react(self, hero):
        self.encounter_counter += 1
        user_input = None
        next_round = False
        
        while user_input is None:
            if next_round:
                user_input = self.printer.screen.getch()
            
            self.multilinePrinter.clear()
            self.multilinePrinter.reset_line()
            self.multilinePrinter.print_line(f"You encountered {self.name}.")
            self.multilinePrinter.print_line(f"1. Ask {self.name} for a money.")
            self.multilinePrinter.print_line("0. Exit")
            self.multilinePrinter.print_line(" ")
            self.multilinePrinter.refresh()
            
            if user_input == ord('1'):
                revenue = self.calc_revenue(hero)
                question = self.create_questions(hero)
                
                answers = []
                if self.encounter_counter >= 3:
                    answers.append("It's you again. I won't give you more money. Go away.")
                    answers.append(f"You turned back and go away.")
                else:
                    answers.append(f"{self.name} gives you {revenue} coins.")
                
                self.multilinePrinter.clear()
                self.multilinePrinter.reset_line()
                self.multilinePrinter.print_line(f"You: {question}")
                self.multilinePrinter.refresh()
                
                time.sleep(3)
                
                for line in answers:
                    self.multilinePrinter.print_line(line)
                
                hero.Backpack.money += revenue
                hero.printer.print_hero_stats()
                
                self.multilinePrinter.refresh()
                self.printer.screen.getch()
                
            elif user_input == ord('0'):
                self.multilinePrinter.clear()
            else:
                user_input = None
            
            next_round = True


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
            