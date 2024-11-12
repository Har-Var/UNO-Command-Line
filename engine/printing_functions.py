from operator import itemgetter

########################################
# Welcome Screen
########################################


def intro_message():
    """
    Prints a welcome message to the user with the game's logo and tagline ("Let's play!").
    """

    welcome_message = """
            Let's play!

            UUUUUUUU    UUUUUUU NNNNNNNN        NNNNNNNN     OOOOOOOOO     
            U:::::U     U:::::U N::::::N        N::::::N   O:::::::::::O   
            U:::::U     U:::::U N:::::::N       N::::::N O:::::::::::::::O 
            U:::::U     U:::::U N::::::::N      N::::::NO:::::::OOO:::::::O
            U:::::U     U:::::U N::::::::::N    N::::::NO::::::O   O::::::O
            U:::::U     U:::::U N:::::::::::N   N::::::NO:::::O     O:::::O
            U:::::U     U:::::U N:::::::N::::N  N::::::NO:::::O     O:::::O
            U:::::U     U:::::U N::::::N N::::N N::::::NO:::::O     O:::::O
            U:::::U     U:::::U N::::::N  N::::N:::::::NO:::::O     O:::::O
            U:::::U     U:::::U N::::::N   N:::::::::::NO:::::O     O:::::O
            U:::::U     U:::::U N::::::N    N::::::::::NO:::::O     O:::::O
            U::::::U   U::::::U N::::::N     N:::::::::NO::::::O   O::::::O
            U:::::::UUU:::::::U N::::::N      N::::::::NO:::::::OOO:::::::O
            U::::::::::::::::U  N::::::N       N:::::::N  O:::::::::::::::O 
              U::::::::::::U    N::::::N        N::::::N   O::::::::::::O   
                UUUUUUUUU       NNNNNNNN         NNNNNNN     OOOOOOOOOO    
    """
    print(welcome_message)


def print_rules():
    """
    Prints the rules of the game UNO.
    The rules are printed out in a formatted string.
    """

    print(
        """
          RULES:
                1. Objective: The objective of UNO is to be the first player to play all of your cards.
                2. Setup: 
                        - Before each game the deck is shuffled. 
                        - Each player draws a set number of cards from the shuffled deck. You can define this first hand deck number in the input option.
                        - The remaining cards form the fodled deck pile, with the top card placed face up next to the folded deck called as live card.
                        - First player is set to Player - 1, rest are AI opponents.
                3. Gameplay:
                        - Players take turns in clockwise order ( from 1-4).
                        - On your turn, you must play a card from your hand that matches either the color, number, or symbol of the live card.
                        - Apart from these you can also play a Black Wild Card (W) or Black Draw Four Card (+4).
                        - The game will show you the available moves matching these conditions, you must select the number of card to be played from this available moves list.
                        - If you don't have a playable card, you must draw a card from the folded deck. The game automatically does that for you.
                        - If you have a playable card but choose not to play it, simply type (pass) in the play move prompt.
                        - If you play a Black Draw Four card (+4) or a Black Wild card (W), you must declare the color the next player must play.
                        - If you play a Black Draw Four card (+4), the next player must draw four cards from the folded deck. The game automatically does that for you.
                        - If you play a Reverse card (Ø), the direction of play reverses.
                        - If you play a Skip card (↕), the next player in the sequence is skipped.
                        - If you play a Draw Two card (+2), the next player must draw two cards from the folded deck. The game automatically does that for you.
                4. Winning:
                        - The first player to play all of their cards wins.
                        - Once a player plays their last card, the game is over.
          """
    )


def begin_print():
    """
    Prints a message to indicate the start of the game
    """

    print(
        """
          #######################################################
          #######################################################

                              So Let's Begin!
          
          #######################################################
          #######################################################

          
          """
    )


########################################
# Printing Cards
########################################


def prRed(skk):
    """
    Prints a string in red color
    :param skk: String to be printed in red color
    """
    print("\033[91m {}\033[00m".format(skk))


def prGreen(skk):
    """
    Prints a string in green color
    :param skk: String to be printed in green color
    """
    print("\033[92m {}\033[00m".format(skk))


def prYellow(skk):
    """
    Prints a string in yellow color
    :param skk: String to be printed in yellow color
    """
    print("\033[93m {}\033[00m".format(skk))


def prBlue(skk):
    """
    Prints a string in blue color
    :param skk: String to be printed in blue color
    """
    print("\033[94m {}\033[00m".format(skk))


def prBlack(skk):
    """
    Prints a string in black color
    :param skk: String to be printed in black color
    """
    print("\033[98m {}\033[00m".format(skk))


# Print Cards
def print_card(card):
    """
    Prints a card in a given color

    Parameters
    ----------
    card : dict
        Dictionary containing the card's face and color
    """

    card_color = card.get("color")
    card_face = card.get("face")
    card_print_rows = ["", "", "", "", ""]
    card_print_rows[0] = " _____ "
    card_print_rows[1] = "|     |"
    card_print_rows[2] = "| " + card_face + "  |"
    card_print_rows[3] = "|     |"
    card_print_rows[4] = " ‾‾‾‾‾ "
    for row in card_print_rows:
        if card_color == "red":
            prRed(row)
        elif card_color == "blue":
            prBlue(row)
        elif card_color == "yellow":
            prYellow(row)
        elif card_color == "green":
            prGreen(row)
        elif card_color == "black":
            prBlack(row)


# Printing Cards for Display PlayerWise


def print_hand(variable_list, player_nature):
    """
    Displays the current player's hand of cards.

    Parameters
    ----------
    variable_list : dict
        Dictionary containing game variables, including the move counter and all players' decks.
    player_nature : str
        A string indicating the player's nature, either "real" for a real player or "ai" for an AI opponent.

    Prints
    ------
    If the player_nature is "real", prints the player's name and their hand of cards.
    If the player_nature is "ai", prints a message indicating that the AI opponent is examining their hand.
    """
    player_id = variable_list.get("move_counter")
    all_players_deck = variable_list.get("all_players_deck")
    players_names = variable_list.get("players_names")

    player_index = player_id - 1

    player_name = players_names[player_index].get("player_name")
    if player_nature == "real":
        print(f"{player_name} (Player-{player_id})'s Hand :-")
        for card in all_players_deck[player_index]:
            print_card(card)
    elif player_nature == "ai":
        print(
            f"AI Opponent ({player_name},Player-{player_id}) is examining their hand... "
        )


def print_livecard(variable_list):
    """
    Prints the current live card.

    Parameters
    ----------
    variable_list : dict
        Dictionary containing game variables, including the move counter and the live card.

    Prints
    ------
    The current live card.
    """
    livecard = variable_list.get("livecard")
    print("Livecard")
    print_card(livecard)


def print_available_moves(player_available_moves, player_nature):
    """
    Prints the available moves for the current player.

    Parameters
    ----------
    player_available_moves : list
        A list of cards that are available moves for the current player.
    player_nature : str
        A string indicating the player's nature, either "real" for a real player or "ai" for an AI opponent.

    Prints
    ------
    If the player_available_moves list is empty, prints a message indicating that no available moves are left, hence passing the turn.
    If the player_nature is "real", prints the list of available moves for the real player.
    If the player_nature is "ai", doesn't print anything (for AI opponents).
    """
    if player_available_moves == []:
        print(
            "No available moves since the drawn card isn't legal either, hence passing the turn"
        )
    else:
        if player_nature == "real":
            print("Available Moves:-")
            for card in player_available_moves:
                print_card(card)
        elif player_nature == "ai":
            pass


def print_table_deck(variable_list):
    """
    Prints the table deck of cards in a sorted order.

    Parameters
    ----------
    variable_list : dict
        Dictionary containing game variables, including the table deck.

    Prints
    ------
    The cards in the table deck, sorted first by color and then by face value in ascending order.
    """
    table_deck = variable_list.get("table_deck")
    # Sort the dictionary by color and then by face value (ascending order)
    sorted_table_deck = sorted(table_deck, key=itemgetter("color", "face"))
    for card in sorted_table_deck:
        print_card(card)


def print_all_cards_easyread(variable_list):
    """
    Prints all the cards in the game in an easy-to-read format.

    Parameters
    ----------
    variable_list : dict
        Dictionary containing game variables, including the folded deck, table deck, live card, all players' decks, and players' names.

    Prints
    ------
    The live card, each player's hand (numbered for identification), the folded deck, and the table deck, all in an easy-to-read format.
    """

    folded_deck = variable_list.get("folded_deck")
    table_deck = variable_list.get("table_deck")
    livecard = variable_list.get("livecard")
    all_players_deck = variable_list.get("all_players_deck")
    players_names = variable_list.get("players_names")

    print("         Live Card")
    print(livecard)

    for i in range(len(all_players_deck)):
        player_id = i + 1
        player_name = players_names[i].get("player_name")
        print(f"         {player_name}")
        print(f"         (Player - {player_id})")
        for j in all_players_deck[i]:
            print(j)
        print("")

    print("         Folded Deck")
    for card in folded_deck:
        print(card)

    print("         Table Deck")
    for card in table_deck:
        print(card)
