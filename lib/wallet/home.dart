import "package:flutter/material.dart";
import "./database.dart";
import "./account.dart";
import "./addAccount.dart";
import "./accountDetails.dart";

class WalletHome extends StatefulWidget
{
    final String title;
    WalletHome({Key key, this.title}): super(key: key);
    @override WalletHomeState createState() => WalletHomeState();
}

class WalletHomeState extends State<WalletHome>
{
    WalletHomeState();

    void addAccount() async
    {
        Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => WalletAddAccount()),
        );
    }

    void accountDetails(acc) async
    {
        Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => WalletAccountDetails(account: acc)),
        );
    }

    accountsListWidget()
    {
        return FutureBuilder(
            future: WalletDatabase.db.getAccounts(),
            builder: (context, snapshot)
            {
                if (snapshot.hasData)
                {
                    return ListView.separated(
                        itemCount: snapshot.data.length,
                        itemBuilder: (BuildContext context, int index)
                        {
                            WalletAccount acc = snapshot.data[index];
                            final tile = ListTile(
                                title: Text(acc.name ?? "<unknown>"),
                                subtitle: Text(acc.currency ?? "<unknown>"),
                                leading: Column(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: <Widget>[
                                        Icon(Icons.account_balance_wallet, color: Colors.blue,),
                                    ],
                                ),
                                trailing: Icon(Icons.keyboard_arrow_right),
                            );
                            return InkWell(
                                child: tile,
                                onTap: () {
                                    accountDetails(acc);
                                },
                            );
                        },
                        separatorBuilder: (context, index)
                        {
                            return Divider();
                        },
                    );
                }
                else return Center(child: Text("Нет счетов"));
            }
        );
    }

    @override Widget build(BuildContext context)
    {
        return Scaffold(
            appBar: AppBar(title: Text(widget.title),),
            body: accountsListWidget(),
            floatingActionButton: FloatingActionButton(
                onPressed: addAccount,
                tooltip: "Добавить счет",
                child: Icon(Icons.add),
            ),
        );
    }
}
