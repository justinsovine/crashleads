import os, sys, bottle

sys.path.append(os.path.dirname(__file__))
os.chdir(os.path.dirname(__file__))

import main

application = bottle.default_app()
