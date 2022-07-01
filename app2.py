# import os
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_restx import Api, Resource
# import json
# from werkzeug.datastructures import FileStorage
#
# basedir = os.path.abspath(os.path.dirname(__file__))
#
# app = Flask(__name__)
#
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#
# db = SQLAlchemy(app)
#
#
# def get_result_from_file(file):
#     data = json.load(file)
#
#     users = data.get('users')
#     places = data.get('places')
#     ratings = data.get('ratings')
#
#     users_dict = dict()
#     places_dict = dict()
#
#     for user in users:
#         new_user = dict()
#         for k, v in user.items():
#             new_key = 'users.' + k
#             new_user[new_key] = v
#         users_dict[user['userID']] = new_user
#     for place in places:
#         new_place = dict()
#         for k, v in place.items():
#             new_key = 'places.' + k
#             new_place[new_key] = v
#         places_dict[place['placeID']] = new_place
#
#     results = list()
#
#     for rating in ratings:
#         result = dict()
#         userID = rating['userID']
#         placeID = rating['placeID']
#         new_rating = dict()
#         for k, v in rating.items():
#             new_key = 'ratings.' + k
#             new_rating[new_key] = v
#         result.update(new_rating)
#         user = users_dict.get(userID)
#         place = places_dict.get(placeID)
#         if user and place:
#             for k, v in user.items():
#                 if v == '?' or v == 'none':
#                     user[k] = "N/A"
#             result.update(user)
#
#             for k, v in place.items():
#                 if v == '?' or v == 'none':
#                     place[k] = "N/A"
#         result.update(place)
#         results.append(result)
#     return results
#
#
# api = Api(app, version="1.0", title="API", description="A simple API", )
# upload_parser = api.parser()
# upload_parser.add_argument('file', location='files', type=FileStorage, required=True)
#
# @api.route("/ratings")
# class Rating(Resource):
#
#     def post(self):
#         args = upload_parser.parse_args()
#         uploaded_file = args['file']
#         results = get_result_from_file(uploaded_file)
#         return results, 201
#
#
# app.run(debug=True)

# import re
#
# pattern = '^a...s$'
# test_string = 'abyss1'
# result = re.match(pattern, test_string)
# b = 1

# import json
# import pandas as pd
# data = json.load(open('sample_data.json'))
# users_df = pd.DataFrame(data['users'])
# places_df = pd.DataFrame(data['places'])
# ratings = data.get('ratings')
# results = []
# for rating in ratings:
#     user = users_df[users_df.userID == rating['userID']]
#     place = places_df[places_df.placeID == rating['placeID']]
#     if not user.empty and not place.empty:
#         results.append(
#             {
#                 "users.userID": user.userID.values[0],
#                 "users.hijos": user.hijos.values[0] if user.hijos.values[0] != '?' or user.hijos.values[0] != 'none' else 'N/A',
#                 "users.budget": user.budget.values[0] if user.budget.values[0] != '?' or user.budget.values[0] != 'none' else 'N/A',
#                 'ratings.placeID': rating['placeID'],
#                 "ratings.rating": rating['rating'] if rating['rating'] != '?' or rating['rating'] != 'none' else 'N/A',
#                 "ratings.food_rating": rating['food_rating'] if rating['food_rating'] != '?' or rating['food_rating'] != 'none' else 'N/A',
#                 "ratings.service_rating": rating['service_rating'] if rating['service_rating'] != '?' or rating['service_rating'] != 'none' else 'N/A',
#                 "places.name": place.name.values[0] if place.name.values[0] != '?' or place.name.values[0] != 'none' else 'N/A',
#             }
#         )
# user = users_df[users_df.userID =='U100000']
# if user.empty:
#     print("Haha")
# b = 1


class Elf:
    def nall_nin(self):
        print('Elf says: Calling the Overlord ...')


class Dwarf:
    def estver_narto(self):
        print('Dwarf says: Calling the Overlord ...')


class Human:
    def ring_mig(self):
        print('Human says: Calling the Overlord ...')


class ElfAdapter:
    def __init__(self, elf):
        self.elf = elf

    def call_me(self):
        self.elf.nall_nin()


class DwarfAdapter:
    def __init__(self, dwarf):
        self.dwarf = dwarf

    def call_me(self):
        self.dwarf.estver_narto()


class HumanAdapter:
    def __init__(self, human):
        self.human = human

    def call_me(self):
        self.human.ring_mig()


# minions = [Elf(), Dwarf(), Human()]
# for minion in minions:
#     if isinstance(minion, Elf):
#         minion.nall_nin()
#     elif isinstance(minion, Dwarf):
#         minion.estver_narto()
#     else:
#         minion.ring_mig()
#
# minions = [ElfAdapter(Elf()), DwarfAdapter(Dwarf()), HumanAdapter(Human())]
# for minion in minions:
#     minion.call_me()

class Observer:
    def update(self, obj, *args, **kwargs):
        raise NotImplementedError


class Observable:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observer(self, *args, **kwargs):
        for observer in self._observers:
            observer.update(self, *args, **kwargs)


class MinionAdapter(Observable):
    _initialised = False

    def __init__(self, minion, **adapted_methods):
        self.minion = minion

        for key, value in adapted_methods.items():
            func = getattr(self.minion, value)
            self.__setattr__(key, func)

        self._initialised = True

    def __getattr__(self, attr):
        return getattr(self.minion, attr)

    def __setattr__(self, key, value):
        if not self._initialised:
            super().__setattr__(key, value)
        else:
            setattr(self.minion, key, value)
            self.notify_observer(key=key, value=value)


minion_adapters = [
    MinionAdapter(Elf(), call_me='nall_nin'),
    MinionAdapter(Dwarf(), call_me='estver_narto'),
    MinionAdapter(Human(), call_me='ring_mig'),
]


# for adapter in minion_adapters:
#     adapter.call_me()
#     print(adapter.__dict__)

# elf_adapter = minion_adapters[0]
# minion_adapters[0].name = 'Elrond'
# print(f'Name for Adapter: {elf_adapter.name}')
# print(f'Name for Minion: {elf_adapter.minion.name}')


class MinionFacade:
    minion_adapters = None

    @classmethod
    def create_minions(cls):
        print('Creating minions ...')
        cls.minion_adapters = [
            MinionAdapter(Elf(), call_me='nall_nin'),
            MinionAdapter(Dwarf(), call_me='estver_narto'),
            MinionAdapter(Human(), call_me='ring_mig'),
        ]

    @classmethod
    def summon_minions(cls):
        print('Summoning minions ...')
        for adapter in cls.minion_adapters:
            adapter.call_me()

    @classmethod
    def monitor_elves(cls, observer):
        cls.minion_adapters[0].add_observer(observer)
        print('Added an observer to the Elves!')

    @classmethod
    def change_elves_name(cls, new_name):
        print('Changing the Elves name ...')
        cls.minion_adapters[0].name = new_name
        print('Added an observer to the Elves!')


# MinionFacade.create_minions()
# MinionFacade.summon_minions()

class EvilOverLord(Observer):
    def update(self, obj, *args, **kwargs):
        print('The Evil Overlord received a message!')
        print(f'Object: {obj}, Args: {args}, Kwargs: {kwargs}')


overlord = EvilOverLord()
MinionFacade.create_minions()
MinionFacade.monitor_elves(overlord)
MinionFacade.change_elves_name('Elrond')

