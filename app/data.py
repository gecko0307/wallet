import io
import datetime
from datetime import datetime

from .namespace import *
from .config import *

def load(name):
    f = io.open('%s/%s' % (Config.templatesPath, name), 'r', encoding = 'utf-8')
    s = f.read()
    f.close()
    return s

def datetimeFromSql(dts):
    return datetime.strptime(dts, '%Y-%m-%d %H:%M:%S')

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
                if d.month == datetime.today().month and d.year == datetime.today().year:
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

def accountData2(id, db):
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
        transactions = {}
        balance = 0
        query = "SELECT * FROM Transactions WHERE ACCOUNT='%s' ORDER BY date('DATETIME')" % id
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
            transactionDateTime = datetimeFromSql(transaction['DATETIME'])
            year = str(transactionDateTime.year)
            month = transactionDateTime.month - 1
            if not year in transactions:
                transactions[year] = [[] for i in range(12)]
            transactions[year][month].append(trans)
            balance += transaction['VALUE']
        data.account = NestedNamespace({
            'id': account['ID'],
            'name': account['NAME'],
            'description': account['DESCRIPTION'],
            'currency': account['CURRENCY'],
            'exchangeRate': account['REPORT_EXCHANGE_RATE'],
            'balance': balance,
            'transactions': None
        })
        data.account.transactions = transactions
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
