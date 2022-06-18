import json
import datetime
from datetime import datetime

import bottle
from bottle import request
from ..namespace import *
from ..data import *

@bottle.route('/balance')
def flow(db):
    year = datetime.now().year
    if 'year' in request.query:
        year = int(request.query['year'])
    d = NestedNamespace({
        'year': year
    })
    if d != None:
        return bottle.template(load('balance.stpl'), data = d)
    else:
        bottle.redirect('/404.html')

@bottle.route('/balance.json')
def balanceJson(db):
    data = {
        'balance': [0 for x in range(12)],
        'maxMonth': 0
    }
    year = datetime.now().year
    if 'year' in request.query:
        year = int(request.query['year'])
    query = select('Transactions')
    query += ' ORDER BY CAST(strftime(\'%m\', DATETIME) AS INTEGER)'
    cursor = db.execute(query)
    for trans in cursor.fetchall():
        d = datetime.strptime(trans['DATETIME'], '%Y-%m-%d %H:%M:%S')
        month = d.month - 1
        query = select('Accounts', ["ID='%s'" % trans['ACCOUNT']])
        exchangeRate = 1
        res = db.execute(query).fetchall()
        if len(res) != 0:
            account = res[0]
            exchangeRate = account['REPORT_EXCHANGE_RATE']
        value = trans['VALUE']
        value *= exchangeRate
        if d.year == year:
            for m in range(month, 12):
                data['balance'][m] += value
            if month > data['maxMonth']:
                data['maxMonth'] = month
        elif d.year < year:
            for m in range(0, 12):
                data['balance'][m] += value
    return data
