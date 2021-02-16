import logging
from typing import List

import requests

from businness_object.rule import Rule
from custom_exception.twitter_api_exception import TwitterApiException


def is_match_save_rules(rule, saved_rules):
    matched_rule = None
    i = 0
    while matched_rule is None and i < len(saved_rules):
        if rule.expression == saved_rules[i].expression:
            matched_rule = saved_rules[i]
        i += 1
    logging.info("I found a matching rule based on expression")
    return matched_rule


class TwitterClientRule:
    __ENDPOINT_RULE = "https://api.twitter.com/2/tweets/search/stream/rules"

    def __init__(self, bearer_token):
        self.__bearer_token = bearer_token

    def add_rule(self, rule: Rule) -> Rule:
        """
        Permet d'ajouter une règle pour filtrer le flux de tweets
        :param rule: La règle à ajouter
        :type rule: Rule
        :return: la règle mise à jour de son id
        :rtype: Rule
        """
        logging.info(f'adding rule {rule}')
        # Creation des headers de la requête
        headers = {
            "Content-type": "application/json",
            "Authorization": f'Bearer {self.__bearer_token}'
        }

        # Création du corps
        body = {
            "add": [
                {"value": rule.expression,
                 "tag": rule.tag}
            ]
        }
        # Exécution de la requête
        response = requests.post(url=TwitterClientRule.__ENDPOINT_RULE
                                 , headers=headers
                                 , json=body)

        # Si la requête n'a pas aboutie correctement on lève une erreur
        if response.status_code != 201:
            raise TwitterApiException(f'Problème lors de la création de règle\n'
                                      f'{response.status_code} : {response.content}')

        # Mise  à jour de l'id de la règle avec l'id renvoyé par twitter
        rule.id = response.json()["data"][0]["id"]
        print(response.json())
        logging.info(f'rule added {rule}')
        return rule

    def add_rules(self, rules: List[Rule]) -> List[Rule]:
        """
        Permet d'ajouter plusieurs règles pour filtrer le flux de tweets
        :param rules: La règle à ajouter
        :type rules: list of Rule
        :return: les règles mise à jour de leur id
        :rtype: list of Rule
        """
        logging.info(f'adding rules {rules}')
        # Creation des headers de la requête
        headers = {
            "Content-type": "application/json",
            "Authorization": f'Bearer {self.__bearer_token}'
        }

        # Création du corps
        body = {
            "add": [{"value": rule.expression, "tag": rule.tag} for rule in rules]
        }
        # Exécution de la requête
        response = requests.post(url=TwitterClientRule.__ENDPOINT_RULE
                                 , headers=headers
                                 , json=body)

        # Si la requête n'a pas aboutie correctement on lève une erreur
        if response.status_code != 201:
            raise TwitterApiException(f'Problème lors de la création de règle\n'
                                      f'{response.status_code} : {response.content}')

        # Creation de nouveau objet rules
        new_rules = []
        for rule in response.json()["data"]:
            new_rules.append(Rule(expression=rule["value"]
                                  , tag=rule["tag"]
                                  , id=rule["id"]))
        logging.info(f'rules add {new_rules}')
        return new_rules

    def delete_rule(self, rule):
        """
        1- Récupère les règles déjà envoyée
        2- Vérifie si la règle existe en se basant sur on expression
        3- Si c'est le cas la supprime

        :param rule: la règle à supprimer
        :type rule: Rule
        :return: s'il y a bien eu suppression
        :rtype: Bool
        """
        logging.info(f'deleting rule {rule}')
        saved_rules = self.get_all_rules()
        matched_rule = is_match_save_rules(rule, saved_rules)
        if matched_rule is not None:
            self.delete_rule_effectively(rule)
        logging.info(f'rule deleted')
        return True

    def delete_rule_effectively(self, *rules):
        # Creation des headers de la requête
        rule_to_delete = list(*rules)
        headers = {
            "Content-type": "application/json",
            "Authorization": f'Bearer {self.__bearer_token}'
        }
        # Création du corps
        body = {
            "delete": {
                "ids": [rule.id for rule in rule_to_delete]
            }
        }
        # Exécution de la requête
        response = requests.post(url=TwitterClientRule.__ENDPOINT_RULE
                                 , headers=headers
                                 , json=body)
        # Si la requête n'a pas aboutie correctement on lève une erreur
        if response.status_code != 200:
            raise TwitterApiException(f'Problème lors de la suppression de règle\n'
                                      f'{response.status_code} : {response.content}')

    def get_all_rules(self) -> List[Rule]:
        """
        Envoie une requête au webservice pour récupérer les règles en base
        :return: les règles déjà envoyé
        :rtype: list of Rule
        """
        logging.info("Getting all rules saved on the API")

        # Creation des headers de la requête
        headers = {
            "Authorization": f'Bearer {self.__bearer_token}'
        }
        # Exécution de la requête
        response = requests.get(url=TwitterClientRule.__ENDPOINT_RULE
                                , headers=headers)
        # Si la requête n'a pas aboutie correctement on lève une erreur
        if response.status_code != 200:
            raise TwitterApiException(f'Problème lors de la récupération des règles\n'
                                      f'{response.status_code} : {response.content}')

        saved_rules = []
        # Check if the data key is present
        if "data" in response.json():
            for rule in response.json()["data"]:
                saved_rules.append(Rule(expression=rule["value"]
                                        , tag=rule["value"]
                                        , id=rule["id"]))
            logging.info(f'All rules saved on the API {saved_rules}')

        return saved_rules

    def delete_all_rule(self):
        """
        Find and delete all the rules
        :return:
        :rtype:
        """
        logging.info("Delete all the rules")
        rules_to_delete = self.get_all_rules()
        if len(rules_to_delete):
            self.delete_rule_effectively(rules_to_delete)
            logging.info("All the rules deleted")
        else:
            logging.info("No rule to delete")
