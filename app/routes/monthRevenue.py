import json
import datetime
from datetime import datetime

import bottle
from bottle import request
from ..namespace import *
from ..data import *

@bottle.route('/monthrevenue')
def monthRevenue(db):
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
        return bottle.template(stpl('monthrevenue'), data = d)
    else:
        bottle.redirect('/404.html')

@bottle.route('/monthrevenue.json')
def monthRevenueJson(db):
    year = datetime.now().year
    month = datetime.now().month - 1
    if 'year' in request.query:
        year = int(request.query['year'])
    if 'month' in request.query:
        month = int(request.query['month'])
    revenue = dict()
    query = select('Transactions')
    cursor = db.execute(query)
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
                if value > 0:
                    if category in revenue:
                        revenue[category] += value
                    else:
                        revenue[category] = value
    return {
        'categories': list(revenue.keys()),
        'revenue': list(revenue.values())
    }
