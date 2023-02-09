# market.csgo.com autobuyer bot
a bot for market.csgo.com that automatically buys items for specific price or lower

## installation 
1. clone this repository:
  ```shell
  git clone https://github.com/4hnme/market.csgo-autobuyer
  ```
## dependencies
  * interface is based on python `curses` library
  > Note: if you are trying to run this on windows, you'll need to install `windows-curses` additionally
  * fonts are made with python `pyfiglet` library 
  > Note: this takes a lot of unnecessary space, feel free to cut it out entirely
  * requests to market.csgo.com are made with python `csgo_market_api` library 

## usage

### configuration
  modify your `config` file according to these rules:
  * create your api key [here](https://market.csgo.com/docs-v2) and put it into your config file
  * item names must be taken directly from market.csgo.com urls
    > `https://market.csgo.com/item/520025252-0-Operation%20Breakout%20Weapon%20Case/` turns into `Operation Breakout Weapon Case`
  * list of items could be placed anywhere in the config file as long as all items follow the "Name, price" pattern and go after the "Items:" line
  * depending on given currency, prices will be divided either by 100 for `RUB` or 1000 for `USD`:
    > `8000` will turn into `80.00 RUB` or `8.00 USD`

    > Note: USD functionality remains untested, if you are stuck with using it proceed with caution

### how to use

  * run the `main.py` file via your command line:
  ```
  python3 main.py
  ```

### controls
  * j(↓) / d - moving down one line / to the bottom
  * k(↑) / u - moving up one line / to the top
  * h(←), l(→) - altering a setting
  * space, enter - select a menu
  * backspace - returning to the main menu
  * p - pause / restart the bot
  * r - refreshing the config (does not modify the file)
  * q - exit the program
  
## применение для людей, проживающих на территориях РФ / РБ:
  поскольку пополнить счёт на своём аккаунте в Steam для некоторых людей стало проблематично или вовсе невозможно, этот скрипт может использоваться для обхода региональных ограничений:
  * находишь предмет, средняя цена которого ниже или примерно равна цены продажи на торговой площадке Steam;
  * вносишь один или несколько таких предметов в `config` и оставляешь скрипт работать в фоне;
  * забираешь купленные предметы с сайта к себе в инвентарь и выставляешь их на торговой площадке Steam.

  этот способ занимает куда больше времени, чем классический "закинуть в тенге", но разница в ценах на market.csgo.com и торговой площадке иногда может компенсировать комиссии при переводе или вообще вывести в плюс
