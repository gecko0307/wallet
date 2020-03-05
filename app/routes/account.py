import bottle
from bottle import request
from ..config import *
from ..data import *

@bottle.route('/account')
def index(db):
    accountId = request.query['id']
    d = accountData(accountId, db)
    if d != None:
        return bottle.template(load('account.stpl'), data = d)
    else:
        bottle.redirect('/404.html')
