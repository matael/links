import sys, os, bottle

sys.path = ['/home/matael/links/'] + sys.path
os.chdir(os.path.dirname(__file__))

import links

application = bottle.default_app()
