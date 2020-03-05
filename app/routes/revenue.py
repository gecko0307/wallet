import json
import datetime
from datetime import datetime

import bottle
from bottle import request
from ..namespace import *
from ..data import *

@bottle.route('/revenue')
def revenue(db):
    year = datetime.now().year
    if 'year' in request.query:
        year = int(request.query['year'])
    d = NestedNamespace({
        'year': year
    })
    if d != None:
        return bottle.template(load('revenue.stpl'), data = d)
    else:
        bottle.redirect('/404.html')

@bottle.route('/revenue.json')
def revenueJson(db):
    revenue = dict()
    query = select('Transactions')
    cursor = db.execute(query)
    for trans in cursor.fetchall():
        if trans['CATEGORY'] != 'notrack':
            category = trans['CATEGORY']
            query = select('Accounts', ["ID='%s'" % trans['ACCOUNT']])
            cursor = db.execute(query)
            account = cursor.fetchall()[0]
            value = trans['VALUE']
            value *= account['REPORT_EXCHANGE_RATE']
            if value > 0:
                if category in revenue:
                    revenue[category] += value
                else:
                    revenue[category] = value
    return {
        'categories': list(revenue.keys()),
        'revenue': list(revenue.values())
    }
