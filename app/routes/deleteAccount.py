import bottle
from bottle import request
from ..data import *

@bottle.route('/deleteAccount')
def deleteAccount(db):
    accountId = request.query['id']
    d = accountData(accountId, db)
    if d != None:
        db.execute('DELETE FROM Accounts WHERE id=?', (accountId, ))
        db.commit()
        bottle.redirect('/')
    else:
        bottle.redirect('/404.html')
