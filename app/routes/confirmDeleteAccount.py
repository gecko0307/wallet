import bottle
from bottle import request
from ..data import *

@bottle.route('/confirmDeleteAccount')
def confirmDeleteAccount(db):
    accountId = request.query['id']
    d = accountData(accountId, db)
    if d != None:
        return bottle.template(load('confirmDeleteAccount.stpl'), data = d)
    else:
        bottle.redirect('/404.html')
