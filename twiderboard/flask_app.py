from flask import Flask, jsonify, render_template, request

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy import desc


import data
from datamodel import TrendyHashtag
from datamodel import Tweet
from datamodel import Member

from streamer import HashtagLogger


app = Flask(__name__)
h = HashtagLogger(data.engine_url, oauth=data.oauth)
h.start()


## Utilities
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


## Ajax queries
@app.route('/trendy')
def trendy():

    session, engine = connect()

    # requests active hashtags
    h_query = session.query(TrendyHashtag).filter(TrendyHashtag.active == True).order_by(desc(TrendyHashtag.created))
    hashtags = h_query.all()

    trendy = []
    for h in hashtags:
        trendy.append([h.hashtag[1:], 1])

    session.close()
    engine.dispose()
    return jsonify(trendy=trendy)


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
    if not new_hash.startswith('#'):
        new_hash = "#" + new_hash
    hashtag = h.add_hashtag(new_hash)  # just to check we create the same hashtag
    return jsonify(hash="Adding %s !" % (hashtag))


@app.route('/remove_hashtag')
def remove_hashtag():
    to_rm = "#" + request.args['hash']
    h.remove_hashtag(to_rm)
    return render_template('index.html')


@app.route('/get_members')
def get_members():
    max_lim = min(100, int(request.args.get('num')))
    cur_hash = "#" + request.args.get('hash')

    session, engine = connect()

    # requests active hashtags
    l_query = session.query(Member).filter(Member.hashtag == cur_hash).order_by(desc(Member.count)).limit(max_lim)
    leaders = l_query.all()

    members = []
    for l in leaders:
        members.append([l.author, l.count])

    session.close()
    engine.dispose()

    return jsonify(members=members)


@app.route('/get_activity')
def get_activity():
    max_lim = min(100, int(request.args.get('num')))
    cur_hash = "#" + request.args.get('hash')

    session, engine = connect()

    # requests active hashtags
    t_query = session.query(Tweet).filter(Tweet.hashtag == cur_hash).order_by(desc(Tweet.inserted)).limit(max_lim)
    tweets = t_query.all()

    activity = []
    for t in tweets:
        activity.append([t.author, t.text, t.created])

    session.close()
    engine.dispose()


    return jsonify(activity=activity)


@app.route('/stop')
def stop():
    h.stop()
    return "Session closed"


## Static part
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/statistics')
def statistics():
    return render_template('statistics.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/hashtag/<cur_hash>')
def show_user_profile(cur_hash):
    """
    Show the data we currently have for this hashtag
    Shall be possible for any hashtag (even inactive), but only active hashtags will
    actually have a link on the webiste.
    """
    #return 'Hashtag %s' % cur_hash
    return render_template('hashtag.html', hashtag=cur_hash)


if __name__ == '__main__':
    app.run(debug=True)
