from .src import TerminalInteractions

def quit_actions():
    print("Quitting app")
    quit()


def main():
    print('Hello, World!')
    interactions = TerminalInteractions()
    interactions.assign_quit_action(quit_actions)


if __name__ == '__main__':
    main()