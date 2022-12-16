import sys
import curses
import threading
from utils import Menu, config_update, add_to_logs, buy
from csgo_market_api import CSGOMarket
just_the_interface = True


# main function, called via wrapper to prevent from messing up the terminal
def main(stdscr):
    # generating variables from the config file
    api_key, objs = config_update()

    # setting up objects for later
    active_menu = Menu(stdscr, 'Main')
    rapira = CSGOMarket(api_key)
    get_balance = rapira.get_money()
    active_menu.lines[1] = 'API-key: ' + str(api_key)
    active_menu.lines[2] = 'Balance: {} {}'.format(
        get_balance['money'],
        get_balance['currency']
    )

    # setting up a new thread for sending buy requests
    if not just_the_interface:
        stop_threads = False
        buyer = threading.Thread(target=buy, args=(
                                       objs, rapira, active_menu,
                                       lambda: stop_threads
                                    ), daemon=True)
        buyer.start()
        add_to_logs('Program Started')
    for x in range(50):
        add_to_logs(x)

    # infinite loop, main body of the script
    while True:
        active_menu.update()
        key = stdscr.getch()
        if key == ord('q'):
            stop_threads = True
            break
        # re-refreshing the config
        if key == ord('r') and not just_the_interface:
            api_key, objs = config_update()
            buyer = threading.Thread(target=buy, args=(
                                         objs, rapira, active_menu,
                                         lambda: stop_threads
                                     ), daemon=True)
            buyer.start()
        # updating the current menu don't ask me why this way
        else:
            x = active_menu.key_handler(key)
            if x is not False:
                active_menu = x
    if not just_the_interface:
        buyer.join()
    sys.exit()


if __name__ == '__main__':
    curses.wrapper(main)