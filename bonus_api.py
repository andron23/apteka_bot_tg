import requests
import json

class Bonus(object):
    def __init__(self):
        self.sign_in = requests.post('https://bonus.rarus-online.com:88/sign_in', headers = {'Content-Type': 'application/json;charset:UTF-8'}, json = {
            "login": "2b1601u0",
            "password": "954885eb725a09a357739eb94851f0e5c59b6c31",
            "role": "organization"
                                                                                                                                                        })

        self.token = self.sign_in.json()['token']

    def check_balance(self, phone): 
        self.card_info = requests.get('https://bonus.rarus-online.com:88/organization/card?phone={}'.format(phone), headers = {
            'Content-Type': 'application/json;charset:UTF-8', 
            'token': self.token})

        self.balance = self.card_info.json()['cards'][0]['actual_balance']
        return(self.balance)

    def update_user_info(self, id, key, value): 
        requests.post('https://bonus.rarus-online.com:88/organization/user/{}'.format(id), 
            headers = {'Content-Type': 'application/json;charset:UTF-8', 'token': self.token}, 
            json = {key: value})

    def get_user_id(self, card):
        self.card_info = requests.get('https://bonus.rarus-online.com:88/organization/card?barcode={}'.format(card), headers = {
            'Content-Type': 'application/json;charset:UTF-8',
            'token': self.token})
        self.id = self.card_info.json()['cards'][0]['user_id']    
        return(self.id)           