import bottle
from bottle import request
from ..data import *

@bottle.route('/editAccount')
def editAccount(db):
    accountId = request.query['id']
    d = accountData(accountId, db)
    if d != None:
        return bottle.template(load('editAccount.stpl'), data = d)
    else:
        bottle.redirect('/404.html')

