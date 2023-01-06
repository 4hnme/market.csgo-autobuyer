import time
import pyfiglet
import curses

stop_threads = False
# declaring array to store menu's text
menus = {
    'Main': [
        'How to use',
        '1 api_key goes here',
        '2 money go here',
        'List of items',
        'Settings menu',
        'History'],
    'Settings': [
        'Go back',
        'Delay between eash buy request: ',
        'Maximal amount of log entries on screen: ',
        'Show titles in that shitty font: '],
    'Logs': ['Go back'],
    'List': [],
    'Hotkeys': [
        'Go back',
        'j / d - moving down one line / to the bottom',
        'k / u - moving up one line / to the top',
        'h, l - altering a setting',
        'space, enter - select a menu',
        'backspace - returning to the main menu',
        'r - refreshing the config (does not modify the file)'
    ]
    }

# keeping everything in one dictionary
# Structure: 'num' = [minimal_value, current_value, maximal_value, step]
settings_values = {
    '1': [0.1, 1, 10, 1],
    '2': [0, 20, 30, 10],
    '3': [0, 1, 1, 1]
}
attachable = (1, 2, 3)


# updating userconfig. Does not affect the config file
def config_update():
    menus['List'] = ['Go back']
    with open(r'config', mode='r', encoding='utf-8') as f:
        data = f.readlines()
        for index in range(len(data)):
            line = data[index]
            data[index] = line.strip(' ').strip('\n')
        key = data[0][data[0].find('=')+1:]
        item_names = data[1][data[1].find('=')+1:].split(',')
        item_prices = data[2][data[2].find('=')+1:].split(',')
        currency = data[3][data[3].find('=')+1:]
        if currency == 'RUB':
            denominator = 100
        else:
            denominator = 1000
        items = []
        for index in range(len(item_names)):
            new_name = item_names[index].strip(' ')
            new_price = int(item_prices[index].strip(' '))
            new_item = mItem(new_name, new_price)
            items.append(new_item)
            menus['List'].append(
                '{}: {} {}'.format(new_name, new_price/denominator, currency)
            )
    return key, items


# class for displaying the menu
class Menu:
    def __init__(self, stdscr, title):
        self.name = title
        self.offset = 0
        self.max_offset = 0
        if settings_values['3'][1] == 1:
            self.title = pyfiglet.figlet_format(title)
        else:
            self.title = title + '\n'*2
        self.lines = menus[title]
        self.stdscr = stdscr
        self.cursor = 0
        self.height = len(self.lines)
        if self.name == 'Settings':
            for i in attachable:
                attach_line(i)

# updating the screen
    def update(self):
        self.stdscr.clear()
        self.stdscr.addstr(self.title)
        self.lines = menus[self.name]
        self.height = len(self.lines)
        if self.name == 'Logs':
            self.max_offset = self.height - settings_values['2'][1]
            if self.max_offset > 0:
                self.height = settings_values['2'][1]
        # going through every line without losing the index
        for x in range(self.offset, self.height + self.offset):
            # checking which line should be highlited
            if x == self.cursor:
                attr = curses.A_REVERSE
            else:
                attr = curses.A_DIM
            # putting the line on the screen. Goes in try because curses
            try:
                self.stdscr.addstr(self.lines[x] + '\n', attr)
            except Exception:
                self.stdscr.addstr('fuck\n')
                # pass

# function for handling key inputs
    def key_handler(self, key):
        # moving cursor up
        if key == ord('k') or key == 259:
            if self.cursor > self.offset:
                self.cursor -= 1
            elif self.offset > 0:
                self.offset -= 1
                self.cursor -= 1
        # moving cursor down
        if key == ord('j') or key == 258:
            if self.cursor < self.height + self.offset - 1:
                self.cursor += 1
            elif self.name == 'Logs' and self.offset < self.max_offset:
                self.offset += 1
                self.cursor += 1
        if key == ord('h') or key == ord('l') or key == 260 or key == 261:
            if self.name == 'Settings' and self.cursor in attachable:
                adjust_line(key, self.cursor)
        # making navigating logs this easier
        if key == ord('u'):
            self.offset = 0
            self.cursor = 0
        if key == ord('d'):
            self.cursor = len(self.lines) - 1
            self.offset = self.max_offset
        # making quick exit to main meny
        if (key == 263 or key == 8) and self.name != 'Main':
            new_menu = Menu(self.stdscr, 'Main')
            return new_menu
        # switching menus
        if key == ord(' ') or key == 10:
            if self.name == 'Main':
                if self.cursor == 0:
                    new_menu = Menu(self.stdscr, 'Hotkeys')
                    return new_menu
                if self.cursor == 3:
                    new_menu = Menu(self.stdscr, 'List')
                    return new_menu
                elif self.cursor == 4:
                    new_menu = Menu(self.stdscr, 'Settings')
                    return new_menu
                elif self.cursor == 5:
                    new_menu = Menu(self.stdscr, 'Logs')
                    return new_menu
            elif self.cursor == 0:
                new_menu = Menu(self.stdscr, 'Main')
                return new_menu
        return False


# actual working settings. It sucks
def adjust_line(key, cursor):
    # j is 104, h is 108 -> 0, 1 -> -0, 2 -> -1, 1
    if key > 200:
        modifier = (key // 261) * 2 - 1
    else:
        modifier = (key // 106) * 2 - 1
    # changing the value keeping it within set boundaries
    temp_values = settings_values[str(cursor)]
    temp_values[1] = round(temp_values[1] + temp_values[3] * modifier)
    if temp_values[1] < temp_values[0]:
        temp_values[1] = temp_values[0]
    elif temp_values[1] > temp_values[2]:
        temp_values[1] = temp_values[2]
    settings_values[str(cursor)] = temp_values
    # adding the visual indication to the setting
    attach_line(cursor)


# attaching a line to the settings
def attach_line(num):
    # generating visual indication of the value withing it's range
    temp_values = settings_values[str(num)]
    vertical_lines = ''
    total_steps = temp_values[2] // temp_values[3]
    complete_steps = temp_values[1] // temp_values[3]
    vertical_lines = '#'*round(complete_steps) + '.'*round(total_steps - complete_steps)
    line = '[{}]{}'.format(
        vertical_lines, temp_values[1]
    )
    temp_line = menus['Settings'][num]
    temp_line = temp_line[0:temp_line.index(':')+2]
    temp_line += line
    menus['Settings'][num] = temp_line


# function to quickly add things to logs
def add_to_logs(msg):
    t = time.localtime()
    text = '[{}]: {}'.format(time.strftime('%H:%M:%S', t), msg)
    # if len(menus['Logs']) > settings_values['2'][1]:
    #     menus['Logs'].pop(1)
    menus['Logs'].append(text)


# class for storing items
class mItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price


# sending buy reques for every item in object list
def buy(items, rapira, menu, stop):
    temp = {}
    global stop_threads
    while True:
        if stop():
            break
        get_balance = rapira.get_money()
        balance1 = get_balance['money']
        menus['Main'][2] = 'Balance: {} {}'.format(
            balance1, get_balance['currency']
        )
        # if menu.title == 'Main':
        #     menu.lines[2] = 'Balance: ' + str(balance1) + ' ' + currency
        # else:
        #     menus['Main'][2] = 'Balance: ' + str(balance1) + ' ' + currency
        for x in items:
            try:
                temp = rapira.buy(x.name, x.price)
            except Exception:
                add_to_logs(
                    'Technical work. The bot will continue running soon...'
                )
                time.sleep(35)
            if temp['success'] is True:
                # check the cost of bought item
                d_balance = -rapira.get_money()['money'] + balance1
                add_to_logs(
                    'Bought {} for {:.2f}{}'.format(
                        x.name, d_balance, get_balance['currency']
                    )
                )
            time.sleep(0.5)
        time.sleep(settings_values['1'][1])
