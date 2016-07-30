import os
import logging
from datetime import datetime

import tweepy
from tweepy import TweepError

from geopy.geocoders import GoogleV3

from .utils import get_pokemon_name
from .pgoapi.utilities import get_name_by_pos
from .rares import RARE_POKEMON

log = logging.getLogger(__name__)


CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
ACCESS_KEY = os.environ['TWITTER_ACCESS_KEY']
ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']

twitter_auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
twitter_auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)


def send_tweet(message, **kwargs):
    api = tweepy.API(twitter_auth)
    try:
        api.update_status(message, **kwargs)
    except TweepError, e:
        log.info('Tweet Failed ({})'.format(e))


def send_pokemon_tweet(name, lat, lon, minutes):

    address = get_name_by_pos(lat, lon).split(',')[0]

    message = ('A wild #{name} appeared at {address}! '
               'Only {minute} minutes left! #PokemonGo #Stanford '
               'https://www.google.com/maps/dir/Current+Location/{lat},{long}'
               ).format(name=name, address=address, minute=minutes,
                        lat=lat, long=lon)

    send_tweet(message, lat=lat, long=lon, display_coordinates=True)


def send_pokemon_tweets(Pokemon, pokemons):
    query = Pokemon.get_active(None, None, None, None)

    encounter_ids = [p['encounter_id'] for p in query]

    count = 0
    for pokemon in pokemons.values():
        name = get_pokemon_name(pokemon['pokemon_id'])
        if (pokemon['encounter_id'] not in encounter_ids and
                name.lower() in RARE_POKEMON):
            minutes, _ = divmod((pokemon['disappear_time'] -
                                datetime.utcnow()).seconds, 60)
            if 60 > minutes and minutes > 2:
                send_pokemon_tweet(name, pokemon['latitude'],
                                   pokemon['longitude'], minutes)
                count += 1
    log.info('Tweeted about {} pokemon'.format(count))
