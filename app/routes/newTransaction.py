import bottle
from bottle import request
from ..data import *

@bottle.post('/newTransaction')
def newTransaction(db):
    transAccount = request.query['account']
    transType = request.query['type']
    query = select('Accounts', ["ID='%s'" % transAccount])
    cursor = db.execute(query)
    accounts = cursor.fetchall()
    if len(accounts) > 0:
        account = accounts[0]
        transDescription = request.forms.getunicode('description') or ''
        transCategory = request.forms.get('category') or 'unspecified'
        transValue = float(request.forms.get('value') or '0.0')
        if transType == 'sub':
            transValue = -transValue
        transCurrency = account['CURRENCY']
        transDate = request.forms.get('date') or datetime.today().strftime('%Y-%m-%d')
        timestamp = '%s 00:00:00' % transDate
        db.execute(
            "INSERT INTO Transactions (DESCRIPTION, CATEGORY, CURRENCY, VALUE, ACCOUNT, DATETIME) VALUES (?, ?, ?, ?, ?, ?)", 
            (transDescription, transCategory, transCurrency, transValue, transAccount, timestamp))
        db.commit()
    bottle.redirect('/account?id=%s' % transAccount)
