import json
import datetime
from datetime import datetime

import bottle
from bottle import request
from ..namespace import *
from ..data import *

@bottle.route('/assets')
def assets(db):
    year = datetime.now().year
    if 'year' in request.query:
        year = int(request.query['year'])
    d = NestedNamespace({
        'year': year
    })
    if d != None:
        return bottle.template(load('assets.stpl'), data = d)
    else:
        bottle.redirect('/404.html')

@bottle.route('/assets.json')
def assetsJson(db):
    data = {
        'accounts': [],
        'labels': [],
        'balances': [],
        'totalBalance': 0
    }
    query = select('Accounts')
    cursor = db.execute(query)
    for account in cursor.fetchall():
        accountBalance = 0
        query = select('Transactions', ["ACCOUNT='%s'" % account['ID']])
        cursor = db.execute(query)
        for transaction in cursor.fetchall():
            accountBalance += transaction['VALUE']
        accountBalance *= account['REPORT_EXCHANGE_RATE']
        acc = {
            'id': account['ID'],
            'name': account['NAME'],
            'description': account['DESCRIPTION'],
            'currency': account['CURRENCY'],
            'exchangeRate': account['REPORT_EXCHANGE_RATE'],
            'balance': accountBalance
        }
        data['accounts'].append(acc)
        data['labels'].append(account['NAME'])
        data['balances'].append(accountBalance)
        data['totalBalance'] += accountBalance
    
    return data
