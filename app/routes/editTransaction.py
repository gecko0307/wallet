import bottle
from bottle import request
from ..data import *

@bottle.route('/editTransaction')
def editTransaction(db):
    transId = request.query['id']
    d = transactionData(transId, db)
    if d != None:
        return bottle.template(load('editTransaction.stpl'), data = d)
    else:
        bottle.redirect('/404.html')
