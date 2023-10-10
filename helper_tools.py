import os


def cls():
    '''
        Clears the command line window for a better and decluttered
        output of our program.
    '''
    os.system('cls' if os.name == 'nt' else 'clear')


def hit_enter():
    '''
        Asks the user to hit enter to proceed.
    '''
    input("\nPlease hit [Enter] to continue.")
