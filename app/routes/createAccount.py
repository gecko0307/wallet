import bottle
from ..data import *

@bottle.route('/createaccount')
def index(db):
    d = profileData(db)
    return bottle.template(stpl('create_account'), data = d)
