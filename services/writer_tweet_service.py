import json
import logging
from concurrent.futures.process import ProcessPoolExecutor

from businness_object.tweet import Tweet


class WriterTweetService:

    def stream_to_file(self, stream):
        # Pour récupérer les différents tweets il faut itérer sur le stream. Mais ce n'est pas
        # car l'objet n'est pas une simple collection. iter_line() retourne un nouvel enregistrement
        # à chaque fois
        for tweet_raw in stream.iter_lines():
            if tweet_raw :
                tweet = self.read_tweet_from_stream(tweet_raw)
                self.write_tweet_to_file(tweet)


    def write_tweet_to_file(self, tweet):
        # Ecriture dans un fichier
        logging.info(f'Write tweet')
        with open("output/tweets.jsonl", mode="a") as file:
            file.write(json.dumps(tweet.__dict__))
            file.write("\n")

    def read_tweet_from_stream(self, tweet_raw):
        logging.info(f'Read tweet')
        tweet_dict = json.loads(tweet_raw)
        tweet = Tweet(contenu=tweet_dict["data"]["text"]
                      , auteur=tweet_dict["includes"]["users"][0]["username"]
                      , date_creation=tweet_dict["data"]["created_at"]
                      , public_metrics=tweet_dict["data"]["public_metrics"]
                      , auteur_name=tweet_dict["includes"]["users"][0]["name"])
        return tweet