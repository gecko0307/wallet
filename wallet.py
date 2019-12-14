# -*- coding: utf-8 -*-

import os
import sys
print(sys.stdout.encoding)
sys.path.append(os.getcwd())

import io
import threading
import json
import datetime
from datetime import datetime
from types import SimpleNamespace

import bottle
from bottle import request
from bottle_sqlite import SQLitePlugin

class NestedNamespace(SimpleNamespace):
    def __init__(self, dictionary, **kwargs):
        super().__init__(**kwargs)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, NestedNamespace(value))
            else:
                self.__setattr__(key, value)

Config = NestedNamespace({
    'appInfo': 'Wallet v0.0.1',
    'sitePath': 'site',
    'databasePath': 'data/assets.db'
})

bottle.install(SQLitePlugin(dbfile = Config.databasePath))

def stpl(name):
    f = io.open('%s/%s.stpl' % (Config.sitePath, name), 'r', encoding = 'utf-8')
    s = f.read()
    f.close()
    return s

def datetimeFromSql(dts):
    return datetime.datetime.strptime(dts, '%Y-%m-%d %H:%M:%S')

# Generates SQL SELECT query matching the kwargs passed
def select(table, kwargs = None):
    sql = list()
    sql.append("SELECT * FROM %s" % table)
    if kwargs:
        sql.append(" WHERE " + " AND ".join("%s" % (v) for v in kwargs))
    return "".join(sql)

def profileData(db):
    data = NestedNamespace({
        'config': {
            'appInfo': Config.appInfo
        },
        'totalBalance': 0,
        'monthRevenue': 0,
        'monthExpense': 0,
        'reportCurrency': 'RUB'
    })
    query = select('Accounts')
    cursor = db.execute(query)
    data.accounts = []
    for account in cursor.fetchall():
        accountBalance = 0
        query = select('Transactions', ["ACCOUNT='%s'" % account['ID']])
        cursor = db.execute(query)
        for transaction in cursor.fetchall():
            accountBalance += transaction['VALUE']
            if transaction['CATEGORY'] != 'notrack':
                d = datetime.strptime(transaction['DATETIME'], '%Y-%m-%d %H:%M:%S')
                if d.month == datetime.today().month:
                    v = transaction['VALUE'] * account['REPORT_EXCHANGE_RATE']
                    if v > 0:
                        data.monthRevenue += v
                    else:
                        data.monthExpense += -v
        acc = NestedNamespace({
            'id': account['ID'],
            'name': account['NAME'],
            'description': account['DESCRIPTION'],
            'currency': account['CURRENCY'],
            'exchangeRate': account['REPORT_EXCHANGE_RATE'],
            'balance': accountBalance
        })
        data.accounts.append(acc)
        data.totalBalance += accountBalance * account['REPORT_EXCHANGE_RATE']
        
    return data

def accountData(id, db):
    data = NestedNamespace({
        'config': {
            'appInfo': Config.appInfo
        }
    })
    query = select('Accounts', ["ID='%s'" % id])
    cursor = db.execute(query)
    accounts = cursor.fetchall()
    if len(accounts) > 0:
        account = accounts[0]
        transactions = []
        balance = 0
        query = select('Transactions', ["ACCOUNT='%s'" % id])
        cursor = db.execute(query)
        for transaction in cursor.fetchall():
            trans = NestedNamespace({
                'id': transaction['ID'],
                'description': transaction['DESCRIPTION'],
                'category': transaction['CATEGORY'],
                'currency': transaction['CURRENCY'],
                'value': transaction['VALUE'],
                'date': transaction['DATETIME']
            })
            transactions.append(trans)
            balance += transaction['VALUE']
        data.account = NestedNamespace({
            'id': account['ID'],
            'name': account['NAME'],
            'description': account['DESCRIPTION'],
            'currency': account['CURRENCY'],
            'exchangeRate': account['REPORT_EXCHANGE_RATE'],
            'balance': balance,
            'transactions': transactions
        })
        return data
    else:
        return None

def transactionData(id, db):
    data = NestedNamespace({
        'config': {
            'appInfo': Config.appInfo
        }
    })
    query = select('Transactions', ["ID='%s'" % id])
    cursor = db.execute(query)
    transactions = cursor.fetchall()
    if len(transactions) > 0:
        transaction = transactions[0]
        data.transaction = NestedNamespace({
            'id': transaction['ID'],
            'account': transaction['ACCOUNT'],
            'description': transaction['DESCRIPTION'],
            'category': transaction['CATEGORY'],
            'currency': transaction['CURRENCY'],
            'value': transaction['VALUE'],
            'date': transaction['DATETIME']
        })
        return data
    else:
        return None

@bottle.route('/<filename:path>')
def serverStatic(filename):
    return bottle.static_file(filename, root = Config.sitePath)

@bottle.route('/')
def index(db):
    d = profileData(db)
    return bottle.template(stpl('index'), data = d)

@bottle.route('/account')
def index(db):
    accountId = request.query['id']
    d = accountData(accountId, db)
    if d != None:
        return bottle.template(stpl('account'), data = d)
    else:
        bottle.redirect('/404.html')

@bottle.route('/createaccount')
def index(db):
    d = profileData(db)
    return bottle.template(stpl('create_account'), data = d)
#
# Account operations:
#
@bottle.post('/newAccount')
def newAccount(db):
    accountName = request.forms.getunicode('name') or 'My Account'
    accountDescription = request.forms.getunicode('description') or ''
    accountCurrency = request.forms.get('currency') or 'RUB'
    accountExchangeRate = request.forms.get('exchangeRate') or 1
    db.execute(
        "INSERT INTO Accounts (NAME, DESCRIPTION, CURRENCY, REPORT_EXCHANGE_RATE) VALUES (?, ?, ?, ?)", 
        (accountName, accountDescription, accountCurrency, accountExchangeRate,))
    db.commit()
    bottle.redirect('/')

@bottle.route('/editAccount')
def editAccount(db):
    accountId = request.query['id']
    d = accountData(accountId, db)
    if d != None:
        return bottle.template(stpl('edit_account'), data = d)
    else:
        bottle.redirect('/404.html')

@bottle.post('/updateAccount')
def updateAccount(db):
    accountId = request.query['id']
    accountName = request.forms.getunicode('name') or 'My Account'
    accountDescription = request.forms.getunicode('description') or ''
    accountCurrency = request.forms.get('currency') or 'RUB'
    accountExchangeRate = request.forms.get('exchangeRate') or 1
    db.execute('UPDATE Accounts SET NAME=?, DESCRIPTION=?, CURRENCY=?, REPORT_EXCHANGE_RATE=? WHERE id=?', 
        (accountName, accountDescription, accountCurrency, accountExchangeRate, accountId, ))
    db.commit()
    bottle.redirect('/account?id=%s' % accountId)

@bottle.route('/confirmDeleteAccount')
def confirmDeleteAccount(db):
    accountId = request.query['id']
    d = accountData(accountId, db)
    if d != None:
        return bottle.template(stpl('confirm_delete_account'), data = d)
    else:
        bottle.redirect('/404.html')

@bottle.route('/deleteAccount')
def deleteAccount(db):
    accountId = request.query['id']
    d = accountData(accountId, db)
    if d != None:
        db.execute('DELETE FROM Accounts WHERE id=?', (accountId, ))
        db.commit()
        bottle.redirect('/')
    else:
        bottle.redirect('/404.html')

#
# Transaction operations:
#
@bottle.post('/newTransaction')
def newTransaction(db):
    transAccount = request.query['account']
    transType = request.query['type']
    query = select('Accounts', ["ID='%s'" % transAccount])
    cursor = db.execute(query)
    accounts = cursor.fetchall()
    if len(accounts) > 0:
        account = accounts[0]
        transDescription = request.forms.getunicode('description') or ''
        transCategory = request.forms.get('category') or 'unspecified'
        transValue = float(request.forms.get('value') or '0.0')
        if transType == 'sub':
            transValue = -transValue
        transCurrency = account['CURRENCY']
        transDate = request.forms.get('date') or datetime.today().strftime('%Y-%m-%d')
        timestamp = '%s 00:00:00' % transDate
        db.execute(
            "INSERT INTO Transactions (DESCRIPTION, CATEGORY, CURRENCY, VALUE, ACCOUNT, DATETIME) VALUES (?, ?, ?, ?, ?, ?)", 
            (transDescription, transCategory, transCurrency, transValue, transAccount, timestamp))
        db.commit()
    bottle.redirect('/account?id=%s' % transAccount)

@bottle.route('/editTransaction')
def editTransaction(db):
    transId = request.query['id']
    d = transactionData(transId, db)
    if d != None:
        return bottle.template(stpl('edit_transaction'), data = d)
    else:
        bottle.redirect('/404.html')

@bottle.post('/updateTransaction')
def updateTransaction(db):
    transId = request.query['id']
    d = transactionData(transId, db)
    accountId = d.transaction.account;
    transDescription = request.forms.getunicode('description') or ''
    transCategory = request.forms.get('category') or 'unspecified'
    transValue = float(request.forms.get('value') or '0.0')
    transDate = request.forms.get('date') or datetime.today().strftime('%Y-%m-%d')
    timestamp = '%s 00:00:00' % transDate
    db.execute('UPDATE Transactions SET DESCRIPTION=?, CATEGORY=?, VALUE=?, DATETIME=? WHERE id=?', 
        (transDescription, transCategory, transValue, timestamp, transId, ))
    db.commit()
    bottle.redirect('/account?id=%s' % accountId)

@bottle.route('/deleteTransaction')
def deleteTransaction(db):
    transId = request.query['id']
    query = select('Transactions', ["ID='%s'" % transId])
    cursor = db.execute(query)
    transactions = cursor.fetchall()
    if len(transactions) > 0:
        transaction = transactions[0]
        transAccount = transaction['ACCOUNT']
        db.execute("DELETE FROM Transactions WHERE ID=%s" % transId)
        db.commit()
        bottle.redirect('/account?id=%s' % transAccount)
    else:
        bottle.redirect('/404.html')

#
# Reports
#

@bottle.route('/assets')
def assets(db):
    year = datetime.now().year
    if 'year' in request.query:
        year = int(request.query['year'])
    d = NestedNamespace({
        'year': year
    })
    if d != None:
        return bottle.template(stpl('assets'), data = d)
    else:
        bottle.redirect('/404.html')

@bottle.route('/assets.json')
def assetsJson(db):
    data = {
        'accounts': [],
        'labels': [],
        'balances': [],
        'totalBalance': 0
    }
    query = select('Accounts')
    cursor = db.execute(query)
    for account in cursor.fetchall():
        accountBalance = 0
        query = select('Transactions', ["ACCOUNT='%s'" % account['ID']])
        cursor = db.execute(query)
        for transaction in cursor.fetchall():
            accountBalance += transaction['VALUE']
        accountBalance *= account['REPORT_EXCHANGE_RATE']
        acc = {
            'id': account['ID'],
            'name': account['NAME'],
            'description': account['DESCRIPTION'],
            'currency': account['CURRENCY'],
            'exchangeRate': account['REPORT_EXCHANGE_RATE'],
            'balance': accountBalance
        }
        data['accounts'].append(acc)
        data['labels'].append(account['NAME'])
        data['balances'].append(accountBalance)
        data['totalBalance'] += accountBalance
    
    return data

@bottle.route('/flow')
def flow(db):
    year = datetime.now().year
    if 'year' in request.query:
        year = int(request.query['year'])
    d = NestedNamespace({
        'year': year
    })
    if d != None:
        return bottle.template(stpl('flow'), data = d)
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

@bottle.route('/balance')
def flow(db):
    year = datetime.now().year
    if 'year' in request.query:
        year = int(request.query['year'])
    d = NestedNamespace({
        'year': year
    })
    if d != None:
        return bottle.template(stpl('balance'), data = d)
    else:
        bottle.redirect('/404.html')

@bottle.route('/balance.json')
def balanceJson(db):
    data = {
        'balance': [0 for x in range(12)]
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
        cursor = db.execute(query)
        account = cursor.fetchall()[0]
        value = trans['VALUE']
        value *= account['REPORT_EXCHANGE_RATE']
        if d.year == year:
            for m in range(month, 12):
                data['balance'][m] += value
        elif d.year < year:
            for m in range(0, 12):
                data['balance'][m] += value
    return data

@bottle.route('/revenue')
def revenue(db):
    year = datetime.now().year
    if 'year' in request.query:
        year = int(request.query['year'])
    d = NestedNamespace({
        'year': year
    })
    if d != None:
        return bottle.template(stpl('revenue'), data = d)
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


@bottle.route('/expences')
def expences(db):
    year = datetime.now().year
    if 'year' in request.query:
        year = int(request.query['year'])
    d = NestedNamespace({
        'year': year
    })
    if d != None:
        return bottle.template(stpl('expences'), data = d)
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
        return bottle.template(stpl('monthexpences'), data = d)
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


@bottle.route('/toppurchases')
def toppurchases(db):
    year = datetime.now().year
    if 'year' in request.query:
        year = int(request.query['year'])
    d = NestedNamespace({
        'year': year
    })
    if d != None:
        return bottle.template(stpl('toppurchases'), data = d)
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

def serverMain():
    bottle.run(host = '0.0.0.0', port = 8080)

serverThread = threading.Thread(target=serverMain)
serverThread.daemon = True
serverThread.start()

from cefpython3 import cefpython as cef
import platform
import sys

def cefMain():
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize()
    browser = cef.CreateBrowserSync(url="http://localhost:8080/", window_title="Wallet")
    browser.SetBounds(0, 0, 1280, 900)
    browser.SetClientHandler(LifespanHandler())
    cef.MessageLoop()
    cef.Shutdown()

class LifespanHandler(object):
    def OnBeforeClose(self, browser):
        print("shutdown")

cefMain()
