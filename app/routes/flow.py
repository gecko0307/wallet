import json
import datetime
from datetime import datetime

import bottle
from bottle import request
from ..namespace import *
from ..data import *

@bottle.route('/flow')
def flow(db):
    year = datetime.now().year
    if 'year' in request.query:
        year = int(request.query['year'])
    d = NestedNamespace({
        'year': year
    })
    if d != None:
        return bottle.template(load('flow.stpl'), data = d)
    else:
        bottle.redirect('/404.html')

@bottle.route('/flow.json')
def flowJson(db):
    data = {
        'revenue': [0 for x in range(12)],
        'expense': [0 for x in range(12)],
        'net': [0 for x in range(12)]
    }
    year = datetime.now().year
    if 'year' in request.query:
        year = request.query['year']
    query = select('Transactions', ['strftime(\'%Y\', DATETIME) = \'' + str(year) + '\''])
    query += ' ORDER BY CAST(strftime(\'%m\', DATETIME) AS INTEGER)'
    cursor = db.execute(query)
    for trans in cursor.fetchall():
        if trans['CATEGORY'] != 'notrack':
            d = datetime.strptime(trans['DATETIME'], '%Y-%m-%d %H:%M:%S')
            month = d.month - 1
            query = select('Accounts', ["ID='%s'" % trans['ACCOUNT']])
            cursor = db.execute(query)
            account = cursor.fetchall()[0]
            value = trans['VALUE']
            value *= account['REPORT_EXCHANGE_RATE']
            if value > 0:
                data['revenue'][month] += value
            else:
                data['expense'][month] += -value
            data['net'][month] += value
    return data
