import bottle
from bottle import request

@bottle.post('/updateAccount')
def updateAccount(db):
    accountId = request.query['id']
    accountName = request.forms.getunicode('name') or 'My Account'
    accountDescription = request.forms.getunicode('description') or ''
    accountCurrency = request.forms.get('currency') or 'RUB'
    accountExchangeRate = request.forms.get('exchangeRate') or 1
    hidden = (request.forms.get('hidden') or 'off') == 'on'
    db.execute('UPDATE Accounts SET NAME=?, DESCRIPTION=?, CURRENCY=?, REPORT_EXCHANGE_RATE=?, HIDDEN=? WHERE id=?', 
        (accountName, accountDescription, accountCurrency, accountExchangeRate, int(hidden), accountId, ))
    db.commit()
    bottle.redirect('/account?id=%s' % accountId)
