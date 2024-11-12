
# UNO Command Line App

## Description
UNO-Command-Line is a command-line-based implementation of the classic card game UNO. This project recreates the traditional gameplay experience of UNO, where players take turns matching cards by color or number and aim to be the first to play all their cards. It includes essential rules of UNO, along with interactive prompts and feedback to make the game engaging in a terminal environment.

## Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Game Rules](#game-rules)
- [Features](#features)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Authors](#authors)
- [Acknowledgments](#acknowledgments)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Har-Var/UNO-Command-Line.git
   cd UNO-Command-Line
   ```
2. Ensure you have Python 3.x installed.
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. For the Initial Run, Clear up the folder `data/reports/`.
5. Copy the report template from `data/report_template/uno_winners.csv` to `data/reports/uno_winners.csv`

## Usage
Run the game with:
```bash
python run_game.py
```

## Game Rules
1. Rules are same as the original UNO game (with 108 cards). See here - [UNO Rules](https://www.unorules.com/)
2. Players take turns playing a card that matches the top card on the discard pile by color, number, or symbol.
3. Special action cards (Reverse, Skip, Draw Two, Wild, and Wild Draw Four) can change the flow of the game.
4. The first player to discard all their cards wins the game.

## Features
- Player can decide on the number of opponents and the number of cards in initial hand.
- Complete implementation of UNO rules, including action and wild cards.
- Interactive prompts to guide players through each turn.
- Basic AI opponents for a challenging solo play experience.
- Game history and statistics are recorded in a CSV file.
- Shows a list of available moves from player's hand based on the Live Card (i.e. card on the top of the table deck)

## Project Structure
- `run_game.py`: Main script that initializes and runs the game.
- `engine/`: Contains helper scripts that manage various aspects of the game.
  - `game_management.py`: Sets up the game environment, manages turns, and checks for the end conditions.
  - `movements.py`: Manages card movements across players’ hands, the table deck, and the folded deck.
  - `printing_functions.py`: Handles display functions such as showing the welcome screen, game over message, player hands, the current "livecard," and other prompts.
- `data/reports/uno_winners.csv`: Stores the log of each game’s winner, including the winning card and total cards played.

## Contributing
Contributions are welcome! Please submit a pull request with any improvements.

## License
This project is licensed under the MIT License.

## Authors
- [Har-Var](https://github.com/Har-Var)

## Acknowledgments
Thanks to the creators of UNO for inspiring this project and to everyone who helped test and improve the game.
