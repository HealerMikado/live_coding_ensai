import json
import logging
import sys

import dotenv
from dependency_injector.wiring import inject, Provide

from container import Container
from services.read_rule_service import ReadRuleService
from services.writer_tweet_service import WriterTweetService
from twitter_client.twitter_client_rule import TwitterClientRule
from twitter_client.twitter_client_stream import TwitterClientStream


@inject
def main(client_rule: TwitterClientRule = Provide[Container.twitter_client_rule]
         , client_stream: TwitterClientStream = Provide[Container.twitter_client_stream]
         , read_rule_service: ReadRuleService = Provide[Container.read_rule_service]
         , write_tweet_service: WriterTweetService = Provide[Container.write_tweet_service]
         ):

    logging.info('Started')
    client_rule.delete_all_rule()

    rules = read_rule_service.read_rules_from_jsonl("input/rules.jsonl")
    client_rule.add_rules(rules=rules)

    # Création de l'objet python qui gère la connexion au stream de tweet
    with client_stream.get_stream() as stream:
        write_tweet_service.stream_to_file(stream)


if __name__ == '__main__':
    logging.basicConfig(filename='twitter.log'
                        , level=logging.INFO
                        , format='%(asctime)s | %(levelname)s | %(message)s'
                        , datefmt='%m/%d/%Y %I:%M:%S %p')
    #logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    dotenv.load_dotenv()
    container = Container()
    container.config.bearer_token.from_env('BEARER_TOKEN')
    container.wire(modules=[sys.modules[__name__]])

    main()  # <-- dependency is injected automatically

