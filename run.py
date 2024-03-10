from blessed import Terminal
from collections import namedtuple
from random import randint
import time
import os

# Related third-party imports
import gspread
from google.oauth2.service_account import Credentials

# Local application imports
import pyfiglet
from colorama import Fore, Style



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
direction = Point(1, 0)  # Initially move to the right
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
    direction = Point(1, 0)  # Initially move to the right
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
            print(term.on_green(' '), end='')

def draw_food():
    """
    Draw the food item on the terminal.
    """
    with term.location(food.x, food.y):
        print(term.on_pink(' '), end='')

def check_collision_with_wall():
    """
    Check if the snake has collided with the wall.
    """
    head = snake[-1]
    return head.x <= 0 or head.x >= term.width - 1 or head.y <= 0 or head.y >= term.height - 1

def check_collision_with_self():
    """
    Check if the snake has collided with itself.
    """
    head = snake[-1]
    return head in snake[:-1]

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
        print("\033[1m{:<15}{:<15}{:<15}\033[0m".format("Rank", "Name", "Score"))
        for idx, (rank, name, score) in enumerate(scores[:10], 1):
            print("{:<15} \033[32m{:<15}\033[0m \033[93m{:<15}\033[0m".format(rank, name, score))
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
    sorted_leaderboard = sorted(leaderboard, key=lambda x: x[1], reverse=True)
    if len(sorted_leaderboard) < 10:
        return True
    lowest_high_score = sorted_leaderboard[-1][1]
    
    if score > lowest_high_score:
        player_name = input("Congratulations! You made it to the scoreboard! Enter your name: ")
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
       "SNAKE GAME",font="eftitalic",))
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
    
    input(Style.RESET_ALL +"\n \033[1m Press Enter to return to the main menu...\033[0m")
    print("You entered:", input())
    main()
def main():
    """
    Welcome message and main menu.
    """
    clear()
    print("\n \033[1m WELCOME TO... \033[0m \n")
    print(
    pyfiglet.figlet_format(
       "SNAKE GAME",font="ogre",))
    print (Fore.YELLOW +"""\033[1m
The exciting classic arcade game where players control a snake moving around a grid.\n
The goal is to eat food pellets to grow longer while avoiding obstacles and the snake's own tail.\n 
It's a simple yet addictive game that challenges players' reflexes and strategy.\033[0m""")
    print (Style.RESET_ALL +"""\033[1m
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
                print("""\033[1m
Thank you for visiting 'Snake Game'!
\n See you next time!\n \033[0m""")
                
            input("\033[1m If you have changed your mind simply click'Run Program'again.\033[0m")
            break
        except ValueError:
            print("Invalid entry. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()