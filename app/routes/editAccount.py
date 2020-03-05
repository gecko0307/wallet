import bottle
from bottle import request
from ..data import *

@bottle.route('/editAccount')
def editAccount(db):
    accountId = request.query['id']
    d = accountData(accountId, db)
    if d != None:
        return bottle.template(stpl('edit_account'), data = d)
    else:
        bottle.redirect('/404.html')

