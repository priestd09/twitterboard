from flask import Flask, jsonify, render_template, request

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

import data
from datamodel import TrendyHashtag
from datamodel import Tweet
from datamodel import Member

from streamer import HashtagLogger


app = Flask(__name__)
h = HashtagLogger(data.engine_url, oauth=data.oauth)
h.start()


def connect():
    """
    Separated so that the method can be run in each created thread.
    Initiates connexion to the database and starts a Session to be used to query it.
    Returns the session used to communicate with the database
    """
    # creates engine, tries to create all the tables needed later on
    engine = create_engine(data.engine_url, echo=data.debug)
    # initiates session to the database, tries to create proper session
    Session = sessionmaker(bind=engine)

    return Session(), engine  # Bridges class to db


@app.route('/nb_trendy')
def nb_trendy():

    session, engine = connect()

    # requests active hashtags
    query = session.query(func.count(TrendyHashtag.id)).filter(TrendyHashtag.active == True)
    hashs = query.first()[0]

    #requests number of tweets
    query = session.query(func.count(Tweet.id))
    tweets = query.first()[0]

    #requests number of members
    query = session.query(func.count(Member.id))
    members = query.first()[0]

    session.close()
    engine.dispose()

    return jsonify(hashs=hashs, tweets=tweets, members=members)


@app.route('/_add_hashtag')
def add_hashtag():
    new_hash = request.args.get('new_hash')
    hashtag = h.add_hashtag(new_hash)  # just to check we create the same hashtag
    return jsonify(hash="Adding %s !" % (hashtag))


@app.route('/remove_hashtag')
def remove_hashtag():
    hashtag = h.remove_hashtag('plop')
    return hashtag


@app.route('/stop')
def stop():
    h.stop()
    return "Session closed"


@app.route('/')
def index():
    return render_template('statistics.html')

if __name__ == '__main__':
    app.run(debug=True)
