import os

import requests

from businness_object.rule import Rule


class TwitterClientRule:
    __ENDPOINT_RULE = "https://api.twitter.com/2/tweets/search/stream/rules"

    def add_rule(self, rule: Rule) -> Rule:
        """
        Permet d'ajouter une règle pour filtrer le flux de tweets
        :param rule: La règle à ajouter
        :type value: Rule
        :return: la règle mise à jour de son id
        :rtype: Rule
        """
        #Creation des headers de la requête
        headers = {
            "Content-type": "application/json",
            "Authorization": f'Bearer {os.getenv("BEARER_TOKEN")}'
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
            raise Exception(f'Problème lors de la création de règle\n'
                            f'{response.status_code} : {response.content}')

        # Mise  à jour de l'id de la règle avec l'id renvoyé par twitter
        rule.id = response.json()["data"][0]["id"]
        print(response.json())
        return rule

    