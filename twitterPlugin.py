#!/usr/bin/python3

from typing import Dict, Optional, Union
from api import NowPlaying, Track
from blaster import BlastPlugin
import configparser
import tweepy


class Radioplayer(BlastPlugin):
    last_playing: Optional[NowPlaying]
    config: configparser.SectionProxy

    def __init__(self):
        # Pull in some config
        config = configparser.ConfigParser()
        config.read('config.ini')
        if "twitter" in config:
            self.config = config['twitter']
            auth = tweepy.OAuthHandler(
                self.config['consumer_key'], self.config['consumer_secret'])
            auth.set_access_token(
                self.config['token'], self.config['token_secret'])

            self.twitter_api = tweepy.API(auth)
            self.emoji = emoji = '🎵'
            self.last_playing = None

            self.poke_track(None)
        else:
            raise Exception("Config for Twitter is missing.")

    def poke_track(self, now_playing: Optional[NowPlaying]):

        if (now_playing != self.last_playing):
            print("RadioPlayer: Now Playing:", now_playing)
            track: Track
            if now_playing:
                if now_playing["track"] != None:
                    track = now_playing["track"]
                else:
                    track = {
                        "title": "",
                        "artist": "",
                        "length": None
                    }

                # Tweet
                songText = track['title'] + ' - ' + track['artist']
                tweet = self.emoji*2 + ' NOW PLAYING: ' + songText + ' ' + self.emoji*2
                self.twitter_api.update_status(tweet)

            self.last_playing = now_playing
