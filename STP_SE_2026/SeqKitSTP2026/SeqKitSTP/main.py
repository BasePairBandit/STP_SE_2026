import logging.config
from SeqKitSTP.settings import LOGGING_CONFIG
from SeqKitSTP.CLI.sequence_menu import run_seq_menu
from SeqKitSTP.CLI.api_menu import run_api_menu


def main():
    while True:
        print(r"""
 ____             _  ___ _   ____   ___ ____   __   
/ ___|  ___  __ _| |/ (_) |_|___ \ / _ \___ \ / /_  
\___ \ / _ \/ _` | ' /| | __| __) | | | |__) | '_ \ 
 ___) |  __/ (_| | . \| | |_ / __/| |_| / __/| (_) |
|____/ \___|\__, |_|\_\_|\__|_____|\___/_____|\___/ 
               |_|                                  

        Select an option:
        1. Sequence tools
        2. API lookup
        3. Exit
        """)

        choice = input("Enter your choice: ")

        if choice == "1":
            run_seq_menu()

        elif choice == "2":
            run_api_menu()

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    logging.config.dictConfig(LOGGING_CONFIG)
    main()