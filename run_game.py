from engine import set_game, main_move_manager

variable_list = set_game()

while True:
    variable_list = main_move_manager(variable_list)
