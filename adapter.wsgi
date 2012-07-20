import sys, os, bottle

sys.path = ['/home/matael/today_quote/'] + sys.path
os.chdir(os.path.dirname(__file__))

import today_quote

application = bottle.default_app()
