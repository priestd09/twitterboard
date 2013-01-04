#!/usr/bin/python
# -*- coding: utf-8 -*-

from tweepy import Stream

from streamer import StreamSaverListener
from streamer import Authentification

from data import engine_url

# most trendy hashtags currently
trendy = ["#smartiphone5BNOLotto", "#enkötüsüde", "#GiveMeThatGlobeIphone5", "#SilivriyeÖzgürlük", "#CiteNomesFeios",  "#121212concert", "#ItsNotCuteWhen", "#nowplaying", "#Blessed", "#breakoutartist"]

l = StreamSaverListener(trendy, engine_url)
myAuth = Authentification(oauth=True)

stream = Stream(myAuth.get_auth(), l)

print "Trends streamed will be : "
print trendy

stream.filter(track=trendy)  # I need this to become a thread
