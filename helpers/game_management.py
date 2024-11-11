import random
import csv
import helpers.printing_functions as pf
import pyinputplus as pyip


########################################
# Setup
########################################

file_path = "data/report/uno_winners.csv"
# Make sure the csv template file is saved as 'utf with BOM' to ensure characters like '↕' don't throw error. Did this in notepad save as encoding = utf with BOM.

########################################
# Initializing Inputs
########################################

def rules_input():
    """
    Function to ask user if they want to read the rules or not
    If yes, prints the rules using pf.print_rules()
    If no, does nothing
    """
    
    read_input = pyip.inputYesNo("Would you like to read the rules? y/n\n")
    if read_input == "yes":
        pf.print_rules()
    else:
        pass

def initializing_inputs():
    """
    Function to initialize inputs for the game
    """
    
    variable_list = {}
    move_counter = 1
    move_direction = +1

    players_no = pyip.inputInt("How many total players do you want?\n")
    first_hand_count = pyip.inputInt("How many cards do you want to be distributed in the first hand?\n")

    players_names = []
    for player in range(players_no):
        if player == 0:
            players_names.append(
                {"player_id": player + 1, "player_name": input("Enter Your Name\n")}
            )
        else:
            players_names.append(
                {
                    "player_id": player + 1,
                    "player_name": input("Enter AI Opponnent Name\n") + "-AI",
                }
            )

    ########################################################################################
    # For Testing
    # players_no = 3
    # first_hand_count = 4

    # players_names = [{'player_id': 1, 'player_name': 'Abra'},
    #                  {'player_id': 2, 'player_name': 'Babra'},
    #                  {'player_id': 3, 'player_name': 'Chabra'}]

    ########################################################################################

    variable_list_update = {
        "move_counter": move_counter,
        "move_direction": move_direction,
        "players_no": players_no,
        "first_hand_count": first_hand_count,
        "players_names": players_names,
    }
    variable_list.update(variable_list_update)
    return variable_list


########################################
# Creating Decks
########################################


def full_uno_deck(variable_list):
    # Adding a space before to accomodate +2 and +4
    """
    Function to generate the full UNO deck of cards
    
    Parameters
    ----------
    variable_list : dict
        Dictionary containing the game variables
    
    Returns
    -------
    variable_list : dict
        Updated dictionary containing the game variables with the key 'card_deck'
    """
    
    possible_faces = [
        " 0",
        " 1",
        " 2",
        " 3",
        " 4",
        " 5",
        " 6",
        " 7",
        " 8",
        " 9",
        "+2",
        " ↕",
        " Ø",
        "+4",
        " W",
    ]
    possible_colors = ["red", "blue", "yellow", "green", "black"]

    # Generating the complete deck of UNO cards
    card_deck = []

    # Add number and action cards for each color
    for color in possible_colors[:4]:
        # Adding one of 0 card
        card_deck.append({"face": possible_faces[0], "color": color})

        # Adding two of each card from 1 to 9
        for face in possible_faces[1:13]:
            for _ in range(2):
                card_deck.append({"face": face, "color": color})

    # Add wild cards
    for face in possible_faces[13:]:
        for _ in range(4):
            card_deck.append({"face": face, "color": possible_colors[4]})

    variable_list_update = {
        "possible_faces": possible_faces,
        "possible_colors": possible_colors,
        "card_deck": card_deck,
    }
    variable_list.update(variable_list_update)

    return variable_list


########################################
# Dividing Decks among player and AI
########################################


def distribute_deck(variable_list):
    """
    Distributes the deck of cards among the players and AI.

    Parameters:
        variable_list (dict): Dictionary containing all game variables.

    Returns:
        dict: Updated dictionary containing the distributed decks and other game variables.
    """


    players_no = variable_list.get("players_no")
    first_hand_count = variable_list.get("first_hand_count")
    card_deck = variable_list.get("card_deck")
    possible_faces = variable_list.get("possible_faces")

    def grp_to_deck(player):
        deck = []
        for i in player:
            deck.append(card_deck[i])
        return deck

    playing_groups = []
    remaining_range = list(range(0, len(card_deck)))
    for no in range(players_no):
        player_grp = random.sample(remaining_range, first_hand_count)
        playing_groups.append(player_grp)
        remaining_range = list(set(remaining_range) - set(player_grp))
    folded_grp = remaining_range

    all_players_deck = []
    for i in range(players_no):
        all_players_deck.append(grp_to_deck(playing_groups[i]))
    folded_deck = grp_to_deck(folded_grp)
    table_deck = []
    while True:
        random_card = random.randint(0, len(folded_deck) - 1)
        if folded_deck[random_card].get("face") not in possible_faces[10:]:
            livecard = folded_deck.pop(random_card)
            break
    table_deck.append(livecard)

    variable_list_update = {
        "all_players_deck": all_players_deck,
        "folded_deck": folded_deck,
        "table_deck": table_deck,
        "livecard": livecard,
    }
    variable_list.update(variable_list_update)

    return variable_list


def set_game():
    """
    Function to set up the game of UNO
    """
    
    variable_list = initializing_inputs()
    variable_list = full_uno_deck(variable_list)
    variable_list = distribute_deck(variable_list)
    pf.intro_message()
    rules_input()
    pf.begin_print()
    return variable_list


def data_upload(variable_list):
    """
    Uploads game data to a CSV file.

    Parameters
    ----------
    variable_list : dict
        Dictionary containing the game variables, including the current move counter,
        list of players' names, the current live card, and the table deck.

    Writes to
    ---------
    A CSV file specified by the global variable `file_path`, appending a row with:
        - The winner's name
        - The live card at the end of the game
        - The total number of moves played

    Prints
    ------
    A message indicating that the winner's name has been added to the CSV file.
    """
    global file_path
    move_counter = variable_list.get("move_counter")
    player_index = move_counter - 1
    winner_name = variable_list.get("players_names")[player_index].get("player_name")

    livecard = variable_list.get("livecard")
    moves_played = len(variable_list.get("table_deck"))
    # Openning the file in append mode
    with open(file_path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([winner_name, livecard, moves_played])

    print(f"Added winner '{winner_name}' to {file_path}")


def print_game_over(variable_list):
    """
    Prints a congratulatory message for the winner and records the winner's name
    to a CSV file.

    Parameters
    ----------
    variable_list : dict
        Dictionary containing the game variables, including the current move counter,
        list of players' names, the current live card, and the table deck.

    Prints
    ------
    A congratulatory message with the winner's name.
    """
    move_counter = variable_list.get("move_counter")
    player_index = move_counter - 1
    winner_name = variable_list.get("players_names")[player_index].get("player_name")
    print(f"Congratulations {winner_name}!, You've won the game!")
    data_upload(variable_list)


def play_again():
    """
    Asks the user if they want to play again and if so, restarts the game by calling set_game().
    If the user does not want to play again, prints a thank you message and quits the game.

    Returns
    -------
    list
        Either a list containing the updated game variables if the user wants to play again,
        or a list containing the string "GAME OVER" if the user does not want to play again.
    """
    replay_response = pyip.inputYesNo("Game Over, would you like to play again? y/n\n")
    if replay_response == "yes":
        variable_list = set_game()
    else:
        print("Thank you for playing!")
        variable_list = ["GAME OVER"]
        quit()
    return variable_list
