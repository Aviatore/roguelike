import curses
import engine
import ui
import time
import boards


def main(screen):
    screen.clear()
    curses.curs_set(False)
    curses.use_default_colors()
    curses.init_pair(1, 39, 21) # WATER_COLOR_PAIR
    curses.init_pair(2, 76, -1) # TREE_COLOR_PAIR
    curses.init_pair(3, 247, 15) # ROCK_COLOR_PAIR
    color_pairs = [
        ['~', 1],
        ['Y', 2],
        ['T', 2],
        ['#', 3],
        ['[', 3],
        [']', 3]
    ]
    
    all_boards = engine.Boards()
    
    board1 = engine.Board('b1', screen, 20, 40) # <board_id>, screen, <door_row_index>, <door_col_index>
    board1.create_board(b2=[0, 6], b3=[12,39], b4=[19,10]) # <dest_board_id>=[<door_row_index>,<door_col_index>]
    
    board2 = engine.Board('b2', screen, 10, 50)
    board2.create_board(b1=[9,4], b3=[5,49])
    
    board3 = engine.Board('b3', screen, 30, 10)
    board3.create_board(b1=[25,0], b2=[5,0])
    
    board4 = engine.Board('b4', screen)
    board4_freePass_destination = {
        'left': 'b5',
        'right': 'b6'
    }
    board4.create_board_template(boards.board_4, door_dest_board_ids=['b1'], freePass_destination=board4_freePass_destination)
    
    board5 = engine.Board('b5', screen)
    board5_freePass_destination = {
        'right': 'b4'
    }
    board5.create_board_template(boards.board_5, freePass_destination=board5_freePass_destination)
    
    all_boards.add_board(board1)
    all_boards.add_board(board2)
    all_boards.add_board(board3)
    all_boards.add_board(board4)
    all_boards.add_board(board5)
    
    all_boards.set_current_board('b1')
    
    printer = ui.Printer(all_boards, curses)
    printer.add_colors(color_pairs)
    
    all_objects = engine.AllObjects()
    
    objects1 = engine.Objects('b1', board1, printer)

    food = engine.Food(all_boards, printer)
    food.create_random()
    food.object_random_position()
    food.put_on_board()
    objects1.add_object(food)
    
    orc = engine.Orc(all_boards, printer)
    orc.create_random()
    orc.object_random_position()
    orc.put_on_board()
    objects1.add_object(orc)
    
    ##
    stolen_ring = engine.Item(all_boards, printer, 'ring', 'ring')
    stolen_ring.object_random_position()
    stolen_ring.put_on_board()
    objects1.add_object(stolen_ring)
    
    sword_revard = engine.Weapon('s2', 'Peace-maker', 50)
    
    hello_answer = engine.Action()
    hello_answer.add_label('It is nice to see you. Please, find my stolen ring.')
    
    found_ring_reaction = engine.Action()
    found_ring_reaction.add_label('I see that you have found my ring. Tkank you very much!\nThis is my reward.')
    
    notAwesome_answer = engine.Action()
    notAwesome_answer.add_label('It was not nice. Good bye.')
    
    action1 = engine.Action()
    action1.add_label('Hello stranger.')
    action1.add_option('Hello.')
    action1.add_option('Might your own buisness.')
    action1.add_reaction('1', hello_answer)
    action1.add_reaction('2', notAwesome_answer)
    action1.add_task_req_item_ids('ring', 'ring')
    action1.add_task_gift_items('ring', sword_revard)
    action1.add_task_react_req_item('ring', found_ring_reaction)
    
    
    stranger = engine.Person_custom('Human', all_boards, printer)
    stranger.set_mark('?')
    stranger.set_name('Edmund')
    stranger.set_position(10, 10)
    stranger.add_action(action1)
    objects1.add_object(stranger)
    ##
    
    objects2 = engine.Objects('b2', board2, printer)
    objects3 = engine.Objects('b3', board3, printer)
    objects4 = engine.Objects('b4', board4, printer)
    objects5 = engine.Objects('b5', board5, printer)
    
    all_objects.add_objects('b1', objects1)
    all_objects.add_objects('b2', objects2)
    all_objects.add_objects('b3', objects3)
    all_objects.add_objects('b4', objects4)
    all_objects.add_objects('b5', objects5)
    
    all_objects.set_current_objects('b1')
    
    hero = engine.Hero('fighter', all_boards, all_objects, printer)
    sword = engine.Weapon('s1', 'sword', dmg=30)
    hero.Inventory.put_on_weapon(sword)
    hero.set_hp(100)
    hero.object_random_position()
    hero.put_on_board()
    printer.print_board()
    screen.refresh()
    
    loop = True
    
    while loop:
        user_input = screen.getch()
        
        if user_input == curses.KEY_UP:
            hero.move("up")
        elif user_input == curses.KEY_DOWN:
            hero.move("down")
        elif user_input == curses.KEY_LEFT:
            hero.move("left")
        elif user_input == curses.KEY_RIGHT:
            hero.move("right")
        
        hero.printer.screen.clear()
        row = 5
        for item in hero.Backpack.other:
            hero.printer.screen.addstr(row, 45, f"Item: {item.name}")
            row += 1
        
        for item in hero.Backpack.weapons:
            hero.printer.screen.addstr(row, 45, f"Weapon: {item.name}")
            row += 1
    
        printer.print_board()
        
        screen.refresh()
        
        curses.flushinp()
        
        time.sleep(0.1)
    

if __name__ == "__main__":
    curses.wrapper(main)