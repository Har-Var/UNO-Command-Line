import movements as mv
import game_management as gm

variable_list = gm.set_game()

while True:
    variable_list = mv.main_move_manager(variable_list)