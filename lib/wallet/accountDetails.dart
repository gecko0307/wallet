import "package:flutter/material.dart";
import "package:vibration/vibration.dart";
import "./confirmDialog.dart";
import "./addTransaction.dart";
import "./account.dart";
import "./transaction.dart";
import "./database.dart";

class WalletAccountDetails extends StatefulWidget
{
    final WalletAccount account;
    WalletAccountDetails({Key key, this.account}): super(key: key);
    @override WalletAccountDetailsState createState() => WalletAccountDetailsState();
}


class WalletAccountMenuItem
{
    final String title;
    const WalletAccountMenuItem({this.title});
}

class WalletAccountDetailsState extends State<WalletAccountDetails>
{
    //final _formKey = GlobalKey<FormState>();
    
    final _categoryIcons = {
        "notrack": "❔",
        "charity": "🎗",
        "household": "🛀",
        "lodging": "🏠",
        "books": "📚",
        "music": "🎵",
        "culture": "🎭",
        "catering": "🍔",
        "clothes": "👔",
        "cosmetics": "💄",
        "gifts": "🎁",
        "food": "🍏",
        "meds": "💊",
        "communication": "📱",
        "software": "🎮",
        "tech": "💻",
        "transport": "🚗",
        "hobby": "🎨",
        "salary": "💼",
        "fee": "💲",
        "find": "💲",
        "ecommerce": "💰",
        "crowdfunding": "💖",
        "interest": "💵",
        "trading": "📈",
        "other": "❓",
        "": "❓",
    };
    
    final List<WalletAccountMenuItem> _menuItems = <WalletAccountMenuItem>[
        const WalletAccountMenuItem(title: "Удалить счет"),
    ];
    
    void _menuSelect(WalletAccountMenuItem item) async
    {
        await confirmDialog(
            context: context,
            onUserAction: (ConfirmAction action) {
                if (action == ConfirmAction.ACCEPT)
                {
                    print("delete");
                    // TODO: delete account
                    WalletDatabase.db.deleteAccount(widget.account);
                    Navigator.pop(context);
                }
                else
                {
                    //
                }
            }
        );
    }

    Widget menu()
    {
        return PopupMenuButton<WalletAccountMenuItem>(
            onSelected: _menuSelect,
            itemBuilder: (BuildContext context) {
                return _menuItems.map((WalletAccountMenuItem item) {
                    return PopupMenuItem<WalletAccountMenuItem>(
                        value: item,
                        child: Text(item.title),
                    );
                }).toList();
            },
        );
    }
    
    transactionsListWidget()
    {
        return FutureBuilder(
            future: WalletDatabase.db.getTransactions(widget.account),
            builder: (context, snapshot)
            {
                if (snapshot.hasError)
                {
                    return Text("Error: ${snapshot.error}");
                }
                else if (snapshot.hasData)
                {
                    return ListView.separated(
                        itemCount: snapshot.data.length,
                        itemBuilder: (BuildContext context, int index)
                        {
                            WalletTransaction trans = snapshot.data[index];
                            final tile = ListTile(
                                leading: Column(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: <Widget>[
                                        Text(
                                            _categoryIcons[trans.category ?? ""] ?? "❓",
                                            style: DefaultTextStyle.of(context).style.apply(fontSizeFactor: 2.0),
                                        ),
                                    ],
                                ),
                                title: Text(trans.description ?? "?"),
                                subtitle: Text(" " + (trans.value.toString() ?? "0.0")),
                                trailing: Icon(Icons.keyboard_arrow_right),
                            );
                            final inkWell = InkWell(
                                child: tile,
                                onTap: () {
                                    //transactionDetails(trans);
                                },
                            );
                            return GestureDetector(
                                onLongPress: () async {
                                    print("long press");
                                    if (await Vibration.hasVibrator()) {
                                        Vibration.vibrate(duration: 50);
                                    }
                                },
                                child: inkWell,
                            );
                        },
                        separatorBuilder: (context, index)
                        {
                            return Divider();
                        },
                    );
                }
                else return Center(child: Text("Нет транзакций"));
            }
        );
    }
    
    void addTransaction() async
    {
        Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => WalletAddTransaction(account: widget.account)),
        );
    }

    @override Widget build(BuildContext context)
    {
        return Scaffold(
            appBar: AppBar(
                title: Text(widget.account.name),
                actions: <Widget>[menu(),],
            ),
            body: transactionsListWidget(),
            floatingActionButton: FloatingActionButton(
                onPressed: addTransaction,
                tooltip: "Добавить транзакцию",
                child: Icon(Icons.add),
            ),
        );
    }

    Widget form(context)
    {
        return Center(child: Text("No data"));
    }
}
