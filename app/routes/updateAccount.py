import bottle
from bottle import request

@bottle.post('/updateAccount')
def updateAccount(db):
    accountId = request.query['id']
    accountName = request.forms.getunicode('name') or 'My Account'
    accountDescription = request.forms.getunicode('description') or ''
    accountCurrency = request.forms.get('currency') or 'RUB'
    accountExchangeRate = request.forms.get('exchangeRate') or 1
    db.execute('UPDATE Accounts SET NAME=?, DESCRIPTION=?, CURRENCY=?, REPORT_EXCHANGE_RATE=? WHERE id=?', 
        (accountName, accountDescription, accountCurrency, accountExchangeRate, accountId, ))
    db.commit()
    bottle.redirect('/account?id=%s' % accountId)
