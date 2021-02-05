import os

import requests


class TwitterStreamClient:
    __URL_STREAM = "https://api.twitter.com/2/tweets/search/stream"

    def get_stream(self) -> requests.Response:
        """
        Permet de récupérer le flux filtré de l'API twitter
        :return: La stream de l'API twitter
        :rtype: requests.Response
        """
        headers = {
            "Authorization": f'Bearer {os.getenv("BEARER_TOKEN")}'
        }
        # Inutilisé pour le moment, pour la prochaine fois
        query_params = {
            "tweet.fields" : "created_at",
            "expansions" : "author_id",
            "user.fields" : "created_at"
        }

        # Remarquez l'ajout d'un paramètre stream. Cela permet de recevoir en continu de nouveaux
        # enregistrement
        stream = requests.get(TwitterStreamClient.__URL_STREAM
                              , headers=headers
                              , stream=True)

        if stream.status_code !=200 :
            raise Exception("Problème lors de la récupération du flux")

        return stream