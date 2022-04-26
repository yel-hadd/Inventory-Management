from http import client
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
import re
from collections import OrderedDict
from pymongo import MongoClient

class AdminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AdminApp(App):
    def build(self):
        return AdminWindow()

    def get_users():
        client = MongoClient()
        db = client.pos
        users = db.users
        _users = OrderedDict(
            first_names = {},
            last_names = {},
            user_names = {},
            passwords = {},
            designations = {}
        )

        first_names = []
        last_names = []
        user_names = []
        passwords = []
        designations = []

        for user in users.find():
            first_names.append(user['first_name'])
            last_names.append(user['last_name'])
            user_names.append(user['user_name'])
            passwords.append(user['password'])
            designations.append(user['designation'])

        for c, v in enumerate(first_names):
            _users['first_names'][c] = first_names[c]
            _users['last_names'][c] = last_names[c]
            _users['user_names'][c] = user_names[c]
            _users['passwords'][c] = passwords[c]
            _users['designations'][c] = designations[c]

        return _users

    def get_products():
        client = MongoClient()
        db = client.pos
        users = db.users
        _users = OrderedDict(
            first_names = {},
            last_names = {},
            user_names = {},
            passwords = {},
            designations = {}
        )

        first_names = []
        last_names = []
        user_names = []
        passwords = []
        designations = []

        for user in users.find():
            first_names.append(user['first_name'])
            last_names.append(user['last_name'])
            user_names.append(user['user_name'])
            passwords.append(user['password'])
            designations.append(user['designation'])

        for c, v in enumerate(first_names):
            _users['first_names'][c] = first_names[c]
            _users['last_names'][c] = last_names[c]
            _users['user_names'][c] = user_names[c]
            _users['passwords'][c] = passwords[c]
            _users['designations'][c] = designations[c]

        return _users


if __name__=="__main__":
    aa = AdminApp()
    aa.run()