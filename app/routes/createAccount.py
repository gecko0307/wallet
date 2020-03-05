import bottle
from ..data import *

@bottle.route('/createaccount')
def index(db):
    d = profileData(db)
    return bottle.template(load('create_account.stpl'), data = d)
