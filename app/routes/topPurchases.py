import json
import datetime
from datetime import datetime

import bottle
from bottle import request
from ..namespace import *
from ..data import *

@bottle.route('/toppurchases')
def toppurchases(db):
    year = datetime.now().year
    if 'year' in request.query:
        year = int(request.query['year'])
    d = NestedNamespace({
        'year': year
    })
    if d != None:
        return bottle.template(load('topPurchases.stpl'), data = d)
    else:
        bottle.redirect('/404.html')

@bottle.route('/toppurchases.json')
def topPurchasesJson(db):
    query = select('Transactions')
    cursor = db.execute(query)
    purchases = []
    for trans in cursor.fetchall():
        if trans['VALUE'] > 0:
            continue
        if(trans['CATEGORY'] == 'household' or 
           trans['CATEGORY'] == 'books' or
           trans['CATEGORY'] == 'music' or
           trans['CATEGORY'] == 'culture' or
           trans['CATEGORY'] == 'catering' or
           trans['CATEGORY'] == 'clothes' or
           trans['CATEGORY'] == 'gifts' or
           trans['CATEGORY'] == 'food' or
           trans['CATEGORY'] == 'software' or
           trans['CATEGORY'] == 'tech' or
           trans['CATEGORY'] == 'transport' or
           trans['CATEGORY'] == 'hobby' or
           trans['CATEGORY'] == 'cosmetics' or
           trans['CATEGORY'] == 'meds'):
            query = select('Accounts', ["ID='%s'" % trans['ACCOUNT']])
            cursor = db.execute(query)
            account = cursor.fetchall()[0]
            value = trans['VALUE']
            value *= account['REPORT_EXCHANGE_RATE']
            d = datetime.strptime(trans['DATETIME'], '%Y-%m-%d %H:%M:%S')
            purchases.append({
                'description': trans['DESCRIPTION'],
                'category': trans['CATEGORY'],
                'value': -value,
                'date': d.strftime('%d.%m.%Y')
            })
    sortedPurchases = sorted(purchases, key = lambda k: k['value'], reverse = True)
    topPurchases = sortedPurchases[0:10]
    return {
        'purchases': topPurchases
    }
