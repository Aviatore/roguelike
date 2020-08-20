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
    curses.init_pair(4, 208, -1)
    color_pairs = [
        ['~', 1],
        ['Y', 2],
        ['T', 2],
        ["`", 2],
        ['#', 3],
        ['[', 3],
        [']', 3],
        ['|', 3],
        ['_', 3],
        ['"', 4]
    ]
    
    all_boards = engine.Boards()
    
    
    board1 = engine.Board('b1', screen)
    board1.create_board_template(boards.first_board, door_dest_board_ids=['b2', 'b3'])
    
    board2 = engine.Board('b2', screen)
    board2.create_board_template(boards.second_board, door_dest_board_ids=['b1', 'b3'])
    
    board3 = engine.Board('b3', screen)
    board3.create_board_template(boards.third_board, door_dest_board_ids=['b2', 'b1', 'b4'])
    
    board4 = engine.Board('b4', screen)
    board4.create_board_template(boards.fourth_board, door_dest_board_ids=['b3'])
    # board1 = engine.Board('b1', screen, 20, 40) # <board_id>, screen, <door_row_index>, <door_col_index>
    # board1.create_board(b2=[0, 6], b3=[12,39], b4=[19,10]) # <dest_board_id>=[<door_row_index>,<door_col_index>]
    
    
    # board5 = engine.Board('b5', screen)
    # board5_freePass_destination = {
    #     'right': 'b4'
    # }
    # board5.create_board_template(boards.board_5, freePass_destination=board5_freePass_destination)
    
    all_boards.add_board(board1)
    all_boards.add_board(board2)
    all_boards.add_board(board3)
    all_boards.add_board(board4)
    
    all_boards.set_current_board('b1')
    
    printer = ui.Printer(all_boards, curses)
    printer.add_colors(color_pairs)
    
    all_objects = engine.AllObjects()
    
    objects1 = engine.Objects('b1', board1, printer)
    
    pedestrian1 = engine.Pedestrian(all_boards, printer)
    pedestrian1.create_random()
    pedestrian1.object_random_position()
    pedestrian1.put_on_board()
    objects1.add_object(pedestrian1)
    
    recycle1 = engine.Recycle_item(all_boards, printer)
    recycle1.create_random()
    recycle1.object_random_position()
    recycle1.put_on_board()
    objects1.add_object(recycle1)
    
    

    lump1 = engine.Lump(all_boards, printer)
    lump1.create_random()
    lump1.object_random_position()
    lump1.put_on_board()
    objects1.add_object(lump1)
    
    objects2 = engine.Objects('b2', board2, printer)
    buyer1 = engine.Buyer(all_boards, printer)
    buyer1.set_position(5, 74, 'b2')
    objects2.add_object(buyer1)
    
    objects3 = engine.Objects('b3', board3, printer)
    objects4 = engine.Objects('b4', board4, printer)
    
    all_objects.add_objects('b1', objects1)
    all_objects.add_objects('b2', objects2)
    all_objects.add_objects('b3', objects3)
    all_objects.add_objects('b4', objects4)
    
    all_objects.set_current_objects('b1')
    
    hero = engine.Hero('hero', all_boards, all_objects, printer)

    hero.set_hp(100)
    hero.object_random_position()
    hero.put_on_board()
    
    printer.add_hero(hero)
    printer.print_board()
    printer.print_hero_stats()
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
        
        hero.move_objects()
        
        hero.printer.screen.clear()
        printer.print_hero_stats()
    
        printer.print_board()
        printer.msgBox_print_line_cached()
        
        # printer.screen.addstr(30, 5, f"DEBUG: {hero.dir} {hero.dir_offset} {hero.distance_row} {hero.distance_col} {hero.reverse_offset}")
        printer.screen.addstr(30, 5, f"DEBUG: {hero.interest_lvl}")
        
        screen.refresh()
        
        curses.flushinp()
        
        all_objects.recreate()
        
        time.sleep(0.1)
    

if __name__ == "__main__":
    curses.wrapper(main)