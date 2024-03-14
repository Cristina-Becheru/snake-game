from blessed import Terminal
from collections import namedtuple
from random import randint
import gspread
from google.oauth2.service_account import Credentials
import pyfiglet
from colorama import Fore, Style
import os

# Google Sheets Setup
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('leaderboard')

# Snake Game Variables
Point = namedtuple('Point', ['x', 'y'])
snake = []
food = None
direction = Point(1, 0)
score = 0
base_speed = 0.1
speed_increase_factor = 0.001

term = Terminal()


def clear():
    """
    Clears the terminal screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def initialize_game():
    """
    Initialize the game state.
    """
    global snake, food, direction, score
    snake = [Point(6, 6), Point(6, 7), Point(6, 8), Point(6, 9)]
    food = generate_food()
    direction = Point(1, 0)
    score = 0


def generate_food():
    """
    Generate a new food item at a random location on the screen.
    """
    width, height = term.width - 1, term.height - 1
    while True:
        x, y = randint(1, width), randint(1, height)
        new_food = Point(x, y)
        if new_food not in snake:
            return new_food


def update_snake_position():
    """
    Update the snake's position based on the specified direction.
    """
    global snake, food, score
    head = snake[-1]
    next_head = Point(head.x + direction.x, head.y + direction.y)
    snake.append(next_head)
    if next_head == food:
        food = generate_food()
        score += 10
    else:
        snake.pop(0)


def draw_snake():
    """
    Draw the snake on the terminal.
    """
    for segment in snake:
        with term.location(segment.x, segment.y):
            print(term.on_yellow(' '), end='')


def draw_food():
    """
    Draw the food item on the terminal.
    """
    with term.location(food.x, food.y):
        print(term.on_pink(' '), end='')


def check_collision():
    """
    Check if the snake has collided with the wall or itself.
    """
    head = snake[-1]
    return (head.x <= 0 or head.x >= term.width - 1 or
            head.y <= 0 or head.y >= term.height - 1 or
            head in snake[:-1])


def start_game():
    """
    Main game loop with restart feature if the snake hits the walls.
    """
    global base_speed, speed_increase_factor, score, direction

    while True:
        initialize_game()

        with term.cbreak(), term.hidden_cursor():
            while True:
                speed = max(0.01, base_speed - speed_increase_factor * score)
                key = term.inkey(timeout=speed)
                if key.is_sequence:
                    if key.name == "KEY_UP" and direction != Point(0, 1):
                        direction = Point(0, -1)
                    elif key.name == "KEY_DOWN" and direction != Point(0, -1):
                        direction = Point(0, 1)
                    elif key.name == "KEY_LEFT" and direction != Point(1, 0):
                        direction = Point(-1, 0)
                    elif key.name == "KEY_RIGHT" and direction != Point(-1, 0):
                        direction = Point(1, 0)

                update_snake_position()

                print(term.home + term.clear)
                draw_snake()
                draw_food()

                print(f"Score: {score}")

                if check_collision():
                    print(Fore.RED + "\033[1mGame Over!\033[0m")
                    break

            if not play_again():
                break

        term.clear()
        term.move_yx(0, 0)


def get_scoreboard():
    """
    Retrieves scoreboard data from a Google Sheets spreadsheet.
    """
    scoreboard = SHEET.worksheet("leaderboard")
    data = scoreboard.get_all_values()

    return data


def show_leaderboard():
    """
    Displays the leaderboard from Google Sheets.
    """
    clear()
    scores = get_scoreboard()
    print("\033[1m \033[4m Scoreboard (Top 10):\033[0m")
    if scores:
        print("\033[1m{:<15}{:<15}{:<15}\033[0m"
              .format("Rank", "Name", "Score"))
        for idx, (rank, name, score) in enumerate(scores[:10], 1):
            print("{:<15} \033[32m{:<15}\033[0m \033[93m{:<15}\033[0m"
                  .format(rank, name, score))
    else:
        print("No scores available.")
    input(" \033[1m \nPress 'Enter' to return to the main menu...\033[0m")
    main()


def update_score(name, score):
    """
    Update the player's score in the Google Sheets scoreboard.
    """
    try:
        sheet = GSPREAD_CLIENT.open('leaderboard')
        scoreboard = sheet.worksheet('leaderboard')
        scoreboard.append_row([name, score])
        print("Score updated successfully!")

    except Exception as e:
        print("Error occurred while updating score:", e)


def is_high_score(score, leaderboard):
    """
    Checks if the player's score qualifies as a high score.
    """
    sorted_leaderboard = sorted(leaderboard, key=lambda x: x[1], reverse=False)
    if len(sorted_leaderboard) < 10:
        return False
    lowest_high_score = sorted_leaderboard[-1][1]

    if score is not None and score > lowest_high_score and score != 0:
        player_name = input("Congratulations! You made it to the scoreboard!"
                            "Enter your name: ")
        return True, player_name
    else:
        return False, None


def show_instructions():
    """
    Display game instructions.
    """
    clear()

    print(

     pyfiglet.figlet_format(
       "SNAKE GAME", font="eftitalic",))
    print(Fore.YELLOW + """\033[1m
             +-++-++-++-++-++-++-++-++-++-++-++-+
             |I||N||S||T||R||U||C||T||I||O||N||S|
             +-++-++-++-++-++-++-++-++-++-++-++-+
\033[0m""")
    print(""" \033[1m
    - Use the arrow keys to control the snake's direction.
    - Navigate the snake to eat food to grow longer.
    - Avoid collisions with the walls or the snake's own body.\033[0m""")
    print(Fore.YELLOW + "\033[1m \nEnjoy playing Snake Game!\033[0m")
    input(Style.RESET_ALL + "\n" +
          "\033[1mPress Enter to return to the main menu...\033[0m")

    main()


def play_again():
    while True:
        choice = input(Fore.RED + "\033[1m \nDo you want to play again?"
                       "(yes/no): \033[0m").lower().strip()
        if choice == 'yes':
            os.system('cls')
            return True
        elif choice == 'no':
            clear()
            print(Fore.YELLOW + "\033[1mThank you for playing!\n"
                  "See you next time!\033[0m")
            exit()


def main():
    """
    Describing message and main menu.
    """
    clear()
    print(
        pyfiglet.figlet_format(
            "SNAKE GAME", font="ogre",))
    print("\033[1;33mThe exciting classic arcade game where players control\n"
          "a snake moving around a grid.\n"
          "It's a simple yet addictive game that challenges players'\n"
          "reflexes and strategy.\033[0m")

    print(Style.RESET_ALL + """\033[1m
Choose an option below:\n
    1) Start\n
    2) Scoreboard\n
    3) Instructions\n
    4) Quit
        \033[0m""")
    while True:
        try:
            choice = int(input("\033[1m Enter your choice (1-4): \033[0m"))
            if choice == 1:
                start_game()
            elif choice == 2:
                show_leaderboard()
            elif choice == 3:
                show_instructions()
            elif choice == 4:
                clear()
            print(Fore.YELLOW + "\033[1mThank you for visiting 'Snake Game'!\n"
                  "See you next time!\033[0m")
            input(Fore.RED + "\033[1mIf you have changed your mind, "
                  "simply click 'Run Program' again!\033[0m")
            break

        except ValueError:
            print("ERROR: Invalid Input! "
                  "Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()
