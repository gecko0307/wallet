import bottle
from ..config import *
from ..data import *

@bottle.route('/hiddenAccounts')
def index(db):
    d = profileData(db)
    return bottle.template(load('hiddenAccounts.stpl'), data = d)
