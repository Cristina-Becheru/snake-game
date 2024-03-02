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
SHEET = GSPREAD_CLIENT.open('leaderboard')


def clear():
    """
    Clears the terminal screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

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
        print("\033[91m No scores available.\033[0m")
    input("\nPress 'Enter' to return to the main menu...")
    main() 
def update_score(name, score):
    """
    Update the player's score in the Google Sheets scoreboard.
    """
    try:
        sheet = GSPREAD_CLIENT.open('leaderboard')
        scoreboard = sheet.worksheet('leaderboard')
        # Add a new row with the player's name and score
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
    r"""
-------------------------------------------------------------------------
|  _____ _   _          _  ________    _____          __  __ ______ 
  / ____| \ | |   /\   | |/ /  ____|  / ____|   /\   |  \/  |  ____|
 | (___ |  \| |  /  \  | ' /| |__    | |  __   /  \  | \  / | |__   
  \___ \| . ` | / /\ \ |  < |  __|   | | |_ | / /\ \ | |\/| |  __|  
  ____) | |\  |/ ____ \| . \| |____  | |__| |/ ____ \| |  | | |____ 
 |_____/|_| \_/_/    \_\_|\_\______|  \_____/_/    \_\_|  |_|______|   
---------------------------------------------------------------------------
""")
    print("""
             +-++-++-++-++-++-++-++-++-++-++-++-+
             |I||N||S||T||R||U||C||T||I||O||N||S|
             +-++-++-++-++-++-++-++-++-++-++-++-+
""")
    print("- Use the arrow keys to control the snake's direction.")
    print("- Navigate the snake to eat food to grow longer.")
    print("- Avoid collisions with the walls or the snake's own body.")
    print("\nEnjoy playing Snake Game!")
    input("\n Press Enter to return to the main menu...")
    print("You entered:",input)
    main()
def main():
    """
    Welcome message and main menu.
    """
    print("WELCOME TO...")
    print(

    r""" 
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
                show_leaderboard()
            elif choice == 3:
                show_instructions()
            elif choice == 4:
                print("""
Thank you for visiting 'Snake Game'!
See you next time!
If you have changed your mind, simply 'Enter your selection' below.
""")
                break  
            else:
                raise ValueError
        except ValueError: 
            print("Invalid input, please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()