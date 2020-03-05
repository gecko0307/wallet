import json
import datetime
from datetime import datetime

import bottle
from bottle import request
from ..namespace import *
from ..data import *

@bottle.route('/expences')
def expences(db):
    year = datetime.now().year
    if 'year' in request.query:
        year = int(request.query['year'])
    d = NestedNamespace({
        'year': year
    })
    if d != None:
        return bottle.template(load('expences.stpl'), data = d)
    else:
        bottle.redirect('/404.html')

@bottle.route('/expences.json')
def expencesJson(db):
    expences = dict()
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
            if value < 0:
                if category in expences:
                    expences[category] += -value
                else:
                    expences[category] = -value
    return {
        'categories': list(expences.keys()),
        'expences': list(expences.values())
    }
