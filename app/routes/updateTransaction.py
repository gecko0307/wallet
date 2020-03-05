import bottle
from bottle import request
from ..data import *

@bottle.post('/updateTransaction')
def updateTransaction(db):
    transId = request.query['id']
    d = transactionData(transId, db)
    accountId = d.transaction.account;
    transDescription = request.forms.getunicode('description') or ''
    transCategory = request.forms.get('category') or 'unspecified'
    transValue = float(request.forms.get('value') or '0.0')
    transDate = request.forms.get('date') or datetime.today().strftime('%Y-%m-%d')
    timestamp = '%s 00:00:00' % transDate
    db.execute('UPDATE Transactions SET DESCRIPTION=?, CATEGORY=?, VALUE=?, DATETIME=? WHERE id=?', 
        (transDescription, transCategory, transValue, timestamp, transId, ))
    db.commit()
    bottle.redirect('/account?id=%s' % accountId)
