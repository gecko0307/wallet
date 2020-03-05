import bottle
from bottle import request
from ..data import *

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
