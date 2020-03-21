import "package:flutter/material.dart";
import "./database.dart";
import "./account.dart";
import "./addAccount.dart";

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

  accountsListWidget()
  {
    return FutureBuilder(
      future: WalletDatabase.db.getAccounts(),
      builder: (context, snapshot)
      {
        if (snapshot.hasData)
        {
          return ListView.builder(
            itemCount: snapshot.data.length,
            itemBuilder: (BuildContext context, int index)
            {
              WalletAccount acc = snapshot.data[index];
              return ListTile(
                title: Text(acc.name ?? "<unknown>"),
                leading: Text(acc.currency ?? "<unknown>"),
                trailing: Text(acc.description ?? "<unknown>"),
              );
            },
          );
        }
        else return Center(child: Text("Нет счетов"));
      }
    );
  }

  // This method is rerun every time setState is called
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
