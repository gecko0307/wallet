import bottle
from bottle import request

@bottle.post('/newAccount')
def newAccount(db):
    accountName = request.forms.getunicode('name') or 'My Account'
    accountDescription = request.forms.getunicode('description') or ''
    accountCurrency = request.forms.get('currency') or 'RUB'
    accountExchangeRate = request.forms.get('exchangeRate') or 1
    hidden = 0
    db.execute(
        "INSERT INTO Accounts (NAME, DESCRIPTION, CURRENCY, REPORT_EXCHANGE_RATE, HIDDEN) VALUES (?, ?, ?, ?, ?)", 
        (accountName, accountDescription, accountCurrency, accountExchangeRate, hidden,))
    db.commit()
    bottle.redirect('/')
