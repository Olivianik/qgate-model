import datetime
import uuid

from generator.base import Base
from faker import Faker
from faker.providers import internet, phone_number
from generator.basic_party import BasicParty

import faker.providers
import numpy


class BasicEvent(Base):

    NAME= "06-basic-event"

    def __init__(self, path, gmodel):
        super().__init__(path, gmodel, BasicEvent.NAME)
        self.fake=Faker(['en_US'])
        self.fake.add_provider(internet)
        self.fake.add_provider(phone_number)

        self.event_inits = {"access": ["login", "logout"]}

        # list of groups and group probability
        #   [[group, ...], [group probability, ...]]
        self.event_groups=[["user profile", "product", "offer"],
                           [0.01, 0.19, 0.8]]

        # list of categorie and probabilities for group
        #   "group": [["category", ...], [category probability, ...]]
        self.event_categories = {"user profile": [["income", "expences", "address", "email", "phone", "children"],
                                                  [0.1, 0.1, 0.2, 0.2, 0.2, 0.2]],
                     "product": [["contract detail", "account detail", "legal conditions","sanctions"],
                                 [0.35, 0.55, 0.05, 0.05]],
                     "offer": [["product list", "service list", "legal conditions", "sanctions"],
                               [0.45, 0.45, 0.05, 0.05]]}

        # list of action and probabilities for group/category
        #   "group/category": [["action", ...], [action probability, ...]]
        self.event_actions = {"user profile/income": [["show", "edit"], [0.999, 0.001]],
                        "user profile/expences": [["show", "edit"], [0.9995, 0.0005]],
                        "user profile/address": [["show", "edit"], [0.999, 0.001]],
                        "user profile/email": [["show", "edit"], [0.995, 0.005]],
                        "user profile/phone": [["show", "edit"], [0.998, 0.002]],
                        "user profile/children": [["show", "edit"], [0.99995, 0.00005]],
                        "product/contract detail": [["show", "edit"], [0.99, 0.01]],
                        "product/account detail": [["show", "edit"], [0.99, 0.01]],
                        "product/legal conditions": [["show", "edit"], [0.9999, 0.0001]],
                        "product/sanctions": [["show", "edit"], [0.9999, 0.0001]],
                        "offer/product list": [["show"], [1]],
                        "offer/service list": [["show"], [1]],
                        "offer/legal conditions": [["show"], [1]],
                        "offer/sanctions": [["show"], [1]]}


    @property
    def Name(self):
        return BasicEvent.NAME

    def generate(self, count):


        # reference to the data from BasicParty
        parties = self.gmodel[BasicParty.NAME]

        # iteration cross all parties
        for party in parties:

            # add new model
            model = self.model_item()

            # "name": "event-id",
            model['event-id']=str(uuid.uuid4())

            # "name": "party-id",
            model['party-id']=party['party-id']

            # only 3 months back history
            # max 0-2 bandl of events per day
            # mix of actions

            # TODO: generate amount of fundles for last 3 months

            # generate bundle (with random amount of iterations)
            for i in range(5):
                # TODO: add login

                # "name": "event-group",
                group = self.rnd_choose(self.event_groups[0], self.event_groups[1])
                model['event-group'] = group

                # "name": "event-category",
                category=self.rnd_choose(self.event_categories[group][0], self.event_categories[group][1])
                model['event-category'] = category

                # "name": "event-action",
                group_category_name=str.format("{0}/{1}", group,category)
                model['event-action'] = self.rnd_choose(self.event_actions[group_category_name][0], self.event_actions[group_category_name][1])

                # "name": "event-detail",
                # "name": "event-date",

            # "name": "record-date"
            model['record-date']=self.gmodel["NOW"]

            self.model.append(model)
