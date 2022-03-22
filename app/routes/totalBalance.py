import json
import datetime
from datetime import datetime

import bottle
from bottle import request
from ..namespace import *
from ..data import *

@bottle.route('/totalbalance')
def flow(db):
    year = datetime.now().year
    if 'year' in request.query:
        year = int(request.query['year'])
    d = NestedNamespace({
        'year': year
    })
    if d != None:
        return bottle.template(load('totalBalance.stpl'), data = d)
    else:
        bottle.redirect('/404.html')

@bottle.route('/totalbalance.json')
def balanceJson(db):
    data = {
        'balance': [0 for x in range(12 * 5)],
        'maxMonth': 0
    }
    years = 0
    yearStart = datetime.now().year
    print(yearStart)
    
    query = select('Transactions')
    query += ' ORDER BY CAST(strftime(\'%m\', DATETIME) AS INTEGER)'
    cursor = db.execute(query)
    for trans in cursor.fetchall():
        d = datetime.strptime(trans['DATETIME'], '%Y-%m-%d %H:%M:%S')
        if d.year <= yearStart:
            yearStart = d.year
        years = d.year - yearStart
        month = d.month - 1
        query = select('Accounts', ["ID='%s'" % trans['ACCOUNT']])
        cursor = db.execute(query)
        account = cursor.fetchall()[0]
        value = trans['VALUE']
        value *= account['REPORT_EXCHANGE_RATE']
        totalMonth = years * 12 + month
        for m in range(totalMonth, len(data['balance'])):
            data['balance'][m] += value
        
    return data
