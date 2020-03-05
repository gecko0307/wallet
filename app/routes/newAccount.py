import bottle
from bottle import request

@bottle.post('/newAccount')
def newAccount(db):
    accountName = request.forms.getunicode('name') or 'My Account'
    accountDescription = request.forms.getunicode('description') or ''
    accountCurrency = request.forms.get('currency') or 'RUB'
    accountExchangeRate = request.forms.get('exchangeRate') or 1
    db.execute(
        "INSERT INTO Accounts (NAME, DESCRIPTION, CURRENCY, REPORT_EXCHANGE_RATE) VALUES (?, ?, ?, ?)", 
        (accountName, accountDescription, accountCurrency, accountExchangeRate,))
    db.commit()
    bottle.redirect('/')
