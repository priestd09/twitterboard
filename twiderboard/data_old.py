"""
Contains all needed information for application to work
and that has to be spread over modules.
"""
# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section

import os

debug = False  # True
root = '/home/jll/Documents/code/twitterboard/'
#root = '/home/test/Documents/twiderboard'
#root = '/home/airballman/Documents/twiderboard/twitterboard/'
# TODO: do that correctly

engine_url = 'sqlite:///twiderboard.db'


log_name = 'board.log'
log_path = os.path.join(root, log_name)