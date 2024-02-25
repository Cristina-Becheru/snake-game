import gspread
from google.oauth2.service_account import Credentials
import time
import random
import os

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('scoreboard')

board = SHEET.worksheet('board')

data = board.get_all_values()


def clear():
    """
    Clears the terminal screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    """
    Welcome message and main menu.
    """
    print("\nWELCOME TO...\n")
    print(
        """
+-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-+
   _____ _   _          _  ________    _____          __  __ ______ 
  / ____| \ | |   /\   | |/ /  ____|  / ____|   /\   |  \/  |  ____|
 | (___ |  \| |  /  \  | ' /| |__    | |  __   /  \  | \  / | |__   
  \___ \| . ` | / /\ \ |  < |  __|   | | |_ | / /\ \ | |\/| |  __|  
  ____) | |\  |/ ____ \| . \| |____  | |__| |/ ____ \| |  | | |____ 
 |_____/|_| \_/_/    \_\_|\_\______|  \_____/_/    \_\_|  |_|______|
+-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-+
        """
    ) 
    print ("""
Navigate a hungry snake through a maze, gobbling up food to grow longer. 
Avoid obstacles and your own tail to survive, testing reflexes and strategic thinking in this addictive classic.
Please select an option:
    1) Start
    2) Scoreboard
    3) Instructions
    4) Quit
        """)
    while True:
        try:
            choice = int(input("Enter your selection (1-4): "))
            if choice == 1:
                start_game()
            elif choice == 2:
                get_scoreboard()
            elif choice == 3:
                show_instructions()
            elif choice == 4:
                print("""
Thank you for visiting 'Snake Game'!
See you next time!
If you have changed your mind, simply click 'Run Program' again.
""")
                break  
            else:
                raise ValueError
        except ValueError: 
            print("Invalid input, please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()