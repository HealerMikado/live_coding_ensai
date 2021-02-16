import os

import requests

from custom_exception.twitter_api_exception import TwitterApiException


class TwitterClientStream:
    __URL_STREAM = "https://api.twitter.com/2/tweets/search/stream"

    def __init__(self, bearer_token:str) -> None:
        self.__bearer_token = bearer_token

    def get_stream(self) -> requests.Response:
        """
        Permet de récupérer le flux filtré de l'API twitter
        :return: La stream de l'API twitter
        :rtype: requests.Response
        """
        headers = {
            "Authorization": f'Bearer {self.__bearer_token}'
        }
        # Inutilisé pour le moment, pour la prochaine fois
        query_params = {
            "tweet.fields" : "created_at,public_metrics",
            "expansions" : "author_id",
            "user.fields" : "created_at"
        }

        # Remarquez l'ajout d'un paramètre stream. Cela permet de recevoir en continu de nouveaux
        # enregistrement
        stream = requests.get(TwitterClientStream.__URL_STREAM
                              , params=query_params
                              , headers=headers
                              , stream=True)

        if stream.status_code !=200 :
            raise TwitterApiException(f'Problème lors de la récupération du flux \n'
                            f'{stream.content}')

        return stream