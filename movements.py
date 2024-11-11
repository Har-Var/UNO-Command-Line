########################################
# Movements
########################################
import random
import printing_functions as pf
import game_management as gm
import pyinputplus as pyip


def turn_fixer(variable_list):
    """
    Adjusts the move counter to ensure it stays within the valid range of player numbers.

    Parameters
    ----------
    variable_list : dict
        Dictionary containing game variables, including the move counter and number of players.

    Returns
    -------
    dict
        Updated dictionary with the corrected move counter.
    """
    move_counter = variable_list.get("move_counter")
    players_no = variable_list.get("players_no")

    if move_counter == players_no + 1:
        move_counter = 1
    elif move_counter == players_no + 2:
        move_counter = 2
    elif move_counter == 0:
        move_counter = players_no
    elif move_counter == -1:
        move_counter = players_no - 1
    else:
        move_counter

    variable_list["move_counter"] = move_counter
    return variable_list


def turn_switcher(variable_list):
    """
    Updates the move counter based on the current move direction and ensures
    it remains within the valid range of player numbers by calling turn_fixer.

    Parameters
    ----------
    variable_list : dict
        Dictionary containing game variables, including the move counter and move direction.

    Returns
    -------
    dict
        Updated dictionary with the adjusted move counter.
    """
    move_counter = variable_list.get("move_counter")
    move_direction = variable_list.get("move_direction")

    move_counter = move_counter + move_direction

    variable_list["move_counter"] = move_counter
    variable_list = turn_fixer(variable_list)

    return variable_list


def draw_card(variable_list):
    """
    Simulates drawing a card from the folded deck for the current player.

    Parameters
    ----------
    variable_list : dict
        Dictionary containing game variables, including the move counter, folded deck, and player decks.

    Returns
    -------
    tuple
        A tuple containing the drawn card and the updated dictionary with the adjusted player decks and folded deck.
    """
    move_counter = variable_list.get("move_counter")
    folded_deck = variable_list.get("folded_deck")
    all_players_deck = variable_list.get("all_players_deck")

    player_index = move_counter - 1
    card_index = random.randint(0, len(folded_deck) - 1)
    drawn_card = folded_deck.pop(card_index)
    all_players_deck[player_index].append(drawn_card)

    # Only printing drawn card if player 1 i.e. real player's move
    if move_counter == 1:
        print("Drawn Card:-")
        pf.print_card(drawn_card)
    else:
        pass

    variable_list["all_players_deck"] = all_players_deck
    variable_list["folded_deck"] = folded_deck
    return drawn_card, variable_list


def checking_legal_move(card, variable_list):
    """
    Checks if the given card is a legal move based on the current livecard.

    Parameters
    ----------
    card : dict
        Dictionary containing the card's face and color.
    variable_list : dict
        Dictionary containing game variables, including the livecard and possible colors.

    Returns
    -------
    bool
        True if the move is legal, False otherwise.
    """
    livecard = variable_list.get("livecard")
    possible_colors = variable_list.get("possible_colors")

    if (card.get("face") == livecard.get("face")) or (
        card.get("color") in [livecard.get("color"), possible_colors[4]]
    ):
        result = True
    else:
        result = False
    return result


def player_available_moves(variable_list):
    """
    Determines the available legal moves for the current player based on their hand and the game's live card.
    If no legal moves are available, draws a card from the folded deck and checks its legality.

    Parameters
    ----------
    variable_list : dict
        Dictionary containing game variables, including the move counter and all players' decks.

    Returns
    -------
    tuple
        A tuple containing the list of available legal moves and the updated game variables dictionary.
    """
    move_counter = variable_list.get("move_counter")
    all_players_deck = variable_list.get("all_players_deck")

    available_moves = []
    player_index = move_counter - 1
    for card in all_players_deck[player_index]:
        if checking_legal_move(card, variable_list):
            available_moves.append(card)
            continue
    if available_moves == []:
        print("No legal moves available, drawing one card from folded deck\n")
        drawn_card, variable_list = draw_card(variable_list)
        if checking_legal_move(drawn_card, variable_list):
            available_moves.append(drawn_card)
        else:
            pass

    return available_moves, variable_list


def post_move_display(variable_list):
    """
    Prints a message indicating the player who made the move and the move itself.

    Parameters
    ----------
    variable_list : dict
        Dictionary containing game variables, including the move counter, livecard, and players' names.
    """
    player_id = variable_list.get("move_counter")
    player_index = player_id - 1
    livecard = variable_list.get("livecard")
    players_names = variable_list.get("players_names")
    player_name = players_names[player_index].get("player_name")

    if player_id == 1:
        # i.e. Real Player Move
        print(f"{player_name} (Player-{player_id}) plays :- ")

    else:
        # i.e. AI opponent Move
        print(f"AI Opponent ({player_name},Player-{player_id}) plays :- ")

    pf.print_card(livecard)
    print("----------------------------------------------------------")


def play_card(card_id, variable_list, available_moves):
    """
    Simulates a player playing a card from their hand.

    Parameters
    ----------
    card_id : int
        The position of the card in the player's hand that they want to play.
    variable_list : dict
        Dictionary containing game variables, including the move counter, livecard, and players' decks.
    available_moves : list
        List of available moves for the current player.

    Returns
    -------
    tuple
        A tuple containing the updated dictionary with the played card removed from the player's deck and added to the table deck, and a game over flag of 1 if the player has won, or 0 if the game is not over.
    """
    move_counter = variable_list.get("move_counter")
    all_players_deck = variable_list.get("all_players_deck")
    table_deck = variable_list.get("table_deck")

    player_index = move_counter - 1
    card_index = card_id - 1

    player_deck_card_index = all_players_deck[player_index].index(
        available_moves[card_index]
    )
    livecard = all_players_deck[player_index].pop(player_deck_card_index)
    table_deck.append(livecard)

    variable_list["livecard"] = livecard
    variable_list["all_players_deck"] = all_players_deck
    variable_list["table_deck"] = table_deck

    if len(all_players_deck[player_index]) == 0:
        game_over_flag = 1
    else:
        game_over_flag = 0

    return variable_list, game_over_flag


# For +2, +4, Reverse and Skip


def livecard_automove(variable_list):
    """
    Automates the moves for special cards (Reverse, Skip, +2, +4, Wild Card) and
    updates the game variables accordingly.

    Parameters
    ----------
    variable_list : dict
        Dictionary containing game variables, including the move counter, livecard, and players' decks.

    Returns
    -------
    dict
        Updated dictionary containing the game variables, including the move counter, livecard, and players' decks.
    """
    players_no = variable_list.get("players_no")
    livecard = variable_list.get("livecard")
    move_counter = variable_list.get("move_counter")
    move_direction = variable_list.get("move_direction")
    possible_faces = variable_list.get("possible_faces")
    folded_deck = variable_list.get("folded_deck")
    all_players_deck = variable_list.get("all_players_deck")
    card_face = livecard.get("face")

    player_index = move_counter - 1

    if card_face == possible_faces[10]:
        print("2 cards were added")
        if move_counter == 1:
            # If real player
            print("Added Cards:-")
        else:
            # If AI opponent
            pass
        for _ in range(2):
            card_index = random.randint(0, len(folded_deck) - 1)
            addcard = folded_deck.pop(card_index)
            all_players_deck[player_index].append(addcard)
            if move_counter == 1:
                # If real player
                pf.print_card(addcard)
            else:
                # If AI opponent
                pass

    elif card_face == possible_faces[11]:
        move_direction = move_direction * -1
        move_counter = move_counter + 2 * move_direction
        print("Move Direction Reversed")

    elif card_face == possible_faces[12]:
        move_counter = move_counter + move_direction
        print("Next Player's Move Skipped")

    elif card_face == possible_faces[13]:
        print("+4 Card")
        valid_colors = ["red", "blue", "green", "yellow"]
        prev_move_counter = move_counter - move_direction
        if prev_move_counter in [1, players_no + 1]:
            # Previous move player is Real Player
            print("What color do you want played?\n")
            color_change = pyip.inputChoice(valid_colors)
        else:
            #  Previous move player is AI opponent
            color_change = random.choice(valid_colors)

        livecard = {"face": "  ", "color": color_change}
        if move_counter == 1:
            # If real player
            print("Added Cards:-")
        else:
            # If AI opponent
            pass
        for _ in range(4):
            card_index = random.randint(0, len(folded_deck) - 1)
            addcard = folded_deck.pop(card_index)
            all_players_deck[player_index].append(addcard)
            if move_counter == 1:
                # If real player
                pf.print_card(addcard)
            else:
                # If AI opponent
                pass

    elif card_face == possible_faces[14]:
        print("Wild Card")
        valid_colors = ["red", "blue", "green", "yellow"]

        prev_move_counter = move_counter - move_direction
        if prev_move_counter in [1, players_no + 1]:
            # Previous move player is Real Player
            print("What color do you want played?\n")
            color_change = pyip.inputChoice(valid_colors)
        else:
            #  Previous move player is AI opponent
            color_change = random.choice(valid_colors)
        livecard = {"face": "  ", "color": color_change}

    variable_list["livecard"] = livecard
    variable_list["move_counter"] = move_counter
    variable_list["move_direction"] = move_direction
    variable_list["folded_deck"] = folded_deck
    variable_list["all_players_deck"] = all_players_deck

    variable_list = turn_fixer(variable_list)
    return variable_list


def pre_move_management(variable_list):
    """
    Manages the pre-move actions for the current player by displaying their hand,
    determining available legal moves, and printing them.

    Parameters
    ----------
    variable_list : dict
        Dictionary containing game variables, including the move counter and all players' decks.

    Returns
    -------
    tuple
        A tuple containing the updated game variables dictionary and the list of available legal moves.
    """
    player_id = variable_list.get("move_counter")
    pf.print_livecard(variable_list)
    if player_id == 1:
        # i.e. Real Player Move
        pf.print_hand(variable_list, player_nature="real")
        available_moves, variable_list = player_available_moves(variable_list)
        pf.print_available_moves(available_moves, player_nature="real")

    else:
        # i.e. AI opponent Move
        pf.print_hand(variable_list, player_nature="ai")
        available_moves, variable_list = player_available_moves(variable_list)
        pf.print_available_moves(available_moves, player_nature="ai")

    print("----------------------------------------------------------")
    return variable_list, available_moves


def play_move_management(card_id, variable_list, available_moves):
    """
    Manages the post-move actions for the current player by displaying the played card,
    switching the turn, and checking for any automatic moves by the livecard.

    Parameters
    ----------
    card_id : int
        The position of the card in the player's hand that they want to play.
    variable_list : dict
        Dictionary containing game variables, including the move counter and all players' decks.
    available_moves : list
        List of available legal moves for the current player.

    Returns
    -------
    dict
        Updated dictionary containing the game variables.
    """
    variable_list, game_over_flag = play_card(card_id, variable_list, available_moves)
    if game_over_flag == 1:
        gm.print_game_over(variable_list)
        variable_list = gm.play_again()
    elif game_over_flag == 0:
        post_move_display(variable_list)
        variable_list = turn_switcher(variable_list)
        variable_list = livecard_automove(variable_list)
    return variable_list


def main_move_manager(variable_list):
    """
    Manages the main game loop by calling pre_move_management to display the player's hand and available moves,
    and then either switching the turn if no moves are available or calling play_move_management to play a card
    from the available moves.

    Parameters
    ----------
    variable_list : dict
        Dictionary containing game variables, including the move counter, livecard, and players' decks.

    Returns
    -------
    dict
        Updated dictionary containing the game variables.
    """
    player_id = variable_list.get("move_counter")
    variable_list, available_moves = pre_move_management(variable_list)

    if len(available_moves) == 0:
        variable_list = turn_switcher(variable_list)
    else:
        if player_id == 1:
            # i.e. Real Player
            card_no = pyip.inputInt("Select card from available moves to play\n",min=1,max=len(available_moves))
        else:
            # AI opponent
            card_no = random.randint(1, len(available_moves))
        variable_list = play_move_management(card_no, variable_list, available_moves)

    return variable_list
