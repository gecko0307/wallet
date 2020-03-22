import "dart:async";
import "package:path/path.dart";
import "package:sqflite/sqflite.dart";
import "./account.dart";
import "./transaction.dart";

class WalletDatabase
{
    WalletDatabase._();
    static final WalletDatabase db = WalletDatabase._();
    
    final String sqlCreateAccountsTable = 
        "CREATE TABLE IF NOT EXISTS Accounts(id INTEGER PRIMARY KEY, name STRING, description TEXT, currency STRING)";
    final String sqlCreateTransactionsTable = 
        "CREATE TABLE IF NOT EXISTS Transactions(id INTEGER PRIMARY KEY, description TEXT, category STRING, currency STRING, value DOUBLE, account INTEGER, datetime STRING)";

    static Database _database;
    Future<Database> get database async
    {
        if (_database != null)
        return _database;

        _database = await _initDatabase();
        return _database;
    }
    
    _createTables(Database db) async
    {
        final batch = db.batch();
        batch.execute(sqlCreateAccountsTable,);
        batch.execute(sqlCreateTransactionsTable,);
        return batch.commit();
    }

    _initDatabase() async
    {
        final String path = join(await getDatabasesPath(), "wallet2.db");
        
        return await openDatabase(path, version: 1,
            onOpen: (db) {
                return _createTables(db);
            },
            onCreate: (Database db, int version) async {
                return _createTables(db);
            }
        );
    }

    insertAccount(WalletAccount acc) async
    {
        final db = await database;
        return await db.insert(
            "Accounts",
            acc.toMap(),
            conflictAlgorithm: ConflictAlgorithm.replace,
        );
    }
    
    insertTransaction(WalletTransaction trans) async
    {
        final db = await database;
        return await db.insert(
            "Transactions",
            trans.toMap(),
            conflictAlgorithm: ConflictAlgorithm.replace,
        );
    }

    deleteAccount(WalletAccount acc) async
    {
        final db = await database;
        return await db.rawDelete("DELETE FROM Accounts WHERE id = ?", [acc.id]);
    }
    
    getAccounts() async
    {
        final db = await database;
        var res = await db.query("Accounts");
        return res.isNotEmpty?
        res.map((c) => WalletAccount.fromMap(c)).toList() :
        [];
    }
    
    getTransactions(WalletAccount acc) async
    {
        final db = await database;
        var res = await db.query("Transactions");
        return res.isNotEmpty?
        res.map((c) => WalletTransaction.fromMap(c)).toList() :
        [];
    }
}
