from dependency_injector import containers, providers

from services.read_rule_service import ReadRuleService
from services.writer_tweet_service import WriterTweetService
from twitter_client.twitter_client_rule import TwitterClientRule
from twitter_client.twitter_client_stream import TwitterClientStream


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    twitter_client_rule = providers.Singleton(
        TwitterClientRule,
        bearer_token=config.bearer_token
    )

    twitter_client_stream = providers.Singleton(
        TwitterClientStream,
        bearer_token=config.bearer_token
    )

    write_tweet_service = providers.Singleton(
        WriterTweetService,
    )

    read_rule_service = providers.Singleton(
        ReadRuleService,
    )

