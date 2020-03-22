import "dart:async";
import "package:path/path.dart";
import "package:sqflite/sqflite.dart";
import "./account.dart";

class WalletDatabase
{
    WalletDatabase._();
    static final WalletDatabase db = WalletDatabase._();

    static Database _database;
    Future<Database> get database async
    {
        if (_database != null)
        return _database;

        _database = await _initDatabase();
        return _database;
    }

    _initDatabase() async
    {
        final String path = join(await getDatabasesPath(), "wallet2.db");
        final String sqlTableCreate = "CREATE TABLE Accounts(id INTEGER PRIMARY KEY, name STRING, description TEXT, currency STRING)";
        return await openDatabase(path, version: 1,
            onOpen: (db) {
                //
            },
            onCreate: (Database db, int version) async {
                return db.execute(sqlTableCreate,);
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
}
