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
    currentDateTime = datetime.now()
    currentYear = currentDateTime.year
    year = currentYear
    if 'year' in request.query:
        year = int(request.query['year'])
    query = select('Transactions')
    # query = select('Transactions', ['strftime(\'%Y\', DATETIME) = \'' + str(year) + '\''])
    query += ' ORDER BY CAST(strftime(\'%m\', DATETIME) AS INTEGER)'
    cursor = db.execute(query)
    
    fullRevenue = 0
    fullExpence = 0
    startYear = currentYear
    
    for trans in cursor.fetchall():
        if trans['CATEGORY'] != 'notrack':
            d = datetime.strptime(trans['DATETIME'], '%Y-%m-%d %H:%M:%S')
            month = d.month - 1
            query = select('Accounts', ["ID='%s'" % trans['ACCOUNT']])
            cursor = db.execute(query)
            account = cursor.fetchall()[0]
            value = trans['VALUE']
            value *= account['REPORT_EXCHANGE_RATE']
            
            if d.year == year:
                if value > 0:
                    data['revenue'][month] += value
                else:
                    data['expense'][month] += -value
                data['net'][month] += value
            
            if value > 0:
                fullRevenue += value
            else:
                fullExpence += -value
            
            y = int(d.year)
            if y < startYear:
                startYear = y
    
    annualRevenue = sum(data['revenue'])
    annualExpence = sum(data['expense'])
    annualNet = annualRevenue - annualExpence
    data['annualRevenue'] = annualRevenue
    data['annualExpence'] = annualExpence
    data['annualNet'] = annualNet
    
    reportYear = year;
    numMonths = 0
    if currentYear == reportYear:
        numMonths = currentDateTime.month;
    else:
        numMonths = 12;
    monthlyRevenue = annualRevenue / numMonths;
    monthlyExpence = annualExpence / numMonths;
    monthlyNet = annualNet / numMonths;
    data['monthlyRevenue'] = monthlyRevenue
    data['monthlyExpence'] = monthlyExpence
    data['monthlyNet'] = monthlyNet
    
    numYearsFull = currentYear - startYear
    numMonthsFull = numYearsFull * 12 + currentDateTime.month
    estimatedAnnualRevenue = monthlyRevenue * 12
    estimatedAnnualExpence = monthlyExpence * 12
    estimatedAnnualNet = monthlyNet * 12
    data['estimatedAnnualRevenue'] = estimatedAnnualRevenue
    data['estimatedAnnualExpence'] = estimatedAnnualExpence
    data['estimatedAnnualNet'] = estimatedAnnualNet
    
    return data

