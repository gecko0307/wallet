import json
import datetime
from datetime import datetime

import bottle
from bottle import request
from ..namespace import *
from ..data import *

@bottle.route('/monthexpences')
def monthExpences(db):
    year = datetime.now().year
    month = datetime.now().month - 1
    if 'year' in request.query:
        year = int(request.query['year'])
    if 'month' in request.query:
        month = int(request.query['month'])
    d = NestedNamespace({
        'year': year,
        'month': month
    })
    if d != None:
        return bottle.template(load('monthExpences.stpl'), data = d)
    else:
        bottle.redirect('/404.html')

@bottle.route('/monthexpences.json')
def monthExpencesJson(db):
    year = datetime.now().year
    month = datetime.now().month - 1
    if 'year' in request.query:
        year = int(request.query['year'])
    if 'month' in request.query:
        month = int(request.query['month'])
    expences = dict()
    query = select('Transactions')
    cursor = db.execute(query)
    purchases = { }
    for trans in cursor.fetchall():
        if trans['CATEGORY'] != 'notrack':
            d = datetime.strptime(trans['DATETIME'], '%Y-%m-%d %H:%M:%S')
            if d.year == year and d.month == month + 1:
                category = trans['CATEGORY']
                query = select('Accounts', ["ID='%s'" % trans['ACCOUNT']])
                cursor = db.execute(query)
                account = cursor.fetchall()[0]
                value = trans['VALUE']
                value *= account['REPORT_EXCHANGE_RATE']
                if value < 0:
                    if category in expences:
                        expences[category] += -value
                    else:
                        expences[category] = -value
                    if not category in purchases:
                        purchases[category] = []
                    purchases[category].append({
                        'description': trans['DESCRIPTION'],
                        'value': -value,
                        'date': d.strftime('%d.%m.%Y')
                    })
    for category, purchasesList in purchases.items():
        # sum up purchases with same description
        mimimizedPurchases = []
        for p in purchasesList:
            outputPurchase = next((x for x in mimimizedPurchases if x['description'] == p['description']), None)
            if outputPurchase == None:
                mimimizedPurchases.append(p)
            else:
                outputPurchase['value'] += p['value']
        
        # get 5 top purchases
        sortedPurchases = sorted(mimimizedPurchases, key = lambda k: k['value'], reverse = True)
        topPurchases = sortedPurchases[0:5]
        purchases[category] = topPurchases
    return {
        'categories': list(expences.keys()),
        'expences': list(expences.values()),
        'topPurchases': purchases
    }
