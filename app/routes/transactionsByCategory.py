import json
import datetime
from datetime import datetime

import bottle
from bottle import request
from ..namespace import *
from ..data import *

@bottle.route('/transactionsByCategory')
def transactionsByCategory(db):
    cat = ''
    if 'cat' in request.query:
        cat = request.query['cat']
    query = select('Transactions')
    cursor = db.execute(query)
    catTrans = []
    totalValue = 0
    for trans in cursor.fetchall():
        if trans['CATEGORY'] == cat:
            query = select('Accounts', ["ID='%s'" % trans['ACCOUNT']])
            cursor = db.execute(query)
            account = cursor.fetchall()[0]
            value = trans['VALUE']
            value *= account['REPORT_EXCHANGE_RATE']
            d = datetime.strptime(trans['DATETIME'], '%Y-%m-%d %H:%M:%S')
            catTrans.append(NestedNamespace({
                'id': trans['ID'],
                'description': trans['DESCRIPTION'],
                'category': trans['CATEGORY'],
                'currency': trans['CURRENCY'],
                'value': value,
                'date': trans['DATETIME']
            }))
            totalValue += value
    d = NestedNamespace({
        'category': cat,
        'transactions': catTrans,
        'totalValue': totalValue
    })
    return bottle.template(load('transactionsByCategory.stpl'), data = d)
    
