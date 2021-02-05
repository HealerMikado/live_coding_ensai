import json

import dotenv

from twitter_client.twitter_stream_client import TwitterStreamClient

# Pour charger les variables du fichier .env en tant que variable d'environnement
dotenv.load_dotenv()

def main():
    #client_rule = TwitterClientRule()
    #dog_rule = Rule("dog", "Je veux des chiens")
    #client_rule.add_rule(dog_rule)

    # Création de l'objet python qui gère la connexion au stream de tweet
    twitter_stream_client = TwitterStreamClient()
    stream = twitter_stream_client.get_stream()

    # Pour récupérer les différents tweets il faut itérer sur le stream. Mais ce n'est pas
    # car l'objet n'est pas une simple collection. iter_line() retourne un nouvel enregistrement
    # à chaque fois
    for tweet in stream.iter_lines():
        # Affichage en console
        print(json.dumps(json.loads(tweet), indent=4))
        # Ecriture dans un fichier
        with open("output/tweets.jsonl", mode="a") as file :
            file.write(json.dumps(json.loads(tweet)))
            file.write("\n")

if __name__ == '__main__':
    main()

