import time
from typing import Union

import requests


def _send_request(func):
    def wrapper(*args, **kwargs):
        url, params, timeout = func(*args, **kwargs)
        end_time = time.time() + timeout
        while True:
            response = requests.get(url, params)
            if response.status_code == 200:
                break
            if time.time() > end_time:
                if response.status_code == 502:
                    raise NoConnection('Нет соединения с серверами market.csgo.com')
                elif response.status_code == 503:
                    raise TechnicalWork('Технические работы')
            time.sleep(1)
        return response.json()
    return wrapper


class CSGOMarket:
    """https://market.csgo.com/docs-v2"""
    def __init__(self, api_key: str, timeout: int = 15):
        self.params = {'key': api_key}
        self.timeout = timeout
        self.url = 'https://market.csgo.com/api/v2/'

    # Buy/sell items
    @_send_request
    def trade_request_take(self, bot_id: Union[str, int] = None):
        api_url = self.url + 'trade-request-take'
        api_params = dict(self.params)
        if bot_id:
            api_params.update({'bot': bot_id})
        return api_url, api_params, self.timeout

    @_send_request
    def trade_request_give(self):
        api_url = self.url + 'trade-request-give'
        return api_url, self.params, self.timeout

    @_send_request
    def trade_request_give_p2p(self):
        api_url = self.url + 'trade-request-give-p2p'
        return api_url, self.params, self.timeout

    @_send_request
    def trade_request_give_p2p_all(self):
        api_url = self.url + 'trade-request-give-p2p-all'
        return api_url, self.params, self.timeout

    @_send_request
    def ping(self):
        api_url = self.url + 'ping'
        return api_url, self.params, self.timeout

    @_send_request
    def go_offline(self):
        api_url = self.url + 'go-offline'
        return api_url, self.params, self.timeout

    @_send_request
    def my_inventory(self):
        api_url = self.url + 'my-inventory'
        return api_url, self.params, self.timeout

    @_send_request
    def add_to_sale(self, item_id: Union[str, int], price: Union[str, int], currency: str = 'RUB'):
        api_url = self.url + 'add-to-sale'
        api_params = dict(self.params)
        api_params.update({'id': item_id, 'price': price, 'cur': currency})
        return api_url, api_params, self.timeout

    @_send_request
    def set_price(self, item_id: Union[str, int], price: Union[str, int], currency: str):
        api_url = self.url + 'set-price'
        api_params = dict(self.params)
        api_params.update({'item_id': item_id, 'price': price, 'cur': currency})
        return api_url, api_params, self.timeout

    @_send_request
    def remove_all_from_sale(self):
        api_url = self.url + 'remove-all-from-sale'
        return api_url, self.params, self.timeout

    @_send_request
    def items(self):
        api_url = self.url + 'items'
        return api_url, self.params, self.timeout

    @_send_request
    def trades(self, extended: bool = False):
        api_url = self.url + 'trades'
        api_params = dict(self.params)
        if extended:
            api_params.update({'extended': 1})
        return api_url, api_params, self.timeout

    @_send_request
    def buy(self, hash_name: str, price: Union[str, int], custom_id: Union[str, int] = None):
        api_url = self.url + 'buy'
        api_params = dict(self.params)
        api_params.update({'hash_name': hash_name, 'price': price})
        if custom_id:
            api_params.update({'custom_id': custom_id})
        return api_url, api_params, self.timeout

    @_send_request
    def buy_id(self, item_id: Union[str, int], price: Union[str, int], custom_id: Union[str, int] = None):
        api_url = self.url + 'buy'
        api_params = dict(self.params)
        api_params.update({'id': item_id, 'price': price})
        if custom_id:
            api_params.update({'custom_id': custom_id})
        return api_url, api_params, self.timeout

    @_send_request
    def buy_for(self, hash_name: str, price: Union[str, int], partner: Union[str, int],
                token: str, custom_id: Union[str, int] = None):
        api_url = self.url + 'buy-for'
        api_params = dict(self.params)
        api_params.update({'hash_name': hash_name, 'price': price, 'partner': partner, 'token': token})
        if custom_id:
            api_params.update({'custom_id': custom_id})
        return api_url, api_params, self.timeout

    @_send_request
    def buy_for_id(self, item_id: Union[str, int], price: Union[str, int], partner: Union[str, int],
                   token: str, custom_id: Union[str, int] = None):
        api_url = self.url + 'buy-for'
        api_params = dict(self.params)
        api_params.update({'id': item_id, 'price': price, 'partner': partner, 'token': token})
        if custom_id:
            api_params.update({'custom_id': custom_id})
        return api_url, api_params, self.timeout

    @_send_request
    def get_buy_info_by_custom_id(self, custom_id: Union[str, int]):
        api_url = self.url + 'get-buy-info-by-custom-id'
        api_params = dict(self.params)
        api_params.update({'custom_id': custom_id})
        return api_url, api_params, self.timeout

    @_send_request
    def get_list_buy_info_by_custom_id(self, custom_id_list: list):
        api_url = self.url + 'get-list-buy-info-by-custom-id'
        api_params = dict(self.params)
        for index, custom_id in enumerate(custom_id_list):
            api_params.update({f'custom_id[{index}]': custom_id})
        return api_url, api_params, self.timeout

    def history(self, date_start: Union[str, int], date_end: Union[str, int] = None):
        api_url = self.url + 'history'
        api_params = dict(self.params)
        api_params.update({'date': date_start})
        if date_end:
            api_params.update({'date_end': date_end})
        return api_url, api_params, self.timeout

    # Account actions
    @_send_request
    def get_money(self):
        api_url = self.url + 'get-money'
        return api_url, self.params, self.timeout

    @_send_request
    def go_offline(self):
        api_url = self.url + 'go-offline'
        return api_url, self.params, self.timeout

    @_send_request
    def update_inventory(self):
        api_url = self.url + 'update-inventory'
        return api_url, self.params, self.timeout

    @_send_request
    def transfer_discounts(self, to_api_key: str):
        api_url = self.url + 'transfer-discounts'
        api_params = dict(self.params)
        api_params.update({'to': to_api_key})
        return api_url, api_params, self.timeout

    @_send_request
    def get_my_steam_id(self):
        api_url = self.url + 'get-my-steam-id'
        return api_url, self.params, self.timeout

    @_send_request
    def set_pay_password(self, old_password: str, new_password: str):
        api_url = self.url + 'set-pay-password'
        api_params = dict(self.params)
        api_params.update({'old_password': old_password, 'new_password': new_password})
        return api_url, api_params, self.timeout

    @_send_request
    def money_send(self, amount: Union[str, int], to_api_key: str, pay_pass: str):
        api_url = self.url + f'money-send/{amount}/{to_api_key}'
        api_params = dict(self.params)
        api_params.update({'pay_pass': pay_pass})
        return api_url, api_params, self.timeout

    # Search items
    @_send_request
    def search_item_by_hash_name(self, hash_name: str):
        api_url = self.url + 'search-item-by-hash-name'
        api_params = dict(self.params)
        api_params.update({'hash_name': hash_name})
        return api_url, api_params, self.timeout

    @_send_request
    def search_item_by_hash_name_specific(self, hash_name: str):
        api_url = self.url + 'search-item-by-hash-name-specific'
        api_params = dict(self.params)
        api_params.update({'hash_name': hash_name})
        return api_url, api_params, self.timeout

    @_send_request
    def search_list_items_by_hash_name_all(self, list_hash_name: list):
        api_url = self.url + 'search-list-items-by-hash-name-all'
        api_params = dict(self.params)
        for index, hash_name in enumerate(list_hash_name):
            api_params.update({f'list_hash_name[{index}]': hash_name})
        return api_url, api_params, self.timeout

    @_send_request
    def get_list_items_info(self, list_hash_name: list):
        api_url = self.url + 'get-list-items-info'
        api_params = dict(self.params)
        for index, hash_name in enumerate(list_hash_name):
            api_params.update({f'list_hash_name[{index}]': hash_name})
        return api_url, api_params, self.timeout

    # Additional
    @_send_request
    def test(self):
        api_url = self.url + 'test'
        return api_url, self.params, self.timeout


class TechnicalWork(Exception):
    pass


class NoConnection(Exception):
    pass
